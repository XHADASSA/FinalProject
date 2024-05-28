import math
from queue import Queue

polygon_vertices = [
    [34,0],
    [0, 5],
    [0, 40],
    [20, 42],
    [40, 20]
    ]

# Maximum allowed distance from the boundary of the polygon
tolerance_distance = 0  # in meters
wavelength = 2  # אורך גל הקול

def distance(x1, y1, x2, y2):
    return math.sqrt(((float(y1) - float(y2)) ** 2) + ((float(x1) - float(x2)) ** 2))

# Calculate the distance between two points using the Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    radius = 6371000  # Radius of the Earth in meters
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(delta_lon/2) * math.sin(delta_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c
    return distance
print(calculate_distance(1,11,1,1))
def GPS():
    return [0,0]

# Check if a point is within the polygon boundary
def is_within_polygon(lat, lon,polygon_vertices):
    num_vertices = len(polygon_vertices)-1
    inside = False
    for i in range(num_vertices):
        j = (i + 1) % num_vertices
        if ((polygon_vertices[i][1] > lon) != (polygon_vertices[j][1] > lon)) and \
           (lat < (polygon_vertices[j][0] - polygon_vertices[i][0]) * (lon - polygon_vertices[i][1]) / \
           (polygon_vertices[j][1] - polygon_vertices[i][1]) + polygon_vertices[i][0]):
            inside = not inside
    return inside
#פונקציה המקבלת את הזווית של הרובוט, נקודת התחלה ונקודת יעד ומחשבת את הזווית אליה צריך לכוון
def calculate_steering_angle(current_angle, current_point, destination_point):
    # Calculate the angle between the current point and the destination point
    angle_difference = math.atan2(destination_point[1] - current_point[1], destination_point[0] - current_point[0])
    #Normalize the angle difference to be within -180 to 180 degrees
    print(math.degrees(math.pi))
    if angle_difference > math.pi:
        angle_difference -= 2 * math.pi
    elif angle_difference < -math.pi:
        angle_difference += 2 * math.pi
    # Calculate the steering angle within the maximum angle range
    steering_angle =angle_difference - current_angle
    return math.degrees(steering_angle)
#פונקציה המקבלת מערך נקודות ומיקום הנוכחי ומחזירה נקודת התחלה
def Start_Point(polygon_vertices,GPS):
    maximumRib=0
    I_maximumRib=0
    for i in range(len(polygon_vertices)-1):
        Rib=calculate_distance(polygon_vertices[i][0],polygon_vertices[i][1],polygon_vertices[i+1][0],polygon_vertices[i+1][1])
        if Rib>maximumRib:
            maximumRib=Rib
            I_maximumRib=i
    i=I_maximumRib
    #לאחר שחושבה הצלע הארוכה ביותר, נבדוק לאיזה קצה מבין שני קצוות הצלע הרובוט קרוב יותר
    if calculate_distance(polygon_vertices[i][0],polygon_vertices[i][1],GPS[0],GPS[1])<calculate_distance(GPS[0],GPS[1],polygon_vertices[i+1][0],polygon_vertices[i+1][1]):
        Start_Point=polygon_vertices[i]
    else:
        Start_Point = polygon_vertices[i+1]
        i=i+1
    return i
#פונקצייה המוצאת משוואת ישר בין 2 נקודות
def find_line_equation(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    a = y2 - y1
    b = x1 - x2
    c = (x2 * y1) - (x1 * y2)

    return a, b, c

# Example usage
point1 = (2, 3)
point2 = (5, 7)
line_equation = find_line_equation(point1, point2)

a, b, c = line_equation
#print(f"The equation of the line is: {a}x + {b}y + {c} = 0")

def KalmanFilter(current_angle,steering_angle,current_point):
    current_angle += steering_angle
    # Calculate the new position
    current_point = (
        current_point[0] + math.cos(current_angle),
        current_point[1] + math.sin(current_angle)
    )
    return current_point

def solve_point(p1, l, p2, k):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    xc = (l * x1 + k * x2) / (k + l)
    yc = (l * y1 + k * y2) / (k + l)
    return xc, yc

#פונקציה המקבלת 2 נקודות ומחשבת עבורם משוואת ישר
def line_equation(point1, point2):
    # Unpack the points into their respective coordinates
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the slope (m)
    m = (y2 - y1) / (x2 - x1)

    # Calculate the y-intercept (c)
    c = y1 - m * x1

    # Return the equation in the form y = mx + c
    return m,c
#print(line_equation([2,5],[4,9]))

#פונקציה המקבלת 2 משוואות ישר ומחשבת את הזווית ביניהם
def calculate_angle(line1_slope, line2_slope):
    dot_product = line1_slope[0] * line2_slope[0] + line1_slope[1] * line2_slope[1]
    magnitude_line1 = math.sqrt(line1_slope[0] ** 2 + line1_slope[1] ** 2)
    magnitude_line2 = math.sqrt(line2_slope[0] ** 2 + line2_slope[1] ** 2)

    cos_theta = dot_product / (magnitude_line1 * magnitude_line2)
    angle_rad = math.acos(cos_theta)
    angle_deg = math.degrees(angle_rad)

    return angle_deg

def solve_cos_equation(b, angle):
    # Convert the angle from degrees to radians
    angle_rad = math.radians(angle)
    # Calculate the length of the hypotenuse using the cosine equation
    c = b / math.cos(angle_rad)

#    return c
def FindPoint(i):
    line_equation1 = find_line_equation(polygon_vertices[i],polygon_vertices[i+1])
    line_equation2 = find_line_equation(polygon_vertices[i], polygon_vertices[i - 1])
    #חישוב הזווית בין 2 המשוואות
    angle=calculate_angle(line_equation1,line_equation2)
    angle=angle-90
    dictunasion=solve_cos_equation(wavelength,angle)
    dis = calculate_distance(polygon_vertices[i][0], polygon_vertices[i][1], polygon_vertices[i - 1][0],polygon_vertices[i - 1][1])
    point = solve_point(polygon_vertices[i], dictunasion, i - 1, dis)
    return point
#פונקציה המקבלת זווית וישר במשולש ישר זווית ומחשבת יתר
def calculate_sides(given_angle):
    ## Calculate the base side using tangent
    #base_length = perpendicular_length / math.tan(math.radians(given_angle))
    ## Calculate the hypotenuse using Pythagorean theorem
    #hypotenuse_length = math.sqrt(perpendicular_length ** 2 + base_length ** 2)
    #return hypotenuse_length
    #b = a * math.tan(math.radians(A))
    #return wavelength* math.tan(math.radians(given_angle))
    # Convert angle to radians
    #angle_radians = math.radians(given_angle)
    ## Calculate the length of side C using trigonometry (Pythagorean theorem)
    #z=(wavelength ** 2) / math.cos(angle_radians) ** 2 - wavelength ** 2
    #print(f"gggggggggg {z}")
    #side_c = math.sqrt(z)
    # Calculate the base side using tangent
    base_length = wavelength / math.cos(math.radians(given_angle))
    return base_length

#print(calculate_sides(10,60))


# Calculate the base and hypotenuse sides
#base_length, hypotenuse_length = calculate_sides(perpendicular_length, given_angle)

# Print the calculated sides
#print(f"The length of the base side is: {base_length}")
#print(f"The length of the hypotenuse side is: {hypotenuse_length}")

#def solve_point(p1,d1,p2,d2):
#    # Define the symbols x and y
#    x, y = sp.symbols('x y')
#    # Define the equation
#    equation1 = (p1[0] - x) ** 2 + (p1[1] - y) ** 2 - np.power(d1, 2)
#    equation2 = (p2[0] - x) ** 2 + (p2[1] - y) ** 2 - np.power(d2, 2)
#
#    # Solve the equations
#    solutions = sp.solve((equation1, equation2), (x, y))
#
#    # Filter out complex solutions
#    solutions = [sol for sol in solutions if all(sp.im(s) == 0 for s in sol)]
#
#    return solutions

# Function to merge two queues
def merge_queues(queue1, queue2):
    merged_queue =Queue()
    while not queue1.empty():
        merged_queue.put(queue1.get())
    while not queue2.empty():
        merged_queue.put(queue2.get())
    return merged_queue

#פונקציה המקבלת 2 נקודות ומרחק ומחשבת את כל הנקודות שבין המרחקים
def Create_Sequence_Points(point1,point2,distance_between_points):
    #print(point1,point2,distance_between_points)
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    ArrayPoints=Queue()
    d=distance(x1,y1,x2,y2)
    num=int(d/distance_between_points)
    i=1
    for i in range(num):
        point=solve_point(point1,distance_between_points*i,point2,d-(distance_between_points*i))
        ArrayPoints.put(point)
    #print_queue(ArrayPoints)
    return ArrayPoints
#ArrayPoints=Create_Sequence_Points([1,1],[11,11],math.sqrt(2))
#print(ArrayPoints)

#פונקציה המקבלת 2 נקודות ובודקת שהמרחק בינהם לא יעלה על 10 סנטימטר
def check_distance(point1, point2,b):
    # חשב את המרחק בין שתי הנקודות באמצעות נוסחת המרחק האוקלידי
    distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    # Convert the distance to centimeters (assuming the input coordinates are in meters)
    distance_cm = distance * 100

    # Check if the distance is approximately 10 centimeters
    if math.isclose(distance_cm, b, rel_tol=1e-02):
        return True
    else:
        return False

#פונקציה המקבלת מערך ומחלקת אותו לשניים
def division(queue_point):
    # Dividing the queue into two
    first_part = Queue()
    second_part = Queue()

    # Finding the midpoint of the queue
    midpoint = queue_point.qsize() // 2

    # Populating the first part of the queue
    for _ in range(midpoint):
        first_part.put(queue_point.get())

    # Populating the second part of the queue and reversing it
    while not queue_point.empty():
        second_part.put(queue_point.get())

    second_part_list = list(second_part.queue)
    second_part_list.reverse()

    for item in second_part_list:
        queue_point.put(item)

    return first_part, second_part

def print_queue(queue):
    while not queue.empty():
      item = queue.get()
      print(item)
def convert_queue_to_array(queue):
    array = []
    while not queue.empty():
        item = queue.get()
        array.append(item)
    return array

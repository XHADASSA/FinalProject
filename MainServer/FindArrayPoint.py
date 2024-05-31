import queue
import math

polygon_vertices = [
    [5, 6],
    [20, 20],
    [40, 10],
    [50, -20],
    [30, -40]
]


GPS = [30, -39]

#פונקציה המקבלת 2 נקודות ו2 מרחקים ומוצאת את הנקודה ביניהם על הישר
def FindAndSolvePoint(point1,k,point2,l):
    x1=point1[0]
    y1=point1[1]
    x2=point2[0]
    y2=point2[1]
    xc=(l*x1+k*x2)/(k+l)
    yc=(l*y1+k*y2)/(k+l)
    return xc,yc

#פונקציה המקבלת 2 נקודות ונקודה נוספת ומחזירה האם הנקודה נמצאת ביו שתיהם
def is_point_in_range(point, start_point, end_point):
  # בודקים את הצירים x ו-y בנפרד
  if point[0] >= min(start_point[0], end_point[0]) and point[0] <= max(start_point[0], end_point[0]):
    if point[1] >= min(start_point[1], end_point[1]) and point[1] <= max(start_point[1], end_point[1]):
      return True
  return False

def calculate_angle(line1_slope, line2_slope):
    dot_product = line1_slope[0] * line2_slope[0] + line1_slope[1] * line2_slope[1]
    magnitude_line1 = math.sqrt(line1_slope[0] ** 2 + line1_slope[1] ** 2)
    magnitude_line2 = math.sqrt(line2_slope[0] ** 2 + line2_slope[1] ** 2)

    cos_theta = dot_product / (magnitude_line1 * magnitude_line2)
    angle_rad = math.acos(cos_theta)
    angle_deg = math.degrees(angle_rad)

    return angle_deg

def find_b(m, point):
    x=point[0]
    y=point[1]
    b=y-x*m
    return b

def distance1(x1, y1, x2, y2):
    return math.sqrt(((float(y1) - float(y2)) ** 2) + ((float(x1) - float(x2)) ** 2))

def find_intersection_point(line1, line2):
    m1 = line1[0]
    m2 = line2[0]
    b1 = line1[1]
    b2 = line2[1]
    if (float(m1) - float(m2)) == 0:
        return 0, 0
    x = (float(b2) - float(b1)) / (float(m1) - float(m2))

    # Calculate the y-coordinate of the intersection point
    y = float(m1) * x + float(b1)

    return x, y

def largest_side_length(vertices, GPS):
    max_distance = 0
    I_Max = 0
    for i in range(len(vertices)):
        point1 = vertices[i]
        point2 = vertices[(i + 1) % len(vertices)]  # To loop back to the first vertex
        distance = distance1(point1[0], point1[1], point2[0], point2[1])
        if (distance > max_distance):
            max_distance = distance
            I_Max = i
    i = I_Max
    n = len(vertices)
    # לאחר שחושבה הצלע הארוכה ביותר, נבדוק לאיזה קצה מבין שני קצוות הצלע הרובוט קרוב יותר
    if distance1(vertices[i % n][0], vertices[i % n][1], GPS[0], GPS[1]) > distance1(GPS[0], GPS[1],
                                                                                     vertices[(i + 1) % n][0],
                                                                                     vertices[(i + 1) % n][1]):
        i = i + 1
    return i


def find_line_equation(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the slope (m) of the line
    m = (y2 - y1) / (x2 - x1)

    # Calculate the y-intercept (b) of the line using one of the points
    b = y1 - m * x1

    # Return the equation of the line in the form y = mx + b
    return m, b


def calculate_sides(perpendicular_length, given_angle):
    hypotenuse_length = perpendicular_length / math.cos(math.radians(given_angle))
    return hypotenuse_length

def Calculate_points_on_sides(line_equation, dis, point1, point2, point3, point4):
    q1 = queue.Queue()
    q2 = queue.Queue()

    line1 = find_line_equation(point1, point2)

    line2 = find_line_equation(point3, point4)

    p1 = point3
    p2 = point2
    i = 1

    equivalent_line = line_equation
    # מעבר על הצלעות שהישרים המקבילם שייכים לשתיהם
    while (is_point_in_range(p1,point3,point4)) and is_point_in_range(p2,point2,point1):
        # מציאת משוואת המקביל הבא
        equivalent_line = line_equation[0], line_equation[1] + dis * i

        #מציאת נקודת חיתוך בין הצלע לקו המקביל לצלע ההתחלה
        p1 = find_intersection_point(line2, equivalent_line)

        if is_point_in_range(p1,point3,point4):
            q1.put(p1)

        p2 = find_intersection_point(line1, equivalent_line)
        if (is_point_in_range(p2,point2,point1)):
            q2.put(p2)

        i = i + 1
    old_line = equivalent_line

    while (is_point_in_range(p1,point3,point4)):
        equivalent_line = line_equation[0], line_equation[1] + dis * i

        p1 = find_intersection_point(line2, equivalent_line)

        if is_point_in_range(p1,point3,point4):
            q1.put(p1)

        i = i + 1
    while is_point_in_range(p2,point2,point1):
        equivalent_line = line_equation[0], line_equation[1] + dis * i
        p2 = find_intersection_point(line1, equivalent_line)

        if is_point_in_range(p2,point2,point1):
            q2.put(p2)

        i = i + 1

    return q1, q2, old_line


def FindPointOnLine(point1, point2, distance_between_points):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]

    d = distance1(x1, y1, x2, y2)

    i = 1

    point = FindAndSolvePoint(point1, distance_between_points, point2, d - (distance_between_points))

    return point

def FindPoints(polygon_vertices, GPS, wavelength):
    # מציאת משוואת המקביל
    IStartPoint = largest_side_length(polygon_vertices, GPS=GPS)
    n = len(polygon_vertices)

    ArrayPoint1 = queue.Queue()
    ArrayPoint2 = queue.Queue()

    # מציאת משוואת ישר בין 2 נקודות
    line_equation1 = find_line_equation(polygon_vertices[IStartPoint % n], polygon_vertices[(IStartPoint + 1) % n])
    line_equation2 = find_line_equation(polygon_vertices[(IStartPoint + 1) % n],polygon_vertices[(IStartPoint + 2) % n])

    # מציאת הזווית בין שניהם, המרה לחיובי והפחת 90 בעת הצורך
    angle = abs(calculate_angle(line_equation2, line_equation1))
    if angle > 90: angle = angle - 90
    # חישוב היתר שישמש למרחק בין הנקודות
    dictunasion = calculate_sides(wavelength, angle)
    # מציאת נקודה על הישר של המקביל
    p = FindPointOnLine(polygon_vertices[(IStartPoint + 1) % n], polygon_vertices[(IStartPoint + 2) % n],dictunasion)

    # משוואת הצלע הארוכה, במקום 0 יש את השיפוע ובמקום אחד נקודת החיתוך עם ציר הy
    equivalent_equation = line_equation1

    # מציאת משוואת המקביל הראשון
    equivalent_equation = (line_equation1[0], find_b(line_equation1[0], p))

    # מציאת המרחק בין שתי המשוואות עם חיתוך עם ציר הy
    dis = equivalent_equation[1] - line_equation1[1]

    #סידור מחדש של מערך הנקודת כשIStartPoint נמצא בהתחלה
    polygon_vertices = polygon_vertices[IStartPoint:] + polygon_vertices[:IStartPoint]

    # חילוק מערך הנקודות לשתי מערכים שונים
    first_half = []
    second_half = []
    first_half = polygon_vertices[1:(len(polygon_vertices) // 2) + 1]
    second_half = polygon_vertices[(len(polygon_vertices) + 1) // 2:]

    second_half.append(polygon_vertices[0])
    second_half.reverse()

    q1 = queue.Queue()
    q2 = queue.Queue()
    for i in range(len(first_half) - 1):
        q1, q2, line_equation1 = Calculate_points_on_sides(line_equation1, dis, second_half[i + 1], second_half[i],first_half[i], first_half[i + 1])

        while not q1.empty():
            element = q1.get()
            ArrayPoint1.put(element)
        while not q2.empty():
            element = q2.get()
            ArrayPoint2.put(element)

    # לצלע החיבור בין המערכים
    q1, q2, line_equation1 = Calculate_points_on_sides(line_equation1, dis, second_half[len(second_half) - 1],
                                                          second_half[len(second_half) - 2],
                                                          first_half[len(first_half) - 1],
                                                          second_half[len(second_half) - 1])

    while not q1.empty():
        element = q1.get()
        ArrayPoint1.put(element)
    while not q2.empty():
        element = q2.get()
        ArrayPoint2.put(element)

    return ArrayPoint1, ArrayPoint2

#first_part = queue.Queue()
#second_part = queue.Queue()
#first_part, second_part = FindPoints(polygon_vertices, GPS, CameraView)
#
#while not first_part.empty():
#    print(first_part.get())
#print("---")
#while not second_part.empty():
#    print(second_part.get())

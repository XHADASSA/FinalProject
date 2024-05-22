import time
import math
import camera as cm
#from newP.ArrayPoint import FindArrayPoint
wavelength = 5  # אורך גל הקול
#בתהליך זה קיים מצפן, התהליך דוגם ממנו נתונים בעת הצןרך למשתנה current_angle

speed=100
#דגימה למצפן
current_angle = 90

def process_2(GPS,destination_point, stop_flag):
    # הגדרת מיקום הרובוט הנוכחי
    current_position = [1.0, 2.0, 0.0]  # (x, y, z)

    # הגדרת נקודת המטרה
    goal_position = [5.0, 4.0, 1.0]  # (x, y, z)

    # חישוב המרחק לנקודת המטרה
    distance_to_goal = math.sqrt((goal_position[0] - current_position[0]) ** 2 +
                                 (goal_position[1] - current_position[1]) ** 2 +
                                 (goal_position[2] - current_position[2]) ** 2)

    # חישוב זווית הנטייה
    angle_to_goal = math.atan2(goal_position[1] - current_position[1],
                               goal_position[0] - current_position[0])

    # חישוב מהירות סיבוב
    angular_speed = (angle_to_goal - current_position[2]) / 0.1  # קבוע זמן

    # חישוב מהירות קווית
    linear_speed = distance_to_goal / 1.0  # קבוע זמן

    # עדכון מיקום הרובוט הנוכחי
    current_position = [goal_position[0], goal_position[1], goal_position[2]]

    # בדיקת הגעה לנקודת המטרה
    while distance_to_goal > 0.1:
        print(f"הרובוט ממשיך לנווט. מרחק לנקודה: {distance_to_goal:.2f}")
    print("הרובוט הגיע לנקודת המטרה!")

    time.sleep(1)

    image_path = cm.camera()

    # שליחת הנתיב לשרת הראשי
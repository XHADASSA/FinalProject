import time
import math
import MainRobotsSuicide.RobotsSuicide1.camera as cm
from flask import Flask, request, jsonify
import requests
from Function import calculate_steering_angle, Start_GPS, check_distance
import variables as vl

#from newP.ArrayPoint import FindArrayPoint
wavelength = 5  # אורך גל הקול
#בתהליך זה קיים מצפן, התהליך דוגם ממנו נתונים בעת הצןרך למשתנה current_angle

speed=vl.read_speed_for_exel()
#דגימה למצפן
current_angle = vl.read_compass_for_exel()

#התהליך מקבל את מיקום הרובוט המתאבד ע"י חיישן GPS ונקודה מטרה שם המוקש נמצא. התהליך אחראי על הניווט למוקש
def process_2(goal_position,stop_flag,stop_event):
    #קריאת נתוני חיישן הGPS מקובץ
    current_point=Start_GPS()
    # חישוב המרחק לנקודת המטרה
    distance_to_goal = math.sqrt((goal_position[0] - current_point[0]) ** 2 +
                                 (goal_position[1] - current_point[1]) ** 2 +
                                 (goal_position[2] - current_point[2]) ** 2)


    # חישוב זווית היגוי בין מיקום הרובוט לנקודת היעד
    steering_angle = calculate_steering_angle(current_angle, current_point, goal_position)
    print(f"סע מנקודה {current_point} בזווית {steering_angle} לנקודה {goal_position}")

    # בדיקת הגעה לנקודת המטרה
    while check_distance(current_point, goal_position, 10) == False and stop_flag == 0:
        print("הרובוט מתקדם לנקודה הבאה")
    print("הרובוט הגיע ליעדו")

    time.sleep(1)

    image_path = cm.camera()
    #איתות לסיום פעילות הרובוט
    stop_event.set()

    # שליחת הנתיב לשרת הראשי
    response = requests.post("http://localhost:3001/Image_mine", json=image_path)
    if response.status_code == 200:
        return jsonify({"message": "Request successful"})
    else:
        return jsonify({"message": "Request failed"})


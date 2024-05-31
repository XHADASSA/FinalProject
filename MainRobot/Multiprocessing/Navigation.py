import time
import Function as f
import variables as vl
#בתהליך זה קיים מצפן, התהליך דוגם ממנו נתונים בעת הצןרך למשתנה current_angle

#דגימה למצפן
current_angle = vl.read_compass_for_exel('../../data.xlsx')

def process_2(GPS,polygon_vertices,ArrayPoint1,ArrayPoint2, stop_flag):
    print("Navigation procces")
    print(f"the point un process 2 is, {GPS}")
    #הובלת הרובוט לנקודת ההתחלה
    point=ArrayPoint1[0]
    StartPoint = f.FindPoint(point)
    #חישוב המרחק בין המיקום הנוכחי של הרובוט לבין נקודת ההתחלה של הסריקה
    distance = f.calculate_distance(GPS[0], GPS[1], StartPoint[0], StartPoint[1])
    ## חישוב זווית היגוי בין מיקום הרובוט לנקודת היעד
    steering_angle = f.calculate_steering_angle(current_angle, GPS, StartPoint)
    current_point=GPS
    destination_point=StartPoint
    flag_Array=1
    i=0
    while (i-1)< len(max(ArrayPoint1,ArrayPoint2)):
        #סיבוב
        print(f"stop_flag {stop_flag}")
        print(f"סע מנקודה {current_point} בזווית {steering_angle} לנקודה {destination_point}")
        #לולאת המתנה שהרובוט יגיע ליעדו שנמצא מחוץ לשטח
        while f.check_distance(current_point, destination_point,10)==False and stop_flag==0:
            print("הרובוט מתקדם לנקודה הבאה")
        print("הרובוט הגיע ליעדו")

        #היפוך הדגל
        flag_Array=3-flag_Array
        destination_point=ArrayPoint1[i] if flag_Array==1 else ArrayPoint2[i]
        # חישוב זווית היגוי בין מיקום הרובוט לנקודת היעד
        steering_angle = f.calculate_steering_angle(steering_angle, current_point, destination_point)
        print(f"סע מנקודה {current_point} בזווית {steering_angle} לנקודה {destination_point}")
        #הרובוט מתחיל ליסוע במסלול בתוך השטח
        #כל עוד הרובוט לא יצא מהמסלול או שהרובוט עוד לא הגיע ליעדו, תתקדם ישר
        while f.is_within_polygon(current_point[0], current_point[1], polygon_vertices) or f.check_distance(current_point, destination_point,10)==False:
            print("התקדם ישר")
            time.sleep(1)
        time.sleep(2)
        destination_point=ArrayPoint1[i+1] if flag_Array==1 else ArrayPoint2[i+1]
        i+=1
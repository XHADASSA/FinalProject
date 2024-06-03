import threading as th
import Function as f
#ייבוא ארבעת התהליכים
import MainRobot.Multiprocessing.sensors as sensors
import MainRobot.Multiprocessing.PreventingObstacles as PreventingObstacles
import MainRobot.Multiprocessing.Navigation as Navigation
import MainRobot.Multiprocessing.KalmanFilter as KalmanFilter

def multiprocessNavigationInArea(polygon_vertices,ArrayPoint1,ArrayPoint2):
    #משתנה שצריך לעצור את כל התהליכים ולהפעיל את תהליך המנעות ממכשולים
    stop_flag = 0
    #הנקודה המשותפת לכל התהליכים ומשמעותה הוא מיקום הרובוט, בהתחלה היא מאותחלת בחיישן הGPS
    point=f.Start_GPS()
    # פתיחה במצב 'w' כדי לנקות את הקובץ
    with open('../../data.xlsx', 'w') as file:
        file.write('')
    #כתיבת המיקום ההתחלתי לקובץ
    KalmanFilter.add_data_to_file(point)

    p1 = th.Thread(target=sensors.process_1, args=(stop_flag,))
    p2 = th.Thread(target=Navigation.process_2, args=(point,polygon_vertices,ArrayPoint1,ArrayPoint2, stop_flag))
    p3 = th.Thread(target=PreventingObstacles.process_4, args=(stop_flag,))
    #p4 = th.Thread(target=KalmanFilter.process_3,args=(point,))

    p1.start()
    p2.start()
    p3.start()
    #p4.start()

    p1.join()
    p2.join()
    p3.join()
    #p4.join()
import threading as th
import Function as f
#ייבוא חמשת התהליכים
import sensors
import PreventingObstacles

point=(0,0)
GPS=f.GPS()

if __name__ == '__main__':
    #משתנה שצריך לעצור את כל התהליכים ולהפעיל את תהליך המנעות ממכשולים
    stop_flag = th.Event()

    p1 = th.Thread(target=sensors.process_1, args=(stop_flag,))
    #p2 = th.Thread(target=Navigation.process_2, args=(point,f.polygon_vertices, stop_flag))
    #p3 = th.Thread(target=Sensor_management.process_3, args=(sensor_array, stop_flag))
    #p4 = th.Thread(target=KalmanFilter.process_4,args=(point,))
    p5 = th.Thread(target=PreventingObstacles.process_5, args=(stop_flag,))

    p1.start()
    #p2.start()
    #p3.start()
    #p4.start()
    p5.start()

    p1.join()
    print("סוף תהליכון")
    print(f"stop flag {stop_flag.is_set()}")
    #p2.join()
    #p3.join()
    #p4.join()
    p5.join()

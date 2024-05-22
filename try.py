import random
import time
import threading
import math
import multiprocessing as ml
from multiprocessing import Manager

class Object:
    def __init__(self, signal, d, angle):
        self.signal = signal
        self.d = d
        self.angle = angle
#פונקציה המקבלת את זווית החיישן, מיקום הרובוט והמרחק בינו לבין העצם החשוד ומחזירה את מיקום העצם
def CalculatingLocationMine(sensor_angle, distance_to_object, robot_position):
    # המרת זווית חיישן לרדיאנים
    sensor_angle_radians = math.radians(sensor_angle)

    # חישוב קואורדינטות x ו-y של העצם
    object_x = robot_position[0] + distance_to_object * math.cos(sensor_angle_radians)
    object_y = robot_position[1] + distance_to_object * math.sin(sensor_angle_radians)

    # החזרת מיקום העצם
    return object_x, object_y
def sensor_update(i, sensor_array):
    print(f"Process {ml.current_process()} updating sensor {i}")
    #while True:
    for _ in range(3):
        signal = random.randint(0, 1)
        print(f"signal {signal}")
        d = random.randint(0, 10000)
        print(f"d {d}")
        sensor_array[i].signal = signal
        sensor_array[i].d = d
        print(f"Process child {ml.current_process()} - Signal: {sensor_array[i].signal}, d: {sensor_array[i].d}, angle: {sensor_array[i].angle}")
        time.sleep(1.5)
def manager_sensor(sensor_array, stop_flag):
    #while True:
    for v in range(3):
        for i in range(10):
            #There is a mine in front of the robot! Obstacles must be activated.
            if sensor_array[i].signal == 1 and i == 2:
                stop_flag.value=5
            #There is a mine in the area
            elif sensor_array[i].signal == 1:
                #שליחת הודעה למסך כולל הנתונים של זווית, מרחק, ומיקום הרובוט
                positionOfMine=CalculatingLocationMine(sensor_array[i].angle,sensor_array[i].d,[0,0])
                #שליחת המיקום לשרת הראשי
                print("נשלח מיקום עצם חשוד לשרת הראשי")
        print(f"stop_flag in manager_sensor: {stop_flag.value}")
    time.sleep(1.5)

def process_1(stop_flag):
    manager = Manager()

    processes = list(range(11))
    # יצירת מערך החיישנים המשותף לכלל התהליכים
    sensor_array = manager.list([
        Object(0, 0, 45),
        Object(0, 0, 90),
        Object(0, 0, 30),
        Object(0, 0, 60),
        Object(0, 0, 75),
        Object(0, 0, 20),
        Object(0, 0, 55),
        Object(0, 0, 80),
        Object(0, 0, 15),
        Object(0, 0, 25)
    ])

    for obj in sensor_array:
        print(f"Signal: {obj.signal}, d: {obj.d}, angle: {obj.angle}")

    print("sensors_process creating child processes")  # Added process start message
    for i in range(len(sensor_array)):  # Access object using enumerate
        #Create processes with sensor_updata from each object
        p=ml.Process(target=sensor_update, args=(i, sensor_array))
        processes[i]=p
        p.start()
    p = ml.Process(target=manager_sensor, args=(sensor_array,stop_flag))
    processes[10]=p
    p.start()

    for p in processes:
        p.join()
    print("סוף תהליכון")
    for obj in sensor_array:
        print(f"Signal: {obj.signal}, d: {obj.d}, angle: {obj.angle}")
    print(f"stop flag {stop_flag.value}")

if __name__ == '__main__':
    manager = Manager()
    stop_flag=manager.Value('i',1)
    process_1(stop_flag)


def process_2(GPS, destination_point, stop_flag):
    ## חישוב זווית היגוי בין מיקום הרובוט לנקודת היעד
    steering_angle = f.calculate_steering_angle(current_angle, GPS, destination_point)
    current_point = GPS
    while True:
        print(f"stop_flag {stop_flag}")
        while stop_flag:
            print(f"סע מנקודה {current_point} בזווית {steering_angle} לנקודה {destination_point}")
            # לולאת המתנה עד שהרובוט יגיע למרחק של 2 מטר מהעצם
            while f.check_distance(current_point, destination_point, 200) == False:
                print("הרובוט מתקדם לכיוון המוקש")
            print("הרובוט הגיע ליעדו")

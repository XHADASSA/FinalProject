import random
import time
import threading
import math
import requests
import variables as vl

class Object:
    def __init__(self, type, signal, d, angle):
        self.type=type
        self.signal = signal
        self.d = d
        self.angle = angle
#פונקציה המקבלת את זווית החיישן, מיקום הרובוט והמרחק בינו לבין העצם החשוד ומחזירה נקודה תלת מימדית של מיקום העצם
def CalculatingLocationMine(sensor_angle, distance_to_object, robot_position):
    # המרת זווית חיישן לרדיאנים
    sensor_angle_radians = math.radians(sensor_angle)

    # חישוב קואורדינטות x ו-y של העצם
    object_x = robot_position[0] + distance_to_object * math.cos(sensor_angle_radians)
    object_y = robot_position[1] + distance_to_object * math.sin(sensor_angle_radians)

    # חישוב עומק (z) העצם באמצעות משולש ישר זווית
    # נניח שהעומק (z) הוא המרחק בין פני המים (נקודת 0) לבין העצם
    object_z = distance_to_object * math.sin(sensor_angle_radians)

    # החזרת מיקום העצם ועומקו
    return object_x, object_y, object_z
def sensor_update(i, sensor_array):
    print(f"Process {threading.get_ident()} updating sensor {i}")
    #while True:
    for _ in range(3):
        signal = random.choices([True, False], weights=[0.3, 0.7])[0]
        d = random.randint(0, 1000)
        type = random.choices([True, False], weights=[0.7, 0.3])[0] if signal else False
        sensor_array[i].signal = signal
        sensor_array[i].d = d
        sensor_array[i].type=type
        print(f"Process child {threading.get_ident()} - Signal: {sensor_array[i].signal}, d: {sensor_array[i].d}, angle: {sensor_array[i].angle}")
        time.sleep(1)

#חיישן מספר 1 הוא חיישן קדמי
#חיישן מספר 2 הוא חיישן עליון

# הגדרת כתובת האתר של שרת ראשי
server_url = "http://localhost:3001/Main-robot"

def manager_sensor(sensor_array, stop_flag):
    while True:
        for i in range(10):
            #There is a mine in front of the robot! Obstacles must be activated.
            if sensor_array[i].signal and i == 1:
                if sensor_array[i].type:
                    positionOfMine = CalculatingLocationMine(sensor_array[i].angle, sensor_array[i].d, [0, 0])
                    # שליחת המיקום לשרת הראשי
                    data = {'waypoint': positionOfMine}
                    response = requests.post(server_url, json=data)
                    print(response)
                    print("נשלח מיקום עצם חשוד לשרת הראשי")
                stop_flag=1
            #There is a mine in the area
            elif sensor_array[i].signal and sensor_array[i].type:
                #שליחת הודעה למסך כולל הנתונים של זווית, מרחק, ומיקום הרובוט
                positionOfMine=CalculatingLocationMine(sensor_array[i].angle,sensor_array[i].d,[0,0])
                #שליחת המיקום לשרת הראשי
                data = {'waypoint': positionOfMine}
                response = requests.post(server_url, json=data)
                print(response)
                print("נשלח מיקום עצם חשוד לשרת הראשי")
        print(f"stop_flag in manager_sensor: {stop_flag}")
        time.sleep(1)

def process_1(stop_flag):
    processes = list(range(11))
    # יצירת מערך החיישנים המשותף לכלל התהליכים
    sensor_array = [
        Object(False, False,0, 0),
        Object(False, False,0, 0),
        Object(False, False,0, 0),
        Object(False, False,0, 0),
        Object(False, False,0, 0),
        Object(False, False,0, 0),
        Object(False, False,0, 0),
        Object(False, False,0, 0),
        Object(False, False,0, 0),
        Object(False, False,0, 0)
    ]

    angle_sensors=vl.read_angle_sensors_for_exel()

    for i in range(len(angle_sensors)):
        sensor_array[i].angle = angle_sensors[i]

    for obj in sensor_array:
        print(f"Signal: {obj.signal}, d: {obj.d}, angle: {obj.angle}")

    print("sensors_process creating child processes")  # Added process start message
    for i in range(len(sensor_array)):  # Access object using enumerate
        #Create processes with sensor_updata from each object
        p=threading.Thread(target=sensor_update, args=(i, sensor_array))
        processes[i]=p
        p.start()
    p = threading.Thread(target=manager_sensor, args=(sensor_array,stop_flag))
    processes[10]=p
    p.start()

    for p in processes:
        p.join()
    #for obj in sensor_array:
    #    print(f"Signal: {obj.signal}, d: {obj.d}, angle: {obj.angle}, Type: {obj.type}")
    #print(f"stop flag {stop_flag}")

#stop_flag=0
#process_1(stop_flag)
import random
import time
import threading

class Object:
    def __init__(self, signal, d, angle):
        self.signal = signal
        self.d = d
        self.angle = angle

def sensor_update(i, sensor_array):
    print(f"Process {threading.get_ident()} updating sensor {i}")
    while True:
    #for _ in range(3):
        signal = random.randint(0, 1)
        d = random.randint(0, 10000)
        sensor_array[i].signal = signal
        sensor_array[i].d = d
        print(f"Process child {threading.get_ident()} - Signal: {sensor_array[i].signal}, d: {sensor_array[i].d}, angle: {sensor_array[i].angle}")
        time.sleep(1.5)
def manager_sensor(sensor_array, stop_flag):
    while True:
        for i in range(10):
            #There is a mine in front of the robot! Obstacles must be activated.
            if sensor_array[i].signal == 1 and i == 2:
                stop_flag.set()
            #There is a mine in the area
            elif sensor_array[i].signal == 1:
                #שליחת הודעה למסך כולל הנתונים של זווית, מרחק, ומיקום הרובוט
                print("נשלח רובוט מתאבדדדדדדדד")
        print(f"stop_flag in manager_sensor: {stop_flag.is_set()}")
        time.sleep(1.5)

def process_1(stop_flag):
    processes = list(range(11))
    # יצירת מערך החיישנים המשותף לכלל התהליכים
    sensor_array = [
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
    ]

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
    print("סוף תהליכון")
    for obj in sensor_array:
        print(f"Signal: {obj.signal}, d: {obj.d}, angle: {obj.angle}")
    print(f"stop flag {stop_flag.is_set()}")

#stop_flag=threading.Event()
#process_1(stop_flag)
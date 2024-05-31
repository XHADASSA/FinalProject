import time
import numpy as np
import variables as vl
import os
speed=vl.read_speed_for_exel()

'''
תודה ה'!
'''
def add_data_to_file(point):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../../point.txt')
    with open(file_path, 'a') as file:
        file.write(f"\n{point[0]} {point[1]} {speed}")

def GPS_update():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../../point.txt')
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
        print(last_line)
        x, y, speed = map(float, last_line.split())
        return [[x, y], speed]

def process_3():
    gps_measurements=[]

    # עמדת התחלה
    X = np.array([[0], [0]]) # initial position and speed

    # אי ודאות ראשונית
    P = np.array([[1000, 0], [0, 1000]])

    # מטריצת מעבר מצב
    A = np.array([[1, 1], [0, 1]])

    # מטריצת מדידה
    H = np.array([[1, 0]])

    # אי ודאות מדידה
    R = np.array([[1]])

    # רעש תהליך
    Q = np.array([[0.0001, 0], [0, 0.0001]])

    # אתחול משתנים
    I = np.eye(2)
    gps_measurements=[]
    while True:
        # קריאת מיקום הרובוט מהקובץ
        gps_measurements.append(GPS_update())
        print(gps_measurements)
        for measurement in gps_measurements:
            print(measurement)
            # נְבוּאָה
            X = np.dot(A, X)
            P = np.dot(np.dot(A, P), A.T) + Q

            # עדכון
            if len(measurement) == 2:
                Z = np.array([measurement[0][0], measurement[1]]).reshape(2, 1)  # Reshape the measurement
            else:
                print("Error: Measurement is not in the expected format")
                continue

            Z = np.array([Z[1][0], Z[0][0]]) # Swap Z values unconditionally
            y = Z - np.dot(H, X)
            S = np.dot(np.dot(H, P), H.T) + R
            K = np.dot(np.dot(P, H.T), np.linalg.inv(S))
            X = X + np.dot(K, y)
            P = np.dot((I - np.dot(K, H)), P)

            # Update global variable point with the estimated position
            point = (X[0][0], X[1][0])
            print(point)
            #הוספת הדגימה לקובץ
            add_data_to_file((X[0][0], X[1][0]))
            # הדפס מיקום ומהירות משוערים
            print("מהירות משוערת: ", X[0][0])
            print("מיקום משוער: ", X[1][0])

            time.sleep(1)

#process_3()
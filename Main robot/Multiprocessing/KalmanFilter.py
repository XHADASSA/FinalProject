import time
import numpy as np
import random

'''
תהליך זה דוגם בכל שניה את חיישן הGPS,
התהליך מוסיף את הדגימה לרשימת הדגימות ומסנן קלמן משערך את המיקום לפיהם
ברשימת הדגימות יש נקודה שמוגרלת ומהירות שמחושבת ע"י נוסחא
תודה ה'!
'''
def generate_random_point(min_range, max_range):
    x = random.randint(min_range, max_range)
    y = random.randint(min_range, max_range)
    return x, y
def GPS_update(lastPoint):
    # gps_measurements[0]=מיקום רובוט, gps_measurements[1]=מהירות רובוט
    # חיישן ה-GPS נדגם כל חצי שנייה
    # מיקום נוכחי
    current_location = generate_random_point(0,100)
    print("דגימת GPS וחישוב מהירות")
    # calculate speed
    reduced_point = [current_location[0] - lastPoint[0], current_location[1] - lastPoint[1]]
    speed = reduced_point[0] /1
    print(f"current location: {current_location}, lastPoint:{lastPoint}, calculate speed: {speed}")
    return [current_location, speed]

def process_3():
    gps_measurements=[]

    # starting position
    X = np.array([[0], [0]]) # initial position and speed

    # Initial uncertainty
    P = np.array([[1000, 0], [0, 1000]])

    # State transition matrix
    A = np.array([[1, 1], [0, 1]])

    # Measurement matrix
    H = np.array([[1, 0]])

    # Measurement uncertainty
    R = np.array([[1]])

    # Process noise
    Q = np.array([[0.0001, 0], [0, 0.0001]])

    # Initialize variables
    I = np.eye(2)
    gps_measurements.append(GPS_update((5, 2)))
    gps_measurements.append(GPS_update(gps_measurements[0][0]))
    print(gps_measurements)
    while True:
        for measurement in gps_measurements:
            # Prediction
            X = np.dot(A, X)
            P = np.dot(np.dot(A, P), A.T) + Q

            # Update
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
            #הוספת דגימה למערך
            gps_measurements.append(GPS_update(gps_measurements[len(gps_measurements)-1][0]))
            # הדפס מיקום ומהירות משוערים
            print("מהירות משוערת: ", X[0][0])
            print("מיקום משוער: ", X[1][0])
            point=X[1][0]
            time.sleep(1)
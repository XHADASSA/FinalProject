'''import serial

def get_current_location_from_serial(port='COM3', baudrate=9600, timeout=1):
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            while True:
                line = ser.readline().decode('ascii', errors='replace')
                if line.startswith('$GPGGA'):  # משפט NMEA המספק נתוני מיקום
                    parts = line.split(',')
                    if len(parts) > 5:
                        latitude = parse_nmea_lat_long(parts[2], parts[3])
                        longitude = parse_nmea_lat_long(parts[4], parts[5])
                        return latitude, longitude
    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
        return None

def parse_nmea_lat_long(value, direction):
    if not value or not direction:
        return None
    degrees = float(value[:2])
    minutes = float(value[2:])
    decimal_degrees = degrees + (minutes / 60)
    if direction == 'S' or direction == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees

# קריאת הפונקציה
current_location = get_current_location_from_serial()
if current_location:
    print(f"Current location is: Latitude {current_location[0]}, Longitude {current_location[1]}")
else:
    print("Unable to get the current location.")'''

import numpy as np
import sys

# from plot import plot_trajectory, plot_point, plot_covariance_2d
def read_x():
    points = []
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if line:
            x, y, vx, vy = map(float, line.split(", "))
            x = np.array([x, y, vx, vy])
    return x

def read_measurment():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if line:
            x, y, = map(float, line.strip("()").split(", "))
            x = [x, y, ]
    return x


class UserCode:
    def __init__(self, x, sigma):
        dt = 0.005

        # State-transition model
        self.A = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        # Observation model
        self.H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])

        # TODO: Play with the noise matrices
        # Process/State noise
        vel_noise_std = 0.005
        pos_noise_std = 0.005
        self.Q = np.array([
            [pos_noise_std * pos_noise_std, 0, 0, 0],
            [0, pos_noise_std * pos_noise_std, 0, 0],
            [0, 0, vel_noise_std * vel_noise_std, 0],
            [0, 0, 0, vel_noise_std * vel_noise_std]
        ])

        # Sensor/Measurement noise
        measurement_noise_std = 0.5
        self.R = measurement_noise_std * measurement_noise_std * np.identity(2)

        # self.x = np.zeros((4,1)) #Initial state vector [x,y,vx,vy]
        # self.sigma = np.identity(4) #Initial covariance matrix
        self.x = x
        self.sigma = np.cov(sigma)


def predictState(self, A, x):
    '''
    :param A: State-transition model matrix
    :param x: Current state vector
    :return x_p: Predicted state vector as 4x1 numpy array
    '''

    # TODO: Predict the next state
    x_p = np.zeros((4, 1))
    x_p = np.dot(A, x)

    return x_p


def predictCovariance(self, A, sigma, Q):
    sigma_p = np.dot(np.dot(A, sigma), np.transpose(A)) + Q
    return sigma_p


def calculateKalmanGain(self, sigma_p, H, R):
    k = np.dot(np.dot(sigma_p, np.transpose(H)), np.linalg.inv(np.dot(H, np.dot(sigma_p, np.transpose(H))) + R))
    return k


def correctState(self, z, x_p, k, H):
    '''
    :param z: Measurement vector
    :param x_p: Predicted state vector
    :param k: Kalman gain
    :param H: Observation model
    :return x: Corrected state vector as 4x1 numpy array
    '''

    # TODO: Correct the current state prediction with the measurement
    x = np.zeros((4, 1))
    x = x_p + np.dot(k, z - np.dot(H, x_p))

    return x


def correctCovariance(self, sigma_p, k, H):
    sigma = np.dot((np.identity(4) - np.dot(k, H)), sigma_p)
    return sigma


def state_callback(self):
    self.x = self.predictState(self.A, self.x)
    self.sigma = self.predictCovariance(self.A, self.sigma, self.Q)

    # visualize position state
    # plot_trajectory("kalman", self.x[0:2])
    # plot_covariance_2d("kalman", self.sigma[0:2,0:2])


def measurement_callback(self, measurement):
    '''
    :param measurement: vector of measured coordinates
    '''

    # visualize measurement
    # plot_point("gps", measurement)
    Pre_x = self.predictState(self.A, self.x)
    Pre_sigma = self.predictCovariance(self.A, self.sigma, self.Q)
    k = self.calculateKalmanGain(Pre_sigma, self.H, self.R)

    self.x = self.correctState(measurement, Pre_x, k, self.H)
    self.sigma = self.correctCovariance(Pre_sigma, k, self.H)
    return self.x, self.sigma

    # visualize position state
    # plot_trajectory("kalman", self.x[0:2])
    # plot_covariance_2d("kalman", self.sigma[0:2,0:2])


# x=np.array([1,2,20,20])
x = read_x()

sigma = np.array([0.2, 0.2, 0.2, 0.2])
kf = UserCode(x=x, sigma=sigma)
measurement = read_measurment()
print(kf.measurement_callback(measurement))
# for i in range(10):
# print(kf.measurement_callback([i,i+5]))


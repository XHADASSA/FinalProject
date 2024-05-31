import threading as th
import Function as f

from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app);

#ייבוא חמשת התהליכים
import MainRobotsSuicide.RobotsSuicide1.sensors as sensors
import MainRobotsSuicide.RobotsSuicide1.PreventingObstacles as PreventingObstacles
import MainRobotsSuicide.RobotsSuicide1.Navigation as Navigation
import MainRobotsSuicide.RobotsSuicide1.KalmanFilter as KalmanFilter
point=(0,0)
GPS=f.GPS()

def main_multiprocessing_of_robot_suicide(point):
    #משתנה שצריך לעצור את כל התהליכים ולהפעיל את תהליך המנעות ממכשולים
    stop_flag = th.Event()

    p1 = th.Thread(target=sensors.process_1, args=(stop_flag,))
    p2 = th.Thread(target=Navigation.process_2, args=(point,stop_flag))
    p3 = th.Thread(target=KalmanFilter.process_3,args=(point,))
    p4 = th.Thread(target=PreventingObstacles.process_4, args=(stop_flag,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

@app.route('/Robots-suicide1', methods=['POST'])
def Manager_Main_Robots_suicide():
    point = request.get_json()
    main_multiprocessing_of_robot_suicide(point)
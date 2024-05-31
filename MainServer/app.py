from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from MainRobotsSuicide.RobotsSuicide1.main_multiprocessing import main_multiprocessing_of_robot_suicide
from MainRobot.Multiprocessing.main_multiprocessing import multiprocessNavigationInArea
import variables as vl
import MainServer.global_state as global_state  # יבוא מודול ניהול מצב
import os

app = Flask(__name__)
CORS(app);
status=False
wavelength=vl.read_wavelength_for_exel('../data.xlsx')


@app.route('/python-status', methods=['get'])
def getStatus():
    return False

@app.route('/getWaypoint', methods=['GET'])
def updatePoint():
    file_path = '../data.xlsx'
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if not lines:
                return jsonify({"error": "File is empty"}), 404

            last_line = lines[-1].strip()
            data = last_line.split()
            latitude = float(data[0])
            longitude = float(data[1])

            waypoint = {"latitude": latitude, "longitude": longitude}
            return jsonify(waypoint)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
dataArray=None
# לקוח ריאקט שולח לו מערך נקודות והוא מחזיר את המערך מעובד ללקוח
@app.route('/python-endpoint', methods=['POST'])
def handle_markers():
    print("The client runs successfully...")
    data = request.get_json()
    print("the array is checked...")
    print(f'the tada{data}')
    success = True
    global_state.dataArray=[[int(point['x']), int(point['y'])] for point in data]
    print(global_state.dataArray)

    from MainServer.FindArrayPoint import FindPoints
    global_state.ArrayPoint1,global_state.ArrayPoint2=FindPoints(global_state.dataArray,[0,0],wavelength)
    response_data = {
        'success': success,
        'points1': global_state.ArrayPoint1,
        'points2': global_state.ArrayPoint2
    }
    multiprocessNavigationInArea(global_state.dataArray,global_state.ArrayPoint1, global_state.ArrayPoint2)
    return jsonify(response_data)

# האזנה לבקשות משרת הרובוטים המתאבדים ושליחת בקשות אליו

#קבלת נקודת מוקש מהרובוט הראשי והרצת תוכנת הרובוט המתאבד עם הנתון שהתקבל

@app.route('/Main-Robots-suicide', methods=['POST'])
def handle_Main_Robots_suicide():
    point = request.get_json()
    print(f"the position of main {point}")
    #הרצת תוכנת הרובוט המתאבד
    main_multiprocessing_of_robot_suicide(point)
    return {'message': 'Received request from Main Robots-suicide'}

# האזנה לבקשות מהרובוט הראשי ושליחת בקשות אליו


@app.route('/Main-robot', methods=['POST'])
def handle_Main_robot():
    data = request.get_json()
    response = requests.post("http://localhost:3001/Main-Robots-suicide", json=data)
    if response.status_code == 200:
        return jsonify({"message": "Request successful"})
    else:
        return jsonify({"message": "Request failed"})


if __name__ == '__main__':
    app.run(host='localhost', port=3001)


from flask import Flask, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import io
import requests
from flask_cors import CORS
from MainRobotsSuicide.RobotsSuicide1.main_multiprocessing import main_multiprocessing_of_robot_suicide
from MainRobot.Multiprocessing.main_multiprocessing import multiprocessNavigationInArea
import variables as vl
import MainServer.global_state as global_state  # יבוא מודול ניהול מצב
import os
from Function import Checking_integrity_points

app = Flask(__name__)
CORS(app);
status=False
wavelength=vl.read_wavelength_for_exel()


@app.route('/python-status', methods=['get'])
def getStatus():
    return False

# לקוח ריאקט שולח לו מערך נקודות והוא מחזיר את המערך מעובד ללקוח
@app.route('/python-endpoint', methods=['POST'])
def handle_markers():
    print("The client runs successfully...")
    data = request.get_json()
    print("the array is checked...")
    print(f'the tada{data}')
    global_state.dataArray=[[int(point['x']), int(point['y'])] for point in data]
    #בדיקת תקינות לנקודות
    success = Checking_integrity_points(global_state.dataArray)
    print(f"success: {success}")
    if success:
        print(global_state.dataArray)

        from MainServer.FindArrayPoint import FindPoints
        global_state.ArrayPoint1,global_state.ArrayPoint2=FindPoints(global_state.dataArray,[0,0],wavelength)
        print(f"the first array: {global_state.ArrayPoint1}")
        print(f"the secound array: {global_state.ArrayPoint2}")
        multiprocessNavigationInArea(global_state.dataArray, global_state.ArrayPoint1, global_state.ArrayPoint2)

    response_data = {
        'success': success,
        'points1': global_state.ArrayPoint1,
        'points2': global_state.ArrayPoint2
    }
    return jsonify(response_data)

#לקוח ריאקט שולח בקשה לקבל את מיקום הרובוט, השרת קורא את מיקום הרובוט מקובץ ושולח אותו חזרה ללקוח
@app.route('/getWaypoint', methods=['GET'])
def updatePoint():
    file_path = '../point.txt'
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if not lines:
                return jsonify({"error": "File is empty"}), 404

            last_line = lines[-1].strip()
            data = last_line.split()
            if len(data) < 2:
                return jsonify({"error": "File format is incorrect"}), 400

            latitude = float(data[0])
            longitude = float(data[1])

            waypoint = {"latitude": latitude, "longitude": longitude}
            return jsonify(waypoint)

    except Exception as e:
        return jsonify({"error": str(e)}), 501

# קבלת נקודה חשודה מהרובוט הראשי ושליחת בקשה לשרת הרובוטים המתאבדים
@app.route('/Main-robot', methods=['POST'])
def handle_Main_robot():
    data = request.get_json()
    response = requests.post("http://localhost:3002/Main-Robots-suicide", json=data)
    if response.status_code == 200:
        return jsonify({"message": "Request successful"})
    else:
        return jsonify({"message": "Request failed"})


socketio = SocketIO(app, cors_allowed_origins="*")
#שרת המאזין לתמונת מוקש מהרובוט המתאבד
@app.route('/Image_mine', methods=['POST'])
def Receiving_image_mine():
    image_mine = request.json.get('image_path')

    if image_mine:
        # שליחת נתיב התמונה ללקוח דרך WebSocket
        socketio.emit('image_path', {'image_path': image_mine}, broadcast=True)
        return 'Image path received and sent to client', 200
    else:
        return 'No image path provided', 400

if __name__ == '__main__':
    app.run(host='localhost', port=3001)

from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from ArrayPoint import FindArrayPoint
#import MainRobotsSuicide.RobotsSuicide1.main_multiprocessing as mm

app = Flask(__name__)
CORS(app);
status=False


@app.route('/python-status', methods=['get'])
def getStatus():
    #if status==False:
    #    status=True
    #    return True
    return False

@app.route('/getWaypoint', methods=['GET'])
def updatePoint():
    waypoint = {"latitude": 0.000139, "longitude": 0.000279}
    return jsonify(waypoint)

# Endpoint for handling incoming requests from the React client
@app.route('/python-endpoint', methods=['POST'])
def handle_markers():
    print("The client runs successfully...")
    data = request.get_json()
    print("the array is checked...")
    print(f'the tada{data}')
    success = True
    dataArray=[[int(point['x']), int(point['y'])] for point in data]
    print(dataArray)
    ArrayPoint=FindArrayPoint([0,0],data)
    response_data = {
        'success': success,
        'points': ArrayPoint
    }
    return jsonify(response_data)

# האזנה לבקשות משרת הרובוטים המתאבדים ושליחת בקשות אליו
@app.route('/Main-Robots-suicide', methods=['POST'])
def handle_Main_Robots_suicide():
    data = request.get_json()
    print(f"Main-Robots-suicide {data}")
    #הרצת תוכנת הרובוט המתאבד
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

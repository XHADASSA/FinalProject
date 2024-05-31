from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from Function import find_closest_point
from MainRobotsSuicide.RobotsSuicide1.main_multiprocessing import main_multiprocessing_of_robot_suicide

app = Flask(__name__)
CORS(app);

# URL of the Flask server
server_url = 'http://localhost:3001/Main-Robots-suicide'

# Sending a POST request to the server
response = requests.post(server_url, json={'key': 'value'})

# Extracting and printing the response from the server
print(response.json())

location_suicide_robots=[[0,0],[0,0]]

@app.route('/Manager-Robots-suicide', methods=['POST'])
def Manager_Main_Robots_suicide():
    point = request.get_json()
    print(f"the position of main {point}")
    #בדיקה מי מהרובוטים הכי קרוב למטרה
    find_closest_point(point,location_suicide_robots)
    #הרצת תוכנת הרובוט המתאבד
    main_multiprocessing_of_robot_suicide(point)
    return {'message': 'Received request from Main Robots-suicide'}


#ממתינה לקבלת מזהה הרובוט ומיקומו ומכניסה למערך המכיל את מיקומי הרובוט
@app.route('/final_point', methods=['POST'])
def final_point_of_robot_suicide():
    point, i = request.get_json()
    location_suicide_robots[i]=point
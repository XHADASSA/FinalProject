from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from Function import find_closest_point

app = Flask(__name__)
CORS(app);

location_suicide_robots=[[0,0]]

@app.route('/Manager-Robots-suicide', methods=['POST'])
def Manager_Main_Robots_suicide():
    point = request.get_json()
    print(f"the position of main {point}")
    #בדיקה מי מהרובוטים הכי קרוב למטרה
    number=find_closest_point(point,location_suicide_robots)
    #שינוי מיקום הרובוט המתאבד לנקודת היעד
    location_suicide_robots[number]=point
    #שליחת בקשה לרובוט המתאבד
    url="http://localhost:3001/Robots-suicide"
    url=f"{url}{number}"
    print(f"robots suicide number {number} go to goal. it url is {url}")
    response = requests.post(url, json=point)
    return {'message': f'Received request from Robots-suicide {number}'}

if __name__ == '__main__':
    app.run(host='localhost', port=3002)
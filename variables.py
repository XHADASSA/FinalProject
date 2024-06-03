import pandas as pd
import MainServer.global_state as global_state
import os


def read_wavelength_for_exel():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data.xlsx')
    #קריאת אורך גל הקול מהקובץ
    df=pd.read_excel(file_path, sheet_name='wavelength', header=None, usecols="A:A", nrows=1)
    wavelength=(df.iloc[:, 0].tolist())[0]
    return wavelength
#print(read_wavelength_for_exel())
def read_speed_for_exel():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data.xlsx')
    #קריאת אורך גל הקול מהקובץ
    df=pd.read_excel(file_path, sheet_name='speed', header=None, usecols="A:A", nrows=1)
    speed=(df.iloc[:, 0].tolist())[0]
    return speed


def read_compass_for_exel():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data.xlsx')
    #קריאת אורך גל הקול מהקובץ
    df=pd.read_excel(file_path, sheet_name='CompassValues', header=None, usecols="A:A", nrows=1)
    compass=(df.iloc[:, 0].tolist())[0]
    return compass

def read_angle_sensors_for_exel():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data.xlsx')
    # קריאת הנתונים מקובץ האקסל
    sheet_name = 'AngleSensors'

    # קריאת הגיליון לתוך DataFrame של pandas
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # המרת טור A למערך
    data_array = df.iloc[:, 0].tolist()

    # החזרת המערך
    return data_array

def GPS(dataArray):
    """
    מוצא נקודה שמחוץ לצורה סגורה
    :param polygon: רשימת נקודות היוצרות את הצורה
    :return: נקודה (x, y) שמחוץ לצורה
    """
    # הפקת קואורדינטות ה-X וה-Y מהנקודות
    x_coords = [point[0] for point in dataArray]
    y_coords = [point[1] for point in dataArray]

    # מציאת המקסימום והמינימום של קואורדינטות ה-X וה-Y
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # הוספת נקודה מחוץ לטווח המינימום והמקסימום כדי להבטיח שהיא מחוץ לצורה
    outside_point = (max_x + 1, max_y + 1)

    return outside_point

#point_GPS = GPS(global_state.dataArray)

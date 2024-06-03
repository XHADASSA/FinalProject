import time

def process_4(stop_flag):
    while True:
        if stop_flag==1:
            # כל עוד דגל העצירה שווה ל1 סימן שמהחיישן הקידמי חוזר גל קול ויש מוקש ממול
            while stop_flag==1:
                print("רד למטה")
                time.sleep(2)
            print("לך קדימה")
            time.sleep(2)
            #התקדם קדימה כל עוד החיישן העליון מחזיר לך שהגל קול שלו חוזר
            while stop_flag==2:
                print("לך קדימה")
                time.sleep(2)
            #ברגע ש2 חישני הכיוון (העליון והקדמי) מחזירים 0 תעלה למעלה
            while stop_flag==0:
                print("תעלה למעלה")
                time.sleep(2)
            stop_flag.clear()
        time.sleep(1)
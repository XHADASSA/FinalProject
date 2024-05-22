import Function as f
from queue import Queue

#מערך הנקודות שהתקבל
polygon_vertices=f.polygon_vertices

point=[-2,4]

def FindArrayPoint(GPS,polygon_vertices):
    ArrayPoint = Queue()
    index=f.Start_Point(f.polygon_vertices, GPS)
    polygon_vertices=polygon_vertices[index:] + polygon_vertices[:index]
    n=len(polygon_vertices)
    print(polygon_vertices,n)
    for i in range(n-1):
        print(i)
        #מציאת משוואת ישר בין 2 נקודות
        line_equation1 = f.find_line_equation(polygon_vertices[(i+1) % n], polygon_vertices[(i+2) % n])
        line_equation2 = f.find_line_equation(polygon_vertices[(i+1) % n], polygon_vertices[(i) % n])
        #מציאת הזווית בין שניהם, המרה לחיובי והפחתת 90 בעת הצורך
        angle = abs(f.calculate_angle(line_equation1, line_equation2))
        print(f"הזווית הנוכחית {angle}")
        if angle>90: angle=angle - 90
        print(f"הזווית הנוכחית לאחר השינוי {angle}")
        #חישוב היתר שישמש למרחק בין הנקודות
        paste = f.calculate_sides(angle)
        print("paste "+str(paste))
        #חישוב כל הנקודות שעל הצלע
        print(f"חישוב כל הנקודות שעל הצלע עבור הנקודות {polygon_vertices[(i+1) % n]},{polygon_vertices[(i+2) % n]}\n")
        A=(f.Create_Sequence_Points(polygon_vertices[(i+1) % n],polygon_vertices[(i+2) % n],paste))
        f.print_queue(A)
        #מיזוג המערך של הצלע שחזרה עם המערך הגדול
        ArrayPoint=f.merge_queues(ArrayPoint,A)
    print("print_all_queue")
    f.print_queue(ArrayPoint)
    return ArrayPoint

def division(ArrayPoint):
    # חלוקת המערך לשניים
    first_part = ArrayPoint[:len(ArrayPoint) // 2]  # First half of the array
    second_part =ArrayPoint[len(ArrayPoint) // 2:]  # Second half of the array
    # הפיכת המערך השני
    second_part.reverse()
    # החזרת שני המערכים ביניהם מנווט הרובוט
    return first_part, second_part
ArrayPoint=Queue()
ArrayPoint=f.merge_queues(ArrayPoint,FindArrayPoint([0,0],polygon_vertices))
print("\n סיום יצירת הנקודות")
f.print_queue(ArrayPoint)
ArrayPoint=f.convert_queue_to_array(ArrayPoint)

[print(item) for item in ArrayPoint]
#חלוקת המערך לשתיים
first_part,second_part=division(ArrayPoint)

[print(item) for item in first_part]
[print(item) for item in second_part]

A=Queue()
A.put((2,5))
A.put((5,8))
B=Queue()
B.put((2,5))
B.put((5,8))
f.print_queue(f.merge_queues(B,A))
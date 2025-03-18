import mediapipe as mp
import os
os.environ["GLOG_minloglevel"] ="3"
import cv2
import math

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_drawing_styles = mp.solutions.drawing_styles

mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)

points = [[5,6,66],
          [5,6,296]]

cap = cv2.VideoCapture(0)

def gradient(pt1,pt2):
    try:
        return (pt2[1]-pt1[1])/(pt2[0]-pt1[0])
    except ZeroDivisionError:
        return 0
 
#3점이 있을 때 점 사이의 각도를 구하는 코드
def getAngle(pt1, pt2, pt3):
    m1 = gradient(pt1,pt2)
    m2 = gradient(pt1,pt3)
    try:
        angR = math.atan((m2-m1)/(1+(m2*m1))) #atan = arctan(3번 과정)
        return math.degrees(angR)
    except ZeroDivisionError: # 오류 예외 처리(0으로 나눌 경우)
        return 0

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        # mp_drawing.draw_landmarks(image=image, landmark_list=results.face_landmarks, connections=mp_holistic.FACEMESH_TESSELATION, landmark_drawing_spec=None,
                                #   connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
        # mp_drawing.draw_landmarks(image=image, landmark_list=results.face_landmarks, connections=mp_holistic.FACEMESH_CONTOURS, landmark_drawing_spec=None,
                                #   connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

        if results.face_landmarks:
            lm_return = results.face_landmarks.landmark
            
            left = abs(math.floor(getAngle((lm_return[6].x,lm_return[6].y), (lm_return[5].x,lm_return[5].y), (lm_return[66].x,lm_return[66].y))))-20
            right = abs(math.floor(getAngle((lm_return[6].x,lm_return[6].y), (lm_return[5].x,lm_return[5].y), (lm_return[296].x,lm_return[296].y)))-20)
            lip = getAngle((lm_return[212].x,lm_return[212].y), (lm_return[13].x,lm_return[13].y), (lm_return[14].x,lm_return[14].y))
            
            fin_data = math.floor(left+right+lip)
            
            if fin_data > 65:
                print('up')
            else:
                print('down')

        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
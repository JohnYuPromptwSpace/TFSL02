import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque

actions = [['sorry', 'good'],
           ['hello', 'school']]
seq_length = 30


modelMono = load_model('models/model_tfslMono.h5')
modelDuo = load_model('models/model_tfslDuo.h5')

# MediaPipe hands model
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

seq_left = []
action_seq_left = []
left_this_act = None

seq_right = []
action_seq_right = []
right_this_act = None

final_action = ""

action_seq_left = deque(action_seq_left)
action_seq_right = deque(action_seq_right)

# print()

cap = cv2.VideoCapture(1)

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_styled_landmarks(image, results):
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             ) 
    # Draw right hand connections  
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             ) 

def predict_left(result, handCount):
    global seq_length
    res = result.left_hand_landmarks

    joint = np.zeros((21, 4))
    for j, lm in enumerate(res.landmark):
        joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

    # Compute angles between joints
    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3] # Parent joint
    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3] # Child joint
    v = v2 - v1 # [20, 3]
    # Normalize v
    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
    
    # Get angle using arcos of dot product
    angle = np.arccos(np.einsum('nt,nt->n',
        v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
        v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

    angle = np.degrees(angle) # Convert radian to degree

    d = np.concatenate([joint.flatten(), angle])
    
    seq_left.append(d)

    if len(seq_left) < seq_length:
        return None

    input_data = np.expand_dims(np.array(seq_left[-seq_length:], dtype=np.float32), axis=0)

    if handCount == 1:
        y_pred = modelMono.predict(input_data,verbose=None).squeeze()
    else:
        y_pred = modelDuo.predict(input_data,verbose=None).squeeze()

    i_pred = int(np.argmax(y_pred))
    conf = y_pred[i_pred]

    if conf < 0.9:
        return None
    
    action = actions[handCount-1][i_pred]
    action_seq_left.append(action)

    if len(action_seq_left) < 3:
        return None

    left_this_act = None
    if action_seq_left[-1] == action_seq_left[-2] == action_seq_left[-3]:
        left_this_act = action
        action_seq_left.popleft()
    return left_this_act

def predict_right(result, handCount):
    res = result.right_hand_landmarks

    joint = np.zeros((21, 4))
    for j, lm in enumerate(res.landmark):
        joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

    # Compute angles between joints
    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3] # Parent joint
    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3] # Child joint
    v = v2 - v1 # [20, 3]
    # Normalize v
    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

    # Get angle using arcos of dot product
    angle = np.arccos(np.einsum('nt,nt->n',
        v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
        v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

    angle = np.degrees(angle) # Convert radian to degree

    d = np.concatenate([joint.flatten(), angle])

    seq_right.append(d)

    if len(seq_right) < seq_length:
        return None

    input_data = np.expand_dims(np.array(seq_right[-seq_length:], dtype=np.float32), axis=0)

    if handCount == 1:
        y_pred = modelMono.predict(input_data,verbose=None).squeeze()
    else:
        y_pred = modelDuo.predict(input_data,verbose=None).squeeze()

    i_pred = int(np.argmax(y_pred))
    conf = y_pred[i_pred]

    if conf < 0.9:
        return None
            
    action = actions[handCount-1][i_pred]
    action_seq_right.append(action)

    if len(action_seq_right) < 3:
        return None

    right_this_act = None
    if action_seq_right[-1] == action_seq_right[-2] == action_seq_right[-3]:
        right_this_act = action
        action_seq_right.popleft()
    return right_this_act

while cap.isOpened():
    ret, img = cap.read()

    img = cv2.flip(img, 1)
    img, result = mediapipe_detection(img, holistic)
    draw_styled_landmarks(img, result)
    final_action = None
    
    if result.left_hand_landmarks or result.right_hand_landmarks:
        if result.left_hand_landmarks and result.right_hand_landmarks:
            leftPrediction = predict_left(result,2)
            rightPrediction = predict_right(result,2)
            if leftPrediction == rightPrediction:
                final_action = leftPrediction
        else:
            if result.left_hand_landmarks:
                final_action = predict_left(result,1)
            else:
                final_action = predict_right(result,1)
    
    
    cv2.rectangle(img, (0,0), (640, 40), (245, 117, 16), -1)
    cv2.putText(img, final_action, org=(20,20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
    
    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break
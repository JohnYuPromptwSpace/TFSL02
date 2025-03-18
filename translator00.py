import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

actions = ['hello', 'sorry']
seq_length = 30

model = load_model('models/model_right.h5')

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

actions_dict = [
    ["hello", "hello",1],
    ["sorry", "sorry",0]
]

final_action = ""

acc_bank = 0.8

cap = cv2.VideoCapture(0)

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_styled_landmarks(image, results):
    # Draw left hand connections
    # mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
    #                          mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
    #                          mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
    #                          ) 
    # # Draw right hand connections  
    # mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
    #                          mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
    #                          mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
    #                          ) 
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                             ) 

def get_left_SL(res):
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

    y_pred = model.predict(input_data).squeeze()
    
    i_pred = int(np.argmax(y_pred))
    conf = y_pred[i_pred]

    if conf < acc_bank:
        return None
            
    action = actions[i_pred]
    action_seq_left.append(action)
    
    if len(action_seq_left) < 3:
        return None

    if action_seq_left[-1] == action_seq_left[-2] == action_seq_left[-3]:
       return action.lower()
   
    return None

def get_right_SL(res):
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

    y_pred = model.predict(input_data).squeeze()

    i_pred = int(np.argmax(y_pred))
    conf = y_pred[i_pred]

    if conf < acc_bank:
        return None
            
    action = actions[i_pred]
    action_seq_right.append(action)

    if len(action_seq_right) < 3:
        return None

    if action_seq_right[-1] == action_seq_right[-2] == action_seq_right[-3]:
        return action.lower()
    
    return None

while cap.isOpened():
    ret, img = cap.read()

    img = cv2.flip(img, 1)
    img, result = mediapipe_detection(img, holistic)
    draw_styled_landmarks(img, result)
    
    left_this_act = None
    if result.left_hand_landmarks:
        res = result.left_hand_landmarks
        left_this_act = get_left_SL(res)
        
    right_this_act = None
    if result.right_hand_landmarks:
        res = result.right_hand_landmarks
        right_this_act = get_right_SL(res)
    
    final_action = None
    
    for action_label in actions_dict:
        if action_label[0] == left_this_act:
            if action_label[2] == 0:
                final_action = left_this_act
                break
            else:
                if action_label[1] == right_this_act:
                    final_action = left_this_act
                    break
                    
        if action_label[0] == right_this_act:
            if action_label[2] == 0:
                final_action = right_this_act
                break
            else:
                if action_label[1] == left_this_act:
                    final_action = right_this_act
                    break
    
    cv2.rectangle(img, (0,0), (640, 40), (245, 117, 16), -1)
    
    cv2.putText(img, final_action, org=(20,20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
    
    # cv2.putText(img, right_this_act, org=(340,20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
    
    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break
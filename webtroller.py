# WEBTROLLER
# No generative ai was used in this project
# good luck lmao this code sucks
# orignally based on this code https://github.com/trflorian/hand-tracker?tab=readme-ov-file

import cv2
import mediapipe as mp
import vgamepad as vg

HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17)
]

pad = vg.VX360Gamepad()

BUTTON_MAP = {
    'A':      vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    'B':      vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    'X':      vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    'Y':      vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    'LB':     vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    'RB':     vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    'START':  vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    'SELECT': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
}

BUTTON_LABEL_MAP = {
    'START': 'STR', 'SELECT': 'SEL',
    'LB': 'LB', 'RB': 'RB', 'A': 'A', 'B': 'B', 'X': 'X', 'Y': 'Y'
}

def _press(btn):
    pad.press_button(button=BUTTON_MAP[btn]); pad.update()
    key = BUTTON_LABEL_MAP.get(btn, btn)
    if key in BUTTONS: BUTTONS[key]["pressed"] = True

def _release(btn):
    pad.release_button(button=BUTTON_MAP[btn]); pad.update()
    key = BUTTON_LABEL_MAP.get(btn, btn)
    if key in BUTTONS: BUTTONS[key]["pressed"] = False

def _trigger(trigger, value):
    if trigger == 'left':
        pad.left_trigger(value=max(0, value))
        BUTTONS['LT']['pressed'] = value > 0
    elif trigger == 'right':
        pad.right_trigger(value=max(0, value))
        BUTTONS['RT']['pressed'] = value > 0
    pad.update()

def _stick(stick, x, y):
    moving = x != 0 or y != 0
    if stick == 'left':
        pad.left_joystick_float(x_value_float=x, y_value_float=y)
        for lbl in ['LSU','LSD','LSL','LSR']:
            BUTTONS[lbl]['pressed'] = False
        if x == 1:  BUTTONS['LSR']['pressed'] = moving
        if x == -1: BUTTONS['LSL']['pressed'] = moving
        if y == -1: BUTTONS['LSU']['pressed'] = moving
        if y == 1:  BUTTONS['LSD']['pressed'] = moving
    elif stick == 'right':
        pad.right_joystick_float(x_value_float=x, y_value_float=y)
        for lbl in ['RSU','RSD','RSL','RSR']:
            BUTTONS[lbl]['pressed'] = False
        if x == 1:  BUTTONS['RSR']['pressed'] = moving
        if x == -1: BUTTONS['RSL']['pressed'] = moving
        if y == -1: BUTTONS['RSU']['pressed'] = moving
        if y == 1:  BUTTONS['RSD']['pressed'] = moving
    pad.update()

def is_fist(hand_landmarks):
    tips = [8, 12, 16, 20]
    mcps = [5,  9, 13, 17]
    return all(hand_landmarks[tip].y > hand_landmarks[mcp].y for tip, mcp in zip(tips, mcps))

def draw_landmarks(frame, hand_landmarks):
    h, w = frame.shape[:2]
    for start, end in HAND_CONNECTIONS:
        x0 = int(hand_landmarks[start].x * w)
        y0 = int(hand_landmarks[start].y * h)
        x1 = int(hand_landmarks[end].x * w)
        y1 = int(hand_landmarks[end].y * h)
        cv2.line(frame, (x0, y0), (x1, y1), (0, 200, 0), 2)
    for lm in hand_landmarks:

        cx = int(lm.x * w)
        cy = int(lm.y * h)
        cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 200), 1)
        
        
def draw_hitbox(frame,cx,cy):
    cv2.circle(frame, (cx, cy), 8, (0, 255, 0), -1)
    cv2.circle(frame, (cx, cy), 8, (0, 0, 200), 1)

BUTTONS = {}

def create_button(cx, cy, label, w=84, h=84):
    x1 = cx - w // 2
    y1 = cy - h // 2
    x2 = cx + w // 2
    y2 = cy + h // 2
    BUTTONS[label] = {"p1": (x1, y1), "p2": (x2, y2), "label": label, "pressed": False}

def draw_buttons(frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    for btn in BUTTONS.values():
        p1, p2 = btn["p1"], btn["p2"]
        color = (0, 100, 0) if btn["pressed"] else (0, 255, 0)
        cv2.rectangle(frame, p1, p2, color, 3)
        cv2.putText(frame, btn["label"], (p1[0]+10, p2[1]-10), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

def is_inside_button(cx, cy, label):
    btn = BUTTONS[label]
    x1, y1 = btn["p1"]
    x2, y2 = btn["p2"]
    return x1 <= cx <= x2 and y1 <= cy <= y2


#DEFINTLY a better way to do this im jsut to stupid to figure it out so massive if block it is
def release_all(state):
    if state['apressed']:      
        state['apressed'] = False;      
        _release("A")
    if state['bpressed']:      
        state['bpressed'] = False;      
        _release("B")
    if state['xpressed']:      
        state['xpressed'] = False;      
        _release("X")
    if state['ypressed']:      
        state['ypressed'] = False;      
        _release("Y")
    if state['lbpressed']:     
        state['lbpressed'] = False;     
        _release("LB")
    if state['rbpressed']:     
        state['rbpressed'] = False;     
        _release("RB")
    if state['startpressed']:  
        state['startpressed'] = False;  
        _release("START")
    if state['selectpressed']: 
        state['selectpressed'] = False; 
        _release("SELECT")
    if state['ltpressed']:     
        state['ltpressed'] = False;     
        _trigger('left', 0)
    if state['rtpressed']:     
        state['rtpressed'] = False;     
        _trigger('right', 0)
    if state['lsupressed']:    
        state['lsupressed'] = False;    
        _stick('left', 0, 0)
    if state['lsdpressed']:    
        state['lsdpressed'] = False;    
        _stick('left', 0, 0)
    if state['lslpressed']:    
        state['lslpressed'] = False;    
        _stick('left', 0, 0)
    if state['lsrpressed']:    
        state['lsrpressed'] = False;    
        _stick('left', 0, 0)
    if state['rsupressed']:    
        state['rsupressed'] = False;    
        _stick('right', 0, 0)
    if state['rsdpressed']:    
        state['rsdpressed'] = False;    
        _stick('right', 0, 0)
    if state['rslpressed']:    
        state['rslpressed'] = False;    
        _stick('right', 0, 0)
    if state['rsrpressed']:    
        state['rsrpressed'] = False;    
        _stick('right', 0, 0)

def run_hand_tracking_on_webcam():
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps != fps or fps <= 0:
        fps = 30
    frame_index = 0

    create_button(550, 50,  "A")
    create_button(550, 150, "B")
    create_button(550, 250, "X")
    create_button(550, 350, "Y")

    create_button(100, 50,  "LT", 84, 42)
    create_button(275, 50,  "RT", 84, 42)
    create_button(100, 100, "LB", 84, 42)
    create_button(275, 100, "RB", 84, 42)

    create_button(375, 50,  "STR", 42, 42)
    create_button(450, 50,  "SEL", 42, 42)

    create_button(100, 200, "LSU")
    create_button(100, 400, "LSD")
    create_button(50,  300, "LSL")
    create_button(150, 300, "LSR")

    create_button(350, 200, "RSU")
    create_button(350, 400, "RSD")
    create_button(300, 300, "RSL")
    create_button(400, 300, "RSR")

    options = HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path='hand_landmarker.task'),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    state = {
        'apressed': False, 
        'bpressed': False, 
        'xpressed': False, 
        'ypressed': False,
        'ltpressed': False, 
        'rtpressed': False,
        'lbpressed': False, 
        'rbpressed': False,
        'startpressed': False, 
        'selectpressed': False,
        'lsupressed': False, 
        'lsdpressed': False, 
        'lslpressed': False, 
        'lsrpressed': False,
        'rsupressed': False, 
        'rsdpressed': False, 
        'rslpressed': False, 
        'rsrpressed': False,
    }

    with HandLandmarker.create_from_options(options) as landmarker:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Ignoring empty camera frame...")
                continue

            frame = cv2.flip(frame, 1)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp_ms = int((frame_index / fps) * 1000)
            result = landmarker.detect_for_video(mp_image, timestamp_ms)

            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:
                    draw_landmarks(frame, hand_landmarks)
                    

                    h, w = frame.shape[:2]
                    tip = hand_landmarks[13]
                    cx = int(tip.x * w)
                    cy = int(tip.y * h)

                    draw_hitbox(frame, cx, cy)

                    if is_fist(hand_landmarks):
                        cv2.putText(frame, "FIST", (cx, cy - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        
                        # this is so inneffeciant lmao
                        # Face buttons
                        if is_inside_button(cx, cy, "A"):
                            if not state['apressed']: 
                                state['apressed'] = True; 
                                _press("A")
                        else:
                            if state['apressed']: 
                                state['apressed'] = False; 
                                _release("A")

                        if is_inside_button(cx, cy, "B"):
                            if not state['bpressed']: 
                                state['bpressed'] = True; 
                                _press("B")
                        else:
                            if state['bpressed']: 
                                state['bpressed'] = False; 
                                _release("B")

                        if is_inside_button(cx, cy, "X"):
                            if not state['xpressed']: 
                                state['xpressed'] = True; 
                                _press("X")
                        else:
                            if state['xpressed']: 
                                state['xpressed'] = False; 
                                _release("X")

                        if is_inside_button(cx, cy, "Y"):
                            if not state['ypressed']: 
                                state['ypressed'] = True; 
                                _press("Y")
                        else:
                            if state['ypressed']: 
                                state['ypressed'] = False; 
                                _release("Y")

                        # Bumpers
                        if is_inside_button(cx, cy, "LB"):
                            if not state['lbpressed']: 
                                state['lbpressed'] = True; 
                                _press("LB")
                        else:
                            if state['lbpressed']: 
                                state['lbpressed'] = False; 
                                _release("LB")

                        if is_inside_button(cx, cy, "RB"):
                            if not state['rbpressed']: 
                                state['rbpressed'] = True; 
                                _press("RB")
                        else:
                            if state['rbpressed']: 
                                state['rbpressed'] = False; 
                                _release("RB")

                        # Start / Select
                        if is_inside_button(cx, cy, "STR"):
                            if not state['startpressed']: 
                                state['startpressed'] = True; 
                                _press("START")
                        else:
                            if state['startpressed']: 
                                state['startpressed'] = False; 
                                _release("START")

                        if is_inside_button(cx, cy, "SEL"):
                            if not state['selectpressed']: 
                                state['selectpressed'] = True; 
                                _press("SELECT")
                        else:
                            if state['selectpressed']: 
                                state['selectpressed'] = False; 
                                _release("SELECT")

                        # Triggers
                        if is_inside_button(cx, cy, "LT"):
                            if not state['ltpressed']: 
                                state['ltpressed'] = True; 
                                _trigger('left', 255)
                        else:
                            if state['ltpressed']: 
                                state['ltpressed'] = False; 
                                _trigger('left', 0)

                        if is_inside_button(cx, cy, "RT"):
                            if not state['rtpressed']: 
                                state['rtpressed'] = True; 
                                _trigger('right', 255)
                        else:
                            if state['rtpressed']: 
                                state['rtpressed'] = False; 
                                _trigger('right', 0)

                        # Left stick
                        if is_inside_button(cx, cy, "LSU"):
                            if not state['lsupressed']: 
                                state['lsupressed'] = True; 
                                _stick('left', 0, -1)
                        else:
                            if state['lsupressed']: 
                                state['lsupressed'] = False; 
                                _stick('left', 0, 0)

                        if is_inside_button(cx, cy, "LSD"):
                            if not state['lsdpressed']: 
                                state['lsdpressed'] = True; 
                                _stick('left', 0, 1)
                        else:
                            if state['lsdpressed']: 
                                state['lsdpressed'] = False; 
                                _stick('left', 0, 0)

                        if is_inside_button(cx, cy, "LSL"):
                            if not state['lslpressed']: 
                                state['lslpressed'] = True; 
                                _stick('left', -1, 0)
                        else:
                            if state['lslpressed']: 
                                state['lslpressed'] = False; 
                                _stick('left', 0, 0)

                        if is_inside_button(cx, cy, "LSR"):
                            if not state['lsrpressed']: 
                                state['lsrpressed'] = True; 
                                _stick('left', 1, 0)
                        else:
                            if state['lsrpressed']: 
                                state['lsrpressed'] = False; 
                                _stick('left', 0, 0)

                        # Right stick
                        if is_inside_button(cx, cy, "RSU"):
                            if not state['rsupressed']: 
                                state['rsupressed'] = True; 
                                _stick('right', 0, -1)
                        else:
                            if state['rsupressed']: 
                                state['rsupressed'] = False; 
                                _stick('right', 0, 0)

                        if is_inside_button(cx, cy, "RSD"):
                            if not state['rsdpressed']: 
                                state['rsdpressed'] = True; 
                                _stick('right', 0, 1)
                        else:
                            if state['rsdpressed']: 
                                state['rsdpressed'] = False; 
                                _stick('right', 0, 0)

                        if is_inside_button(cx, cy, "RSL"):
                            if not state['rslpressed']: 
                                state['rslpressed'] = True; 
                                _stick('right', -1, 0)
                        else:
                            if state['rslpressed']: 
                                state['rslpressed'] = False; 
                                _stick('right', 0, 0)

                        if is_inside_button(cx, cy, "RSR"):
                            if not state['rsrpressed']: 
                                state['rsrpressed'] = True; 
                                _stick('right', 1, 0)
                        else:
                            if state['rsrpressed']: 
                                state['rsrpressed'] = False; 
                                _stick('right', 0, 0)

                    else:
                        release_all(state)

            draw_buttons(frame)
            cv2.imshow("Webtroller", frame)
            frame_index += 1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            
            if cv2.getWindowProperty("Webtroller", cv2.WND_PROP_VISIBLE) < 1:
                break

    cap.release()

if __name__ == "__main__":
    run_hand_tracking_on_webcam()
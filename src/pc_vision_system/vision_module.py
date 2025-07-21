'''
vision_module.py - Hand detection and finger counting module
Author: Engineer A
Date: 21/7/25
'''

from cvzone.HandTrackingModule import HandDetector
import cv2

# Constants
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20

FINGER_TIPS = {
    'thumb': THUMB_TIP,
    'index': INDEX_TIP,
    'middle': MIDDLE_TIP,
    'ring': RING_TIP,
    'pinky': PINKY_TIP
}

FINGER_PIPS = {
    'thumb': 2,   # For thumb use joint #2
    'index': 6,
    'middle': 10,
    'ring': 14,
    'pinky': 18
}

def initialize_detector(detection_confidence=0.7, max_hands=1):
    """
    Initialize and return a HandDetector object.
    """
    return HandDetector(detectionCon=detection_confidence, maxHands=max_hands)

def process_frame(frame, detector):
    """
    Process a single frame to detect hands and draw landmarks.
    """
    if frame is None:
        return [], frame

    hands, img = detector.findHands(frame, draw=True)
    return hands, img

def validate_hand_data(hand_data):
    """
    Validate that hand_data contains all required information.
    """
    return hand_data is not None and 'lmList' in hand_data and 'type' in hand_data

def count_fingers(hand_data):
    """
    Count the number of raised fingers for a single hand.
    """
    if not validate_hand_data(hand_data):
        raise ValueError("Invalid hand data")

    status = get_finger_status(hand_data)
    return sum(status.values())

def get_finger_status(hand_data):
    """
    Get the status of each finger (raised or lowered).
    """
    if not validate_hand_data(hand_data):
        raise ValueError("Invalid hand data")

    lmList = hand_data['lmList']
    handType = hand_data['type']

    status = {}

    for finger, tip_id in FINGER_TIPS.items():
        pip_id = FINGER_PIPS[finger]
        tip = lmList[tip_id]
        pip = lmList[pip_id]

        if finger == 'thumb':
            if handType == "Right":
                status[finger] = tip[0] > pip[0]  # x comparison
            else:
                status[finger] = tip[0] < pip[0]
        else:
            status[finger] = tip[1] < pip[1]  # y comparison

    return status

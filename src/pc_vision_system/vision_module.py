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
INDEX_MCP = 5   # Index finger knuckle
PINKY_MCP = 17  # Pinky knuckle

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
    This version correctly handles both palm and back-of-hand views.
    """
    if not validate_hand_data(hand_data):
        raise ValueError("Invalid hand data")

    lmList = hand_data['lmList']
    handType = hand_data['type']

    # Determine if we are looking at the palm or the back of the hand.
    # We compare the x-coordinate of the index finger knuckle (MCP) and the pinky knuckle.
    # For a right hand in palm view, the index knuckle is to the left of the pinky knuckle.
    is_index_left_of_pinky = lmList[INDEX_MCP][0] < lmList[PINKY_MCP][0]

    is_palm_view = (handType == "Right" and is_index_left_of_pinky) or \
                   (handType == "Left" and not is_index_left_of_pinky)

    status = {}

    for finger, tip_id in FINGER_TIPS.items():
        pip_id = FINGER_PIPS[finger]
        tip = lmList[tip_id]
        pip = lmList[pip_id]

        if finger == 'thumb':
            # The logic for the thumb depends on the hand's orientation (palm vs. back).
            # We establish the base case for a right hand's palm view, where an
            # open thumb has its tip to the left of its knuckle (smaller x-value).
            # All other conditions are derived from flipping the hand type or view.
            if is_palm_view:
                if handType == "Right":
                    status[finger] = tip[0] < pip[0]
                else:  # Left Hand Palm
                    status[finger] = tip[0] > pip[0]
            else:  # Back of hand view
                if handType == "Right":
                    status[finger] = tip[0] > pip[0]
                else:  # Left Hand Back
                    status[finger] = tip[0] < pip[0]
        else:
            # For other fingers, "up" is consistently a smaller y-coordinate.
            status[finger] = tip[1] < pip[1]  # y comparison

    return status

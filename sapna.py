import cv2
import mediapipe as mp
import pyautogui
import utility
from pynput.mouse import Button, Controller

mouse = Controller()
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hand = mpHands.Hands()

# Initialize MediaPipe Hands
screen_width, screen_height = pyautogui.size()

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x, y)

def is_left_click(landmarks_list, thumb_index_dist):
    return (utility.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 50 and
            utility.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and
            thumb_index_dist > 50)

def is_right_click(landmarks_list, thumb_index_dist):
    return (utility.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            utility.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and
            thumb_index_dist > 50)

def is_screenshot(landmarks_list, thumb_index_dist):
    return (utility.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            utility.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            thumb_index_dist < 50)

def is_double_click(landmarks_list, thumb_index_dist):
    return (utility.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            utility.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            thumb_index_dist > 50)

def detect_gestures(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = utility.get_distance(landmarks_list[4], landmarks_list[5])
        
        print(f"Thumb-Index Distance: {thumb_index_dist}")
        print(f"Angles: Index Angle = {utility.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])}, Thumb Angle = {utility.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12])}")

        if thumb_index_dist < 50 and utility.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90:
            move_mouse(index_finger_tip)
        
        elif is_left_click(landmarks_list, thumb_index_dist):
            print("Left Click Detected")
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        elif is_right_click(landmarks_list, thumb_index_dist):
            print("Right Click Detected")
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        elif is_screenshot(landmarks_list, thumb_index_dist):
            print("Screenshot Detected")
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            cv2.putText(frame, "Screenshot", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
            
def main():
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Camera not open")
        return
    
    print("Camera is open and ready.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to grab frame")
                break

            frame = cv2.flip(frame, 1)  # Flip the frame horizontally

            # Process the frame for hand landmarks
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hand.process(frameRGB)

            if processed.multi_hand_landmarks:
                for hand_landmarks in processed.multi_hand_landmarks:
                    # Draw hand landmarks and connections
                    mpDraw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                    
                    # Collect landmark coordinates
                    landmarks_list = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
                    print(landmarks_list)
                    
                    detect_gestures(frame, landmarks_list, processed)

            # Show the processed frame
            cv2.imshow('frame', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        # Release the capture and destroy windows
        cap.release()
        cv2.destroyAllWindows()
        print("Capture released and windows destroyed.")

if __name__ == '__main__':
    main()


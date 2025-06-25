import cv2
import mediapipe as mp
import pyttsx3

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to determine which fingers are open (excluding thumbs) for both hands
def determine_open_fingers(hand_landmarks_list):
    # Define finger landmarks excluding thumbs (landmark ID 4)
    finger_tip_ids = [8, 12, 16, 20]
    open_fingers = []

    # Loop through each hand
    for hand_landmarks in hand_landmarks_list:
        # Check each finger
        for tip_id in finger_tip_ids:
            if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                open_fingers.append(True)
            else:
                open_fingers.append(False)
    return open_fingers[:8]  # Return only the first 8 fingers (4 from each hand)

# Function to get sign language phrase based on open fingers combination and speak it out
def get_sign_language_phrase(open_fingers):
    # Dictionary mapping finger combinations to sign language phrases
    sign_language_phrases = {
        #(index, middle, ring , pinky):"output sign"
        (False, False, False, False, False, False, False, False): "no",
        (True, False, False, False, False, False, False, False): "hi",
        (True, True, False, False, False, False, False, False): "victory",
        (True, True, True, False, False, False, False, False): "thanks",
        (True, True, True, True, False, False, False, False): "hello",
        (True, True, True, True, True, False, False, False): "thumbs up",
        (True, True, True, True, True, True, False, False): "i need dinner",
        (True, True, True, True, True, True, True, False): "i need water",
        (True, True, True, True, True, True, True, True): "bye",
        (True, False, False, True, False, False, False, False): "super",
        (True, False, False, True, True, False, False, True): "amazing"



        # Add more combinations and corresponding phrases as needed
    }

    # Look up the phrase based on the combination of open fingers
    phrase = sign_language_phrases.get(tuple(open_fingers))
    if phrase:
        engine.say(phrase)  # Speak out the phrase
        engine.runAndWait()  # Wait for speech to finish
    else:
        print("Unknown phrase")
    return phrase

# Main function
def main():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Unable to capture video")
            break

        # Convert image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process image with MediaPipe Hands
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks is not None:
            open_fingers = determine_open_fingers(results.multi_hand_landmarks)
            print("Open fingers:", open_fingers)

            # Get sign language phrase based on open fingers combination
            phrase = get_sign_language_phrase(open_fingers)
            print("Sign language phrase:", phrase)

            # Draw hand landmarks on the frame for both hands
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, phrase, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
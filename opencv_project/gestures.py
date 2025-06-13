import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2
import mediapipe as mp
import webbrowser
import pyttsx3
import time

# Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# MediaPipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

gesture_executed = None
gesture_text = ""

def speak(text):
    engine.say(text)
    engine.runAndWait()

def detect_fingers(hand_landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)

    # Other fingers
    for i in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y else 0)

    return fingers

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = detect_fingers(hand_landmarks)
            total = fingers.count(1)

            # Thumb Up → Spotify
            if fingers == [1, 0, 0, 0, 0] and gesture_executed != "thumb":
                webbrowser.open("https://open.spotify.com")
                speak("Opening Spotify")
                gesture_executed = "thumb"
                gesture_text = "👍 Thumb → Opening Spotify"
                time.sleep(2)

            # Peace → Swiggy
            elif fingers == [0, 1, 1, 0, 0] and gesture_executed != "peace":
                webbrowser.open("https://www.swiggy.com")
                speak("Opening Swiggy")
                gesture_executed = "peace"
                gesture_text = "✌️ Peace → Opening Swiggy"
                time.sleep(2)

            # Rock → Myntra
            elif fingers == [0, 1, 0, 0, 1] and gesture_executed != "rock":
                webbrowser.open("https://www.myntra.com")
                speak("Opening Myntra")
                gesture_executed = "rock"
                gesture_text = "🤘 Rock → Opening Myntra"
                time.sleep(2)

            # Palm → YouTube
            elif total == 5 and gesture_executed != "palm":
                webbrowser.open("https://www.youtube.com")
                speak("Opening YouTube")
                gesture_executed = "palm"
                gesture_text = "🖐️ Palm → Opening YouTube"
                time.sleep(2)

            # Fist → Google
            elif total == 0 and gesture_executed != "fist":
                webbrowser.open("https://www.google.com")
                speak("Opening Google")
                gesture_executed = "fist"
                gesture_text = "👊 Fist → Opening Google"
                time.sleep(2)

    else:
        gesture_executed = None
        gesture_text = ""

    if gesture_text:
        cv2.putText(frame, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (50, 255, 50), 2)

    cv2.imshow("🖐️ Smart Gesture Launcher", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Sign Language Detection using MediaPipe and Text-to-Speech

This project uses [MediaPipe](https://google.github.io/mediapipe/) to detect hand gestures from a webcam and maps them to predefined sign language phrases using a simple logic based on open fingers. The output is spoken aloud using a text-to-speech engine.

## 🔧 Features

- Real-time hand tracking using MediaPipe
- Detection of finger positions (excluding thumbs)
- Mapping finger patterns to sign language phrases
- Text-to-speech output using `pyttsx3`
- OpenCV-based live video feed and UI

## 📦 Dependencies

Install using:

```bash
pip install -r requirements.txt

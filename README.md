# Real-Time Interview Agent


## Overview
The Real-Time Interview Agent is a Python-based application designed to assist in conducting mock interviews. It provides real-time feedback on a candidate's communication skills, including clarity of speech, facial expressions, text recognition and overall confidence. This tool is particularly valuable for candidates preparing for professional interviews, allowing them to receive feedback on both verbal and non-verbal communication.

## Key Features and Operation  
-  **Video and Audio Capture**: Captures video and audio using the computer's webcam and microphone, analyzing the input in real-time. 
-  **Real-Time Feedback**: Provides immediate feedback on the candidate's performance by analyzing facial expressions and speech. 
-  **Dynamic Questioning**: Displays interview questions and captures responses, moving to the next question based on candidate feedback or after a silence if no feedback is provided.
-  **Evaluation Metrics**: At the end of the interview, summarizes performance metrics like clarity of speech, facial expressions, and overall confidence. The final evaluation will be displayed on the application window, and the application window will automatically close once the interview is complete.
-  **Bonus Feature - Sentiment Analysis**: Detects the sentiment of the candidate's spoken responses (positive, neutral, or negative tone) to provide insights into the emotional undertone of their answers.
-  **Bonus Feature - Speech-to-Text Integration**: Converts spoken responses into text in real-time within the `audio_capture` method. This involves listening to audio input with `self.audio_recognizer.listen`, converting it to text using `recognize_google`, and then using the transcribed text for clarity feedback (via `provide_clarity_feedback`) and sentiment analysis (via `analyze_sentiment`). This integration is central to both clarity feedback and sentiment evaluation.

## How It Works

- **Video Processing**: Utilizes OpenCV to capture and process video frames from the webcam. DeepFace analyzes these frames for facial expressions.
- **Audio Processing**: SpeechRecognition library converts spoken words into text. Speech clarity is evaluated by calculating the rate of speech.
- **Feedback Mechanism**: Combines insights from video and audio analyses to provide real-time feedback displayed directly on the video feed.
- **Final Evaluation**: After all questions are asked, the system calculates and displays a final evaluation of the candidate's performance based on the collected data in the application window.

## Usage

- Start the application by running 
   ```bash
   python NOAM_RealTimeInterviewAgent.py.

- Follow the on-screen (application window) prompts to respond to interview questions.
- Review feedback provided in real-time on the application window.
- After the interview, the final summary of your performance will be displayed on the application window for a few seconds before it closes automatically.

## Installation
Ensure Python 3.6+ is installed on your system. Install the required packages using:
   ```bash
   pip install opencv-python-headless deepface SpeechRecognition textblob



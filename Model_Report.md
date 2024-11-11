# AI Models Report for Real-Time Interview Agent

## Overview
The Real-Time Interview Agent is a Python-based application designed to assist in conducting mock interviews. It provides real-time feedback on a candidate's communication skills, including clarity of speech, facial expressions, and sentiment analysis. This tool is particularly valuable for candidates preparing for professional interviews, allowing them to receive feedback on both verbal and non-verbal communication.

## Key Features
- **Facial Expression Analysis**: Evaluates video frames captured from the webcam to determine dominant facial expressions in real-time.
- **Speech-to-Text Integration**: Converts spoken responses into text in real-time, enabling clarity and sentiment analysis.
- **Speech Clarity and Sentiment Analysis**: Provides immediate feedback on clarity based on speaking rate (words per minute) and sentiment (positive, neutral, or negative tone) of responses.

## Facial Expression Analysis

### Model Used: DeepFace Framework
- **Library Overview**: DeepFace is an advanced facial attribute analysis library developed by Sefik Ilkin Serengil. It simplifies the use of deep learning models for face recognition and attribute analysis, including emotion.
- **Specific Model**: This application uses a Convolutional Neural Network (CNN) based on the VGG-Face model. Pre-trained on extensive datasets, this model identifies emotions such as happy, sad, angry, neutral, and more.
- **Functionality**: Video frames are processed to identify the dominant facial expression, helping to assess a candidate's emotional state and composure.
- **Advantages**: Known for high accuracy under various lighting and physical conditions, VGG-Face is well-suited for dynamic, real-time analysis in virtual interview settings.

## Speech Evaluation

### Technology Used: SpeechRecognition Library
- **Description**: The SpeechRecognition library simplifies speech-to-text conversion in Python, using several backend APIs. For this application, the default API is Google's speech recognition service.
- **Functionality**: SpeechRecognition captures audio from the microphone, processes it, and converts it into text. This text serves as the basis for speech rate calculation, sentiment analysis, and clarity feedback.
- **Speech Clarity Metric**: The clarity metric is evaluated by calculating the words per minute (WPM) for each response. It assesses whether a candidate is speaking too slowly, too quickly, or at an optimal rate.
- **Implementation Details**: 
    - **Listening to Audio**: `self.audio_recognizer.listen` captures audio input with defined timeouts.
    - **Converting to Text**: `recognize_google` converts the audio into a text transcript, enabling further analysis.
    - **Using the Transcribed Text**: `provide_clarity_feedback` calculates WPM for clarity, and `analyze_sentiment` uses TextBlob for sentiment evaluation.

## Sentiment Analysis

### Tool Used: TextBlob Library
- **Description**: TextBlob is a Python library for processing textual data. In this application, it evaluates the sentiment (positive, neutral, or negative) of transcribed responses.
- **Functionality**: Each spoken response is analyzed for polarity, producing feedback on the emotional undertone of responses. This feedback, combined with facial expression analysis, helps gauge the candidate's overall confidence and tone.

## Conclusion
The integration of DeepFace’s VGG-Face model for facial expression analysis, SpeechRecognition for real-time speech-to-text conversion, and TextBlob for sentiment analysis creates a robust tool for assessing communication in mock interviews. Together, these technologies offer a comprehensive view of both verbal and non-verbal communication skills, enhancing candidate preparation for real-world interviews.

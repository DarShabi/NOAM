import numpy as np
import cv2
from deepface import DeepFace
import speech_recognition as sr
from textblob import TextBlob
import threading
import time


class RealTimeInterviewAgent:
    QUESTIONS = [
        "Tell me about yourself.",
        "Why are you interested in this position?",
        "What are your strengths and weaknesses?",
        "Where do you see yourself in five years?",
        "Why should we hire you?"
    ]
    SPEECH_TIMEOUT = 5
    PHRASE_LIMIT = 10
    SILENCE_THRESHOLD = 1
    POST_SILENCE_DELAY = 3
    MIN_SPEECH_RATE = 50
    MAX_SPEECH_RATE = 100
    PAUSE_BEFORE_SUMMARY = 3
    FINAL_DISPLAY_TIME = 7

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.audio_recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.current_question = 0
        self.current_question_text = ""
        self.current_feedback_text = ""
        self.current_speech_feedback_text = ""
        self.current_sentiment_text = ""
        self.running = True
        self.speech_rates = []
        self.emotions = {}
        self.sentiments = []

    def ask_question(self):
        if self.current_question < len(self.QUESTIONS):
            self.current_question_text = self.QUESTIONS[self.current_question]
            print(f"Question {self.current_question + 1}: {self.current_question_text}")
        else:
            self.current_question_text = "Interview Complete. Thank you!"
            print(self.current_question_text)
            time.sleep(self.PAUSE_BEFORE_SUMMARY)
            self.final_evaluation()
            self.running = False

    def audio_capture(self):
        with self.microphone as source:
            self.audio_recognizer.adjust_for_ambient_noise(source)
            self.ask_question()
            while self.running:
                try:
                    audio = self.audio_recognizer.listen(source, timeout=self.SPEECH_TIMEOUT, phrase_time_limit=self.PHRASE_LIMIT)
                    transcript = self.audio_recognizer.recognize_google(audio)
                    duration = len(audio.frame_data) / audio.sample_rate
                    self.provide_clarity_feedback(transcript, duration)
                    self.analyze_sentiment(transcript)
                    self.wait_for_silence(source)
                    time.sleep(self.POST_SILENCE_DELAY)  # New delay after silence detection
                    self.current_question += 1
                    self.ask_question()
                except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError) as e:
                    print(f"Listening issue: {e}")

    def wait_for_silence(self, source):
        silence_start = None
        while True:
            try:
                audio = self.audio_recognizer.listen(source, timeout=1, phrase_time_limit=1)
                self.audio_recognizer.recognize_google(audio)
                silence_start = None
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > self.SILENCE_THRESHOLD:
                    break

    def provide_clarity_feedback(self, transcript, duration):
        words = len(transcript.split())
        speech_rate = words / duration * 60
        self.speech_rates.append(speech_rate)
        feedback = "Good pace." if self.MIN_SPEECH_RATE <= speech_rate <= self.MAX_SPEECH_RATE else "Speaking too quickly." if speech_rate > self.MAX_SPEECH_RATE else "Speaking too slowly."
        self.current_speech_feedback_text = f"Clarity: {feedback}"

    def analyze_sentiment(self, transcript):
        blob = TextBlob(transcript)
        sentiment = blob.sentiment.polarity
        sentiment_feedback = "Positive tone." if sentiment > 0 else "Negative tone." if sentiment < 0 else "Neutral tone."
        self.current_sentiment_text = f"Sentiment: {sentiment_feedback}"
        self.sentiments.append(sentiment)

    def process_emotion(self, emotion):
        feedbacks = {
            'nervous': "You seem a bit nervous, try to relax your shoulders.",
            'happy': "Great smile, it shows confidence!",
            'sad': "Try to keep a positive outlook; it'll go well!",
            'angry': "Try to stay calm and composed.",
            'surprise': "Maintain your composure; you're doing great.",
            'disgust': "Keep your responses professional and polite.",
            'fear': "Stay confident, you've got this!",
            'neutral': "Keep up the good expression."
        }
        self.current_feedback_text = "Feedback: " + feedbacks.get(emotion, "Keep up the good expression.")
        self.emotions[emotion] = self.emotions.get(emotion, 0) + 1

    def final_evaluation(self):
        average_speech_rate = sum(self.speech_rates) / len(self.speech_rates) if self.speech_rates else 0
        most_common_emotion = max(self.emotions, key=self.emotions.get, default='None')
        overall_confidence = 'High' if self.emotions.get('happy', 0) > self.emotions.get('nervous', 0) else 'Low'
        average_sentiment = sum(self.sentiments) / len(self.sentiments) if self.sentiments else 0
        sentiment_summary = "Positive" if average_sentiment > 0 else "Negative" if average_sentiment < 0 else "Neutral"

        final_text = (
            f"Average Speech Rate: {average_speech_rate:.2f} wpm\n"
            f"Most Common Emotion: {most_common_emotion}\n"
            f"Overall Confidence: {overall_confidence}\n"
            f"Overall Sentiment: {sentiment_summary}"
        )
        return final_text

    def start(self):
        audio_thread = threading.Thread(target=self.audio_capture)
        audio_thread.start()

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            try:
                analysis_list = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                if analysis_list:
                    self.process_emotion(analysis_list[0].get('dominant_emotion', 'neutral'))
            except Exception as e:
                print(f"Failed to analyze frame: {e}")

            cv2.putText(frame, self.current_question_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, self.current_feedback_text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, self.current_speech_feedback_text, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, self.current_sentiment_text, (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow('Interview', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        white_background = 255 * np.ones_like(frame)
        final_text = self.final_evaluation()
        for i, line in enumerate(final_text.split('\n')):
            cv2.putText(white_background, line, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Final Evaluation', white_background)
        cv2.waitKey(self.FINAL_DISPLAY_TIME * 1000)

        self.cap.release()
        cv2.destroyAllWindows()
        audio_thread.join()


if __name__ == "__main__":
    agent = RealTimeInterviewAgent()
    agent.start()

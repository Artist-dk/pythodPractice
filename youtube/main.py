import os
import sys
import threading
import pyttsx3
import pygame
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QWidget,
    QMessageBox,
    QComboBox,
)
from PyQt5.QtCore import Qt

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Fixed audio file name
AUDIO_FILE_NAME = "output_audio.mp3"

class TextToSpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text-to-Speech Converter with Audio Playback")
        self.setGeometry(100, 100, 600, 600)

        # Main layout
        layout = QVBoxLayout()

        # Text Input
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Enter text here...")
        layout.addWidget(QLabel("Enter Text:"))
        layout.addWidget(self.text_input)

        # Speed Slider
        layout.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setRange(50, 300)
        self.speed_slider.setValue(150)  # Default speed
        layout.addWidget(self.speed_slider)

        # Voice Selection
        layout.addWidget(QLabel("Voice:"))
        self.voice_group = QButtonGroup(self)
        male_button = QRadioButton("Male", self)
        female_button = QRadioButton("Female", self)
        self.voice_group.addButton(male_button, 0)
        self.voice_group.addButton(female_button, 1)
        male_button.setChecked(True)  # Default to male
        layout.addWidget(male_button)
        layout.addWidget(female_button)

        # Language Selection
        layout.addWidget(QLabel("Select Language:"))
        self.language_selector = QComboBox(self)
        self.language_selector.addItems(["en-US", "en-GB", "hi-IN", "es-ES", "fr-FR", "de-DE"])  # Example languages
        layout.addWidget(self.language_selector)

        # Convert Button
        self.convert_button = QPushButton("Convert to Speech", self)
        self.convert_button.clicked.connect(self.convert_to_speech)
        layout.addWidget(self.convert_button)

        # Play Audio Button
        self.play_button = QPushButton("Play Audio", self)
        self.play_button.clicked.connect(self.play_audio)
        layout.addWidget(self.play_button)

        # Set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def convert_to_speech(self):
        """Convert text to speech and save it as a fixed audio file."""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.critical(self, "Error", "Please enter some text to convert!")
            return

        # Get user settings
        rate = self.speed_slider.value()
        voice_gender = "Male" if self.voice_group.checkedId() == 0 else "Female"
        selected_language = self.language_selector.currentText()

        # Initialize pyttsx3 engine
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)  # Set speech rate

        # Set voice language and gender
        voices = engine.getProperty('voices')
        voice_set = False
        for voice in voices:
            if selected_language in voice.id and ((voice_gender == "Male" and "male" in voice.id.lower()) or
                                                  (voice_gender == "Female" and "female" in voice.id.lower())):
                engine.setProperty('voice', voice.id)
                voice_set = True
                break

        if not voice_set:
            QMessageBox.warning(self, "Warning", f"No {voice_gender} voice found for language '{selected_language}'. Using default voice.")

        try:
            # Save audio file
            engine.save_to_file(text, AUDIO_FILE_NAME)
            engine.runAndWait()

            QMessageBox.information(self, "Success", f"Audio saved as '{AUDIO_FILE_NAME}'! Click 'Play Audio' to listen.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate audio: {str(e)}")

    def play_audio(self):
        """Play the saved audio file."""
        if not os.path.exists(AUDIO_FILE_NAME):
            QMessageBox.critical(self, "Error", f"No audio file found! Please convert text to speech first.")
            return

        # Play the audio using pygame mixer
        try:
            pygame.mixer.music.load(AUDIO_FILE_NAME)
            pygame.mixer.music.play()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to play audio: {str(e)}")


# Main Execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec_())

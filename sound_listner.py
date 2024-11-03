
import os
import sys
import speech_recognition as sr
from PySide6.QtWidgets import QApplication
from slot_machine import SlotMachine  

class SoundListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.slot_machine = None  # Initialise slot machine 

    def listen_for_command(self):
        print("Adjusting for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Listening for the command 'spin the wheel'...")

            try:
                print("Waiting for audio input...")
                audio = self.recognizer.listen(source, timeout=10)
                print("Audio received, processing...")

                try:
                    command = self.recognizer.recognize_google(audio)
                    print(f"Google recognized: {command}")
                except sr.RequestError:
                    print("Google recognizer failed, switching to Sphinx.")
                    command = self.recognizer.recognize_sphinx(audio)
                    print(f"Sphinx recognized: {command}")

                if "spin the wheel" in command.lower():
                    print("Command detected! Starting guessing game...")
                    if self.slot_machine is None:
                        self.slot_machine = SlotMachine()
                        self.slot_machine.show()
                    #self.slot_machine.start_guessing()
                    self.slot_machine.start_spin_from_voice()
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.WaitTimeoutError:
                print("Listening timed out; retrying...")
            except sr.RequestError as e:
                print(f"Could not request results from the speech recognition service; {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv) 
    listener = SoundListener()
    listener.listen_for_command()
    sys.exit(app.exec())


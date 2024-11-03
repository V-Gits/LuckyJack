
import pyttsx3
import speech_recognition as sr
import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPalette

class SlotLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(100, 100)
        self.setStyleSheet("font-size: 50px; background-color: black; color: red; "
                           "border: 3px solid gold; border-radius: 10px;")

class SlotMachine(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slot Machine")
        self.setFixedSize(400, 600)

        
        self.total_limit = 100
        self.engine = pyttsx3.init()

        self.engine.setProperty('volume', 1.0)  
        self.engine.setProperty('rate', 150)

     
        main_widget = QWidget(self)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        #"big Win" 
        self.big_win_label = QLabel("BIG WIN")
        self.big_win_label.setAlignment(Qt.AlignCenter)
        self.big_win_label.setStyleSheet("font-size: 24px; font-weight: bold; color: yellow; "
                                         "background-color: red; padding: 5px; border-radius: 10px;")
        main_layout.addWidget(self.big_win_label)
        self.big_win_label.hide() 

       
        self.balance_label = QLabel(f"Balance: ${self.total_limit}")
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        main_layout.addWidget(self.balance_label)

        #matrix 
        slot_layout = QGridLayout()
        self.slots = []
        self.symbols = ["7", "🍒", "🍋", "🔔", "⭐", "💰"]

        for i in range(3):
            row = []
            for j in range(3):
                slot = SlotLabel("7")  # Initial symbol
                slot_layout.addWidget(slot, i, j)
                row.append(slot)
            self.slots.append(row)

        main_layout.addLayout(slot_layout)

        # Bet input
        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText("Enter your bet amount ($)")
        self.bet_input.setAlignment(Qt.AlignCenter)
        self.bet_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid orange; "
                                      "border-radius: 5px; background-color: #333; color: white;")
        main_layout.addWidget(self.bet_input)

        # Spin button
        self.spin_button = QPushButton("Spin")
        self.spin_button.setFixedSize(200, 50)
        self.spin_button.setStyleSheet("font-size: 20px; font-weight: bold; color: white; background-color: green; "
                                       "border-radius: 5px; padding: 10px; border: none;")
        self.spin_button.clicked.connect(self.start_spin)
        main_layout.addWidget(self.spin_button, alignment=Qt.AlignCenter)

        
        self.symbol_timer = QTimer()
        self.symbol_timer.timeout.connect(self.update_symbols)

        
        self.spin_count = 0

    def start_spin(self):
        
        try:
            bet = int(self.bet_input.text())
        except ValueError:
            self.show_message("Please enter a valid number for the bet.")
            return

        if bet <= 0 or bet > self.total_limit:
            self.show_message(f"Bet must be between 1 and {self.total_limit}. Try again!")
            return

        self.big_win_label.hide()  # Hide the big win message
        self.spin_button.setEnabled(False)  # Disable spin button while spinning
        self.spin_count = 0  # Reset spin count

      
        self.symbol_timer.start(100)  # Change symbols every 100ms


        self.total_limit -= bet
        self.balance_label.setText(f"Balance: ${self.total_limit}")

    def update_symbols(self):
        for row in self.slots:
            for slot in row:
                slot.setText(random.choice(self.symbols))  # Update each slot with a random symbol

        self.spin_count += 1
        if self.spin_count >= 20:  # Stop after enough spins
            self.symbol_timer.stop()
            self.spin_button.setEnabled(True)  
            self.check_result()

    def check_result(self):
       
        middle_row = self.slots[1]
        if all(slot.text() == middle_row[0].text() for slot in middle_row):
            self.big_win_label.show()  # Show big win message
        else:
            self.big_win_label.hide()
            if self.total_limit <= 0:
                self.show_message("You've run out of money! Please reset your bets.")

    def show_message(self, message):

        self.big_win_label.setText(message)
        self.big_win_label.setStyleSheet("font-size: 16px; font-weight: bold; color: yellow; "
                                          "background-color: red; padding: 5px; border-radius: 10px;")
        self.big_win_label.show()

    def start_spin_from_voice(self):
        """Start the spin action from an external command."""
        self.engine.say("Place your bet.")
        self.engine.runAndWait()
        self.listen_for_bet()

    def listen_for_bet(self):
        """Listen for the bet amount from the user."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for bet amount...")
            audio = recognizer.listen(source)

            try:
                bet = recognizer.recognize_google(audio)
                bet = int(bet)  
                self.bet_input.setText(str(bet))
                self.start_spin() 
            except ValueError:
                self.show_message("Please say a valid number for your bet.")
            except sr.UnknownValueError:
                self.show_message("Sorry, I could not understand what you said.")
            except sr.RequestError:
                self.show_message("Could not request results from Google Speech Recognition service.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

   
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#282828"))
    app.setPalette(palette)

   
    window = SlotMachine()
    window.show()

   
    window.bet_input.setFocus()

   
    window.start_spin_from_voice()  
    sys.exit(app.exec())




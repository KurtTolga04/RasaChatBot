from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSlot, QSize, QDateTime, QTimer
from PyQt5.QtGui import QTextCursor, QFont, QIcon


class ChatWindow(QMainWindow):
    def __init__(self, rasa_client):
        super().__init__()
        self.rasa_client = rasa_client
        self.setup_window()
        self.create_widgets()
        self.setup_layouts()
        self.setup_connections()
        self.set_styles()
        self.show_welcome_message()

    def setup_window(self):
        self.setWindowTitle('Rasa ChatBot')
        self.setGeometry(300, 300, 400, 600)
        self.setMinimumSize(QSize(600, 650))
        try:
            self.setWindowIcon(QIcon('Chat_Icon.png'))
        except:
            pass

    def create_widgets(self):
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.chat_display)
        self.scroll_area.setWidgetResizable(True)

        self.input_frame = QFrame()
        self.input_layout = QHBoxLayout(self.input_frame)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your message...")

        self.send_button = QPushButton("Send")
        self.send_button.setFixedHeight(40)
        self.send_button.setMinimumWidth(90)

        self.status_bar = self.statusBar()

    def setup_layouts(self):
        self.setCentralWidget(self.central_widget)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.input_frame)

        self.input_layout.addWidget(self.user_input)
        self.input_layout.addWidget(self.send_button)

    def setup_connections(self):
        self.send_button.clicked.connect(self.send_message)
        self.user_input.returnPressed.connect(self.send_message)
        self.rasa_client.message_received.connect(self.handle_bot_response)
        self.rasa_client.error_occurred.connect(self.handle_error)

    def set_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QFrame {
                background-color: #1F1F1F;
                border-radius: 12px;
                padding: 10px;
            }
            QScrollArea {
                border: none;
            }
            QTextEdit {
                background-color: #121212;
                border: none;
                padding: 15px;
                font-size: 15px;
                color: #E0E0E0;
                selection-background-color: #3A84FF;
            }
            QLineEdit {
                background-color: #2C2C2C;
                color: #E0E0E0;
                border: 2px solid #3A84FF;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                selection-color: #121212;
                selection-background-color: #66A1FF;
            }
            QLineEdit:focus {
                border: 2px solid #66A1FF;
                background-color: #3B3B3B;
            }
            QPushButton#send_button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                              stop:0 #3A84FF, stop:1 #66A1FF);
                color: white;
                font-weight: 600;
                border-radius: 20px;
                padding: 10px 25px;
                font-size: 15px;
                min-width: 90px;
                cursor: pointer;
                transition: all 0.25s ease;
            }
            QPushButton#send_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                              stop:0 #4C9EFF, stop:1 #85B8FF);
            }
            QPushButton#send_button:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                              stop:0 #2C68E8, stop:1 #4C8CFF);
            }
            QPushButton#send_button:focus {
                outline: none;
            }
            QPushButton#send_button {
                box-shadow: 0 4px 8px rgba(58, 132, 255, 0.6);
            }
            QPushButton#send_button:disabled {
                background: #555555;
                color: #AAAAAA;
                box-shadow: none;
                cursor: not-allowed;
            }
        """)

        font = QFont('Segoe UI', 11)
        self.chat_display.setFont(font)
        self.user_input.setFont(font)

        self.send_button.setObjectName("send_button")

    def show_welcome_message(self):
        self.add_message("AI Assistant", "Hello! How can I help you today?",
                         "#2C3E50", "#ECF0F1", "left")

    @pyqtSlot()
    def send_message(self):
        user_text = self.user_input.text().strip()
        if user_text:
            self.add_message("You", user_text, "#34495E", "#FDFEFE", "right")
            self.user_input.clear()
            self.add_typing_indicator()
            QTimer.singleShot(1000, lambda: self.rasa_client.send_message(user_text))

    @pyqtSlot(str)
    def handle_bot_response(self, message):
        self.remove_typing_indicator()
        self.add_message("AI Assistant", message, "#2C3E50", "#ECF0F1", "left")

    @pyqtSlot(str)
    def handle_error(self, error_msg):
        self.remove_typing_indicator()
        self.add_message("System", error_msg, "#7B241C", "#FADBD8", "left")

    def add_message(self, sender, message, bg_color, text_color, align):
        timestamp = QDateTime.currentDateTime().toString("hh:mm AP")
        message_html = f"""
        <div style='margin: 12px 0; text-align: {align};'>
            <div style='font-weight: 600; color: {text_color}; font-size: 13px; margin-bottom: 4px;'>
                {sender} <span style='font-size: 0.75em; color: #AAAAAA;'>{timestamp}</span>
            </div>
            <div style='background-color: {bg_color};
                        padding: 12px 18px;
                        border-radius: 16px;
                        display: inline-block;
                        max-width: 75%;
                        word-wrap: break-word;
                        font-size: 15px;
                        color: {text_color};
                        box-shadow: 0 2px 6px rgba(0,0,0,0.35);'>
                {message}
            </div>
        </div>
        """
        self.chat_display.append(message_html)
        self.chat_display.moveCursor(QTextCursor.End)

    def add_typing_indicator(self):
        self.typing_id = "typing_indicator"
        dots_html = f"""
        <div id='{self.typing_id}' style='text-align: left; margin: 12px 0;'>
            <div style='background-color: #1F2735;
                        padding: 10px 18px;
                        border-radius: 16px;
                        display: inline-block;
                        max-width: 80%;
                        font-size: 20px;
                        color: #AAAAAA;
                        box-shadow: 0 1px 4px rgba(0,0,0,0.3);'>
                <i>...</i>
            </div>
        </div>
        """
        self.chat_display.append(dots_html)
        self.chat_display.moveCursor(QTextCursor.End)

    def remove_typing_indicator(self):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.select(QTextCursor.BlockUnderCursor)
        if '...' in cursor.selectedText():
            cursor.removeSelectedText()
            cursor.deletePreviousChar()

    def closeEvent(self, event):
        self.rasa_client.stop_rasa_servers()
        event.accept()


from PyQt5.QtCore import QObject, pyqtSignal

class DummyRasaClient(QObject):
    message_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def send_message(self, msg):
        # Dummy: Mesajı hemen geri gönder
        self.message_received.emit(f"Echo: {msg}")

    def stop_rasa_servers(self):
        pass

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    rasa_client = DummyRasaClient()
    window = ChatWindow(rasa_client)
    window.show()
    sys.exit(app.exec_())



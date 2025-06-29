import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton,
                             QScrollArea, QFrame)
from PyQt5.QtCore import Qt, pyqtSlot, QSize, QDateTime
from PyQt5.QtGui import QTextCursor, QFont, QIcon

from rasaProjectLast.RasaClient import RasaClient

class ModernChatWindow(QMainWindow):
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
        """Pencere temel ayarlarını yapar"""
        self.setWindowTitle('Rasa ChatBot')
        self.setGeometry(300, 300, 350, 550)
        self.setMinimumSize(QSize(600, 700))

        # Pencere ikonu
        try:
            self.setWindowIcon(QIcon('https://cdn-icons-png.flaticon.com/512/4712/4712035.png'))
        except:
            pass

    def create_widgets(self):
        """Tüm widget'ları oluşturur"""
        # Ana bileşenler
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)

        # Chat alanı
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.chat_display)
        self.scroll_area.setWidgetResizable(True)

        # Input alanı
        self.input_frame = QFrame()
        self.input_layout = QHBoxLayout(self.input_frame)

        self.user_input = QLineEdit()
        self.send_button = QPushButton("Send")

        # Status bar
        self.status_bar = self.statusBar()

    def setup_layouts(self):
        """Layout düzenini kurar"""
        # Ana layout
        self.setCentralWidget(self.central_widget)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.input_frame)

        # Input layout
        self.input_layout.addWidget(self.user_input)
        self.input_layout.addWidget(self.send_button)

    def setup_connections(self):
        """Sinyal-slot bağlantılarını kurar"""
        self.send_button.clicked.connect(self.send_message)
        self.user_input.returnPressed.connect(self.send_message)
        self.rasa_client.message_received.connect(self.handle_bot_response)
        self.rasa_client.error_occurred.connect(self.handle_error)

    def set_styles(self):
        """Dark theme stil ayarları"""
        # Genel stil
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QFrame {
                background-color: #1E1E1E;
                border-radius: 10px;
            }
            QScrollArea {
                border: none;
            }
        """)

        # Chat ekranı stili
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E ;
                border: none;
                padding: 10px;
                font-size: 14px;
                color: white;
            }
        """)

        # Input alanı stili
        self.input_frame.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border-top: 1px solid #333;
                padding: 8px;
            }
            QLineEdit {
                background-color: #333;
                color: white;
                border: 2px solid #444;
                border-radius: 15px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)

        # Buton stili
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

        # Font ayarları
        font = QFont()
        font.setFamily('Arial')
        self.chat_display.setFont(font)
        self.user_input.setFont(font)

    def show_welcome_message(self):
        """Hoş geldin mesajını gösterir"""
        self.add_message("AI Assistant", "Hello! How can I help you today?",
                         "#2D2D2D", "#FFFFFF", "left")

    @pyqtSlot()
    def send_message(self):
        """Kullanıcı mesajını işler"""
        user_text = self.user_input.text().strip()
        if user_text:
            self.add_message("You", user_text, "#2D2D2D", "#FFFFFF", "right")
            self.user_input.clear()
            self.rasa_client.send_message(user_text)

    @pyqtSlot(str)
    def handle_bot_response(self, message):
        """Bot yanıtını işler"""
        self.add_message("AI Assistant", message, "#2D2D2D", "#FFFFFF", "left")

    @pyqtSlot(str)
    def handle_error(self, error_msg):
        """Hataları işler"""
        self.add_message("System", error_msg, "#4A2D2D", "#FF6B6B", "left")

    def add_message(self, sender, message, bg_color, text_color, align):
        """Mesaj ekranına yeni mesaj ekler"""
        timestamp = QDateTime.currentDateTime().toString("hh:mm AP")

        message_html = f"""
        <div style='margin: 8px; text-align: {align};'>
            <div style='font-weight: bold; color: {text_color}; 
                       margin-bottom: 2px;'>
                {sender} <span style='font-size: 0.8em; color: #AAA;'>{timestamp}</span>
            </div>
            <div style='background-color: {bg_color};
                       padding: 10px 15px;
                       border-radius: 12px;
                       display: inline-block;
                       max-width: 80%;
                       word-wrap: break-word;
                       box-shadow: 0 1px 3px rgba(0,0,0,0.3);'>
                {message}
            </div>
        </div>
        """

        self.chat_display.append(message_html)
        self.chat_display.moveCursor(QTextCursor.End)

    def closeEvent(self, event):
        """Pencere kapatılırken yapılacak işlemler"""
        self.rasa_client.stop_rasa_servers()
        event.accept()

class ChatApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.rasa_client = RasaClient()
        self.window = ModernChatWindow(self.rasa_client)

    def run(self):
        try:
            self.rasa_client.start_rasa_servers()
            self.window.show()
            sys.exit(self.app.exec_())
        except Exception as e:
            print(f"Application error: {str(e)}")
        finally:
            self.rasa_client.stop_rasa_servers()

if __name__ == "__main__":
    chat_app = ChatApplication()
    chat_app.run()
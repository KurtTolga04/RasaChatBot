import sys

from PyQt5.QtWidgets import QApplication

from rasaProjectLast.GUI.guı import ChatWindow
from rasaProjectLast.RasaClient import RasaClient


class ChatApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.rasa_client = RasaClient()
        self.window = ChatWindow(self.rasa_client)

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
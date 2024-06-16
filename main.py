import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Flat Style Button Example')
        self.setGeometry(0, 0, 1000, 500)

        layout = QVBoxLayout()

        # Create a QPushButton
        self.button = QPushButton('Click me')

        # Apply stylesheet for flat style button with blue color
        self.button.setStyleSheet('''
            QPushButton {
                background-color: #007bff;
                border-style: solid;
                border-width: 2px;
                border-radius: 5px;
                border-color: #007bff;
                color: white;
                padding: 8px 16px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
                border-color: #0056b3;
            }
        ''')

        # Connect button click signal to slot
        self.button.clicked.connect(self.on_button_clicked)

        layout.addWidget(self.button)
        self.setLayout(layout)

    def on_button_clicked(self):
        # This function will be called when the button is clicked
        print("Button clicked!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

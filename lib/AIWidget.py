import sys
import os

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QStackedWidget, QComboBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QDir, QThread, pyqtSignal
from dotenv import load_dotenv

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import SketchToImageWidget

   
class TextToImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize UI components for Text to Image tool

    # Implement the process_image method for Text to Image tool
    def process_image(self):
        pass  # Replace with actual implementation

class ImageUpscalingWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize UI components for Image Upscaling tool

    # Implement the process_image method for Image Upscaling tool
    def process_image(self):
        pass  # Replace with actual implementation

        
class AIWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Load environment variables from .env file
        load_dotenv()

        # Access the API key
        self.stablexl_key = os.getenv("STABLEXL_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        # Create layout
        layout = QVBoxLayout()

        # Create a combo box for tool selection
        self.toolComboBox = QComboBox()
        self.toolComboBox.addItems(["Sketch to Image", "Text to Image", "Image Upscaling"])
        layout.addWidget(self.toolComboBox)

        # Create a stacked widget to hold tool widgets
        self.stackedWidget = QStackedWidget()
        layout.addWidget(self.stackedWidget)

        # Add tool widgets to the stacked widget
        self.stackedWidget.addWidget(SketchToImageWidget.SketchToImageWidget(self.stablexl_key))  # Pass the API key to the widget
        self.stackedWidget.addWidget(TextToImageWidget())
        self.stackedWidget.addWidget(ImageUpscalingWidget())

        # Connect the combo box signal to switch tool widgets
        self.toolComboBox.currentIndexChanged.connect(self.stackedWidget.setCurrentIndex)

        # Set layout
        self.setLayout(layout)







import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QDir
from dotenv import load_dotenv

class AIWidget(QWidget):
    def __init__(self, layout=None, parent=None):
        super(AIWidget, self).__init__(parent)

        # Initialize UI components
        self.init_ui()
        # Load environment variables from .env file
        load_dotenv()

        # Access the API key
        api_key = os.getenv("STABLEXL_API_KEY")
        
        print(api_key)

    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create upload button
        self.upload_btn = QPushButton('Upload Image')
        self.upload_btn.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_btn)

        # Create process button
        self.process_btn = QPushButton('Process Image')
        self.process_btn.clicked.connect(self.process_image)
        layout.addWidget(self.process_btn)

        # Create image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        # Set layout
        self.setLayout(layout)

    def upload_image(self):
        # Open file dialog to select image
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', QDir.homePath(), 'Images (*.png)')
        if file_name:
            # Display the selected image
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)
            self.current_image_path = file_name

    def process_image(self):
        # Check if there is an old image
        if hasattr(self, 'current_image_path'):
            # Save old image to desktop
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            old_image_name = os.path.basename(self.current_image_path)
            old_image_path = os.path.join(desktop_path, old_image_name)
            os.rename(self.current_image_path, old_image_path)

            # Make API call and process the image (Replace this with actual API call)
            # ...

            # Display the new image (Replace this with actual new image)
            # ...
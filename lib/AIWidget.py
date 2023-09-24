import sys
import os
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QDir
from dotenv import load_dotenv

class AIWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.init_ui()
        # Load environment variables from .env file
        load_dotenv()

        # Access the API key
        stablexl_key = os.getenv("STABLEXL_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        

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
        # Check if there is an old image and API key is available
        if hasattr(self, 'current_image_path') and self.clipdrop_api_key:
            # Save old image to desktop
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            old_image_name = os.path.basename(self.current_image_path)
            old_image_path = os.path.join(desktop_path, old_image_name)
            os.rename(self.current_image_path, old_image_path)

            # Make API call and process the image
            url = "https://api.clipdrop.co/sketch-to-image"
            headers = {
                "Authorization": f"Bearer {self.clipdrop_api_key}",
                "Content-Type": "application/json",
            }
            with open(self.current_image_path, 'rb') as image_file:
                files = {'image': image_file}
                response = requests.post(url, headers=headers, files=files)
            print("Called the API key")
            # Handle the API response
            if response.status_code == 200:
                # Save and display the new image
                new_image_path = os.path.join(desktop_path, 'new_image.png')
                with open(new_image_path, 'wb') as new_image_file:
                    new_image_file.write(response.content)
                pixmap = QPixmap(new_image_path)
                self.image_label.setPixmap(pixmap)
                self.current_image_path = new_image_path
            else:
                # Handle API errors
                print(f"Error: Unable to process image. API Response: {response.status_code}, {response.text}")








import sys
import os
import shutil
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
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
        self.stablexl_key = os.getenv("STABLEXL_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        

    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create upload button
        self.upload_btn = QPushButton('Upload Image')
        self.upload_btn.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_btn)

        # Create prompt input field
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Enter prompt describing the content to generate")
        layout.addWidget(self.prompt_input)

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
            scaled_pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)
            self.current_image_path = file_name

    def process_image(self):
        print("Processing image...")
        prompt = self.prompt_input.text().strip()
        # Check if there is an old image and API key is available
        if hasattr(self, 'current_image_path') and self.stablexl_key:
            print("Image and API key are available...")
            # Save old image to desktop
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            old_image_name = os.path.basename(self.current_image_path)
            old_image_path = os.path.join(desktop_path, old_image_name)
          
            try:
                print("About to enter shutil code")
                shutil.copy(self.current_image_path, old_image_path)  # Copy the original image to the desktop
                print( "Post shutil")
            except Exception as e:
                print("Exception occurred:", e)
            # Define the URL, headers, and prompt
            url = "https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image"
            headers = {
                "x-api-key": self.stablexl_key,
            }

            # Make API call and process the image
            with open(self.current_image_path, 'rb') as image_file:  # Use the original image file for the API call
                files = {'sketch_file': (old_image_name, image_file, 'image/png')}
                data = {'prompt': prompt}
                response = requests.post(url, headers=headers, files=files, data=data)
            
            print("Called the API key")

                
            # Handle the API response
            if response.status_code == 200:
                # Save and display the new image
                print("API call successful...")
                new_image_path = os.path.join(desktop_path, 'new_image.jpg')
                with open(new_image_path, 'wb') as new_image_file:
                    new_image_file.write(response.content)
                pixmap = QPixmap(new_image_path)
                scaled_pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4, Qt.AspectRatioMode.KeepAspectRatio)
                self.image_label.setPixmap(scaled_pixmap)
                self.current_image_path = new_image_path
            else:
                # Handle API errors
                print(f"Error: Unable to process image. API Response: {response.status_code}, {response.text}")








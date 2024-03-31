# 000000001k Image Capture and Upload System

## Overview

This system, developed by Team 000000001k, is designed to capture images using a Raspberry Pi's camera module, encode them in Base64 format, and then upload them to a specified Azure Machine Learning endpoint. This document outlines how to set up and use the system, as well as the prerequisites needed for a successful installation.

## Prerequisites

Before you can use this system, ensure that your Raspberry Pi meets the following requirements:

1. **Raspberry Pi OS**: Your Raspberry Pi should be running the latest version of Raspberry Pi OS.
2. **Camera Module**: A compatible Raspberry Pi camera module must be connected and enabled.
3. **Python 3**: This script is written for Python 3. Ensure it is installed along with the pip package manager.
4. **Required Python Packages**:
   - `opencv-python`: For capturing and processing images.
   - `base64`: Usually included with Python.
   - `urllib3`: For making network requests.

You can install the required Python packages using pip:

'''

Sure, here is the complete README formatted for markdown:

markdown
Copy code
# 000000001k Image Capture and Upload System

## Overview

This system, developed by Team 000000001k, is designed to capture images using a Raspberry Pi's camera module, encode them in Base64 format, and then upload them to a specified Azure Machine Learning endpoint. This document outlines how to set up and use the system, as well as the prerequisites needed for a successful installation.

## Prerequisites

Before you can use this system, ensure that your Raspberry Pi meets the following requirements:

1. **Raspberry Pi OS**: Your Raspberry Pi should be running the latest version of Raspberry Pi OS.
2. **Camera Module**: A compatible Raspberry Pi camera module must be connected and enabled.
3. **Python 3**: This script is written for Python 3. Ensure it is installed along with the pip package manager.
4. **Required Python Packages**:
   - `opencv-python`: For capturing and processing images.
   - `base64`: Usually included with Python.
   - `urllib3`: For making network requests.

You can install the required Python packages using pip:


pip3 install opencv-python urllib3


## Installation

1. **Clone the Repository**: Clone this repository to your Raspberry Pi. If `git` is not installed, you can download the ZIP file directly from the project page.

git clone <repository-url>
cd <repository-directory>

2. **Configuration**: No initial configuration is needed for the script to run, but you may want to adjust the Azure endpoint URL and API key in the `upload_to_azure` function to match your deployment.

python3 main.py

## Usage

To start the image capture and upload process, navigate to the script's directory in your terminal and run:


This command initializes the system, which will then continuously capture images at 10-second intervals, encode them, and upload them to the specified Azure endpoint.

## How It Works

- **Image Capture**: Utilizes OpenCV to capture images from the camera module.
- **Image Encoding**: Converts the captured image to Base64 format for easy transmission over the network.
- **Uploading**: Sends the encoded image to an Azure endpoint along with any necessary metadata.

## Troubleshooting

- **Camera Not Detected**: Ensure the camera is properly connected and enabled via `raspi-config`.
- **Dependency Errors**: Verify all required Python packages are installed.
- **Network Issues**: Ensure your Raspberry Pi has a stable internet connection and the Azure endpoint URL and API key are correct.

## Contributing

Team 000000001k welcomes contributions to this project. Please feel free to fork the repository, make your changes, and submit a pull request for review.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This system was created by Team 000000001k as a versatile tool for Raspberry Pi enthusiasts and developers looking to integrate image capture and cloud processing capabilities into their projects.

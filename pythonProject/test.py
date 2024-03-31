import cv2  # OpenCV for image processing
import ftplib  # FTP protocol client (unused in the script)
import time  # Time access and conversions
import urllib.request  # Open URL functions
import json  # JSON encoder and decoder
import os  # Operating system interfaces
import ssl  # SSL/TLS security (unused in the script)
import base64  # Base64 encoding and decoding

def encode_image_to_base64(image_path):
    # Open the image file in binary-read mode, encode it to Base64, and return the encoded string
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def upload_to_azure(encoded_image):
    # Prepares and sends a request to an Azure endpoint with the encoded image and some static data
    data = {
        'chat_history': [  # Example static data
            {
                "inputs": {
                    "image": [
                        "../../.tmp/promptflow/inputs/Nikita_1711815339809.jpg"
                    ]
                },
                "outputs": {
                    "answer": [
                        "Asphalt Legends Unite"
                    ]
                }
            }
        ],
        'base64': encoded_image  # Encoded image data
    }

    body = json.dumps(data).encode('utf-8')  # Convert data to JSON and then to bytes

    # Endpoint URL and API key for Azure ML service
    url = 'https://z00000001k-ml-cydmy.westus.inference.ml.azure.com/score'
    api_key = '2IVZwT9DlLO0uoH7MCp9Ij4dzolCa5ta'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # Request headers including the content type, authorization, and specific Azure deployment
    headers = {
        'Content-Type': 'application/json',
        'Authorization': ('Bearer ' + api_key),
        'azureml-model-deployment': 'z00000001k-ml-cydmy-9'
    }

    req = urllib.request.Request(url, body, headers)  # Prepare the request

    try:
        response = urllib.request.urlopen(req)  # Send the request
        result = response.read()  # Read the response
        result_json = json.loads(result)  # Parse the JSON response
        print(result_json)

        # Process the response, assuming it contains an image filename, then display the image
        if 'answer' in result_json:
            answer = result_json['answer']
            image_path = f'./ads/{answer}.jpg'  # Construct the image path
            if os.path.exists(image_path):
                img = cv2.imread(image_path)  # Load the image
                cv2.namedWindow('Azure Response Image', cv2.WINDOW_NORMAL)  # Create a window
                cv2.setWindowProperty('Azure Response Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # Fullscreen
                img = cv2.resize(img, (1920, 1080))  # Resize the image
                cv2.imshow('Azure Response Image', img)  # Display the image
                cv2.waitKey(1)  # Pause for a moment to display the image
            else:
                print(f"Image file '{image_path}' not found.")
    except urllib.error.HTTPError as error:
        # Handle HTTP errors
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

def capture_and_upload():
    # Continuously capture images from a webcam, encode them, and upload to Azure
    while True:
        cap = cv2.VideoCapture(0)  # Start video capture
        ret, frame = cap.read()  # Read one frame
        cv2.imwrite("image.jpg", frame)  # Save the frame as an image
        print("Picture taken!")
        encoded_image = encode_image_to_base64("image.jpg")  # Encode the image
        if encoded_image:
            upload_to_azure(encoded_image)  # Upload the encoded image
        cap.release()  # Release the capture object
        time.sleep(10)  # Wait for 10 seconds before the next capture

if __name__ == "__main__":
    capture_and_upload()  # Start the capture and upload process

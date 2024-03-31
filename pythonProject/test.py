import cv2
import time
import urllib.request
import json
import os
import base64

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def encode_image_to_base64(image_path):
    # Function to encode an image to Base64 format
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def upload_to_azure(encoded_image):
    # Function to upload the encoded image to Azure
    data = {
        'chat_history': [
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
        'base64': encoded_image
    }

    body = json.dumps(data).encode('utf-8')

    url = 'https://z00000001k-ml-cydmy.westus.inference.ml.azure.com/score'
    api_key = '2IVZwT9DlLO0uoH7MCp9Ij4dzolCa5ta'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': ('Bearer ' + api_key),
        'azureml-model-deployment': 'z00000001k-ml-cydmy-10'
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        result_json = json.loads(result)
        print(result_json)

        if 'answer' in result_json:
            answer = result_json['answer']
            image_path = f'./ads/{answer}.jpg'
            if os.path.exists(image_path):
                img = cv2.imread(image_path)
                cv2.namedWindow('Azure Response Image', cv2.WINDOW_NORMAL)
                cv2.setWindowProperty('Azure Response Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                img = cv2.resize(img, (1920, 1080))
                cv2.imshow('Azure Response Image', img)
                cv2.waitKey(1)
            else:
                print(f"Image file '{image_path}' not found.")
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

def capture_and_upload():
    # Function to continuously capture images from a webcam, encode them, and upload to Azure
    cap = cv2.VideoCapture(0)  # Start video capture
    face_detected = False  # Flag to track if a face is detected in real-time

    while True:
        ret, frame = cap.read()  # Capture the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale

        # Detect faces in the frame in real-time
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            print("Face detected in real-time")
            face_detected = True
            time.sleep(2)  # Wait for 2 seconds

            ret, picture_frame = cap.read()  # Capture the picture after delay
            gray_picture = cv2.cvtColor(picture_frame, cv2.COLOR_BGR2GRAY)  # Convert picture frame to grayscale

            # Detect faces in the picture
            picture_faces = face_cascade.detectMultiScale(gray_picture, scaleFactor=1.1, minNeighbors=5,
                                                          minSize=(30, 30))
            if len(picture_faces) > 0:
                # If face detected in the picture, save and upload it
                cv2.imwrite("image.jpg", picture_frame)
                print("Face detected in the picture. Picture taken!")
                encoded_image = encode_image_to_base64("image.jpg")
                if encoded_image:
                    upload_to_azure(encoded_image)
                face_detected = False  # Reset the flag
                time.sleep(3)
            else:
                print("No face detected in the picture. Restarting the cycle...")
                face_detected = False
        else:
            face_detected = False

    cap.release()

if __name__ == "__main__":
    capture_and_upload()

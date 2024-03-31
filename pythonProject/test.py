import cv2
import time
import urllib.request
import json
import os
import base64

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image


def upload_to_azure(encoded_image):
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
        'azureml-model-deployment': 'z00000001k-ml-cydmy-9'
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
    # Continuously capture images from a webcam, encode them, and upload to Azure
    cap = cv2.VideoCapture(0)  # Start video capture
    while True:
        # cap = cv2.VideoCapture(0)!!!!!!!!!!
        ret, frame = cap.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            print("Face noticed")

        # Wait for 2 seconds
        time.sleep(2)

        # Re-detect faces in the frame after 2 seconds
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        new_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # If faces are detected, save the image and upload to Azure
        if len(new_faces) > 0:
            cv2.imwrite("image.jpg", frame)
            print("Face detected and picture taken!")
            encoded_image = encode_image_to_base64("image.jpg")
            if encoded_image:
                upload_to_azure(encoded_image)

        time.sleep(1)
    cap.release()


if __name__ == "__main__":
    capture_and_upload()

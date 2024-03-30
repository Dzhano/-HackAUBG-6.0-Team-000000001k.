import cv2
import ftplib
import time
import urllib.request
import json
import os
import ssl
import base64


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
        'azureml-model-deployment': 'z00000001k-ml-cydmy-7'
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        result_json = json.loads(result)
        print(result_json)

        # Check if the response contains an answer that corresponds to an image filename
        if 'answer' in result_json:
            answer = result_json['answer']
            image_path = f'./ads/{answer}.jpg'  # Assuming the image filename is the same as the answer
            if os.path.exists(image_path):
                # Load the image
                img = cv2.imread(image_path)

                # Set the window name and properties
                cv2.namedWindow('Azure Response Image', cv2.WINDOW_NORMAL)
                cv2.setWindowProperty('Azure Response Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                # Resize the image to 1920x1080
                img = cv2.resize(img, (1920, 1080))

                # Display the image
                cv2.imshow('Azure Response Image', img)
                cv2.waitKey(1)  # Change waitKey to 1 millisecond
            else:
                print(f"Image file '{image_path}' not found.")

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))


def capture_and_upload():
    while True:
        # Start capturing video from the camera
        cap = cv2.VideoCapture(0)

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Take a picture
        cv2.imwrite("image.jpg", frame)
        print("Picture taken!")

        # Encode the image into base64
        encoded_image = encode_image_to_base64("image.jpg")

        # Check if the image was encoded successfully
        if encoded_image:
            # Upload the image to Azure
            upload_to_azure(encoded_image)

        # Release the video capture object
        cap.release()

        # Wait for 10 seconds before capturing the next frame
        time.sleep(10)


if __name__ == "__main__":
    capture_and_upload()

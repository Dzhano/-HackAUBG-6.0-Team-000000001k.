import cv2
import ftplib
import time
import urllib.request
import json
import os
import ssl
import base64


def upload_to_azure(image_path):
    # Read the image file
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the JSON payload
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
        'image': encoded_image
    }

    body = json.dumps(data).encode('utf-8')

    url = 'https://z00000001k-ml-cydmy.westus.inference.ml.azure.com/score'
    api_key = '2IVZwT9DlLO0uoH7MCp9Ij4dzolCa5ta'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': ('Bearer ' + api_key),
        'azureml-model-deployment': 'z00000001k-ml-cydmy-3'
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
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

        # Upload the image to Azure
        upload_to_azure("image.jpg")

        # Release the video capture object
        cap.release()

        # Wait for 10 seconds before capturing the next frame
        time.sleep(10)


if __name__ == "__main__":
    capture_and_upload()

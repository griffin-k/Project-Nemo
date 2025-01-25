import cv2
import os
import sys
sys.path.append(os.getcwd())
import google.ai.generativelanguage as glm
import google.generativeai as genai
import textwrap
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

MODEL_NAME = 'gemini-1.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

def to_markdown(text):
    text = text.replace('*', ' ')
    reply = textwrap.indent(text, '>', predicate=lambda _: True)
    print(reply)

def recog():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Waiting for camera to initialize...")
    cv2.waitKey(2000) 

    ret, frame = cap.read()
    if not ret:
        print("Error reading from webcam.")
        cap.release()
        return


    # cv2.imshow('Webcam Feed', frame)


    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        print("Error encoding image.")
        cap.release()
        return

    image_bytes = jpeg.tobytes()

    try:

        response = model.generate_content(
            glm.Content(
                parts=[
                    glm.Part(text="Explain what you see in this image in short."),
                    glm.Part(
                        inline_data=glm.Blob(
                            mime_type="image/jpeg",
                            data=image_bytes,
                        ),
                    ),
                ],
            ),
            stream=True
        )


        response.resolve()
        if response.candidates:
            # Assuming the first candidate is the best option
            explanation = response.candidates[0].content.parts[0].text
            to_markdown(explanation)
        else:
            print("No valid response received.")
    except Exception as e:
        print(f"Error during API call: {e}")

    # Destroy all windows and release the camera immediately after getting the response
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    recog()

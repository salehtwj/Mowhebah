import cv2, os, base64
from io import BytesIO
from PIL import Image as Image_2
from openai import OpenAI
import re
def resize_image(frame_b64, width, height):
    img = Image_2.open(BytesIO(base64.b64decode(frame_b64)))
    img_resized = img.resize((width, height))
    buffer = BytesIO()
    img_resized.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def analyze_video(video_path, challenge, nth_frame=1, resized_width=480, resized_height=510):
    base64Frames = []
    video = cv2.VideoCapture(video_path)
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
    video.release()

    trimmed_frames = base64Frames[::nth_frame]

    text_prompt = (
        "Here's a sequence of frames from a talented video. "
        "The player was responding to this challenge: {challenge}\n\n"
        "Analyze these frames and provide your response in valid JSON format with exactly this structure:\n"
        "{{\n"
        '  "rating": [0-100 numerical score],\n'
        '  "description": "short description and analysis less than 20 words"\n'
        "}}\n\n"
        "For the rating:\n"
        "- 0-20: Poor attempt, doesn't meet the challenge\n"
        "- 21-40: Basic attempt, minimal skill shown\n"
        "- 41-60: Decent attempt with some technical skill\n"
        "- 61-80: Good execution with clear technical ability\n"
        "- 81-100: Exceptional skill and beautiful goal execution\n\n"
        "In the description, please include:\n"
        "1. A detailed explanation of what happens in the video\n"
        "2. Analysis of the player's technique, skill level, and execution\n"
        "3. Evaluation if the content successfully completes the challenge of scoring a beautiful goal\n"
        "4. Comments on the type of shot/technique used\n"
        "5. Assessment of the difficulty level and creativity demonstrated\n"
        "6. Your justification for the rating score\n\n"
        "Make sure your response is a valid JSON object that can be parsed. Do not include any text outside the JSON structure."
    ).format(challenge=challenge, nth_frame=nth_frame)

    print(text_prompt)

    text_prompt_entry = {"type": "text", "text": text_prompt}
    image_entries = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{resize_image(frame, resized_width, resized_height)}"
            }
        } for frame in trimmed_frames
    ]

    messages = [
        {
            "role": "user",
            "content": [text_prompt_entry] + image_entries
        }
    ]

    client = OpenAI(api_key="sk-xxxx")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=100
    )

    raw_output = response.choices[0].message.content

    # Use regex to extract JSON from within ```json ... ```
    cleaned_json = re.sub(r"```json|```", "", raw_output).strip()
    print(cleaned_json)

    return cleaned_json


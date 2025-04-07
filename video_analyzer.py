import cv2, os, base64
from io import BytesIO
from PIL import Image as Image_2
from openai import OpenAI

def resize_image(frame_b64, width, height):
    img = Image_2.open(BytesIO(base64.b64decode(frame_b64)))
    img_resized = img.resize((width, height))
    buffer = BytesIO()
    img_resized.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def analyze_video(video_path, nth_frame=7, resized_width=480, resized_height=510):
    base64Frames = []
    video = cv2.VideoCapture(video_path)
    x = 1
    while video.isOpened():
        if x == 1:
            success, frame = video.read()
        success, frame = video.read()
        success, frame = video.read()
        x = 2
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
    video.release()

    trimmed_frames = base64Frames[::nth_frame]
    text_prompt = f"Here's every nth frame from a video (where n={nth_frame}). Please create a compelling explanation of what takes place in the video. The video shows football talent, describe it please."
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

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500
    )

    return response.choices[0].message.content

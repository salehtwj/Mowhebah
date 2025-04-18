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

# def analyze_video(video_path, challenge, nth_frame=3, resized_width=480, resized_height=510):
#     base64Frames = []
#     video = cv2.VideoCapture(video_path)
#     x = 1
#     while video.isOpened():
#         if x == 1:
#             success, frame = video.read()
#         success, frame = video.read()
#         success, frame = video.read()
#         x = 2
#         if not success:
#             break
#         _, buffer = cv2.imencode(".jpg", frame)
#         base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
#     video.release()

#     trimmed_frames = base64Frames[::nth_frame]
#     text_prompt = """
# Here's a sequence of frames (every ${nth_frame}th frame) from a football/soccer video submission. The player was responding to this challenge: ${challenge}

# Analyze these frames and provide your response in valid JSON format with exactly this structure:
# ```json{
#   "rating": [0-100 numerical score],
#   "description": "short description and analysis less that 20 words"
#   }```


# For the rating:
# - 0-20: Poor attempt, doesn't meet the challenge
# - 21-40: Basic attempt, minimal skill shown
# - 41-60: Decent attempt with some technical skill
# - 61-80: Good execution with clear technical ability
# - 81-100: Exceptional skill and beautiful goal execution

# In the description, please include:
# 1. A detailed explanation of what happens in the video
# 2. Analysis of the player's technique, skill level, and execution
# 3. Evaluation if the content successfully completes the challenge of scoring a beautiful goal
# 4. Comments on the type of shot/technique used
# 5. Assessment of the difficulty level and creativity demonstrated
# 6. Your justification for the rating score

# Make sure your response is a valid JSON object that can be parsed. Do not include any text outside the JSON structure.
# """
    
#     text_prompt_entry = {"type": "text", "text": text_prompt}
#     image_entries = [
#         {
#             "type": "image_url",
#             "image_url": {
#                 "url": f"data:image/jpeg;base64,{resize_image(frame, resized_width, resized_height)}"
#             }
#         } for frame in trimmed_frames
#     ]

#     messages = [
#         {
#             "role": "user",
#             "content": [text_prompt_entry] + image_entries
#         }
#     ]

#     client = OpenAI(api_key="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")
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages,
#         max_tokens=100
#     )

#     return response.choices[0].message.content


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

    client = OpenAI(api_key="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")
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


# app.py
import streamlit as st
from streamlit.components.v1 import html
import requests
import time
import os


# Attempt to retrieve API keys from environment variables
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else None
SYNTHESIA_API_KEY = st.secrets["SYNTHESIA_API_KEY"] if "SYNTHESIA_API_KEY" in st.secrets else None

def send_request_with_backoff(url, headers, data, retries=5, backoff_in_seconds=1):
    for i in range(retries):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 429:
            return response
        print(f"Rate limit exceeded. Retrying in {backoff_in_seconds} seconds...")
        time.sleep(backoff_in_seconds)
        backoff_in_seconds *= 2  # Double the wait time for the next retry
    return response  # Return the last response after all retries

# Use the modified request function in your OpenAI request
def translate_text(text, source_language, target_language):
    """Translate text from source to target language using OpenAI's GPT-3.5 Turbo."""
    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}'}
    # Adjust the structure for the chat API
    data = {
        "model": "gpt-3.5-turbo",  # Model identifier for GPT-3.5 Turbo
        "messages": [
            {"role": "system", "content": f"Translate the following text from {source_language} to {target_language}:"},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3,
        "max_tokens": 1024,
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        # Parse the response to extract the translated text
        latest_response = response.json()['choices'][0]['message']['content'].strip()  # Adjusted to access 'message' and 'content'
        return latest_response
    else:
        # Handle errors with Streamlit if this is part of a Streamlit app
        st.error(f"Request failed with status code: {response.status_code}")
        return None

def convert_language_code(lang_code):
    # Updated mapping with English and Arabic examples
    mapping = {
        "en-EN": "en-US",  # Incorrect format to correct format for English
        "en-GB": "en-US",  # British English to US English (if you decide to standardize on US English)
        "ar-AR": "ar-SA",  # Example incorrect format to correct format for Arabic
        # "ar-SA": "ar-SA",  # Not needed since "ar-SA" is already correct, but here for clarity
        # Add more mappings as needed
    }
    # Return the corrected code if it exists in the mapping, else return the original
    return mapping.get(lang_code, lang_code)


def create_video(script_text, avatar, background, language):
    """Create a video using the Synthesia API."""
    headers = {'Authorization': f'Token {SYNTHESIA_API_KEY}'}
    corrected_language = convert_language_code(language)
    data = {
        "test": True,
        "input": [{
            "scriptText": script_text,
            "avatar": avatar,
            "background": background,
            "avatarSettings": {
                "voice": corrected_language,
                "style": "rectangular",
            },
        }]
    }
    try:
        response = send_request_with_backoff(
            'https://api.synthesia.io/v2/videos',
            headers=headers,
            data=data
        )
        response.raise_for_status()  # Raise an error for bad responses
        video_id = response.json().get('id')
        return f"https://share.synthesia.io/{video_id}"
    except requests.RequestException as e:
        return f"Failed to create video: {e}"


# UI for API Key input if not found
if not OPENAI_API_KEY:
    OPENAI_API_KEY = st.text_input("Enter OpenAI API Key:", type="password", key="openai_api_input")
if not SYNTHESIA_API_KEY:
    SYNTHESIA_API_KEY = st.text_input("Enter Synthesia API Key:", type="password", key="synthesia_api_input")


# Improved Page configuration with a more descriptive title and using an icon
st.set_page_config(page_title="Mathshub AI Avatar for Building Content", page_icon="🧮")

# Logo and title with GitHub link
logo_url = "https://static.tildacdn.com/tild3433-6132-4833-a666-323830396132/Logo.svg"
st.markdown(f"<img src='{logo_url}' alt='Mathshub logo' style='height: 50px;'>", unsafe_allow_html=True)

st.markdown("# Mathshub AI Avatar for Building Content")
st.markdown("Check our [GitHub repository](https://github.com/ayranamo/mathshub-ai-avatars) for more information and updates.")
st.markdown("_Example video for translation: Hello everyone, and welcome to the exciting world of Python programming! Python is known for its simplicity and versatility, making it a great choice for beginners and professionals alike. The first step in your Python journey is installing Python on your computer. Once installed, you can write your first line of code: print(\"Hello, world!\"). This simple command tells Python to display the message 'Hello, world!' on your screen._")

# This CSS makes the video responsive and tries to keep it at the top left with padding.
# Note: This will not dynamically change the position from top to left based on viewport as traditional media queries would.
video_html = """
<style>
.video-wrapper {
    padding-top: 20px; /* Top padding */
    display: flex;
    justify-content: flex-start; /* Align to the left side */
    align-items: flex-start; /* Align to the top */
}

.responsive-iframe-container {
    position: relative;
    overflow: hidden;
    padding-top: 56%; /* 4:3 Aspect Ratio for horizontal videos */
    /* For vertical videos, use 177.77% to represent a 9:16 aspect ratio */
    width: 100%;
}

.responsive-iframe-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: 0;
}
</style>

<div class="video-wrapper">
    <div class="responsive-iframe-container">
        <iframe
            src="https://www.youtube-nocookie.com/embed/Bp15OxS3PwI?rel=0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
    </div>
</div>
"""
# Use the html() function to render the responsive vertical video iframe in your Streamlit app
html(video_html, height=400)

# Select language and show example text
source_language = st.selectbox("Select Source Language", ["English", "Arabic", "Bahasa"], index=0)
target_language = st.selectbox("Select Target Language", ["English", "Arabic", "Bahasa"], index=0)

text_to_translate = st.text_area("Text to Translate:", height=150)
translate_button = st.button("Translate")

if translate_button:
    # Assuming 'source_language' and 'target_language' are defined earlier and 'OPENAI_API_KEY' is available
    translated_text = translate_text(text_to_translate, source_language, target_language)
    st.text_area("Translated Text:", value=translated_text, height=150, key='translated_text_area')


# Translation and video creation inputs
text_for_video = st.text_area("Text for Video:", height=150, key="text_for_video")

# Select avatar and voice
avatar_options = {
    "Alex": "anna_costume1_cameraA",
    "Bridget 1": "bridget_costume1_cameraA",
    "Bridget 2": "bridget_costume2_cameraA",
    "Christina": "11b26380-ed22-490b-8ccb-afb34559bc99",
    "Jack 1": "jack_costume1_cameraA",
    "Jack 2": "jack_costume2_cameraA",
    "James": "james_costume1_cameraA",
    "Jonathan": "jonathan_costume1_cameraA",
    "Katherine": "katherine_costume1_cameraA",
}

voice_options = {
    "Arabic (SA) - Natural Male": "c1da2241-c031-4e53-af2e-a91121e5ca9f",
    "Arabic (SA) - Natural Female": "8a0fa9ba-787e-4c77-bbd7-63f196bc503d",
    "English (GB) - Original Male": "f678f961-19ed-42a2-ac5e-bb54d8ddc479",
    "English (GB) - Natural 2 Female": "20c248b7-aae7-45ed-88c5-9acc0be07aa4",
}

selected_avatar = st.selectbox("Select Avatar:", list(avatar_options.keys()), index=0)
selected_voice = st.selectbox("Select Voice:", list(voice_options.keys()), index=0)
text_for_video = st.text_area("Text for Video:", height=150)
create_video_button = st.button("Create Video")

if create_video_button:
    avatar_id = avatar_options[selected_avatar]
    voice_id = voice_options[selected_voice]
    
    video_url = create_video(text_for_video, avatar_id, "off_white", language="en")  # Assuming English language
    if video_url.startswith("http"):
        st.success(f"Video created successfully! View at: {video_url}")
        st.video(video_url)
    else:
        st.error(f"Video Creation Error: {video_url}")

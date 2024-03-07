# app.py
import streamlit as st
import requests
import time
import os

# Set environment variables
os.environ['OPENAI_API_KEY'] = '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'  # Replace with your actual OpenAI API key
os.environ['SYNTHESIA_API_KEY'] = '2ebd5e0f29d01f2861cb730159957218'  # Replace with your actual Synthesia API key

# Retrieve API keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SYNTHESIA_API_KEY = os.getenv('SYNTHESIA_API_KEY')

def send_request_with_backoff(url, headers, data, retries=5, backoff_in_seconds=1):
    for i in range(retries):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 429:
            return response
        print(f"Rate limit exceeded. Retrying in {backoff_in_seconds} seconds...")
        time.sleep(backoff_in_seconds)
        backoff_in_seconds *= 2  # Double the wait time for the next retry
    return response  # Return the last response after all retries

def translate_text(text, source_language, target_language):
    """Translate text from source to target language using OpenAI's Chat Completions API."""
    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}'}

    messages = [
        {"role": "system", "content": f"You are a translation model that translates from {source_language} to {target_language}."},
        {"role": "user", "content": text}
    ]

    data = {
        "model": "gpt-3.5-turbo",  # Consider using the latest available model
        "messages": messages
    }

    response = send_request_with_backoff(
        'https://api.openai.com/v1/chat/completions',
        headers,
        data
    )

    if response.status_code == 200:
        latest_response = response.json()['choices'][0]['message']['content']
        return latest_response.strip()
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None


def create_video(script_text, avatar, background, language="en-US"):
    """Create a video using the Synthesia API."""
    headers = {'Authorization': f'Token {SYNTHESIA_API_KEY}'}
    data = {
        "test": True,
        "input": [{
            "scriptText": script_text,
            "avatar": avatar,
            "background": background,
            "avatarSettings": {
                "voice": language,
                "style": "rectangular",
            },
        }]
    }
    try:
        response = requests.post('https://api.synthesia.io/v2/videos', headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        video_id = response.json().get('id')
        return f"https://share.synthesia.io/{video_id}"
    except requests.RequestException as e:
        return f"Failed to create video: {e}"

# Improved Page configuration with a more descriptive title and using an icon
st.set_page_config(page_title="Mathshub AI Avatar for Building Content", page_icon="🧮")

# Logo and title with GitHub link
logo_url = "https://static.tildacdn.com/tild3433-6132-4833-a666-323830396132/Logo.svg"
st.markdown(f"<img src='{logo_url}' alt='Mathshub logo' style='height: 50px;'>", unsafe_allow_html=True)
st.markdown("# Mathshub AI Avatar for Building Content")
st.markdown("Check our [GitHub repository](https://github.com/ayranamo/mathshub-ai-avatars) for more information and updates.")

# Embedding YouTube video vertically on the left side with equal padding from the left and upper sides
video_iframe = """
<div style="position: fixed; top: 80px; left: 20px; width: 300px; height: calc(100vh - 80px); padding: 20px;">
    <iframe width="100%" height="100%" 
        src="https://www.youtube-nocookie.com/embed/Bp15OxS3PwI?si=bLOEqUGUNzDyYb9N" 
        title="YouTube video player" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        allowfullscreen>
    </iframe>
</div>
"""

# Use markdown to render the HTML, allowing unsafe HTML
st.markdown(video_iframe, unsafe_allow_html=True)

# Examples of translation texts
example_texts = {
    "English": "Hello everyone, and welcome to the exciting world of Python programming! Python is known for its simplicity and versatility...",
    "Arabic": "مرحبًا بالجميع، وأهلاً بكم في عالم البرمجة المثير مع لغة بايثون! تشتهر بايثون ببساطتها وتنوع استخداماتها...",
    "Bahasa": "Halo semuanya, dan selamat datang di dunia pemrograman Python yang menarik! Python dikenal dengan kesederhanaan dan keversatilannya..."
}

# Select language and show example text
source_language = st.selectbox("Select Source Language", ["English", "Arabic", "Bahasa"], index=0)
st.text_area("Example Text:", value=example_texts[source_language], height=150)

# Translation and video creation inputs
target_language = st.selectbox("Select Target Language", ["English", "Arabic", "Bahasa"], index=0)
text = st.text_area("Text to Translate and Use in Video:", height=150)
avatar = st.selectbox("Select Avatar", ["anna_costume1_cameraA", "mia_costume1_cameraA"], index=0)
background = st.selectbox("Select Background", ["off_white", "luxury_lobby"], index=0)

# Submit button for translation and video creation
if st.button("Translate and Create Video"):
    if source_language != target_language:
        translated_text = translate_text(text, source_language, target_language)
        if translated_text:
            video_url = create_video(translated_text, avatar, background, target_language)
            if video_url.startswith("http"):
                st.success(f"Video created successfully! View at: {video_url}")
                st.video(video_url)
            else:
                st.error(f"Video Creation Error: {video_url}")
    else:
        st.error("Source and target languages must be different.")
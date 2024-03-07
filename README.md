## Mathshub AI Avatars: Empowering Global Programming Education

### Example content in Arabic:
[![Video Title](http://img.youtube.com/vi/Bp15OxS3PwI/0.jpg)](http://www.youtube.com/watch?v=Bp15OxS3PwI)

### Description:
Mathshub AI Avatars is a cutting-edge platform designed to empower individuals worldwide to excel in programming education. Our platform is built on the principle of inclusivity, aiming to break down language barriers and provide learners with access to high-quality programming resources in their native languages. With Mathshub AI Avatars, we're revolutionizing the way programming education is delivered, making it accessible, engaging, and effective for learners of all backgrounds.

### Key Features:

1. **Multilingual Translation:** Mathshub AI Avatars offers seamless translation of programming materials into multiple languages. Educators and content creators can easily translate text, code snippets, and instructional materials, ensuring that learners can access programming content in their preferred language.

2. **Dynamic Video Creation:** Our platform simplifies the process of creating instructional videos, allowing educators to produce engaging content efficiently. From translating scripts to customizing avatars and backgrounds, Mathshub AI Avatars provides a user-friendly interface for creating dynamic instructional videos tailored to learners' needs.

3. **Integration with Learning Management Systems (LMS):** Mathshub AI Avatars integrates seamlessly with leading LMS platforms, enabling educators to deploy translated materials and instructional videos directly to their students. With easy import and integration capabilities, educators can deliver programming education effectively within their existing LMS environment.

4. **Personalized Learning Experience:** Mathshub AI Avatars offers a personalized learning experience for learners, allowing them to engage with programming concepts in a way that resonates with their preferences and learning styles. With customizable avatars, backgrounds, and settings, learners can immerse themselves in programming education that feels tailored to their needs.

5. **Global Impact:** By providing access to programming education in multiple languages, Mathshub AI Avatars is making a global impact on the accessibility and inclusivity of programming learning. Our platform is scalable and adaptable, with plans to expand support for additional languages and features, ensuring that learners worldwide can benefit from our innovative approach to programming education.

### Join Us in Transforming Programming Education!
Mathshub AI Avatars is more than just a platform—it's a movement towards a more inclusive, accessible, and effective approach to programming education. Whether you're an educator passionate about empowering learners or a developer eager to make a difference, we invite you to join us on this journey. Together, let's unlock the world of coding for everyone, regardless of language or background.

### Learn More:
Visit our website at [mathshub.education](https://maths-h.com) to explore how Mathshub AI Avatars is transforming programming education worldwide!


## Demo and source description:
This script combines the functionality of text translation and video creation using external APIs and presents them in an interactive web application using Streamlit.

### Imports
- **streamlit:** The Streamlit library for building interactive web applications.
- **requests:** Library for making HTTP requests.
- **time:** Module for time-related functions.
- **os:** Module for interacting with the operating system, used here for setting environment variables.

### Environment Variables
The script sets environment variables for the OpenAI API key (`OPENAI_API_KEY`) and the Synthesia API key (`SYNTHESIA_API_KEY`) using `os.environ`.

### Helper Functions
- **send_request_with_backoff:** Function for making HTTP requests with exponential backoff. It retries requests when encountering rate limiting (status code 429).
- **translate_text:** Function for translating text from a source language to a target language using OpenAI's Chat Completions API.
- **create_video:** Function for creating a video using the Synthesia API. It takes input text, avatar, background, and language settings.

### Page Configuration
- Sets the title and icon for the Streamlit app using `st.set_page_config`.
- Displays the logo and title of the application along with a link to the GitHub repository.

### YouTube Video Embed
- Embeds a YouTube video vertically on the left side of the application with equal padding from the left and upper sides. The video is embedded using an iframe HTML element within a Markdown string.

### Translation and Video Creation Inputs
- Provides dropdowns for selecting source and target languages, text areas for inputting text, and dropdowns for selecting avatar and background settings.
- Includes a button for triggering translation and video creation.

### Translation and Video Creation Logic
- Translates input text to the target language using the `translate_text` function.
- Creates a video from the translated text using the `create_video` function.
- Displays the success message and the video if the creation is successful, or an error message otherwise.

## For More Information
Check our [GitHub repository](https://github.com/ayranamo/mathshub-ai-avatars) for more information and updates.

## Example Usage
To see the script in action, you can run the `app.py` file and interact with the Streamlit application.



import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image
import os

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def get_gemini_response(prompt, image):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            prompt,
            image
        ]
    )

    return response.text


# Streamlit app
st.set_page_config(page_title="Calorie Advisor")

st.header("🍎 Calorie Advisor")

input_prompt = """
You are a food calorie advisor.

Analyze the food shown in the image.

Identify each food item and provide:

1. Food name
2. Estimated portion size
3. Estimated calories

Also provide:

- Total estimated calories
- Approximate protein
- Approximate carbohydrates
- Approximate fat

Keep the answer simple and easy to understand.

Important:
These values are estimates because the exact portion size,
ingredients, and cooking method cannot always be determined
from an image.
"""

uploaded_file = st.file_uploader(
    "Upload a food image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Food",
        use_container_width=True
    )

    if st.button("Calculate Calories"):

        with st.spinner("Analyzing food..."):

            response = get_gemini_response(
                input_prompt,
                image
            )

        st.subheader("🍽️ Calorie Analysis")

        st.write(response)


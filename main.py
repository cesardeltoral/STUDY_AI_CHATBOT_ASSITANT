import time
import os
import streamlit as st
from openai import OpenAI
from PIL import Image  # For handling image display

# streamlit run main.py 👉 to run the app

# to train your bot with specific data 👇
# https://platform.openai.com/assistants

# Enter your Assistant ID here.
ASSISTANT_ID = "enter_your_assistant_id"

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("enter_your_environmental_variable_with_openai_api_key"))

# Streamlit app UI
st.title("Study AI Chatbot")

# Load and display the image directly from the same directory
try:
    # Open the image file in the same directory
    image = Image.open("STUDY_AI_BOT.jpeg")
    # Display the image with a smaller width
    st.image(image, caption="", width=400)  # Adjust width as needed
except FileNotFoundError:
    st.write("⚠️ Image not found in the current directory. Please check the file name.")

st.write("Type your question below and get a response from the assistant!")

# Input field for the user's question
user_question = st.text_input("Your Question:")

# Submit button to send the question
if st.button("Ask"):
    # Only proceed if there is a question to submit
    if user_question.strip():
        # Create a thread with the user's question
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": user_question,
                }
            ]
        )

        # Submit the thread to the assistant (as a new run)
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
        st.write("🕐 Waiting for response...")

        # Wait for the run to complete
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            time.sleep(1)

        # Get the latest message from the thread
        message_response = client.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data

        # Check if there are any messages and get the content
        if messages:
            latest_message = messages[0]
            plain_text_response = latest_message.content[0].text.value
            st.write("💬 Assistant Response:", plain_text_response)
        else:
            st.write("⚠️ No response received from the assistant.")
    else:
        st.write("⚠️ Please enter a question to ask.")

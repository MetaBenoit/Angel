# The final Streamlit App with integrated router logic

import streamlit as st
# We now import the specialist functions directly from main.py
from main import query_local_model, query_gemini_model, generate_image

# --- App Configuration ---
st.set_page_config(
    page_title="HybridBrain Agent",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 HybridBrain Agent")

# --- Create tabs for different functionalities ---
tab1, tab2 = st.tabs(["💬 Chat (T2T)", "🖼️ Image Generation (T2I)"])

# --- Code for the Chat Tab ---
with tab1:
    st.header("Text-to-Text Conversation")
    
    # NEW: Add a toggle to let the user choose the model
    use_cloud_model = st.toggle("☁️ Use Cloud Model (Smarter, Slower)", value=False)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask the AI anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.spinner("AI is thinking..."):
            # ROUTER LOGIC is now here in the app
            if use_cloud_model:
                response = query_gemini_model(prompt)
            else:
                response = query_local_model(prompt)
        
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# --- Code for the Image Generation Tab ---
# In app.py, replace the "with tab2:" block

with tab2:
    st.header("Text-to-Image Generation")
    
    img_prompt = st.text_input("Enter a prompt to generate an image:", key="img_prompt")

    if st.button("Generate Image"):
        if img_prompt:
            with st.spinner("Generating image... this may take a minute."):
                response = generate_image(img_prompt)
                
                # Check if the response is an error string or actual image data (bytes)
                if isinstance(response, str):
                    st.error(response) # Display errors
                else:
                    st.image(response, caption=img_prompt, use_column_width=True)
        else:
            st.warning("Please enter a prompt for the image.")       
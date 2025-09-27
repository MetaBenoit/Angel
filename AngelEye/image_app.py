# The final Streamlit App for the "Angel" agent

import streamlit as st
from main import query_local_model, query_gemini_model, generate_image

# --- App Configuration ---
st.set_page_config(
    page_title="Angel Agent",
    page_icon="😇",
    layout="wide"
)

st.title("😇 Angel")
st.caption("Your private AI agent with a powerful cloud connection.")

# --- Create tabs for different functionalities ---
tab1, tab2 = st.tabs(["💬 Chat (T2T)", "🖼️ Image Generation (T2I)"])

# --- Code for the Chat Tab ---
with tab1:
    st.header("Text-to-Text Conversation")
    
    use_cloud_model = st.toggle("☁️ Use Cloud Model (Smarter, Slower)", value=False)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Angel anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Angel is thinking..."):
            if use_cloud_model:
                response = query_gemini_model(prompt)
            else:
                response = query_local_model(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# --- Code for the Image Generation Tab ---
with tab2:
    st.header("Text-to-Image Generation")
    
    img_prompt = st.text_input("Enter a prompt to generate an image:", key="img_prompt")

    if st.button("Generate Image"):
        if img_prompt:
            with st.spinner("Angel is creating an image..."):
                response = generate_image(img_prompt)
                
                if isinstance(response, str) and "https://" in response:
                    st.image(response, caption=img_prompt, use_column_width=True)
                else:
                    st.error(response)
        else:
            st.warning("Please enter a prompt for the image.")
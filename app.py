import streamlit as st
from datetime import datetime
import webbrowser
import wikipedia
import pytz
from typing import Optional

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

WEBSITES = {
    "youtube": "https://youtube.com",
    "github": "https://github.com",
    "google": "https://google.com",
    # Add more sites as needed
}

def say(text: str) -> None:
    """Cloud-compatible alternative to text-to-speech"""
    st.write(f"🔊: {text}")

def open_website(query: str) -> Optional[str]:
    query = query.lower()
    for site, url in WEBSITES.items():
        if f"open {site}" in query:
            webbrowser.open(url)
            return f"Opening {site.capitalize()}"
    return None

def main():
    st.set_page_config(page_title="JARVIS Assistant", layout="centered")
    st.title("🤖 JARVIS Assistant")
    
    if query := st.chat_input("Type your command..."):
        st.session_state.messages.append({"role": "user", "content": query})
        
        if response := open_website(query):
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.session_state.messages.append({"role": "assistant", "content": f"I heard: {query}"})
        
        say(response or f"Processed: {query}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if __name__ == "__main__":
    main()
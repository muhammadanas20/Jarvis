import streamlit as st
from datetime import datetime
import webbrowser
import pyttsx3
import wikipedia
import pytz
import requests
from typing import Optional

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'jarvis_active' not in st.session_state:
    st.session_state.jarvis_active = True

# Initialize TTS engine
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    TTS_ENABLED = True
except Exception as e:
    st.warning(f"Text-to-speech disabled: {str(e)}")
    TTS_ENABLED = False

def say(text: str) -> None:
    """Safe text-to-speech with error handling"""
    if not TTS_ENABLED:
        st.warning(f"(Text-to-speech would say: '{text}')")
        return
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")

# Enhanced website dictionary
WEBSITES = {
    "youtube": "https://youtube.com",
    "github": "https://github.com",
    "google": "https://google.com",
    # Add 30+ more sites as needed
    "netflix": "https://netflix.com",
    "spotify": "https://spotify.com",
    "wikipedia": "https://wikipedia.org"
}

def open_website(query: str) -> Optional[str]:
    """Handle website opening with improved matching"""
    query = query.lower()
    
    # Direct matches
    for site, url in WEBSITES.items():
        if f"open {site}" in query or f"go to {site}" in query:
            webbrowser.open(url)
            return f"Opening {site.capitalize()}"
    
    # Search handling
    if "search for" in query or "google" in query:
        search_term = query.replace("search for", "").replace("google", "").strip()
        if search_term:
            webbrowser.open(f"https://google.com/search?q={search_term}")
            return f"Searching for {search_term}"
    
    return None

def get_time() -> str:
    """Get formatted time with timezone"""
    tz = timezone('Asia/Kolkata')
    return datetime.now(tz).strftime("%I:%M %p")

def get_date() -> str:
    """Get formatted date"""
    return datetime.now().strftime("%A, %B %d, %Y")

def process_command(query: str) -> str:
    """Enhanced command processor"""
    if not query:
        return "I didn't catch that. Could you repeat please?"
    
    # Website handling
    if website_result := open_website(query):
        return website_result
    
    # Core commands
    query_lower = query.lower()
    if any(greet in query_lower for greet in ["hello", "hi", "hey"]):
        return "Hello! How may I assist you today?"
    
    elif "time" in query_lower:
        return f"The current time is {get_time()}"
    
    elif "date" in query_lower or "today" in query_lower:
        return f"Today is {get_date()}"
    
    elif any(bye in query_lower for bye in ["bye", "exit", "quit"]):
        st.session_state.jarvis_active = False
        return "Goodbye! Have a wonderful day."
    
    elif "wikipedia" in query_lower:
        try:
            term = query_lower.replace("wikipedia", "").strip()
            summary = wikipedia.summary(term, sentences=2)
            return f"According to Wikipedia: {summary}"
        except:
            return "I couldn't find that on Wikipedia."
    
    # Default response
    return f"I heard: '{query}'. How can I help with this?"

def main():
    st.set_page_config(
        page_title="JARVIS AI Assistant",
        page_icon="🤖",
        layout="centered"
    )
    
    st.title("🤖 JARVIS AI Assistant")
    st.write("Your digital assistant is ready to help!")
    
    # Sidebar with controls
    with st.sidebar:
        st.header("Control Panel")
        st.write("**Input Methods:**")
        input_method = st.radio(
            "Choose input:",
            ("Text", "Voice (if available)"),
            horizontal=True
        )
        
        st.write("**Common Commands:**")
        st.code("""
        - Open websites: "open youtube"
        - Search: "search for AI news"
        - Time/Date: "what time is it"
        - Wikipedia: "wikipedia Tesla"
        """)
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
        
        if not st.session_state.jarvis_active:
            if st.button("Activate JARVIS"):
                st.session_state.jarvis_active = True
                st.experimental_rerun()

    # Chat interface
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            st.caption(msg["time"])

    # Command processing
    if st.session_state.jarvis_active:
        if input_method == "Text":
            if query := st.chat_input("Type your command..."):
                handle_command(query)
        else:
            if st.button("🎤 Use Voice Command"):
                st.warning("Voice input requires local execution")
                # Implement voice logic here for local use
    else:
        st.warning("JARVIS is currently inactive")

def handle_command(query: str) -> None:
    """Process and display command results"""
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": query,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    
    # Process command
    response = process_command(query)
    
    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    
    # Speak response
    say(response)
    
    # Rerun to update UI
    st.experimental_rerun()

if __name__ == "__main__":
    main()
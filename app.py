import streamlit as st
import speech_recognition as sr
import webbrowser
from datetime import datetime
import pyttsx3
import os
import subprocess
import wikipedia
import wolframalpha
import requests
import json
from pytz import timezone

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'jarvis_active' not in st.session_state:
    st.session_state.jarvis_active = True

# Initialize speech engine once
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)  # Slightly slower speech rate
except Exception as e:
    st.error(f"Could not initialize text-to-speech engine: {str(e)}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=8)
            st.info("Recognizing...")
            try:
                query = r.recognize_google(audio, language='en-in')
                st.success(f"Recognized: {query}")
                return query.lower().strip()
            except sr.UnknownValueError:
                st.warning("Sorry, I couldn't understand what you said")
                return None
            except sr.RequestError:
                st.error("Speech recognition service unavailable")
                return None
        except sr.WaitTimeoutError:
            st.warning("No speech detected. Please try again")
            return None

def say(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")

def open_website(query):
    websites = {
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://twitter.com",
        "x": "https://twitter.com",
        "discord": "https://discord.com",
        "github": "https://github.com",
        "linkedin": "https://www.linkedin.com",
        "reddit": "https://www.reddit.com",
        "amazon": "https://www.amazon.com",
        "netflix": "https://www.netflix.com",
        "spotify": "https://www.spotify.com",
        "twitch": "https://www.twitch.tv",
        "pinterest": "https://www.pinterest.com",
        "whatsapp": "https://web.whatsapp.com",
        "gmail": "https://mail.google.com",
        "google": "https://www.google.com",
        "maps": "https://www.google.com/maps",
        "drive": "https://drive.google.com",
        "meet": "https://meet.google.com",
        "classroom": "https://classroom.google.com",
        "wikipedia": "https://www.wikipedia.org",
        "stackoverflow": "https://stackoverflow.com",
        "leetcode": "https://leetcode.com",
        "geeksforgeeks": "https://www.geeksforgeeks.org",
        "udemy": "https://www.udemy.com",
        "coursera": "https://www.coursera.org",
        "kaggle": "https://www.kaggle.com",
        "notion": "https://www.notion.so",
        "dropbox": "https://www.dropbox.com",
        "zoom": "https://zoom.us",
        "slack": "https://slack.com",
        "trello": "https://trello.com",
        "medium": "https://medium.com",
        "quora": "https://www.quora.com"
    }
    
    for site_name, url in websites.items():
        if site_name in query:
            st.success(f"Opening {site_name.capitalize()}")
            webbrowser.open(url)
            return f"Opening {site_name.capitalize()}"
            
    if "search for" in query or "google" in query:
        search_query = query.replace("search for", "").replace("google", "").strip()
        if search_query:
            st.success(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return f"Searching for {search_query}"
            
    return None

def get_time():
    now = datetime.now(timezone('Asia/Kolkata'))
    current_time = now.strftime("%I:%M %p")
    return f"The current time is {current_time}"

def get_date():
    today = datetime.now(timezone('Asia/Kolkata'))
    current_date = today.strftime("%A, %B %d, %Y")
    return f"Today is {current_date}"

def process_command(query):
    if not query:
        return "I didn't catch that. Could you repeat please?"
    
    # Website opening
    website_result = open_website(query)
    if website_result:
        return website_result
    
    # Basic commands
    if any(greet in query for greet in ["hello", "hi", "hey"]):
        return "Hello Sir, how can I assist you today?"
    
    elif "your name" in query:
        return "I am JARVIS, your virtual assistant."
    
    elif "time" in query:
        return get_time()
    
    elif "date" in query or "today" in query:
        return get_date()
    
    elif any(bye in query for bye in ["bye", "goodbye", "exit", "quit"]):
        st.session_state.jarvis_active = False
        return "Goodbye Sir. Have a nice day!"
    
    elif "wikipedia" in query:
        try:
            search_term = query.replace("wikipedia", "").strip()
            result = wikipedia.summary(search_term, sentences=2)
            return f"According to Wikipedia: {result}"
        except:
            return "Sorry, I couldn't find that on Wikipedia."
    
    elif "calculate" in query or "what is" in query and ("+" in query or "-" in query or "*" in query or "/" in query):
        try:
            calculation = query.replace("calculate", "").replace("what is", "").strip()
            result = eval(calculation)  # Caution: eval can be dangerous in production
            return f"The result is {result}"
        except:
            return "I couldn't perform that calculation."
    
    elif "weather" in query:
        return "I can check weather if you enable location services."
    
    # Default response
    return f"I heard: {query}. How may I assist you with this?"

def main():
    st.set_page_config(page_title="JARVIS AI Assistant", page_icon="🤖")
    
    st.title("🤖 JARVIS AI Assistant")
    st.write("Your personal voice-controlled assistant is ready to help!")
    
    # Sidebar with information
    with st.sidebar:
        st.header("Command Guide")
        st.write("Try these commands:")
        st.write("- Open websites: 'open youtube', 'go to github'")
        st.write("- Search: 'search for python tutorials', 'google streamlit docs'")
        st.write("- Information: 'what's the time', 'what day is today'")
        st.write("- Wikipedia: 'wikipedia artificial intelligence'")
        st.write("- Calculations: 'calculate 15 multiplied by 3'")
        st.write("- Conversation: 'hello jarvis', 'goodbye'")
        
        st.markdown("---")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.experimental_rerun()
        
        if st.button("Restart JARVIS"):
            st.session_state.jarvis_active = True
            st.experimental_rerun()

    # Chat container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                st.caption(message["time"])

    # Voice input button
    if st.session_state.jarvis_active:
        if st.button("🎤 Click to Speak", use_container_width=True):
            query = takeCommand()
            if query:
                # Add user message to chat
                st.session_state.messages.append({
                    "role": "user",
                    "content": query,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                
                # Process the command
                response = process_command(query)
                
                # Add assistant response to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                
                # Speak the response
                say(response)
                
                # Rerun to update the chat
                st.experimental_rerun()
    else:
        st.warning("JARVIS is currently inactive. Click 'Restart JARVIS' to continue.")

if __name__ == "__main__":
    main()
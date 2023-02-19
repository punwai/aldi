import json
import openai
import pyaudio
import socket
import speech_recognition as sr
import streamlit as st
import random

from prompt import PROMPT_BASE


# OpenAI settings
openai.api_key = None
MODEL = "text-davinci-003"


# audio recording
recognizer = sr.Recognizer()
mic = sr.Microphone()
st.session_state.text = ""

HOST = "169.254.224.133"
PORT = 65436

# send port message to listening socket
def send_port_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(json.dumps(message), 'utf-8'))
        # data = s.recv(1024)

    # print(f"Received {data!r}")

# call openAI api to prompt model
def extract_API_calls(command):
    prompt = PROMPT_BASE + command + "\n"

    response = openai.Completion.create(
    model=MODEL,
    prompt=prompt,
    max_tokens=60)

    commands = response["choices"][0]["text"]
    try:
        print(commands)
        commands = json.loads(commands)
        print(commands)
        # send_port_message(commands)
    except:
        print("GPT returned an invalid response")

    return parse_response_to_commands(commands)


# take in API call as a string and return list of strings
def parse_response_to_commands(response):
    commands = []
    # command_list = json.loads(response)
    # return command_list
    return response


### WEBSITE GUI ###
st.title("A.L.D.I. :brain:", anchor="Title")
st.text("Automata Language-based Dynamic Interpreter")

st.text("")
st.text("")

if st.button(label="record", key="record", type="primary"):
    with st.spinner('recording...'):
        with mic as source:
            audio = recognizer.listen(source, phrase_time_limit=5)
    
    text_from_audio = recognizer.recognize_google(audio)
    # if text_from_audio.split()[0] != "Jarvis":
    #     st.session_state.text = "error: did not detect command beginning with 'jarvis'"
    #     commands = None
        
    # else:
    st.session_state.text = text_from_audio
    commands = extract_API_calls(st.session_state.text)

    st.text("")
    st.text("")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("prompt: ")
        st.markdown(f"**{st.session_state.text}**")

    # st.text("")
    # st.text("")

    with col2:
        st.subheader("api calls: ")
        st.write(commands)
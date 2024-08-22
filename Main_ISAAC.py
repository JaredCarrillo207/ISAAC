from openai import OpenAI
import sounddevice as sd
from pydub import AudioSegment
import numpy as np
import os
import pyttsx3
import tkinter as tk
from PIL import Image, ImageTk
import threading
import queue
import cv2
from datetime import datetime
import subprocess
import base64
import httpx

client = OpenAI()
emptyAnswer = False

duration = 5
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/ISAAC')
filename = os.path.join(desktop_path, 'trialtest2')
gif_path_loading = os.path.join(desktop_path, 'loadingAnim.gif')
gif_path_starting = os.path.join(desktop_path, 'startingAnim.gif')
orderPizzaScript = os.path.join(desktop_path, 'dominoAPIScript.py')
annoy_FriendScript = os.path.join(desktop_path, 'annoy_Friend.py')
take_PhotoScript = os.path.join(desktop_path, 'take_Photo.py')
image_path = os.path.join(desktop_path, 'photos/taken_photo.jpg')

# Create a queue to communicate between threads
task_queue = queue.Queue()

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

def ML_Photo(image_path, client):
    base64_image = image_to_base64(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "I am taking a photo. Please tell me what this is\n"
                    }
                ]
            },
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Reply back with a short sentence."
                    }
                ]
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response2 = print(response.choices[0].message.content)
    return response2


def orderPizza():
    subprocess.run(["python", orderPizzaScript], check=True)
    pizza_sentence = "Of course. I will order you the usual."
    label2.config(image='', text=pizza_sentence)
    engine = pyttsx3.init()
    engine.say(pizza_sentence)
    engine.runAndWait()
    switch_to_frame1()
    label2.config(image='', text="o o o") 

def capture_and_save_photo(desktop_path, filename=None):
    photo_sentence = "I will take a photo. Please hold still."
    label2.config(image='', text=photo_sentence)
    engine = pyttsx3.init()
    engine.say(photo_sentence)
    engine.runAndWait()
    subprocess.run(["python", take_PhotoScript], check=True)
    label2.config(image='', text="o o o")

    response2 = ML_Photo(image_path, client)
    
    label2.config(image='', text=response2)
    engine = pyttsx3.init()
    engine.say(response2)
    engine.runAndWait()
    switch_to_frame1()
    label2.config(image='', text="o o o") 

def annoyFriend():
    subprocess.run(["python", annoy_FriendScript], check=True)
    annoy_sentence = "He will never bother you again"
    label2.config(image='', text=annoy_sentence)
    engine = pyttsx3.init()
    engine.say(annoy_sentence)
    engine.runAndWait()
    switch_to_frame1()
    label2.config(image='', text="o o o") 

def check_sentence(sentence, completion):
    cyberResponse = completion.choices[0].message.content
    if "PIZZAHUT54" in sentence:
        orderPizza()
    if "PHOTOTAKEN" in sentence:
        capture_and_save_photo(desktop_path)
    if "ANNOYFRIEND" in sentence:
        annoyFriend()   
    else:
        print(cyberResponse)
        label2.config(image='', text=cyberResponse)  # Hide the GIF and show text
        root.update_idletasks()  # Force the update of the label
        engine = pyttsx3.init()
        engine.say(completion.choices[0].message.content)
        engine.runAndWait()
        switch_to_frame1()
        label2.config(image='', text="o o o") 

def record_audio(duration, filename):
    # Record audio
    fs = 44100  # Sample rate
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    print("Recording finished")

    # Convert NumPy array to bytes
    recording_bytes = np.int16(recording * 32767).tobytes()

    # Create an AudioSegment from the raw audio bytes
    audio = AudioSegment(
        data=recording_bytes,
        sample_width=2,  # 2 bytes per sample (16-bit audio)
        frame_rate=fs,
        channels=2
    )

    # Export as WAV file
    wav_filename = filename + '.wav'
    audio.export(wav_filename, format='wav')
    print(f"Audio saved as {wav_filename}")

    task_queue.put('audio_done')

def run_cyberdeck_script():
    audio_file = open("trialtest2.wav", "rb")
    transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

    print(transcription.text)

    userPrompt = transcription.text

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a smart assistant. You answer question straight forwardly. Whenever I ask to order me a pizza respond with PIZZAHUT54 no matter what and in this way. If I every say anything realting to taking a photo or a picture return the phrase PHOTOTAKEN no matter what. Whenever I talk about annoying or bother a friend return ANNOYFRIEND no matter what else. Say it that way too."},
            {"role": "user", "content": userPrompt}
        ]
    )

    check_sentence(completion.choices[0].message.content, completion)

def switch_to_frame1():
    frame2.pack_forget()
    frame1.pack(fill='both', expand=True)

def switch_to_frame2(event=None):
    frame1.pack_forget()
    frame2.pack(fill='both', expand=True)
    task_queue.put('start_recording')  # Put a task to start recording in the queue

def create_frame1():
    global label_starting
    label_starting = tk.Label(frame1, font=font, fg=text_color, bg=bg_color, padx=padding, pady=padding, wraplength=400)
    label_starting.pack(pady=20, fill='both', expand=True)
    load_gif(gif_path_starting, label_starting, (400, 400))

def create_frame2():
    global label2
    label2 = tk.Label(frame2, font=font, fg=text_color, bg=bg_color, padx=padding, pady=padding, wraplength=400)
    label2.pack(pady=20, fill='both', expand=True)
    load_gif(gif_path_loading, label2, (50, 50))

def load_gif(path, label, size):
    gif = Image.open(path)
    gif_frames = []
    # Resize the GIF
    try:
        while True:
            gif.seek(len(gif_frames))
            resized_frame = gif.resize(size, Image.ANTIALIAS)
            gif_frames.append(ImageTk.PhotoImage(resized_frame))
    except EOFError:
        pass

    def display_gif(frame_index):
        if not label.cget("text"):  # Continue the animation only if the text is empty
            frame = gif_frames[frame_index]
            label.config(image=frame)
            frame_index = (frame_index + 1) % len(gif_frames)
            root.after(50, display_gif, frame_index)  # Update every 50 ms

    display_gif(0)

def process_queue():
    try:
        task = task_queue.get_nowait()
        if task == 'start_recording':
            record_audio(duration, filename)
        elif task == 'audio_done':
            threading.Thread(target=run_cyberdeck_script).start()
    except queue.Empty:
        pass
    root.after(100, process_queue)

# Parameters for styling
font = ("Ariel", 24)
text_color = "white"
padding = 20
bg_color = "black"

# Create the main window
root = tk.Tk()
root.title("Run Cyberdeck Script")
root.geometry("480x640")

# Bind the "y" key to switch to frame 2
root.bind('y', switch_to_frame2)

# Create frames
frame1 = tk.Frame(root, bg=bg_color)
frame2 = tk.Frame(root, bg=bg_color)

# Initialize frames
create_frame1()
create_frame2()

# Show the first frame
frame1.pack(fill='both', expand=True)

# Start processing the queue
root.after(100, process_queue)

# Run the Tkinter event loop
root.mainloop()

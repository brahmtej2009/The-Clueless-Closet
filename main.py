
# Pytterns is my own framework for creating terminal panels, and it is being used here for display!

# IN this project, we detect a user's clothes, match it with the weather, and give recommendations.
# I am a beginner dev, so the code is not very clean, but it works! I will be improving it over time. 

from pytterns import Pytterns
pt=Pytterns()

print("\033c", end="")
pt.panel(60,content=[""],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")
from colorama import Fore, Style
import time

print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.CYAN}Importing Libraries...","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")
import cv2
import requests
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from transformers import pipeline
import json
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry




print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.CYAN}Loading AI","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")

ai_model = pipeline("image-classification", model="google/vit-base-patch16-224")

print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.LIGHTRED_EX}Fetching Weather Data","Loading Data from settings.json file..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")

try:
    with open("settings.json", "r") as settings:
        data=json.load(settings)
except Exception as e:
    print("\033c", end="")
    pt.panel(60,content=[f"{Style.BRIGHT}{Fore.RED}ERROR FETCHING DATA","Please check the settings.json file!","Error is printed below for reference"],center=True,border_bold=True,padding=1, center_content=True,title=f"CRITICAL ERROR",color="RED")
    print(f"Error: {Style.BRIGHT}{Fore.RED}{e}")
    exit()
    


cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": data["latitude"],
	"longitude": data["longitude"],
    "timezone": "auto",
	"daily": ["rain_sum", "showers_sum", "snowfall_sum", "precipitation_sum", "precipitation_hours", "precipitation_probability_max", "uv_index_max", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max"],
	"forecast_days": 1,
}


responses = openmeteo.weather_api(url, params=params)  
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone: {response.Timezone()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
time.sleep(1)




print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.BLUE}Loading Camera","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")



global cam
cam=None
def setup_camera():
    
    #This sets up the cam, and also swaps it when retriggered.
    global cam
    print(cam)
    if cam==None:
        print("Loading Camera for first time on Default...")
        cam=0
        global cap
        cap = cv2.VideoCapture(cam, cv2.CAP_DSHOW) #This was AI's suggestion, this makes camera load much faster in windows through Direct Show.
        
    
    else:
        print(f"Switching Camera to {cam+1}...")
        cap.release()

        cap = cv2.VideoCapture(cam+1, cv2.CAP_DSHOW)
        cam+=1
            
        if not cap.isOpened():
            print("No more cameras found, switching back to default...")
            cap.release()
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cam=0


current_frame = None
setup_camera()





print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.YELLOW}DEFINING FUNCTIONS","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")

# This part was generated.
def newframe():
    global current_frame
    ret, frame = cap.read()
    if ret:
        current_frame = frame
        # Convert BGR (OpenCV) to RGB (Tkinter)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img).resize((600, 400))
        imgtk = ImageTk.PhotoImage(image=img)
        videofeed.imgtk = imgtk
        videofeed.configure(image=imgtk)
    window.after(10, newframe) # Repeat every 10ms

def checkimg():

    #Preparing the image for use with the AI, as it needs conversion. This is generated.
    img_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    
    a=ai_model(pil_img)
    lables = [p['label'].lower() for p in a]
    
    print(str(data["warm_stuff_top"]).lower())
    print(str(data["cool_stuff_top"]).lower())
    
    
    detected_warm = []
    detected_cool = []

    for p in a:
        label = p['label'].lower()
        # Check if any word in our list is part of the AI label
        if any(item.lower() in label for item in data["warm_stuff_top"]):
            detected_warm.append(label)
        elif any(item.lower() in label for item in data["cool_stuff_top"]):
            detected_cool.append(label)

    # 3. Decision Logic
    warm_top = len(detected_warm) > 0
    cool_top = len(detected_cool) > 0
            
    if warm_top: #We give priority to warm top, because you could have a Jacket and a shirt. Jacket is more important.
        cool_top=False

    result.delete(1.0, END)
    
    found_stuff = ", ".join(detected_warm + detected_cool)
    print(f"Detected Warm Items: {found_stuff}")
    if not found_stuff:
        result.insert(END, "AI Result: No recognized clothing detected.\nStand closer!")
    else:
        result.insert(END, f"AI Detected: {found_stuff}\nWarm Mode: {warm_top}\nCool Mode: {cool_top}")







print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.GREEN}Loading Window","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")

window = tk.Tk()
window.title("The Clueless Closet")
label = Label(window, text="Welcome to The Clueless Closet!", font=("Arial", 16)).pack()
#w= Frame(window, width=600, height=400).pack() This is a mistake, I thought I would need a frame to hold the video feed, but it is not necessary.
videofeed = tk.Label(window)
videofeed.pack()

result = Text(window, height=5, width=50)
result.pack()

cam_btn=tk.Button(window, text="Switch Camera", command=lambda:setup_camera())
cam_btn.pack()  

btn = tk.Button(window, text="SCAN", command=checkimg)
btn.pack()

newframe()
window.mainloop()


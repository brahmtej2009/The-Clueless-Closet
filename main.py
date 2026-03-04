
# Pytterns is my own framework for creating terminal panels, and it is being used here for display!

# IN this project, we detect a user's clothes, match it with the weather, and give recommendations.
# I am a beginner dev, so the code is not very clean, but it works! I will be improving it over time. 

from pytterns import Pytterns
pt=Pytterns()

# Disable this to turn off AI Loading and only load weather, this is for weather debugging
quick_launch=False

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
if not quick_launch:
    from transformers import pipeline
import json
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import torch



print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.CYAN}Loading AI","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")



# Auto-detect the best hardware
if torch.cuda.is_available():
    current_device = 0  # NVIDIA GPU
elif torch.backends.mps.is_available():
    current_device = "mps" # Apple Silicon
else:
    current_device = -1 # CPU
    
print(f"Using device: {current_device}")
time.sleep(2)
    
if not quick_launch:
    ai_model = pipeline("zero-shot-image-classification", model="patrickjohncyh/fashion-clip",device=current_device)

if not quick_launch:
    roastai = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct", device=current_device)

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

weather=response.Daily()

# RAIN
daily_rain_sum = int(weather.Variables(0).ValuesAsNumpy()[0])
daily_showers_sum = int(weather.Variables(1).ValuesAsNumpy()[0])
daily_snowfall_sum = int(weather.Variables(2).ValuesAsNumpy()[0])
daily_precipitation_sum = int(weather.Variables(3).ValuesAsNumpy()[0])
daily_precipitation_hours = int(weather.Variables(4).ValuesAsNumpy()[0])
daily_precipitation_probability_max = int(weather.Variables(5).ValuesAsNumpy()[0])
daily_uv_index_max = int(weather.Variables(6).ValuesAsNumpy()[0])
daily_temperature_2m_max = int(weather.Variables(7).ValuesAsNumpy()[0])
daily_temperature_2m_min = int(weather.Variables(8).ValuesAsNumpy()[0])
daily_apparent_temperature_max = int(weather.Variables(9).ValuesAsNumpy()[0])

global rain_possible
global snow_possible
rain_possible=daily_precipitation_probability_max > 50 or daily_precipitation_sum > 0 or daily_showers_sum > 0 or daily_rain_sum > 0 or daily_snowfall_sum > 0
snow_possible=daily_snowfall_sum > 0


#global heat_score
#heat_score=data["personal_temp"]
#heat_score+= (daily_temperature_2m_max+daily_apparent_temperature_max)/2 + daily_uv_index_max/2 # Logic I made, which kinda works good for my area. You can adjust it if needed.
#In Code below, we add 10 if warm clothes are detected, and subtract 10 if cool clothes are detected, this is to adjust the heat score based on what the user is wearing, so that the recommendation is more accurate. 


pt.panel(60,content=[f"{Style.BRIGHT}{Fore.BLUE}RAIN POSSIBLE: {rain_possible}", f"{Style.BRIGHT}{Fore.RED}HEAT SCORE: {0}",f"{Style.BRIGHT}{Fore.GREEN}SNOW POSSIBLE: {snow_possible}"],center=True,border_bold=True,padding=1, center_content=True,title=f"Processed Weather Status",color="Yellow")

print("Daily Rain Sum:", daily_rain_sum, type(daily_rain_sum),"\n Daily Showers Sum:",daily_showers_sum,type(daily_showers_sum),"\n Daily Snowfall Sum:",daily_snowfall_sum,type(daily_snowfall_sum),"\n Daily Precipitation Sum: ",daily_precipitation_sum,type(daily_precipitation_sum),"\n Daily Precipitation Hours:",daily_precipitation_hours,type(daily_precipitation_hours),"\n Daily Precipitation Probability Max:",daily_precipitation_probability_max,type(daily_precipitation_probability_max),"\n Daily UV Index Max:",daily_uv_index_max,type(daily_uv_index_max),"\n Daily Temperature 2m Max:",daily_temperature_2m_max,type(daily_temperature_2m_max),"\n Daily Temperature 2m Min:",daily_temperature_2m_min,type(daily_temperature_2m_min),"\n Daily Apparent Temperature Max:",daily_apparent_temperature_max,type(daily_apparent_temperature_max))
      #print(f"Temperature today: {response.Daily().Temperature2mMax()}°C max, {response.Daily().Temperature2mMin()}°C min")
time.sleep(10)

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
    window.after(40, newframe) # Repeat every 10ms
def checkimg():

    #Preparing the image for use with the AI, as it needs conversion. This is generated.
    img_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    
    
    if not quick_launch:
        top_raw=ai_model(pil_img, candidate_labels=data["warm_stuff_top"]+data["cool_stuff_top"], top_k=10)
        bottom_raw=ai_model(pil_img, candidate_labels=data["stuff_bottom"], top_k=10)
        additional_raw=ai_model(pil_img, candidate_labels=data["rain_stuff"]+data["snow_stuff"], top_k=10)

    else:
        exit("Quick Launch is enabled, AI is not loaded. Disable quick_launch to use AI features.")
    
    
    # In this model, the best result is the first one, and the score reduces thereafter.
    global best_guess
    
    global top
    top=[]
    for i in top_raw:
        if i['score'] > 0.25:  # Only include high-confidence predictions
            top.append(i["label"].lower())
    if len(top)==0:
        top=["AI Couldnt Detect Any Top"]
        
    global bottom
    bottom=[]
    for i in bottom_raw:
        if i['score'] > 0.35:  # Only include high-confidence predictions
            bottom.append(i["label"].lower())
    if len(bottom)==0:
        bottom=["User didnt show any lower clothing. Ignore"]
        
        
    global additional
    additional=[]
    for i in additional_raw:
        if i['score'] > 0.45:  # Only include high-confidence predictions
            additional.append(i["label"].lower())
            print(i["score"], i["label"])
    if len(additional)==0:
        additional=["No additional items, like raincoat or umbrella, were detected. No snow related items were detected either."]        
            
    
    print(f"Top Predictions: {top}")
    print(f"Bottom Predictions: {bottom}")
    print(f"Additional Predictions: {additional}")
    
    result.delete("1.0", END)
    result.insert(END, roast())
    
    """        

    warm_top = best_guess in data["warm_stuff_top"]
    cool_top = best_guess in data["cool_stuff_top"]
    stuff_bottom = best_guess in data["stuff_bottom"]
    rain_stuff = best_guess in data["rain_stuff"]
    
    
    print(f"AI Raw Output: {a}")
    print(str(data["warm_stuff_top"]).lower())
    print(str(data["cool_stuff_top"]).lower())
    
    
    detected_warm = []
    detected_cool = []
    raw_detected = []
    for p in a:
        label = p['label'].lower()
        raw_detected.append(label)
        # Check if any word in our list is part of the AI label
        if any(item.lower() in label for item in data["warm_stuff_top"]):
            detected_warm.append(label)
        elif any(item.lower() in label for item in data["cool_stuff_top"]):
            detected_cool.append(label)

    # 3. Decision Logic
    warm_top = len(detected_warm) > 0
    cool_top = len(detected_cool) > 0
    
    if warm_top>cool_top:
        cool_top=False
    elif cool_top>warm_top:
        warm_top=False
    else:
        warm_top=None
        cool_top=None
            
    if warm_top: #We give priority to warm top, because you could have a Jacket and a shirt. Jacket is more important.
        cool_top=False"""

def roast():
    top_str = ", ".join(top) if isinstance(top, list) else str(top)
    bottom_str = ", ".join(bottom) if isinstance(bottom, list) else str(bottom)
    add_str = "nothing" if "No additional items" in str(additional) else ", ".join(additional)

    print("\n\ntop_str:", top_str)
    print("bottom_str:", bottom_str)
    print("add_str:", add_str)
    # Short, punchy weather context
    weather_info = f"{daily_apparent_temperature_max}C, UV Index Score {daily_uv_index_max}, {daily_precipitation_probability_max}% rain."

    
   
    prompt = f"""<|im_start|>system
You are a toxic GenZ fashion bully. Your job is to analyze the user's fit against the weather. You have to be a critic, brutal, harsh, savage and dank. Use all kinds of words
Rules:
- Logic: If they wear a shirt in freezing cold or have no umbrella in rain, or are wearing a jacket in warm weather, shame them brutally. Roast and cook them without limits, be rude like a bully.
- If the fit makes sense for the weather, sarcastically roast their fit BRUTALLY.
- Be brutal, Shame them if their fit does not match their weather. If they dont have the right gear for the weather, Include extra sentence to Extra Shame on that. 
- NO poetic metaphors. Max 3 Brief SHORT sentences. DO not exceed word limit of 60. No Censorship. Simple Human Brutal English, Shame and Insult me.<|im_end|>
<|im_start|>user
Example: You are seriously soo dumb, that you think wearing a thin shirt is going to protect you from the literall snow gods outside. GO IN YOUR WARDROBE AND WEAR SOMETHING WARM! Or you would become a part of someone's Icecream<|im_end|>

WEATHER: {weather_info}
FIT: {top_str} (top), {bottom_str} (bottom), {add_str} (extras).
Personal Temp: {data["personal_temp"]} This number shows: Lower the number, less temperature I like. Higher the number, more heat I like. default 0
Example: You are seriously soo dumb, that you think wearing a thin shirt is going to protect you from the literall snow gods outside. GO IN YOUR WARDROBE AND WEAR SOMETHING WARM! Or you would become a part of someone's Icecream<|im_end|>

Roast me based on the weather:<|im_end|>
<|im_start|>assistant\n"""

    # All the parameters here are complete hit and try for me. If some other value works better here, please let me know.
    output = roastai(prompt, 
        max_new_tokens=70, 
        do_sample=True, 
        temperature=1.2, # 
        top_p=0.9,
        return_full_text=False,
        pad_token_id=roastai.tokenizer.eos_token_id)
    return "You are seriously soo dumb, that you think wearing a thin shirt is going to protect you from the literall snow gods outside. GO IN YOUR WARDROBE AND WEAR SOMETHING WARM! Or you would become a part of someone's Icecream"
#    return output[0]['generated_text'].strip()



print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.GREEN}Loading Window","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")

window = tk.Tk()
window.title("The Clueless Closet")
window.geometry("900x850")

label = Label(window, text="Welcome to The Clueless Closet!", font=("Arial", 16)).pack()
#w= Frame(window, width=600, height=400).pack() This is a mistake, I thought I would need a frame to hold the video feed, but it is not necessary.
videofeed = tk.Label(window)
videofeed.pack()

result = Text(window, height=10, width=100)
result.pack()

cam_btn=tk.Button(window, text="Switch Camera", command=lambda:setup_camera())
cam_btn.pack()  

btn = tk.Button(window, text="SCAN", command=lambda: checkimg())
btn.pack()

newframe()
window.mainloop()


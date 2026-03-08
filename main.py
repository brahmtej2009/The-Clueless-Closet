
# Pytterns is my own framework for creating terminal panels, and it is being used here for display!

# IN this project, we detect a user's clothes, match it with the weather, and give recommendations.
# I am a beginner dev, so the code is not very clean, but it works! I will be improving it over time. 


# The places where AI was used for code generation, are marked with #NOTE:AI tag.

from pytterns import Pytterns
pt=Pytterns()

# AI takes a lot of time to load, so while development, I just toggle this and it skips AI Loading. So I can see the interface asap.
quick_launch=False
CPU_only=False


# You would see this code a lot of times here. This renders that good looking panel which comes in the terminal once you run this project
print("\033c", end="")
pt.panel(60,content=[""],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")

# From here we start importing core dependencies 
from colorama import Fore, Style
import time

# Display the Importing Libraries Panel
print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.CYAN}Importing Libraries...","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")

#Import the libraries
import cv2
import requests
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
# This is here because pipeline takes a long time to import, so to speed up development, I toggle it from above
if not quick_launch:
    from transformers import pipeline,GenerationConfig
import json
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import torch
import os
import threading
import personalities

# I had issue when running the code through cmd, as the Path there was the default windows one.. We have to change it to current dir for it to load files from here.
os.chdir(os.path.dirname(os.path.abspath(__file__))) #Found this from the internet, which is used as a common fix for this issue.


# Everything is now imported, we load the AI
print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.CYAN}Loading AI","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")



# As we know, AI works better on GPU. Before this project was complete CPU based, which made it quite slow.
# This automatically checks for Nvidia/Apple hardware, if not found, then goes to CPU processing.

if CPU_only:
    current_device=-1
elif torch.cuda.is_available():
    current_device = 0  # NVIDIA GPU
elif torch.backends.mps.is_available():
    current_device = "mps" # Apple Silicon
else:
    current_device = -1 # CPU

    
    
#Quick launch toggle prevents AI from Loading here.
if not quick_launch:
    #This is the AI which scans ur clothes and converts it to words
    ai_model = pipeline("zero-shot-image-classification", model="patrickjohncyh/fashion-clip",device=current_device)

if not quick_launch:
    # This Ai takes the words and weather data and makes roasts outa that
    if current_device == -1:
        # device doesnt have a GPU, so run a smaller model on CPU
        roastai = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct", device=current_device)
        pt.panel(60,content=[f"{Style.BRIGHT}{Fore.RED}NO SUPPORTED GPU DETECTED","Fallbacking to Low Performance AI"],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")
        time.sleep(10)
    else:
        pt.panel(60,content=[f"{Style.BRIGHT}{Fore.BLUE}Compatible GPU Detected..","Launching best performing AI Model.","If this is the first time,","Please wait for AI To download.","It will take ~10 Minutes"],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")
        roastai = pipeline("text-generation", model="unsloth/Hermes-3-Llama-3.1-8B-bnb-4bit", device=current_device)

     


# Fetch weather now
print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.LIGHTRED_EX}Fetching Weather Data","Loading Data from settings.json file..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")

# Load settings file from current directory. 
try:
    with open("settings.json", "r") as settings:
        global data
        data=json.load(settings)
except Exception as e:
    print("\033c", end="")
    pt.panel(60,content=[f"{Style.BRIGHT}{Fore.RED}ERROR FETCHING DATA","Please check the settings.json file!","Error is printed below for reference"],center=True,border_bold=True,padding=1, center_content=True,title=f"CRITICAL ERROR",color="RED")
    print(f"Error: {Style.BRIGHT}{Fore.RED}{e}")
    exit()

# This code was fetched from Open-Meteo's official documentation, It retries if the fetch failed, so the code doesnt crash.
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

#Here we display the stuff we got back from the API in the terminal, for dev use.
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone: {response.Timezone()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

weather=response.Daily()

# This is all the stuff which is fetched
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

# Now we make the stuff which we are going to use in functions Global. I know its not a good practice, but if it works, we dont touch that again.
global rain_possible
global snow_possible

# This gives us a basic True or False for rain possibility, works quite good.
rain_possible=daily_precipitation_probability_max > 50 or daily_precipitation_sum > 0 or daily_showers_sum > 0 or daily_rain_sum > 0 or daily_snowfall_sum > 0
snow_possible=daily_snowfall_sum > 0

# This displays the final processed information in the terminal as a proper panele.
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.BLUE}RAIN POSSIBLE: {rain_possible}",f"{Style.BRIGHT}{Fore.GREEN}SNOW POSSIBLE: {snow_possible}"],center=True,border_bold=True,padding=1, center_content=True,title=f"Processed Weather Status",color="Yellow")

print("Daily Rain Sum:", daily_rain_sum, type(daily_rain_sum),"\n Daily Showers Sum:",daily_showers_sum,type(daily_showers_sum),"\n Daily Snowfall Sum:",daily_snowfall_sum,type(daily_snowfall_sum),"\n Daily Precipitation Sum: ",daily_precipitation_sum,type(daily_precipitation_sum),"\n Daily Precipitation Hours:",daily_precipitation_hours,type(daily_precipitation_hours),"\n Daily Precipitation Probability Max:",daily_precipitation_probability_max,type(daily_precipitation_probability_max),"\n Daily UV Index Max:",daily_uv_index_max,type(daily_uv_index_max),"\n Daily Temperature 2m Max:",daily_temperature_2m_max,type(daily_temperature_2m_max),"\n Daily Temperature 2m Min:",daily_temperature_2m_min,type(daily_temperature_2m_min),"\n Daily Apparent Temperature Max:",daily_apparent_temperature_max,type(daily_apparent_temperature_max))


# Now we load camera
print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.BLUE}Loading Camera","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")

# Make camera a global, as it is used at a lot of places.
global cam
cam=None

# This function starts the camera on the default ID (0) on its first run. Then when triggered again, it changes the camera till the time it cycles back to the default one.

def setup_camera():
    
    #This sets up the cam, and also swaps it when retriggered.
    global cam


    if cam==None:
        cam=0
        global cap
        cap = cv2.VideoCapture(cam, cv2.CAP_DSHOW) #This was AI's suggestion, this makes camera load much faster in windows through Direct Show.
        
    
    else:
#        print(f"Switching Camera to {cam+1}...")
        cap.release()

        cap = cv2.VideoCapture(cam+1, cv2.CAP_DSHOW)
        cam+=1
            
        if not cap.isOpened():
#            print("No more cameras found, switching back to default...")
            cap.release()
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cam=0
            
current_frame = None

last_scanned_img = None
setup_camera()

# Now we define all the functions which work inter-relatedly to make everything work.
print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.YELLOW}DEFINING FUNCTIONS","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")


# NOTE: AI
# The function below used AI code generation due to its complexity.
def newframe():
    global current_frame
    ret, frame = cap.read()
    if ret:
        current_frame = frame
        # OPENCV USES BGR which needs to be converted to RGB for use with tkinter.. Else it wont work
        global img
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#        img = Image.fromarray(img).resize((600, 400)) # I realized i didnt need this later.. it works better without this.
        
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        videofeed.imgtk = imgtk
        videofeed.configure(image=imgtk)
    window.after(40, newframe) # This repeats every 40 ms, giving us that smooth video feel.
    
    
def multi_threaded_scan():
    if not quick_launch:
        btn.config(state=tk.DISABLED, text="Processing...")
        threading.Thread(target=checkimg, daemon=True).start()
    else:
        messagebox.showinfo("QuickLaunch Enabled","Quicklaunch is enabled. Please disable it to use AI Features.")
    
#NOTE: AI
# AI generated a few parts of the following function. I used it to remove all bugs.
def checkimg():
    #Preparing the image for use with the AI, as it needs conversion. This is generated.
    img_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    global last_scanned_img
    last_scanned_img = img.copy()
    
    
    if not quick_launch:
        # We scan 3 times, for top, bottom and additional stuff, to make scores for everything
        top_raw=ai_model(pil_img, candidate_labels=data["warm_stuff_top"]+data["cool_stuff_top"], top_k=10)
        bottom_raw=ai_model(pil_img, candidate_labels=data["stuff_bottom"], top_k=10)
        additional_raw=ai_model(pil_img, candidate_labels=data["rain_stuff"]+data["snow_stuff"], top_k=10)

    else:
        # For the quick launch we did above, we exit the code here if it was enabled..
        exit("Quick Launch is enabled, AI is not loaded. Disable quick_launch to use AI features.")
    
    
    # In this model, the best result is the first one, and the score reduces as we go to the right.
    global best_guess
    global top
    top=[]
    # Here we just take the raw data, and filter the ones who the AI is confident about, and only include those.
    for i in top_raw:
        if i['score'] > 0.35:  # Only include high-confidence predictions
            top.append(i["label"].lower())
    if len(top)==0 or "nothing" in top:
        top=["AI Couldnt Detect Any Top"]
        
        
    # Same here as above, filter stuff which AI is confident about
    global bottom
    bottom=[]
    for i in bottom_raw:
        if i['score'] > 0.45:  # Only include high-confidence predictions
            bottom.append(i["label"].lower())
    if len(bottom)==0 or "no lower clothing visible" in bottom:
        bottom=["User didnt show any lower clothing."]
        
    
    # Same here, filter stuff which AI is confident about, for additional items like umbrella or snow gear and stuff    
    global additional
    additional=[]
    for i in additional_raw:
        if i['score'] > 0.6:  # Only include high-confidence predictions
            additional.append(i["label"].lower())
#            print(i["score"], i["label"])
    if len(additional)==0 or "nothing" in additional:
        additional=["No additional items, like raincoat or umbrella, were detected. No snow protection related items were detected either."]        
            

    global airoastresp
    airoastresp = roast()
    update_display(airoastresp)
    btn.config(state=tk.NORMAL, text="SCAN FIT")
    save_fit.config(state=NORMAL)
    


def diary_log():
    
    # Here, we make a snapshot of the user, with the roast, and this is like a track record of all the roasts.
    
    img_width, img_height = last_scanned_img.size
    
    try:
        cnfg=ImageFont.truetype(data["font_file"], size=data["font_size"])
    except:
        cnfg=ImageFont.load_default()
        
    margin = data["font_margin"]
    max_text_width = img_width - 2 * margin
    
        
    # NOTE: AI was used for this function for proper rendering of text
    def wrap_text(text, width, font):
        lines = []
        for paragraph in text.split('\n'):
            words = paragraph.split()
            while words:
                line = ''
                while words and font.getbbox(line + words[0])[2] <= width:
                    line += (words.pop(0) + ' ')
                lines.append(line.strip())
        return lines

    # AI helped in all this:
    wrapped_lines = wrap_text(airoastresp, max_text_width, cnfg)

    line_height = cnfg.getbbox("hg")[3] - cnfg.getbbox("hg")[1]
    text_height = len(wrapped_lines) * line_height + 2 * margin 
    new_img_height = img_height + text_height

    new_img = Image.new("RGB", (img_width, new_img_height), tuple(data["txt_bg"]))
    new_img.paste(last_scanned_img, (0, text_height))
    
    # This function was made by help from AI. Due to its complexity.
    draw = ImageDraw.Draw(new_img)
    y_position = margin 
    for line in wrapped_lines:
        text_width = cnfg.getbbox(line)[2] - cnfg.getbbox(line)[0]
        x_position = (img_width - text_width) // 2
        draw.text((x_position, y_position), line, fill=tuple(data["txt_color"]), font=cnfg)
        y_position += line_height
        
        
        
    # I'll ad timestamps to the images so name is never the same.Ig this is also good for diary as it keeps a track of time too.
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    new_filename = f"diary/fit_{timestamp}.jpg"
    if not os.path.exists("diary"):
        os.makedirs("diary")
    
    # Save the image in the diary folder. (Automatically generated if not present by default)
    new_img.save(new_filename)  
    
    messagebox.showinfo("Success", "Snapshot Saved!")
    

def update_display(roast_text):
    # This function is AI Generated to combine properly with my code and the AI generated UI
    # Update Detections
    detect_box.config(state=NORMAL)
    detect_box.delete("1.0", END)
    detect_box.insert(END, f"TOP: {', '.join(top)}\nBOTTOM: {', '.join(bottom)}\nEXTRAS: {', '.join(additional)}")
    detect_box.config(state=DISABLED)
    
    # Update Roast
    result.config(state=NORMAL)
    result.delete("1.0", END)
    result.insert(END, roast_text)
    result.config(state=DISABLED)


def roast():
    
    # We convert the lists to string for proper rendering here. And pass that as a paragraph to an AI, which then makes the roast for us!
    
    top_str = ", ".join(top) if isinstance(top, list) else str(top)
    bottom_str = ", ".join(bottom) if isinstance(bottom, list) else str(bottom)
    add_str = "nothing" if "No additional items" in str(additional) else ", ".join(additional)
    occasion_str=occasion.get()
 
    
    weather_info = f"{daily_apparent_temperature_max}C, UV Index Score {daily_uv_index_max}, {daily_precipitation_probability_max}% rain."

    WI=f"""<|im_start|>user
WEATHER: {weather_info}
FIT: {top_str} (top), {bottom_str} (bottom), {add_str} (extras).
Personal Temp Pref: {data["personal_temp"]} (Lower=likes cold, Higher=likes heat)
Occasion: {occasion_str}
<|im_end|>
<|im_start|>assistant\n"""

    personality=personalities.SYSTEM_PROMPTS[data["personality"]][0]
    
    prompt=personality+WI
    # All the parameters here are complete hit and try for me. If some other value works better here, please let me know.
    roast_config = GenerationConfig(
    max_new_tokens=250,
    do_sample=True,
    temperature=0.6,
    top_p=0.95,
    top_k=50,
    repetition_penalty=1.1,
    pad_token_id=roastai.tokenizer.eos_token_id)
    
    output = roastai(prompt, generation_config=roast_config,return_full_text=False)

    
    # I faced issue that AI generated a lot of text and got cut off due to the token limit. So i made this so it only takes the sentence completion, and doesnt show the extra text.
    #NOTE:This is a very basic BETA method.
    text = output[0]['generated_text'].strip()
    
    last_dot_index = text.rfind('.')

    if last_dot_index != -1:
        clean_text = text[:last_dot_index + 1]
    else:
        clean_text = text
    
    return clean_text


print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.GREEN}Loading Window","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")


#NOTE: AI
# AI was used to generate most of the Tkinter UI as it was a very complicated process to nicely fit buttons, camera feed and sidebar in the UI.

window = tk.Tk()
window.title("The Clueless Closet")
window.configure(bg="#f0f0f0")
window.state('zoomed')

# Centering Logic: Give weights to columns/rows so they expand and center the content
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(1, weight=1)

try:
    # Scale image to a large resolution to "stretch" it across the screen
    load_img = Image.open(personalities.SYSTEM_PROMPTS[data["personality"]][1]).resize((1920, 1080))
    bg_image = ImageTk.PhotoImage(load_img)
except Exception:
    bg_image = tk.PhotoImage(file=personalities.SYSTEM_PROMPTS[data["personality"]][1])

# Background fits the window via relwidth/relheight
background_label = tk.Label(window, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = bg_image

# --- STYLISH HEADER ---
header = tk.Label(window, text="✦ Welcome to The Clueless Closet! ✦", 
                  font=("Arial", 26, "bold"), fg="white", 
                  bg="#1a1a1a", padx=30, pady=15, 
                  relief="solid", borderwidth=3)
header.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

# Mode Indicator (Floating top right) - Modern badge
mode_text = f"{str(data['personality']).upper()} MODE"
mode_lbl = tk.Label(window, text=mode_text, font=("Arial", 16, "bold"), 
                    fg="white", bg="#ff4757", padx=20, pady=8, 
                    relief="solid", borderwidth=2)
mode_lbl.place(relx=0.98, rely=0.03, anchor="ne")

# --- LEFT COLUMN (Camera & Buttons) ---
left_frame = tk.Frame(window, bg="") 
left_frame.grid(row=1, column=0, sticky="nsew", padx=(40, 15), pady=(0, 25))

# Inner Grid Configuration for Left Frame
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_rowconfigure(1, weight=0)
left_frame.grid_columnconfigure(0, weight=1)

# Video Feed with modern styling
videofeed = tk.Label(left_frame, bg="#111111", relief="solid", borderwidth=3) 
videofeed.grid(row=0, column=0, sticky="nsew", pady=15, padx=10)

# Button Frame - FIXED stable structure
btn_frame = tk.Frame(left_frame, bg="#f8f9fa", height=70, relief="solid", borderwidth=1)
btn_frame.grid(row=1, column=0, pady=15, sticky="ew")
btn_frame.grid_propagate(False)
btn_frame.grid_rowconfigure(0, weight=0)
btn_frame.grid_columnconfigure(0, weight=1)

# Button container
btn_container = tk.Frame(btn_frame, bg="#f8f9fa")
btn_container.grid(row=0, column=0, sticky="nsew", padx=25, pady=12)
btn_container.grid_rowconfigure(0, weight=0)
btn_container.grid_columnconfigure(0, weight=0)

# STYLISH STABLE BUTTONS with icons
cam_btn = tk.Button(btn_container, text="🎥 Switch Camera", 
                    command=lambda: setup_camera(),
                    bg="#ff9500", fg="white", activebackground="#ff9500", 
                    activeforeground="white", font=("Arial", 12, "bold"), 
                    padx=20, pady=10, width=14,
                    relief="flat", bd=0, highlightthickness=0,
                    takefocus=False)
cam_btn.pack(side=tk.LEFT, padx=(12, 6))

btn = tk.Button(btn_container, text="🔍 SCAN FIT", 
                command=multi_threaded_scan,
                bg="#2ecc71", fg="white", activebackground="#2ecc71", 
                activeforeground="white", font=("Arial", 12, "bold"), 
                padx=25, pady=10, width=12,
                relief="flat", bd=0, highlightthickness=0,
                takefocus=False)
btn.pack(side=tk.LEFT, padx=6)

save_fit = tk.Button(btn_container, text="📸 Snapshot", 
                     command=lambda: diary_log(),
                     bg="#5d00ff", fg="white", activebackground="#5d00ff", 
                     activeforeground="white", font=("Arial", 12, "bold"), 
                     padx=20, pady=10, width=12,
                     relief="flat", bd=0, highlightthickness=0,
                     state=tk.DISABLED, takefocus=False)
save_fit.pack(side=tk.LEFT, padx=(6, 12))

# --- RIGHT COLUMN (STYLISH Sidebar) ---
sidebar = tk.Frame(window, bg="white", relief="solid", bd=3, padx=25, pady=25)
sidebar.grid(row=1, column=1, sticky="ne", padx=(15, 40), pady=(15, 25))

# Occasion - Modern styling
tk.Label(sidebar, text="🎯 Occasion", font=("Arial", 12, "bold"), 
         fg="#2c3e50", bg="white").pack(anchor="w", pady=(0, 8))
occasion = tk.Entry(sidebar, width=32, font=("Arial", 11), 
                    relief="solid", bd=2, bg="#f8f9fa")
occasion.pack(anchor="w", pady=(0, 20), ipady=8)

# Weather Display - Modern card
tk.Label(sidebar, text="🌤️ Conditions", font=("Arial", 12, "bold"), 
         fg="#34495e", bg="white").pack(anchor="w", pady=(0, 8))
weather_frame = tk.Frame(sidebar, bg="#e8f8f5", relief="solid", bd=2)
weather_frame.pack(anchor="w", pady=(0, 20), fill="x")
weather_lbl = tk.Label(weather_frame, 
                       text=f"Temperature: {daily_apparent_temperature_max}°C  |  Rain: {daily_precipitation_probability_max}%", 
                       font=("Arial", 12, "bold"), fg="#2c3e50", 
                       bg="#e8f8f5", padx=20, pady=12)
weather_lbl.pack(anchor="w")

# Detections Section - Modern styling
tk.Label(sidebar, text="👕 Detected Clothing", font=("Arial", 12, "bold"), 
         fg="#34495e", bg="white").pack(anchor="w", pady=(0, 8))
detect_box = tk.Text(sidebar, height=7, width=42, font=("Consolas", 11, "bold"), 
                     state=tk.DISABLED, relief="solid", bd=2, 
                     bg="#f8f9fa", fg="#2c3e50")
detect_box.pack(pady=10, fill="x")

# Results Section - Modern styling
tk.Label(sidebar, text="💬 Results", font=("Arial", 12, "bold"), 
         fg="#2c3e50", bg="white").pack(anchor="w", pady=(20, 8))
result = tk.Text(sidebar, height=11, width=42, font=("Arial", 11, "italic"), 
                 wrap=tk.WORD, state=tk.DISABLED, 
                 bg="#fff5f7", fg="#4a4a4a", relief="solid", bd=2)
result.pack(pady=10, fill="x")

newframe()
print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.GREEN}Started...","Please open the Launched Window..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Cyan")

window.mainloop()


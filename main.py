
# Pytterns is my own framework for creating terminal panels, and it is being used here for display!

# IN this project, we detect a user's clothes, match it with the weather, and give recommendations.
# I am a beginner dev, so the code is not very clean, but it works! I will be improving it over time. 


from pytterns import Pytterns
pt=Pytterns()

# AI takes a lot of time to load, so while development, I just toggle this and it skips AI Loading. So I can see the interface asap.
quick_launch=False


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

# I had issue when running the code through cmd, as the Path there was the default windows one.. We have to change it to current dir for it to load files from here.
os.chdir(os.path.dirname(os.path.abspath(__file__))) #Found this from the internet, which is used as a common fix for this issue.


# Everything is now imported, we load the AI
print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.CYAN}Loading AI","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")



# As we know, AI works better on GPU. Before this project was complete CPU based, which made it quite slow.
# This automatically checks for Nvidia/Apple hardware, if not found, then goes to CPU processing.

# I did have some issues with my GPU, Nvidia GTX 1650, with torch. To make it work you need the latest drivers from Nvidia App
if torch.cuda.is_available():
    current_device = 0  # NVIDIA GPU
elif torch.backends.mps.is_available():
    current_device = "mps" # Apple Silicon
else:
    current_device = -1 # CPU
    
#print(f"Using device: {current_device}")
#time.sleep(2)
    
    
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

# This is all the stuff which is fetched, It gets displayed in terminal for short time.
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


# THE heat score logic below is retired, that didnt work as well.

#global heat_score
#heat_score=data["personal_temp"]
#heat_score+= (daily_temperature_2m_max+daily_apparent_temperature_max)/2 + daily_uv_index_max/2 # Logic I made, which kinda works good for my area. You can adjust it if needed.
#In Code below, we add 10 if warm clothes are detected, and subtract 10 if cool clothes are detected, this is to adjust the heat score based on what the user is wearing, so that the recommendation is more accurate. 



# This displays the final processed information in the terminal as a proper panele.
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.BLUE}RAIN POSSIBLE: {rain_possible}",f"{Style.BRIGHT}{Fore.GREEN}SNOW POSSIBLE: {snow_possible}"],center=True,border_bold=True,padding=1, center_content=True,title=f"Processed Weather Status",color="Yellow")

print("Daily Rain Sum:", daily_rain_sum, type(daily_rain_sum),"\n Daily Showers Sum:",daily_showers_sum,type(daily_showers_sum),"\n Daily Snowfall Sum:",daily_snowfall_sum,type(daily_snowfall_sum),"\n Daily Precipitation Sum: ",daily_precipitation_sum,type(daily_precipitation_sum),"\n Daily Precipitation Hours:",daily_precipitation_hours,type(daily_precipitation_hours),"\n Daily Precipitation Probability Max:",daily_precipitation_probability_max,type(daily_precipitation_probability_max),"\n Daily UV Index Max:",daily_uv_index_max,type(daily_uv_index_max),"\n Daily Temperature 2m Max:",daily_temperature_2m_max,type(daily_temperature_2m_max),"\n Daily Temperature 2m Min:",daily_temperature_2m_min,type(daily_temperature_2m_min),"\n Daily Apparent Temperature Max:",daily_apparent_temperature_max,type(daily_apparent_temperature_max))


# We give some time for the person to read this stuff, 3 seconds is enough to kill code at that spot and read it properly.
time.sleep(3)


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
 #   print(cam)
    if cam==None:
#        print("Loading Camera for first time on Default...")
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


# NOTE: This function was AI generated due to its complexity.
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
    btn.config(state=tk.DISABLED, text="Processing...")
    threading.Thread(target=checkimg, daemon=True).start()
    
# This is the actual code which checks the frame with the AI and generates everything.
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
            

    
    # This prints the stuff out for debug. 
    
    #print(f"Top Predictions: {top}")
    # #print(f"Bottom Predictions: {bottom}")
    # #print(f"Additional Predictions: {additional}")
    # 
    # 
    #     
    #Once the image is processed, we have to enable the snapshot button so we can save
    # (It was disabled at boot)
    
    
    # This is the AI's roast response, which is given from the roast function below. then we update the panel with that roast.

    global airoastresp
    airoastresp = roast()
    update_display(airoastresp)
    btn.config(state=tk.NORMAL, text="SCAN FIT")
    save_fit.config(state=NORMAL)
    
    
    # This code below was removed because the roast method was changed from static to dynamic ai generated
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

# No need for this as its now being shown in tkinter:
#    print("\n\ntop_str:", top_str)
#    print("bottom_str:", bottom_str)
#    print("add_str:", add_str)
    
    
    weather_info = f"{daily_apparent_temperature_max}C, UV Index Score {daily_uv_index_max}, {daily_precipitation_probability_max}% rain."

    # This is the paragraph given to AI, i know its a bit rough, but it gets the work done.
    



    prompt = f"""<|im_start|>system
You are a toxic GenZ fashion bully. Analyze the user's fit vs the weather.
Rules:
- Style: Brutal, GenZ slang, hater energy. No poetic metaphors.
- Logic: If fit vs weather is a fail, max aggression. If it matches, roast the style sarcastically.
- Constraint: Max 2 sentences. No yapping. Stop immediately.
- Generation: You have to roast ME. Not my items. Roast like a human bully would tease me.
- Censorship: No Rudeness Filter
<|im_end|>

<|im_start|>user
WEATHER: 2C, UV Index 1, 80% rain.
FIT: T-shirt (top), Mesh Shorts (bottom), Slippers (extras).
Personal Temp: -5
Occasion: School
Example Output:You're so cold, even your common sense has frostbite. You are here like its a beach day, you absolute clown. Cover Yourself!
<|im_end|>

<|im_start|>user
WEATHER: {weather_info}
FIT: {top_str} (top), {bottom_str} (bottom), {add_str} (extras).
Personal Temp Pref: {data["personal_temp"]} (Lower=likes cold, Higher=likes heat)
Occasion: {occasion_str}
<|im_end|>
<|im_start|>assistant\n"""
    
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


# Now, everything is done, tkinter launches now and everything comes together!
print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.GREEN}Loading Window","Please wait..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Yellow")


# AI was used to generate the code below to make a good looking colorful and modern UI

window = tk.Tk()
window.title("The Clueless Closet")
# This is not needed, but if user wishes, he can turn uncomment this and set values to make a custom sized window
#window.geometry("1100x700"))
window.configure(bg="#f0f0f0")

# --- MAIN LAYOUT ---
# Header
header = tk.Label(window, text="Welcome to The Clueless Closet!", font=("Helvetica", 24, "bold"), bg="#f0f0f0", pady=10)
header.grid(row=0, column=0, columnspan=2)

# Left Frame (Video & Buttons)
left_frame = tk.Frame(window, bg="#f0f0f0", padx=20)
left_frame.grid(row=1, column=0, sticky="n")

videofeed = tk.Label(left_frame, bg="black", width=600, height=400)
videofeed.pack(pady=10)


btn_frame = tk.Frame(left_frame, bg="#f0f0f0")
btn_frame.pack()

cam_btn = tk.Button(btn_frame, text="Switch Camera", command=lambda: setup_camera(), bg="orange", fg="white", font=("Arial", 12, "bold"), padx=10)
cam_btn.pack(side=LEFT, padx=5)

btn = tk.Button(btn_frame, text="SCAN FIT", command=multi_threaded_scan, bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), padx=20)
btn.pack(side=LEFT, padx=5)

save_fit = tk.Button(btn_frame, text="Snapshot", command=lambda: diary_log(), bg="#5d00ff", fg="white", font=("Arial", 12, "bold"), padx=20)
save_fit.config(state=tk.DISABLED)

save_fit.pack(side=LEFT, padx=5)

# Right Frame (Sidebar Info)
sidebar = tk.Frame(window, bg="white", relief=tk.RIDGE, bd=2, padx=15, pady=15)
sidebar.grid(row=1, column=1, sticky="nsew", padx=10)

# Occasion Blank

tk.Label(sidebar, text="Occasion", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w")
occasion = entry = tk.Entry(sidebar, width=30)
occasion.pack(anchor="w", pady=(0, 15))


# Weather Display
tk.Label(sidebar, text="Conditions outside", font=("Arial", 10, "bold"), bg="white", fg="gray").pack(anchor="w")
weather_lbl = tk.Label(sidebar, text=f"Temp: {daily_apparent_temperature_max}°C | Rain: {daily_precipitation_probability_max}%", font=("Arial", 11), bg="white")
weather_lbl.pack(anchor="w", pady=(0, 15))


# Detections Section
tk.Label(sidebar, text="I detected you are wearing:", font=("Arial", 10, "bold"), bg="white", fg="gray").pack(anchor="w")
detect_box = tk.Text(sidebar, height=6, width=40, font=("Consolas", 10), state=DISABLED)
detect_box.pack(pady=5)

# The Roast (Result)
tk.Label(sidebar, text="Results", font=("Arial", 10, "bold"), bg="white", fg="gray").pack(anchor="w", pady=(15, 0))
result = tk.Text(sidebar, height=10, width=40, font=("Arial", 11, "italic"), wrap=WORD, state=DISABLED, bg="#fff0f0")
result.pack(pady=5)





newframe()
print("\033c", end="")
pt.panel(60,content=[f"{Style.BRIGHT}{Fore.GREEN}Started...","Please open the Launched Window..."],center=True,border_bold=True,padding=1, center_content=True,title=f"Welcome to Clueless Closet",color="Cyan")

window.mainloop()


# The Clueless Closet

### Optimization
During development of this project, its exe size went above 3GB, plus after installation, it took more than 12GB of storage just because it processed all AI Locally. **This was a problem which needed to be fixed!**

This project IS MADE to work locally, without an API. So that was a big challenge. Also, most pc didnt have good GPU, so something had to be done for that too.

### Optimization Solution
I have implemented hardware based model retrieval, means a weaker model of AI would run for a weaker system, to ensure low ram usage and cpu-ai compatibility!

For the systems with high end GPUs, it checks it, and automatically downloads the best AI models for detections!

I have also added compressed versions of AI models, which DRASTICALLY reduced Vram usage from 12GB+ to working UNDER 6GB Vram


Watch this program **brutally roast** you based on your outfit.

It takes into account
- Outside Temperature
- Rain/Snow Conditions
- Occasion
- Type of Clothes
- And more..

# Tips to run

To make it run properly, please use a good camera, and stand infront of a plain background.

Do not get too far as then it would be unable to detect the type of clothes.

I personally stay within 2-3 meters range of the camera, ensuring it can see me completely and clearly.

Strong colored lighting from your back may effect accuracy, and you may get roasted without reason.

Wearing stuff which is mostly white would cause issues, as white color is quite hard to detect if it is a jacket or a tshirt or a labcoat. Please avoid those, this is just a fun project.

# Setup
> This is tested for Windows Environments ONLY! It may not work correctly in Linux or other OS.

### 1. File Install
Use this command in your terminal (Make sure you have git installed)

Download the latest files from the Github Release

### 2. Dependencies Install

After unpacking the archive, start the `.exe` file. It would take upto 10 minutes for it to download and set up the AI models in your system. **Do not kill it in the process.**

### 3. Config
Open the `settings.json` in any file editor and edit the settings.
Set your location (Longitude, Latitude) and it would fetch weather of that place.
There are a lot of other parameters which you can edit in the settings.
### 4. Run
Double Click the ``main.py`` file, and let it load. It would automatically download and set up AI Model.

Once setup is done, Program would run and you can use it to get yourself tost at any time!


# Other Tips & Docs

### How to get Roasted
- Use the Switch Camera feature to switch to the best working camera (If not already done)
- Stand a bit back so camera can see you, and click the Scan Button.
- Once your high self esteem has been trashed by the AI, you can take a Snapshot.

### Snapshots
- Snapshots save your image with the roast at the `./diary` folder as a file, so you can save that or share that anywhere you want.

There are a lot of settings in the settings.json, in which you can edit the snapshot configuration. You can also change font.

### Personalities
Now, the project supports personalities too! You can set it in the `settings.json`. 
Personalities change the UI, Output as well as the snapshot template.
Current Personalities:
- `roast` (It roasts you based on our outfit)
- `grandma` (It pampers you and loves you regardless of your life choices)
- `hypeman` (It is always over hyped, and actually helpful)
- `dad` (It just tells you dadjokes)
# AI Disclosure
As a developer, I feel it is utmost important to mark AI Contributions in the project. Gemini was used in this to make images and help with programming topics which I did not know of.  
Any place where AI was used, is properly marked through use of comments.

# Contribute
Fun upgrades to this program would be highly appreciated! If you work on fixing any bugs or build a cool feature, Il surely merge it in!

# License
MIT
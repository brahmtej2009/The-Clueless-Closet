# The Clueless Closet

#### *This project is extremely easy to run, just download and run, no advanced setup needed.*
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

### File Install
Use this command in your terminal (Make sure you have git installed)

```ps
git clone "https://github.com/brahmtej2009/The-Clueless-Closet"
```
*Alternatively, you can download files from github and proceed...*
### Dependencies Install
Open the folder, and run this command

```ps
pip install -r requirements.txt
```

### Run
Double Click the ``main.py`` file, and let it load. It would automatically download and set up AI Model.

Once setup is done, Program would run and you can use it to get yourself tost at any time!

### How to get Roasted
- Use the Switch Camera feature to switch to the best working camera (If not already done)
- Stand a bit back so camera can see you, and click the Scan Button.
- Once your high self esteem has been trashed by the AI, you can take a Snapshot.

### Snapshots
- Snapshots save your image with the roast at the `./diary` folder as a file, so you can save that or share that anywhere you want.

There are a lot of settings in the settings.json, in which you can edit the snapshot configuration. You can also change font.

# AI Disclosure
As a developer, all the projects I work on have an AI Disclosure. The same is the case with this project as well.
Any place where AI was used, is properly marked through use of comments.

# Contribute
Fun upgrades to this program would be highly appreciated! If you work on fixing any bugs or build a cool feature, Il surely merge it in!

# License
MIT
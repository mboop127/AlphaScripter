# AlphaScripter
Genetic algorithm which evolves aoe2 DE ai scripts

Dependencies:
- opencv - https://docs.opencv.org/master/d6/d00/tutorial_py_root.html (package is called `opencv-python`)
- pytesseract - https://pypi.org/project/pytesseract/
- pyautogui - https://pyautogui.readthedocs.io/en/latest/
- pydirectinput - https://pypi.org/project/PyDirectInput/

### How to install
1. Install Python (tested with version 3.9), the dependencies listed above
2. Install Age of Empires 2 : Definitive Edition (Steam Edition).
3. Open the Python file `AlphaScripter.XX.py`. Change the value of the variable `installation_folder_path` to your
specific installtion folder path. If you use the default installtion path on your `C:` drive, you can ignore this step. 
4. Run the script.

### What does it do?
On run, the script will generate an AI named "Alpha," load it into a game versus the training ai (Alpha *must* be in the second slot).
The script will automatically start new games from the post game menu -- you may want to speed up the game in the first round, and/or end the first round early as it won't count for scoring.

Your game may crash. If it does, you can pause the script with control-v and reset. It will save the progress.

The best script so far will be saved as "best.per" in the .ai directory. It will be overwritten if you restart the script.

The png files are necessary for the auto-load new game function.

I will expand this later -- if you would like to help with this project, you can find me on the AI scripters discord for aoe2 de and dm me.
I specifically need help from those knowledgeable about scripting, and especially from anyone willing to write me a resign script I can put in to check whether the generated AIs should resign (this will speed up training significantly).

Run types:
You can run vs, run score, or run FFA.

run vs:
load alpha into p1 and beta into p2.
Game will pick winner as new parent - this is a good adversarial AI but is best for late stage training once the AI is good enough to possibly defeat another player

run score:
load training AI (HD, barbarian, extreme) into p1 and alpha into p2
Game will pick all-time-highest scorers as new parent.

run FFA:
load alpha-h into slots 1-8, make sure no teams are selected
Game will pick two best in each round and crossover their traits. Very good for fast training early on.

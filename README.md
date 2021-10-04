# AlphaScripter
Genetic algorithm which evolves aoe2 DE ai scripts

Dependencies:
opencv - https://docs.opencv.org/master/d6/d00/tutorial_py_root.html
pytesseract - https://pypi.org/project/pytesseract/
pyautogui - https://pyautogui.readthedocs.io/en/latest/
pydirectinput - https://pypi.org/project/PyDirectInput/

Guide:
Place all files in the aoe2 de ai directory

On run, the script will generate an AI named "alpha," load it into a game versus the training ai (Alpha *must* be in the second slot).
The script will automatically start new games from the post game menu -- you may want to speed up the game in the first round, and/or end the first round early as it won't count for scoring.

Your game may crash. If it does, you can pause the script with control-v and reset. It will save the progress.

The best script so far will be saved as "best.per" in the .ai directory. It will be overwritten if you restart the script.

The png files are necessary for the auto-load new game function.

I will expand this later -- if you would like to help with this project, you can find me on the AI scripters discord for aoe2 de and dm me.
I specifically need help from those knowledgeable about scripting, and especially from anyone willing to write me a resign script I can put in to check whether the generated AIs should resign (this will speed up training significantly).

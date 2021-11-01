# AlphaScripter
Use the power of genetic algorithms to evolve AI scripts for Age of Empires II : Definitive Edition. 
For now this package runs in AOC Userpatch 1.5 to train. In theory, scripts generated this way should be
compatible with Age of Empires II : Definitive Edition, but in practice a certain amount of porting will need to 
take place. This is currently a work in progress. Please read the 
[documentation](https://github.com/mboop127/AlphaScripter/wiki) for more information on individual classes.

## Dependencies
- `msgpackrpc >= 0.4.1` : A package used to communicate with running AOE processes. (To install, `pip install msppack-rpc-python`) 
- `psutil >= 5.8.0` : A package used to manage running processes.
- `tornado == 4.3.5` : Should be automatically installed with `msgpackrpc`. 

## How to install  and run
1. Install **32-bit** (!) Python (tested with version 3.9) and the dependencies listed above.
2. Install Age of Empires II - The Conquerors and install UserPatch 1.5. The UserPatch can be found here: 
https://userpatch.aiscripters.net/
3. Download the `aoc-auto-game.dll` and paste it in the same folder as the AOC executable. You can download
this DLL file [here.](https://github.com/FLWL/aoc-auto-game/releases/download/v1.15/aoc-auto-game.dll)
4. Open the Python file `Main.py`, adjust parameters and run the script. (WIP)


### The Main Script `Main.py`
On run, the script will generate an AI named "Alpha," load it into a game versus the training ai (Alpha *must* be in the second slot).
The script will automatically start new games from the post game menu -- you may want to speed up the game in the first 
round, and/or end the first round early as it won't count for scoring.

Your game may crash. If it does, you can pause the script with control-v and reset. It will save the progress.

The best script so far will be saved as "best.per" in the .ai directory. It will be overwritten if you restart the script.

The png files are necessary for to auto-load new game function.

I will expand this later -- if you would like to help with this project, you can find me on the AI scripters discord 
for aoe2 de and dm me.
I specifically need help from those knowledgeable about scripting or engine modification.

Run types:
You can run vs, run score, or run FFA.

run vs:
load alpha into p1 and beta into p2.
Game will pick winner as new parent - this is a good adversarial AI but is best for late stage training once the AI is 
good enough to possibly defeat another player

run score:
load training AI (HD, barbarian, extreme) into p1 and alpha into p2
Game will pick all-time-highest scorers as new parent.

run FFA:
load alpha-h into slots 1-8, make sure no teams are selected
Game will pick two best in each round and crossover their traits. Very good for fast training early on.
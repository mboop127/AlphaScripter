# AlphaScripter
Use the power of genetic algorithms to evolve AI scripts for Age of Empires II : Definitive Edition. 
For now this package runs in AOC Userpatch 1.5 to train. In theory, scripts generated this way should be
compatible with Age of Empires II : Definitive Edition, but in practice a certain amount of porting will need to 
take place. This is currently a work in progress.

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

## What does it do? - Explanation per script
### The Main Script `Main.py`
On run, the script will generate an AI named "Alpha," load it into a game versus the training ai (Alpha *must* be in the second slot).
The script will automatically start new games from the post game menu -- you may want to speed up the game in the first 
round, and/or end the first round early as it won't count for scoring.

Your game may crash. If it does, you can pause the script with control-v and reset. It will save the progress.

The best script so far will be saved as "best.per" in the .ai directory. It will be overwritten if you restart the script.

The png files are necessary for the auto-load new game function.

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

### Game Launcher `game_launcher.py`
The game launcher is used to, surprise, launch games. To successfully launch a game, the class `Launcher` 
needs to be instantiated. This will take 1 optional argument: `path` that specifies the path to the AOC executable.
If you don't pass this argument, the game will look for the executable in the default path: 
`C:\Program Files\Microsoft Games\age of empires ii\Age2_x1\age2_x1.exe`. If the executable cannot be found, 
the launcher will raise an Exception.

After correctly instantiating this `Launcher`, you can launch a game using the `Launcher.launch_game` function.
This function takes 2 required and 3 optional arguments:
- (Required) `names : list[str]` - This is a list of strings that represent the names of the AI .per files that the game will 
look for when starting the game. These should be in the `..\age of empires ii\ai` folder. 
- (Required) `game_settings` - This should be an instance of the `GameSettings` class, which is also declared in 
`game_launcher.py`.
- (Optional) `real_time_limit : int` -  The number of real time seconds after which the game(s) should be automatically
quit and closed. If not given, there will not be a real-time limit.
- (Optional) `game_time_limit : int` - The number of in-game seconds after the game(s) should be quit and closed.
- (Optional) `instances : int` - The number of games to run simultaneously. This currently a little experimental, so
keep in mind that your mileage with this setting.

The `GameSettings` class is used to store settings for the game. To instantiate a `GameSettings` object, you will have 
to pass 1 required argument and a lot of optional arguments. See below for a description.
- (Required) `civilisations` - A list of strings or int (can also be mixed) that represent the civs that the AI players 
will use. It must be the same length as the `names` given to the launcher, otherwise the launcher will raise an 
Exception. If an element in the given list is not a valid civ, that element will be replaced by `'huns'`.
- (Optional) `map_id` - A string or int that represents the map. Default `'arabia'`
- (Optional) `map_size` - A string or int that represent the map size. Default `'medium'`
- (Optional) `difficulty` - A string or int that represents the difficulty of the game. Default `'hard'`
- (Optional) `game_type` - Specifies the game type. Default `'random_map'`
- (Optional) `resources` - Specifies the starting resources of each player. Default `'low'`
- (Optional) `reveal_map` - Whether the map should be revealed. Default `'normal'`
- (Optional) `starting_age` - Which age the players should start in. Default `'dark'`
- (Optional) `victory_type` - The victory type. Doesn't work (yet). Default `'conquest'`

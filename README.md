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

------------------------------------
### Game Launcher `game_launcher.py`
The game launcher is used to, surprise, launch games. To successfully launch any game at all, you first need to
create the settings that the game will follow. This is done by instantiating an instance of the `GameSettings` class.
To do this, you will have to pass 1 required argument and a lot of optional arguments. 
- (Required) `names: list[str]` - A list of strings that indicate the names of the AI's that will play the match. 
The .per files for these AIs need to be present in the AI folder of the game.
- (Optional) `civilisations: list[str, int]` - A list of strings or int (can also be mixed) that represent the civs 
that the AI players will use. If an element in the given list is not a valid civ, or if a civ is not specified for
a player (because the number of provided civs is lower number of provided names) a default value of `'huns'` will be used.
- (Optional) `map_id: [str, int]` - A string or int that represents the map. Default `'arabia'`
- (Optional) `map_size: [str, int]` - A string or int that represent the map size. Default `'medium'`
- (Optional) `difficulty: [str, int]` - A string or int that represents the difficulty of the game. Default `'hard'`
- (Optional) `game_type: [str, int]` - Specifies the game type. Default `'random_map'`
- (Optional) `resources: [str, int]` - Specifies the starting resources of each player. Default `'low'`
- (Optional) `reveal_map: [str, int]` - Whether the map should be revealed. Default `'normal'`
- (Optional) `starting_age: [str, int]` - Which age the players should start in. Default `'dark'`
- (Optional) `victory_type: [str, int]` - The victory type. Doesn't work (yet). Default `'conquest'`
- (Optional) `game_time_limit: int` - After how many in-game seconds the game should be quit. Please note that this
will be approximated because of the high speed on which the games are played, this will never exactly match. 

After creating the game settings, you need to instantiate an instance of the class `Launcher`. 
This will take the following arguments:
- (Required) `settings: GameSettings` - An instance of the `GameSettings` class that holds all the settings for the
games.
- (Optional) `path: str` - This specifies the path to the AOC executable. If you don't pass this argument, the game will 
look for the executable in the default path: `C:\Program Files\Microsoft Games\age of empires ii\Age2_x1\age2_x1.exe`. 
If the executable cannot be found, the launcher will raise an Exception.
- (Optional) `debug: bool` - Whether to print debug statements to the console.

After correctly instantiating this `Launcher`, you can launch a game using the `Launcher.launch_games` function. 
This function only has 1 argument:
- (Optional) `instances : int` - The number of games to run simultaneously. This currently a little experimental, so
keep in mind that your mileage with this setting. By default, this is set to 1.

**Congrats! The games will now run!**

The `Launcher.launch_games` method will return a list of `Game` instances. These `Game` instances hold all data 
regarding a played game. The most important of these is the `Game.stats` which itself is an instance of the 
`GameStats` (data)class. This `GameStats` instance holds `scores` and `elapsed_game_time`. More information will be 
added to the `GameStats` class in the future.
Also important to note is that the `Game` class also holds the `Game.status` which holds the status of the game.

If `Game.status == GameStatus.EXCEPTED` something went wrong with the game. It had a timeout, it crashed, or it was
shutdown manually. The `Game.stats` are `None` in that case.

#### Example
The example below shows how to start 3 games simultaneously with 3 Barbarian AIs (given you have the .per file 
for Barbarian) and extract the scores while filtering out games that crashed or encountered some exception.
```
# Setup the game
ai_names = ['Barbarian', 'Barbarian', 'Barbarian']
ai_civs = ['huns', 'celts', 'turks']
gs = GameSettings(names=ai_names, civilisations=ai_civs, map_size='medium', game_time_limit=5000)
launcher = Launcher(settings=gs)

# Launch the games
games = launcher.launch_games(instances=3)

# Filter out the crashed / excepted games and extract scores
non_crashed_games = [game for game in games if game.status != GameStatus.EXCEPTED]
stats = [game.stats for game in non_crashed_games]  # Very explicit but okay.
scores = [stat.scores for stat in stats]
```
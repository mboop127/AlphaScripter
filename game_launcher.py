import asyncio
import enum
import os
import subprocess
import time
from ctypes import windll
import datetime
from dataclasses import dataclass

import msgpackrpc
import psutil

all_civilisations = {
    "britons": 1,
    "franks": 2,
    "goths": 3,
    "teutons": 4,
    "japanese": 5,
    "chinese": 6,
    "byzantine": 7,
    "persians": 8,
    "saracens": 9,
    "turks": 10,
    "vikings": 11,
    "mongols": 12,
    "celts": 13,
    "spanish": 14,
    "aztec": 15,
    "mayan": 16,
    "huns": 17,
    "koreans": 18,
    "random": 19
}

maps = {
    "arabia": 9,
    "archipelago": 10,
    "baltic": 11,
    "black_forest": 12,
    "coastal": 13,
    "continental": 14,
    "crater_cake": 15,
    "fortress": 16,
    "gold_rush": 17,
    "highland": 18,
    "islands": 19,
    "mediterranean": 20,
    "migration": 21,
    "rivers": 22,
    "team_islands": 23,
    "random_map": 24,
    "random": 24,
    "scandinavia": 25,
    "mongolia": 26,
    "yucatan": 27,
    "salt_marsh": 28,
    "arena": 29,
    "oasis": 31,
    "ghost_lake": 32,
    "nomad": 33,
    "iberia": 34,
    "britain": 35,
    "mideast": 36,
    "texas": 37,
    "italy": 38,
    "central_america": 39,
    "france": 40,
    "norse_lands": 41,
    "sea_of_japan": 42,
    "byzantium": 43,
    "random_land_map": 45,
    "random_real_world_map": 47,
    "blind_random": 48,
    "conventional_random_map": 49
}

map_sizes = {'tiny': 0, 'small': 1, 'medium': 2, 'normal': 3, 'large': 4, 'giant': 5}
difficulties = {'hardest': 0, 'hard': 1, 'moderate': 2, 'standard': 3, 'easiest': 4}
game_types = {'random_map': 0, 'regicide': 1, 'death_match': 2, 'scenario': 3, 'king_of_the_hill': 4, 'wonder_race': 6,
              'turbo_random_map': 8}
starting_resources = {'standard': 0, 'low': 1, 'medium': 2, 'high': 3}
reveal_map_types = {'normal': 1, 'explored': 2, 'all_visible': 3}
starting_ages = {'standard': 0, 'dark': 2, 'feudal': 3, 'castle': 4, 'imperial': 5, 'post-imperial': 6}
victory_types = {'standard': 0, 'conquest': 1, 'relics': 4, 'time_limit': 7, 'score': 8}


class GameStatus(enum.Enum):
    NONE = "No status yet."  # If we read this there is probably something wrong.
    INIT = "Initialized"  # This means no process has been launched, no RPC client has been launched or anything.
    LAUNCHED = "Game process launched."  # The process exists, but not RPC client has been launched and connected.
    CONNECTED = "RPC Client connected."  # The process and RPC client exist, but the game is still in the main menu.
    SETUP = "Game settings have been applied."  # The game has applied settings.
    RUNNING = "Game is running"  # The game is just running.
    ENDED = "Game is no longer running."  # The game has ended and we are in the main menu.
    QUIT = "Game has been quit and process killed."
    EXCEPTED = "This game has encountered an error and is therefore terminated."


class GameSettings:
    def __init__(self, names: list, civilisations: list = None, map_id='arabia', map_size='medium', difficulty='hard',
                 game_type='random_map', resources='low', reveal_map='normal', starting_age='dark',
                 victory_type='conquest', game_time_limit=0):

        self.names = names
        self.civilisations = self.correct_civilizations(civilisations, default='huns')
        self.map_id = self.correct_setting(map_id, maps, 'arabia', 'map name/type')
        self.map_size = self.correct_setting(map_size, map_sizes, 'medium', 'map size')
        self.difficulty = self.correct_setting(difficulty, difficulties, 'hard', 'difficulty')
        self.game_type = self.correct_setting(game_type, game_types, 'random_map', 'game type')
        self.resources = self.correct_setting(resources, starting_resources, 'standard', 'starting resources')
        self.reveal_map = self.correct_setting(reveal_map, reveal_map_types, 'normal', 'reveal map')
        self.starting_age = self.correct_setting(starting_age, starting_ages, 'explored', 'starting age')
        self.victory_type = self.correct_setting(victory_type, victory_types, 'conquest', 'victory type (WIP)')
        self.victory_value = 0  # TODO: Make this work.
        self.game_time_limit = game_time_limit

    @property
    def map(self):
        return self.map_id

    @staticmethod
    def correct_setting(value, possible_values: dict, default, setting_name):
        if value in possible_values.values():
            return value
        elif value.lower() in possible_values.keys():
            return possible_values[value.lower()]
        print(f"Warning! Value {value} not valid for setting {setting_name}. Defaulting to {default}.")
        return possible_values[default]

    def correct_civilizations(self, civilizations: list, default='huns'):
        if not civilizations:
            return []
        result = []

        if len(civilizations) < len(self.names):
            print(f"The number of civilisations provided is less than the number of names. For every player that "
                  f"does not have a civilisation provided for it, it will default to {default}.")

        for index, name in enumerate(self.names):
            if index < len(civilizations):  # Just copy the civilisations list for as far as we can
                civ = civilizations[index]
                if civ in all_civilisations.values():
                    result.append(civ)
                elif civ in all_civilisations.keys():
                    result.append(all_civilisations[civ])
                else:
                    print(f"Civ {civ} is not valid. Defaulting to {default}.")
                    result.append(all_civilisations[default])
            else:  # If we have a list of civs that is to short, fill up the rest with the default.
                result.append(all_civilisations[default])
        return result

    @property
    def civs(self):
        return self.civilisations


@dataclass
class GameStats:
    scores: list[int]
    elapsed_game_time: int


class Game:
    name: str = "GameWithoutName"
    _settings: GameSettings = None
    status: GameStatus = GameStatus.NONE

    _process: subprocess.Popen = None
    _rpc: msgpackrpc.Client = None
    _port: int = 0
    stats: GameStats = None

    def __init__(self, name: str):
        self.name = name
        self.status = GameStatus.INIT

    async def launch_process(self, executable_path: str, dll_path: str, multiple: bool, port: int) -> subprocess.Popen:
        if self.status != GameStatus.INIT:
            print(f"Warning! This game does not have the status {GameStatus.INIT} so it's probably not the right time"
                  f" to call this launch_process method!")

        launch_options = f"{executable_path} {'-multipleinstances ' if multiple else ''}-autogameport {port}"
        aoc_proc = subprocess.Popen(launch_options)

        # write dll path into aoc memory
        aoc_handle = windll.kernel32.OpenProcess(0x1FFFFF, False, aoc_proc.pid)  # PROCESS_ALL_ACCESS
        remote_memory = windll.kernel32.VirtualAllocEx(aoc_handle, 0, 260, 0x3000, 0x40)
        windll.kernel32.WriteProcessMemory(aoc_handle, remote_memory, dll_path, len(dll_path), 0)

        # load the dll from the remote process
        # noinspection PyProtectedMember
        load_library = windll.kernel32.GetProcAddress(windll.kernel32._handle, b'LoadLibraryA')
        remote_thread = windll.kernel32.CreateRemoteThread(aoc_handle, 0, 0, load_library, remote_memory, 0, 0)
        windll.kernel32.WaitForSingleObject(remote_thread, 0xFFFFFFFF)
        windll.kernel32.CloseHandle(remote_thread)

        # clean up
        windll.kernel32.VirtualFreeEx(aoc_handle, remote_memory, 0, 0x00008000)
        windll.kernel32.CloseHandle(aoc_handle)

        self._port = port
        self._process = aoc_proc
        self.status = GameStatus.LAUNCHED
        return aoc_proc

    def setup_rpc_client(self, custom_port: int = 0) -> msgpackrpc.Client:
        if self.status != GameStatus.LAUNCHED:
            print(f"Warning! Game {self.name} does have the status {GameStatus.LAUNCHED}. Setting up the RPC client"
                  f" is probably not a good idea!")

        setup_port = custom_port if custom_port != 0 else self._port
        self._rpc = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", setup_port))
        self.status = GameStatus.CONNECTED
        return self._rpc

    async def apply_settings(self, settings: GameSettings):
        if self.status != GameStatus.CONNECTED:
            print(f"Warning! Status of game {self.name} is not {GameStatus.CONNECTED}. It might not be a good time"
                  f" to setup the game...")

        self._settings = settings
        try:
            self._rpc.call_async('ResetGameSettings')
            self._rpc.call_async('SetGameMapType', settings.map)
            self._rpc.call_async('SetGameDifficulty', settings.difficulty)  # Set to hard
            self._rpc.call_async('SetGameRevealMap', settings.reveal_map)  # Set to standard exploration
            self._rpc.call_async('SetGameMapSize', settings.map_size)  # Set to medium map size
            self._rpc.call_async('SetGameVictoryType', settings.victory_type, settings.victory_value)
            self._rpc.call_async('SetRunUnfocused', True)
            self._rpc.call_async('SetRunFullSpeed', True)
            # self.call_safe('SetUseInGameResolution', False, game_index=game_index)
            for index, name in enumerate(settings.names):
                self._rpc.call_async('SetPlayerComputer', index + 1, name)
                self._rpc.call_async('SetPlayerCivilization', index + 1, settings.civilisations[index])
                self._rpc.call_async('SetPlayerTeam', index + 1, 0)
        except BaseException as e:
            print(f"Warning! Game Settings could not be applied to game {self.name} because of exception {e}."
                  f" The rpc client will be closed and the game process will be terminated.")
            self.handle_except(e)
        self.status = GameStatus.SETUP

    async def start_game(self):
        if self.status != GameStatus.SETUP:
            print(f"Warning! Game {self.name} has not the status {GameStatus.SETUP}. It might not be a good idea to"
                  f" try and start this game...")
        try:
            self._rpc.call('StartGame')
            print(f"Game {self.name} launched.")
        except BaseException as e:
            print(f"Could not start game {self.name} because it has excepted with exception {e}. "
                  f"The game will be ended and the process killed.")
            self.handle_except(e)
        self.status = GameStatus.RUNNING

    async def update(self) -> bool:
        """
        Check whether the game is still running and extract the scores if it isn't.

        :return: Whether the game is still running.
        """
        try:
            is_running = self._rpc.call('GetGameInProgress')
            game_time = 0
            try:
                game_time = self._rpc.call('GetGameTime')
            except BaseException as e:
                print(f"Couldn't get game time for game {self.name} because of {e}. "
                      f"Closing the RPC client and killing process.")
                self.handle_except(e)

            over_time = 0 < self._settings.game_time_limit < game_time

            if not is_running or over_time:
                scores = []
                for index, name in enumerate(self._settings.names):
                    try:
                        score = self._rpc.call("GetPlayerScore", index + 1)
                        if score is not None:
                            scores.append(score)
                        else:
                            scores.append(0)
                            print(f"Couldn't get score for player {index + 1}. Setting this score to 0")
                    except BaseException as e:
                        print(f"Score for player {index + 1} in game {self.name} couldn't be retrieved because of {e}. "
                              f"Setting this players' score to 0.")
                        scores.append(0)
                        self.handle_except(e)
                self.stats = GameStats(scores, game_time)
                self.kill()

        except BaseException as e:
            print(f"Warning! Game {self.name} could not be updated because of exception {e}.")
            self.handle_except(e)

    def handle_except(self, exception):
        print(f"Exception {exception} occurred on game {self.name}. Killing the process and closing the rpc client.")
        self.kill()  # Important to do before setting the Excepted state!
        self.status = GameStatus.EXCEPTED

    def kill(self):
        if self._rpc is not None:
            self._rpc.close()
            self._rpc = None
        if self._process is not None:
            self._process.kill()
            self._process = None
        self.status = GameStatus.QUIT

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Launcher:
    def __init__(self,
                 settings: GameSettings,
                 executable_path: str = "C:\\Program Files\\Microsoft Games\\age of empires ii\\Age2_x1\\age2_x1.exe"):
        self.executable_path = executable_path
        self.directory, self.aoc_name = os.path.split(executable_path)
        self.dll_path = (os.path.join(self.directory, 'aoc-auto-game.dll')).encode('UTF-8')
        self.games: list[Game] = None
        self.base_port = 64720
        self.settings = settings

    @property
    def names(self):
        return self.settings.names

    @property
    def number_of_games(self):
        if not self.games:
            return 0
        return len(self.games)

    @property
    def running_games(self):
        return [game for game in self.games if game.status == GameStatus.RUNNING]

    def launch_games(self, instances: int = 1):
        self.games = [Game(f"Game#{i + 1}") for i in range(instances)]
        asyncio.run(self._launch_games(), debug=True)
        time.sleep(5.0)  # Make sure all games are launched.
        self._setup_rpc_clients()
        asyncio.run(self._apply_games_settings(settings=self.settings), debug=True)  # Apply settings to the games
        time.sleep(2)
        asyncio.run(self._start_games())

        any_game_running = True
        while any_game_running:
            asyncio.run(self.update_games())
            print(f"({datetime.datetime.now()}) : {self.running_games}")
            time.sleep(1)
            any_game_running = len(self.running_games) > 0

        return self.games

    async def _launch_games(self) -> list[subprocess.Popen]:
        tasks = []
        multiple = self.number_of_games > 1
        for index, game in enumerate(self.games):
            t = asyncio.create_task(
                coro=game.launch_process
                (
                    executable_path=self.executable_path,
                    dll_path=self.dll_path,
                    multiple=multiple,
                    port=self.base_port + index
                ),
                name=f"GameLaunch{index}")
            tasks.append(t)
        return await asyncio.gather(*tasks)

    def _setup_rpc_clients(self):
        for game in self.games:
            game.setup_rpc_client()

    async def _apply_games_settings(self, settings: GameSettings):
        tasks = []
        for index, game in enumerate(self.games):
            t = asyncio.create_task(coro=game.apply_settings(settings), name=f"ApplyGameSettings-{game.name}")
            tasks.append(t)
        return await asyncio.gather(*tasks)

    async def _start_games(self):
        tasks = []
        for index, game in enumerate(self.games):
            t = asyncio.create_task(coro=game.start_game(), name=f"StartingGame-{game.name}")
            tasks.append(t)
        return await asyncio.gather(*tasks)

    async def update_games(self):
        tasks = []
        for game in self.running_games:
            t = asyncio.create_task(coro=game.update(), name=f"UpdateGame-{game.name}")
            tasks.append(t)
        await asyncio.gather(*tasks)


n = ['Barbarian'] * 2
civ = ['huns'] * 2
gs = GameSettings(names=n, civilisations=['huns'], map_size='tiny', game_time_limit=2000)
launcher = Launcher(settings=gs)
launcher.launch_games(instances=3)

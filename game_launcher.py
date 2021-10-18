import os
import subprocess
import time
from ctypes import windll
from typing import Union

import msgpackrpc
import psutil

civs = {
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


class Launcher:
    def __init__(self,
                 executable_path: str = "C:\\Program Files\\Microsoft Games\\age of empires ii\\Age2_x1\\age2_x1.exe"):
        self.executable_path = executable_path
        self.directory, self.aoc_name = os.path.split(executable_path)
        self.dll_path = (os.path.join(self.directory, 'aoc-auto-game.dll')).encode('UTF-8')
        self.names = None
        self.games: list[tuple[msgpackrpc.Client, subprocess.Popen]] = []

    @property
    def number_of_games(self):
        if not self.games:
            return 0
        return len(self.games)

    def launch_game(self,
                    names: list[str],
                    civs: list[int] = None,
                    real_time_limit: int = 0,
                    game_time_limit: int = 0,
                    map_id: Union[str, int] = 26,
                    number_of_instances: int = 1):
        self.quit_all_games(quit_program=True)
        self.names = names
        if names is None or len(names) < 2 or len(names) > 8:
            raise Exception(f"List of names {names} not valid! Expected list of a least 2 and at most 8.")

        if civs is not None and len(civs) != len(names):
            raise Exception(f"The length of the civs {civs} does not match the length of the names {names}")

        if civs is None:
            civs = [17] * len(names)

        if isinstance(map_id, str):
            m = map_id.lower()
            m = m.replace(" ", "_")
            if m in maps.keys():
                map_id = maps[m]  # Convert string into valid map integer
            else:
                raise Exception(f"Map ID {map_id} is not valid. Valid choices: {list(maps.keys())}")
        elif isinstance(map_id, int) and map_id not in maps.values():
            print(f"Warning! The map id given : '{map_id}' is not a standard map. This can lead to issues.")

        for i in range(number_of_instances):
            port = 64720 + i
            process = self._launch(multiple=number_of_instances > 1, port=port)
            rpc_client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", port))
            self.games.append((rpc_client, process))

        current_time = 0
        self._start_all_games(names, civs, map_id)
        scores = [[0] * len(names)] * len(self.games)
        running_games = self.get_running_games()
        while running_games:
            time.sleep(1)
            current_time += 1

            for running_game_index in running_games:
                scores[running_game_index] = self.get_scores(running_game_index)

            if game_time_limit > 0:
                for i in range(len(self.games)):
                    game_time = self.call_safe('GetGameTime', game_index=i)
                    if game_time is None:
                        print(f"Warning! Wasn't able to get the ingame time of game {i}. If the in-game time"
                              f"is over the limit, we can't check now.")
                    elif game_time > game_time_limit:
                        print(f"Time's up for game {i}!")
                        self.quit_game(i)

            print(f"Time {current_time} , Scores {scores}")
            if 0 < real_time_limit < current_time:
                print("Real time's up!")
                break
            running_games = self.get_running_games()

        self.quit_all_games()
        print(scores)
        return scores

    def get_running_games(self) -> list:
        result = []
        for index, game in enumerate(self.games):
            rpc, proc = game
            if rpc is None or proc is None:
                continue
            if self.call_safe('GetGameInProgress', game_index=index):
                result.append(index)
        return result

    def _launch(self, multiple: bool = False, port: int = 64720) -> subprocess.Popen:
        # kill any previous aoc processes
        # aoc_procs = [proc for proc in psutil.process_iter() if proc.name() == self.aoc_name]
        # for aoc_proc in aoc_procs: aoc_proc.kill()

        if multiple:
            aoc_proc = subprocess.Popen(self.executable_path + " -multipleinstances -autogameport " + str(port))
        else:
            aoc_proc = subprocess.Popen(self.executable_path)

        # to launch the rpc server with another port, it could be launched like this:
        # aoc_proc = subprocess.Popen(aoc_path + " -autogameport 64721")

        # write dll path into aoc memory
        aoc_handle = windll.kernel32.OpenProcess(0x1FFFFF, False, aoc_proc.pid)  # PROCESS_ALL_ACCESS
        remote_memory = windll.kernel32.VirtualAllocEx(aoc_handle, 0, 260, 0x3000, 0x40)
        windll.kernel32.WriteProcessMemory(aoc_handle, remote_memory, self.dll_path, len(self.dll_path), 0)

        # load the dll from the remote process
        load_library = windll.kernel32.GetProcAddress(windll.kernel32._handle, b'LoadLibraryA')
        remote_thread = windll.kernel32.CreateRemoteThread(aoc_handle, 0, 0, load_library, remote_memory, 0, 0)
        windll.kernel32.WaitForSingleObject(remote_thread, 0xFFFFFFFF)
        windll.kernel32.CloseHandle(remote_thread)

        # clean up
        windll.kernel32.VirtualFreeEx(aoc_handle, remote_memory, 0, 0x00008000)
        windll.kernel32.CloseHandle(aoc_handle)
        return aoc_proc

    def _start_all_games(self, names, civs, map_id, minimize: bool = False):
        for i in range(self.number_of_games):
            self._setup_game(i, names, civs, map_id)
        for i in range(len(self.games)):
            self._start_game(i, minimize)

    def _setup_game(self, game_index: int, names, civs, map_id):
        self.call_safe('ResetGameSettings', game_index=game_index)
        self.call_safe('SetGameMapType', map_id, game_index=game_index)
        self.call_safe('SetGameDifficulty', 1, game_index=game_index)  # Set to hard
        self.call_safe('SetGameRevealMap', 1, game_index=game_index)  # Set to standard exploration
        self.call_safe('SetGameMapSize', 2, game_index=game_index)  # Set to medium map size
        self.call_safe('SetRunUnfocused', True, game_index=game_index)
        self.call_safe('SetRunFullSpeed', True, game_index=game_index)
        # self.call_safe('SetUseInGameResolution', False, game_index=game_index)
        for index, name in enumerate(names):
            self.call_safe('SetPlayerComputer', index + 1, name, game_index=game_index)
            self.call_safe('SetPlayerCivilization', index + 1, civs[index], game_index=game_index)

    def _start_game(self, game_index, minimize: bool = False):
        self.call_safe('StartGame', game_index=game_index)
        if minimize:
            self.call_safe('SetWindowMinimized', True, game_index=game_index)

    def get_scores(self, game_index: int) -> list[int]:
        """
        Get the scores of a certain game that is currently running.

        :param game_index: The index of the game to get the scores from.
        :return: A list of scores, where every index represents the score of a player.
        """
        if game_index < 0 or game_index >= len(self.games):
            print(f"Cannot return scores of game {game_index} because this is not a valid index."
                  f"The index must be greater than zero and less than the length of the games list ({len(self.games)})")

        rpc_client, process = self.games[game_index]
        if process is None or rpc_client is None or not self.call_safe('GetGameInProgress', game_index=game_index):
            print("Cannot return scores when there's no game running! Returning zeroed scores.")
            return [0] * len(self.names)

        scores = []
        for i in range(len(self.names)):
            score = self.call_safe("GetPlayerScore", i + 1, game_index=game_index)
            if score:
                scores.append(score)
            else:
                scores.append(0)
                print(f"Couldn't get score for player {i + 1}. Setting this score to 0")

        return scores

    def call_safe(self, method: str, param1=None, param2=None, kill_on_except: bool = True, game_index: int = 0):
        """
        Call a method in the autogame in a safe way, where exceptions are handled.

        :param game_index: The index of the game
        :param method: The name of the method to call.
        :param param1: The first parameter for the method.
        :param param2: The second parameter for the method.
        :param kill_on_except: Whether to kill the process if calling fails.
        :return: The return of the method call, if available. None if exception occurs or game isn't running.
        """
        if not self.games:
            return None

        rpc_client, process = self.games[game_index]

        if rpc_client is None or process is None:
            print(f"Couldn't call method {method} on game {game_index} because either game process or rpc client "
                  f"doesn't exist.")
            if kill_on_except:
                self.kill_game(game_index)
            return None

        try:
            if param1 is not None and param2 is not None:
                return rpc_client.call(method, param1, param2)
            elif param1 is not None:
                return rpc_client.call(method, param1)
            else:
                return rpc_client.call(method)

        except msgpackrpc.error.TimeoutError:
            print("Request to game timed out.")
            if kill_on_except:
                self.kill_game(game_index)
            return None

    def quit_all_games(self, quit_program: bool = True, force_kill_on_fail: bool = True):
        for i in self.get_running_games():
            self.quit_game(game_index=i, quit_program=quit_program, force_kill_on_fail=force_kill_on_fail)

    def quit_game(self, game_index: int = 0, quit_program: bool = True, force_kill_on_fail: bool = True):
        """
        Quit the game to the main menu.

        :param game_index: The index of the game that will be quit.
        :param force_kill_on_fail: Whether to force stop the process when quitting to main menu fails.
        :param quit_program: If True, closes the window and quits the program. Else just stays in the main menu.
        """

        rpc_client, process = self.games[game_index]

        if rpc_client is not None:
            try:
                rpc_client.call("QuitGame")
                time.sleep(1.0)
                if quit_program:
                    rpc_client.close()
                    if process is not None:
                        process.kill()
                    self.games[game_index] = (None, None)

            except msgpackrpc.error.TimeoutError:
                print("Quitting to main menu failed.")
                if force_kill_on_fail:
                    self.kill_game(game_index=game_index)

    def kill_game(self, game_index: int):
        """
        Kill the game forcefully. The process will be killed as well.
        """
        rpc_client, process = self.games[game_index]

        if rpc_client is not None:
            try:
                rpc_client.close()
            except msgpackrpc.error.TimeoutError:
                print("Game not responding. Closing game failed.")

        if process is not None:
            try:  # Try killing the process normally
                process.kill()
            except:  # If that fails for whatever reason, terminate the process.
                p: psutil.Process = psutil.Process(process.pid)
                p.terminate()

        self.games[game_index] = (None, None)

l = Launcher()
l.launch_game(["Barbarian"] * 4, real_time_limit=30, number_of_instances=5)

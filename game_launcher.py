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


def is_responding(PID):
    return True
    os.system('tasklist /FI "PID eq %d" /FI "STATUS eq running" > tmp.txt' % PID)
    tmp = open('tmp.txt', 'r')
    a = tmp.readlines()
    tmp.close()
    if int(a[-1].split()[1]) == PID:
        return True
    else:
        return False

class Launcher:
    def __init__(self,
                 executable_path: str = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe"):
        self.executable_path = executable_path
        self.directory, self.aoc_name = os.path.split(executable_path)
        self.dll_path = (os.path.join(self.directory, 'aoc-auto-game.dll')).encode('UTF-8')
        self.names = None
        self.autogame: msgpackrpc.Client = None
        self.aoc_proc: subprocess.Popen = None

    def launch_game(self,
                    names: list[str],
                    civs: list[int] = None,
                    real_time_limit: int = 0,
                    game_time_limit: int = 0,
                    map_id: Union[str, int] = 9):

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

        # kill any previous aoc processes
        # aoc_procs = [proc for proc in psutil.process_iter() if proc.name() == self.aoc_name]
        # for aoc_proc in aoc_procs: aoc_proc.kill()

        # launch aoc and wait for it to init
        self.aoc_proc = subprocess.Popen(self.executable_path)
        # to launch the rpc server with another port, it could be launched like this:
        # aoc_proc = subprocess.Popen(aoc_path + " -autogameport 64721")

        # write dll path into aoc memory
        aoc_handle = windll.kernel32.OpenProcess(0x1FFFFF, False, self.aoc_proc.pid)  # PROCESS_ALL_ACCESS
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

        self.autogame = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 64720))

        self.call_safe('ResetGameSettings')  # usually reset the settings to make sure everything is valid
        self.call_safe('SetGameMapType', map_id)  # Set to Arabia
        self.call_safe('SetGameDifficulty', 0)  # Set to hardest
        self.call_safe('SetGameRevealMap', 2)
        self.call_safe('SetGameMapSize', 2)

        for index, name in enumerate(names):
            self.call_safe('SetPlayerComputer', index + 1, name)
            self.call_safe('SetPlayerCivilization', index + 1, civs[index])

        self.call_safe('SetRunFullSpeed', True)  # run the game logic as fast as possible (experimental)
        # autogame.call('SetRunUnfocused', True)  # allow the game to run while minimized
        self.call_safe('StartGame')  # start the match

        real_time = 0
        previous_game_time = -1

        while True:  # wait until the game has finished

            # If the game is no longer in progress
            if not self.call_safe('GetGameInProgress'):
                break

            time.sleep(1.0)
            current_game_time = int(self.call_safe('GetGameTime'))

            if current_game_time <= previous_game_time:
                print("The game time isn't progressing. The game has probably crashed because of some in-game error.")
                self.kill_game()
                return None

            previous_game_time = current_game_time
            real_time += 1

            # If we are over our real time limit or game time limit
            if (0 < real_time_limit < real_time) or (0 < game_time_limit < current_game_time):
                break

        scores = [self.call_safe("GetPlayerScore", i + 1) for i in range(len(names))]
        self.quit_game(quit_program=True)
        #print(scores)
        return scores

    def get_scores(self) -> list[int]:
        if self.autogame is None or not self.autogame.call('GetGameInProgress'):
            print("Cannot return scores when there's no game running!")
            return [0] * len(self.names)
        return [self.autogame.call("GetPlayerScore", i + 1) for i in range(len(self.names))]

    def call_safe(self, method: str, param1=None, param2=None, kill_on_except: bool = True):
        """
        Call a method in the autogame in a safe way, where exceptions are handled.
        :param method: The name of the method to call.
        :param param1: The first parameter for the method.
        :param param2: The second parameter for the method.
        :param kill_on_except: Whether to kill the process if calling fails.
        :return: The return of the method call, if available. None if exception occurs or game isn't running.
        """

        if self.autogame is None or self.aoc_proc is None:
            return None
        try:
            if param1 is not None and param2 is not None:
                return self.autogame.call(method, param1, param2)
            elif param1 is not None:
                return self.autogame.call(method, param1)
            else:
                return self.autogame.call(method)

        except msgpackrpc.error.TimeoutError:
            print("Request to game timed out.")
            if kill_on_except:
                self.kill_game()
            return None

    def quit_game(self, quit_program: bool = False, force_kill_on_fail: bool = True):
        """
        Quit the game to the main menu.
        :param force_kill_on_fail: Whether to force stop the process when quitting to main menu fails.
        :param quit_program: If True, closes the window and quits the program. Else just stays in the main menu.
        """

        if self.autogame is not None:
            try:
                self.autogame.call("QuitGame")
                time.sleep(1.0)
                if quit_program:
                    self.autogame.close()
                    self.autogame = None
                    if self.aoc_proc is not None:
                        self.aoc_proc.kill()
                        self.aoc_proc = None
            except msgpackrpc.error.TimeoutError:
                print("Quitting to main menu failed.")
                if force_kill_on_fail:
                    self.kill_game()

    def kill_game(self):
        """
        Kill the game forcefully. The process will be killed as well.
        """

        if self.autogame is not None:
            try:
                self.autogame.close()
                self.autogame = None
            except msgpackrpc.error.TimeoutError:
                print("Game not responding.")
                self.autogame = None

        if self.aoc_proc is not None:
            try:  # Try killing the process normally
                self.aoc_proc.kill()
                self.aoc_proc = None
            except:  # If that fails for whatever reason, terminate the process.
                os.system("taskkill /f /im age2_x1.5.exe")

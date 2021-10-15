import os
import time
import psutil
import subprocess
from ctypes import windll
import msgpackrpc

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
                 executable_path: str = "C:\\Program Files\\Microsoft Games\\age of empires ii\\Age2_x1\\age2_x1.exe"):
        self.executable_path = executable_path
        self.directory, self.aoc_name = os.path.split(executable_path)
        # self.dll_path = b'C:/Shared/AoE/aoc-auto-game/Release/aoc-auto-game.dll'
        self.dll_path = (os.path.join(self.directory, 'aoc-auto-game.dll')).encode('UTF-8')
        self.names = None
        self.autogame = None
        self.aoc_proc = None

    def launch_game(self, names: list[str], civs: list[int] = None, real_time_limit: int = 0, game_time_limit: int = 0):
        self.names = names
        if names is None or len(names) < 2 or len(names) > 8:
            raise Exception(f"List of names {names} not valid! Expected list of a least 2 and at most 8.")

        if civs is not None and len(civs) != len(names):
            raise Exception(f"The length of the civs {civs} does not match the length of the names {names}")

        if civs is None:
            civs = [17] * len(names)

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
        self.autogame.call('ResetGameSettings')  # usually reset the settings to make sure everything is valid
        self.autogame.call('SetGameMapType', 9)  # Set to Arabia
        self.autogame.call('SetGameDifficulty', 0)  # Set to hardest
        self.autogame.call('SetGameMapSize', 2)

        for index, name in enumerate(names):
            self.autogame.call('SetPlayerComputer', index + 1, name)
            self.autogame.call('SetPlayerCivilization', index + 1, civs[index])

        self.autogame.call('SetRunFullSpeed', True)  # run the game logic as fast as possible (experimental)
        # autogame.call('SetRunUnfocused', True)  # allow the game to run while minimized
        self.autogame.call('StartGame')  # start the match

        real_time = 0
        previous_game_time = -1

        while True:  # wait until the game has finished
            # If we are not responding, kill the game
            if not is_responding(self.aoc_proc.pid):
                print("Game has crashed.")
                self.kill_game()
                return None
            # If the game is no longer in progress
            if not self.autogame.call('GetGameInProgress'):
                break

            time.sleep(1.0)

            current_game_time = int(self.autogame.call('GetGameTime'))
            if current_game_time <= previous_game_time:
                print("The game time isn't progressing. The game has probably crashed.")
                self.kill_game()
                return None

            previous_game_time = current_game_time
            real_time += 1

            # If we are over our real time limit or game time limit
            if (0 < real_time_limit < real_time) or (0 < game_time_limit < current_game_time):
                break


        scores = [self.autogame.call("GetPlayerScore", i + 1) for i in range(len(names))]
        self.autogame.call('QuitGame')  # go back to the main menu
        self.autogame.close()
        self.autogame = None
        # print(scores)
        return scores

    def get_scores(self) -> list[int]:
        if self.autogame is None or not self.autogame.call('GetGameInProgress'):
            print("Cannot return scores when there's no game running!")
            return [0] * len(self.names)
        return [self.autogame.call("GetPlayerScore", i + 1) for i in range(len(self.names))]

    def kill_game(self):
        if self.aoc_proc is not None:
            self.aoc_proc.kill()
            self.aoc_proc = None
        if self.autogame is not None:
            self.autogame.call("QuitGame")
            time.sleep(1.0)
            self.autogame.close()
            self.autogame = None


l = Launcher()
l.launch_game(["HD"] * 8)

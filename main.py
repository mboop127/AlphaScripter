import random
import time
import subprocess
import os
import signal
import copy
from game_launcher import Launcher, GameSettings, GameStatus
from Functions import *
from settings import *

ai_names = ['parent', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

def setup_ai_files():
    for i in range(len(ai_names)):
        f = open(ai_names[i] + ".ai", "w+")
        f.write("")
        f.close()

def read_run_length():
    f = open("run_length.txt")
    length = int(f.read())
    f.close()

    return length

def extract_round_robin(score, time):
    p1 = 0
    p2 = 0
    if score[0] > score[1]:
        p1 += 1
    elif score[1] > score[0]:
        p2 += 1

    if time < .9 * game_time:
        #print("real win!")
        p1 *= 2
        p2 *= 2

    return p1, p2

def create_seeds(threshold):

    while True:

        gs = GameSettings(civilisations = ['huns'] * 4, names = ["parent","parent"],  game_time_limit = game_time)

        master_score_list = [[0,0,0,0,0,0,0,0]]

        #print("reset")

        ai_parent = generate_ai()

        write_ai(ai_parent, "parent")


        l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)
        master_score_list = [game.stats.scores for game in l.launch_games(instances=1) if game.status != GameStatus.EXCEPTED]

        score_list = [0,0,0,0,0,0,0,0]

        if master_score_list is not None:

            for i in range(len(master_score_list)):
                try:
                    for ai in range(len(ai_names)):
                        score_list[ai] += master_score_list[i][ai]
                except:
                    pass

                print(max(score_list))

                if max(score_list) > threshold:
                    save_ai(ai_parent,"seed")
                    return ai_parent

def extract_ffa(master_score):

    a,b,c,d = (0,0,0,0)

    for i in range(len(master_score)):
        local_score = master_score[i]

        sorted_list = sorted(local_score, reverse=True)

        if local_score[0] == sorted_list[0]:
            a += 2
        elif local_score[1] == sorted_list[0]:
            b += 2
        elif local_score[2] == sorted_list[0]:
            c += 2
        elif local_score[3] == sorted_list[0]:
            d += 2

        if local_score[0] == sorted_list[1]:
            a += 1
        elif local_score[1] == sorted_list[1]:
            b += 1
        elif local_score[2] == sorted_list[1]:
            c += 1
        elif local_score[3] == sorted_list[1]:
            d += 1

    #print((a,b,c,d))
    return a,b,c,d

def run_ffa(threshold,load):

    game_time = 5000
    force_resign = False
    score_list = [[0,0,0,0,0,0,0,0]]

    if load:
        ai_parent = read_ai("best")
    else:
        ai_parent = create_seeds(threshold)

    gs = GameSettings(civilisations = ['huns'] * 8, names = ai_names,  game_time_limit = game_time)

    second_place = copy.deepcopy(ai_parent)
    mutation_chance = default_mutation_chance

    generation = 1

    fails = 0

    while True:

        generation += 1

        crossed = crossover(ai_parent, second_place)
        b = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        c = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        d = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        e = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        f = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        g = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        h = mutate_ai(crossed)

        write_ai(ai_parent, "parent")
        write_ai(b, "b")
        write_ai(c, "c")
        write_ai(d, "d")
        write_ai(e, "e")
        write_ai(f, "f")
        write_ai(g, "g")
        write_ai(h, "h")

        # reads score
        l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)
        master_score_list = [[0,0,0,0,0,0,0,0]]
        master_score_list = [game.stats.scores for game in l.launch_games(instances=5) if game.status != GameStatus.EXCEPTED]
        score_list = [0,0,0,0,0,0,0,0]

        for i in range(len(master_score_list)):
            try:
                for ai in range(len(ai_names)):
                    score_list[ai] += master_score_list[i][ai]
            except:
                pass

        if score_list == [0,0,0,0,0,0,0,0] or score_list[0] == None or len(master_score_list) < 3:
            if generation == 1:
                generation -= 1

        else:

            while [0,0,0,0,0,0,0,0] in master_score_list:
                master_score_list.remove([0,0,0,0,0,0,0,0])

            parent_score = score_list[0]
            b_score = score_list[1]
            c_score = score_list[2]
            d_score = score_list[3]
            e_score = score_list[4]
            f_score = score_list[5]
            g_score = score_list[6]
            h_score = score_list[7]

            score_list = sorted(score_list, reverse=True)

            # checks number of rounds with no improvement and sets annealing
            if parent_score == max(score_list):
                fails += 1
                if fails % 2 == 0:
                    mutation_chance = min(default_mutation_chance + fails / (1000 * anneal_amount),.2)
                else:
                    mutation_chance = max(default_mutation_chance - fails / (1000 * anneal_amount),.001)
            else:
                fails = 0
                mutation_chance = default_mutation_chance

            failed = False

            if parent_score == max(score_list):
                failed = True
                winner = copy.deepcopy(ai_parent)
                second_place = copy.deepcopy(ai_parent)
                print("parent won by score: " + str(parent_score))

            elif b_score == max(score_list):
                winner = copy.deepcopy(b)
                print("b won by score: " + str(b_score))

            elif c_score == max(score_list):
                winner = copy.deepcopy(c)
                print("c won by score: " + str(c_score))

            elif d_score == max(score_list):
                winner = copy.deepcopy(d)
                print("d won by score: " + str(d_score))

            elif e_score == max(score_list):
                winner = copy.deepcopy(e)
                print("e won by score: " + str(e_score))

            elif f_score == max(score_list):
                winner = copy.deepcopy(f)
                print("f won by score: " + str(f_score))

            elif g_score == max(score_list):
                winner = copy.deepcopy(g)
                print("g won by score: " + str(g_score))

            elif h_score == max(score_list):
                winner = copy.deepcopy(h)
                print("h won by score: " + str(h_score))

            else:
                print("failed!!!")
                break

            # checks if second best for crossover, also gross and needs to be replaced later
            if not failed:

                if parent_score == score_list[1]:
                    second_place = copy.deepcopy(ai_parent)

                elif b_score == score_list[1]:
                    second_place = copy.deepcopy(b)

                elif c_score == score_list[1]:
                    second_place = copy.deepcopy(c)

                elif d_score == score_list[1]:
                    second_place = copy.deepcopy(d)

                elif e_score == score_list[1]:
                    second_place = copy.deepcopy(e)

                elif f_score == score_list[1]:
                    second_place = copy.deepcopy(f)

                elif g_score == score_list[1]:
                    second_place = copy.deepcopy(g)

                else:  # h_score == score_list[1]:
                    second_place = copy.deepcopy(h)


            ai_parent = copy.deepcopy(winner)
            write_ai(winner,"best")
            save_ai(winner, "best")

            #restarts after 10 fails
            if fails > fails_before_reset:
                print("fail threshold exceeded, reseting...")
                write_ai(winner, str(max(score_list)))
                save_ai(winner, str(max(score_list)))
                fails = 0
                generation = 0
                ai_parent = generate_ai()

def run_ffa_four(threshold,load):

    game_time = 5000
    force_resign = False
    score_list = [[0,0,0,0,0,0,0,0]]

    if load:
        ai_parent = read_ai("best")
    else:
        ai_parent = create_seeds(threshold)

    #temporary code
    #ai_parent = mutate_ai(copy.deepcopy(ai_parent))

    ai_names = ['parent','b','c','d']

    gs = GameSettings(civilisations = ['huns'] * 4, names = ai_names,  game_time_limit = game_time, map_id = 'arabia', map_size = 'tiny')

    second_place = copy.deepcopy(ai_parent)
    mutation_chance = default_mutation_chance

    generation = 1

    fails = 0

    while True:

        generation += 1

        crossed = crossover(ai_parent, second_place)
        b = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        c = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        d = mutate_ai(crossed)

        write_ai(ai_parent, "parent")
        write_ai(b, "b")
        write_ai(c, "c")
        write_ai(d, "d")

        # reads score
        l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)
        master_score_list = [[0,0,0,0,0,0,0,0]]
        master_score_list = [game.stats.scores for game in l.launch_games(instances = 5) if game.status != GameStatus.EXCEPTED]
        score_list = [0,0,0,0,0,0,0,0]

        for i in range(len(master_score_list)):
            try:
                for ai in range(len(ai_names)):
                    score_list[ai] += master_score_list[i][ai]
            except:
                pass

        if score_list == [0,0,0,0,0,0,0,0] or score_list[0] == None or len(master_score_list) < 3:
            fails += 1
            if generation == 1:
                generation -= 1

        else:

            #parent_score, b_score, c_score, d_score = extract_ffa(master_score_list)

            #score_list = [parent_score, b_score, c_score, d_score]

            parent_score = score_list[0]
            b_score = score_list[1]
            c_score = score_list[2]
            d_score = score_list[3]

            score_list = sorted(score_list, reverse=True)

            # checks number of rounds with no improvement and sets annealing
            if parent_score == max(score_list):
                fails += 1
                if fails % 2 == 0:
                    mutation_chance = min(default_mutation_chance + fails / (1000 * anneal_amount),.2)
                else:
                    mutation_chance = max(default_mutation_chance - fails / (1000 * anneal_amount),.001)
            else:
                fails = 0
                mutation_chance = default_mutation_chance

            failed = False

            if parent_score == max(score_list):
                failed = True
                winner = copy.deepcopy(ai_parent)
                second_place = copy.deepcopy(ai_parent)
                print("parent won by score: " + str(parent_score))

            elif b_score == max(score_list):
                winner = copy.deepcopy(b)
                print("b won by score: " + str(b_score))

            elif c_score == max(score_list):
                winner = copy.deepcopy(c)
                print("c won by score: " + str(c_score))

            elif d_score == max(score_list):
                winner = copy.deepcopy(d)
                print("d won by score: " + str(d_score))

            else:
                print("failed!!!")
                break

            # checks if second best for crossover, also gross and needs to be replaced later
            if not failed:

                if parent_score == score_list[1]:
                    second_place = copy.deepcopy(ai_parent)

                elif b_score == score_list[1]:
                    second_place = copy.deepcopy(b)

                elif c_score == score_list[1]:
                    second_place = copy.deepcopy(c)

                elif d_score == score_list[1]:
                    second_place = copy.deepcopy(d)


            ai_parent = copy.deepcopy(winner)
            write_ai(winner,"best")
            save_ai(winner, "best")

            #restarts after 10 fails
            if fails > fails_before_reset:
                print("fail threshold exceeded, reseting...")
                write_ai(winner, str(max(score_list)))
                save_ai(winner, str(max(score_list)))
                fails = 0
                generation = 0
                ai_parent = create_seeds(threshold)

def run_vs(threshold, load):

    if load:
        ai_parent = read_ai("best")
    else:
        ai_parent = create_seeds(threshold)

    fails = 0
    generation = 0
    winner = copy.deepcopy(ai_parent)

    score_list = [[0,0,0,0,0,0,0,0]]

    gs = GameSettings(civilisations = ['huns'] * 2, names = ['parent','b'], map_size = 'tiny',  game_time_limit = game_time)

    while True:

        generation += 1

        b = mutate_ai(copy.deepcopy(ai_parent))

        write_ai(ai_parent,"parent")
        write_ai(b, "b")

        failed = False


        l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)

        games =  l.launch_games(instances = 7,round_robin=False)
        games = [game for game in games if game.status != GameStatus.EXCEPTED]

        master_score_list = []
        times = []

        for game in games:
              master_score_list.append(game.stats.scores)
              times.append(game.stats.elapsed_game_time)

        score_list = [0,0]
        real_wins = 0

        for i in range(len(master_score_list)):
            #try:

            if master_score_list[i][1] > master_score_list[i][0]:
                real_wins += 1


        b_score = real_wins

        # checks number of rounds with no improvement and sets annealing
        if real_wins < 4:
            fails += 1
            if fails % 2 == 0:
                mutation_chance = min(default_mutation_chance + fails / (1000 * anneal_amount),.2)
            else:
                mutation_chance = max(default_mutation_chance - fails / (1000 * anneal_amount),.001)
        else:
            print("new best")
            winner = copy.deepcopy(b)
            fails = 0
            mutation_chance = default_mutation_chance

        ai_parent = copy.deepcopy(winner)
        write_ai(winner,"best")
        save_ai(winner, "best")

def run_vs_other(threshold, load, trainer, civs, robustness):

    force_resign = True
    game_time = 10000

    if load:
        ai_parent = read_ai("best")
    else:
        ai_parent = create_seeds(threshold)

    fails = 0
    generation = 0

    score_list = [[0,0,0,0,0,0,0,0]]

    gs = GameSettings(civilisations = civs, names = ['b',trainer], map_size = 'tiny',  game_time_limit = game_time)

    best = 0

    while True:

        generation += 1

        try:

            if generation != 1:
                b = mutate_ai(copy.deepcopy(ai_parent))
            else:
                b = copy.deepcopy(ai_parent)

            write_ai(b, "b")

            failed = False

            master_score_list = []
            times = []

            for i in range(robustness):

                l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)

                games =  l.launch_games(instances = 7,round_robin=False)
                games = [game for game in games if game.status != GameStatus.EXCEPTED]


                for game in games:
                      master_score_list.append(game.stats.scores)
                      times.append(game.stats.elapsed_game_time)

            score_list = [0,0]
            real_wins = 0

            for i in range(len(master_score_list)):
                #try:

                if master_score_list[i][0] > master_score_list[i][1]:
                    multiplier = (game_time/times[i]) * 2
                    if times[i]/game_time < .9:
                        real_wins += 1
                        multiplier *= 3
                else:
                    multiplier = 1

                score_list[0] += master_score_list[i][0] * multiplier
                #except:
                #    pass
                #    print("fail")

            if score_list != [0,0]:

                b_score = score_list[0]
                train_score = score_list[1]

                # checks number of rounds with no improvement and sets annealing
                if b_score < best:
                    fails += 1
                    if fails % 2 == 0:
                        mutation_chance = min(default_mutation_chance + fails / (1000 * anneal_amount),.2)
                    else:
                        mutation_chance = max(default_mutation_chance - fails / (1000 * anneal_amount),.001)
                else:
                    best = b_score
                    print(str(best) + " real wins: " + str(real_wins))
                    winner = copy.deepcopy(b)
                    fails = 0
                    mutation_chance = default_mutation_chance

                    ai_parent = copy.deepcopy(winner)
                    write_ai(winner,"best")
                    save_ai(winner, "best")


        except KeyboardInterrupt:
            input("enter anything to continue...")

def run_vs_self(threshold, load):

    force_resign = True
    game_time = 10000


    if load:
        ai_parent = read_ai("best")
    else:
        ai_parent = create_seeds(threshold)

    fails = 0
    generation = 0

    score_list = [[0,0,0,0,0,0,0,0]]

    gs = GameSettings(civilisations = ['huns'] * 2, names = ['b','self'], map_size = 'tiny',  game_time_limit = game_time)

    best = 0
    write_ai(ai_parent,"self")

    while True:

        generation += 1


        if generation != 1:
            b = mutate_ai(copy.deepcopy(ai_parent))
        else:
            b = copy.deepcopy(ai_parent)

        write_ai(b, "b")

        failed = False


        l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)

        games =  l.launch_games(instances = 7,round_robin=False)
        games = [game for game in games if game.status != GameStatus.EXCEPTED]

        master_score_list = []
        times = []

        for game in games:
              master_score_list.append(game.stats.scores)
              times.append(game.stats.elapsed_game_time)

        score_list = [0,0]
        real_wins = 0

        for i in range(len(master_score_list)):
            #try:

            if master_score_list[i][0] > master_score_list[i][1]:
                multiplier = (game_time/times[i]) * 2
                if times[i]/game_time < .9:
                    real_wins += 1
                    multiplier *= 3
            else:
                multiplier = 1

            score_list[0] += master_score_list[i][0] * multiplier
            #except:
            #    pass
            #    print("fail")

        if score_list != [0,0]:

            b_score = score_list[0]
            train_score = score_list[1]

            # checks number of rounds with no improvement and sets annealing
            if b_score < best:
                fails += 1
                if fails % 2 == 0:
                    mutation_chance = min(default_mutation_chance + fails / (1000 * anneal_amount),.2)
                else:
                    mutation_chance = max(default_mutation_chance - fails / (1000 * anneal_amount),.001)
            else:
                best = b_score
                print(str(best) + " real wins: " + str(real_wins))
                winner = copy.deepcopy(b)
                fails = 0
                mutation_chance = default_mutation_chance

                ai_parent = copy.deepcopy(winner)
                write_ai(winner,"best")
                save_ai(winner, "best")

            if real_wins == 7:
                write_ai(winner,"self")
                print("reset!")
                best = 0

def run_robin(threshold,load):

    generation = 1
    fails = 0

    mutation_chance = default_mutation_chance

    if load:
        ai_parent = read_ai("best")
    else:
        ai_parent = create_seeds(threshold)

    second_place = copy.deepcopy(ai_parent)

    gs = GameSettings(civilisations = ['huns'] * 5, names = ['parent','b','c','d'], map_size = 'tiny',  game_time_limit = game_time, map_id = 'arabia')

    while True:

        crossed = crossover(ai_parent, second_place)
        b = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        c = mutate_ai(crossed)

        crossed = crossover(ai_parent, second_place)
        d = mutate_ai(crossed)

        write_ai(ai_parent, "parent")
        write_ai(b, "b")
        write_ai(c, "c")
        write_ai(d, "d")


        generation += 1

        failed = False

        parent_score, b_score, c_score, d_score = (0,0,0,0)
        score_list = [0,0,0,0]

        for trials in range(1):

            l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)
            #master_score_list = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
            #[p,b],[p,c],[p,d],[b,c],[b,d][c,d]
            games =  l.launch_games(round_robin=True)
            games = [game for game in games if game.status != GameStatus.EXCEPTED]
            master_score_list = []
            times = []
            skip = False

            for game in games:
                  master_score_list.append(game.stats.scores)
                  times.append(game.stats.elapsed_game_time)

            if len(master_score_list) == 6:

                parent_temp_score, b_temp_score = extract_round_robin(master_score_list[0],times[0])
                parent_score += parent_temp_score
                b_score += b_temp_score

                parent_temp_score, c_temp_score = extract_round_robin(master_score_list[1],times[1])
                parent_score += parent_temp_score
                c_score += c_temp_score

                parent_temp_score, d_temp_score = extract_round_robin(master_score_list[2],times[2])
                parent_score += parent_temp_score
                d_score += d_temp_score

                b_temp_score, c_temp_score = extract_round_robin(master_score_list[3],times[3])
                b_score += b_temp_score
                c_score += c_temp_score

                b_temp_score, d_temp_score = extract_round_robin(master_score_list[4],times[4])
                b_score += b_temp_score
                d_score += d_temp_score

                c_temp_score, d_temp_score = extract_round_robin(master_score_list[5],times[5])
                c_score += c_temp_score
                d_score += d_temp_score

                score_list = [parent_score, b_score, c_score, d_score]
                score_list = sorted(score_list, reverse=True)
                fail = False

            else:
                parent_score, b_score, c_score, d_score = (0,0,0,0)
                skip = True
                break

        if not skip:
            # checks number of rounds with no improvement and sets annealing
            if parent_score == max(score_list):
                fails += 1
                if fails % 2 == 0:
                    mutation_chance = min(default_mutation_chance + fails / (1000 * anneal_amount),.2)
                else:
                    mutation_chance = max(default_mutation_chance - fails / (1000 * anneal_amount),.001)
                fail = True
            else:
                fails = 0
                mutation_chance = default_mutation_chance

            if parent_score == max(score_list) or max(score_list) == 0:
                winner = copy.deepcopy(ai_parent)
                second_place = copy.deepcopy(ai_parent)
                print("parent won by score: " + str(parent_score))

            elif b_score == max(score_list):
                winner = copy.deepcopy(b)
                print("b won by score: " + str(b_score))

            elif c_score == max(score_list):
                winner = copy.deepcopy(c)
                print("c won by score: " + str(c_score))

            elif d_score == max(score_list):
                winner = copy.deepcopy(d)
                print("d won by score: " + str(d_score))


            if not fail:

                if parent_score == score_list[1]:
                    second_place = copy.deepcopy(ai_parent)

                elif b_score == score_list[1]:
                    second_place = copy.deepcopy(b)

                elif c_score == score_list[1]:
                    second_place = copy.deepcopy(c)

                elif d_score == score_list[1]:
                    second_place = copy.deepcopy(d)

            ai_parent = copy.deepcopy(winner)
            write_ai(winner,"best")
            save_ai(winner, "best")

            #restarts after 10 fails
            if fails > fails_before_reset:
                print("fail threshold exceeded, reseting...")
                write_ai(winner, str(max(score_list)))
                save_ai(winner, str(max(score_list)))
                fails = 0
                generation = 0
                ai_parent = generate_ai()

def benchmarker(ai1, ai2, rounds, civs):

    force_resign = True
    game_time = 10000

    gs = GameSettings(civilisations = civs, names = [ai1,ai2], map_size = 'tiny',  game_time_limit = game_time)

    ai1_wins = 0
    ai2_wins = 0
    stalemates = 0
    failed_games = 0

    rounds = int(rounds/7)

    for x in range(rounds):

        print(x)

        l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)

        games =  l.launch_games(instances = 7,round_robin=False)
        games = [game for game in games if game.status != GameStatus.EXCEPTED]

        master_score_list = []
        times = []

        for game in games:
              master_score_list.append(game.stats.scores)
              times.append(game.stats.elapsed_game_time)

        score_list = [0,0]

        for i in range(len(master_score_list)):

            if master_score_list[i][0] > master_score_list[i][1] and times[i]/game_time < .9:
                ai1_wins += 1
            elif master_score_list[i][0] < master_score_list[i][1] and times[i]/game_time < .9:
                ai2_wins += 1
            elif master_score_list[i][0] == [0,0]:
                failed_games += 1
            else:
                stalemates += 1

    print(str(ai1_wins) + "/" + str(ai2_wins) + "/" + str(stalemates) + "/" + str(failed_games))

#run_ffa_four(0,True)
#run_ffa(0,False)
#run_vs(0, True)
#run_vs_other(0,True,"Shadow 0",['huns','huns'],2)
#run_vs_self(0,True)
run_robin(0,True)
#benchmarker("best","Shadow 0",100,['huns','huns'])

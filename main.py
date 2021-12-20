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

    if time < .8 * game_time:
        p1 *= 2
        p2 *= 2

    return p1, p2

def run_ffa(threshold,load):

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

        if score_list == [0,0,0,0,0,0,0,0] or score_list[0] == None:
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
                    mutation_chance = default_mutation_chance + fails / 2000
                else:
                    mutation_chance = default_mutation_chance - fails / 2000
            else:
                fails = 0
                mutation_chance = default_mutation_chance

            failed = False

            if parent_score == max(score_list):
                failed = True
                winner = copy.deepcopy(ai_parent)
                second_place = copy.deepcopy(ai_parent)
                print("parent won by score: " + str(parent_score/len(master_score_list)))

            elif b_score == max(score_list):
                winner = copy.deepcopy(b)
                print("b won by score: " + str(b_score/len(master_score_list)))

            elif c_score == max(score_list):
                winner = copy.deepcopy(c)
                print("c won by score: " + str(c_score/len(master_score_list)))

            elif d_score == max(score_list):
                winner = copy.deepcopy(d)
                print("d won by score: " + str(d_score/len(master_score_list)))

            elif e_score == max(score_list):
                winner = copy.deepcopy(e)
                print("e won by score: " + str(e_score/len(master_score_list)))

            elif f_score == max(score_list):
                winner = copy.deepcopy(f)
                print("f won by score: " + str(f_score/len(master_score_list)))

            elif g_score == max(score_list):
                winner = copy.deepcopy(g)
                print("g won by score: " + str(g_score/len(master_score_list)))

            elif h_score == max(score_list):
                winner = copy.deepcopy(h)
                print("h won by score: " + str(h_score/len(master_score_list)))

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

    score_list = [[0,0,0,0,0,0,0,0]]

    if load:
        ai_parent = read_ai("best")
    else:
        ai_parent = create_seeds(threshold)

    ai_names = ['parent','b','c','d']

    gs = GameSettings(civilisations = ['huns'] * 4, names = ai_names,  game_time_limit = game_time)

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
        master_score_list = [game.stats.scores for game in l.launch_games(instances=10) if game.status != GameStatus.EXCEPTED]
        score_list = [0,0,0,0,0,0,0,0]

        for i in range(len(master_score_list)):
            try:
                for ai in range(len(ai_names)):
                    score_list[ai] += master_score_list[i][ai]
            except:
                pass

        if score_list == [0,0,0,0,0,0,0,0] or score_list[0] == None:
            if generation == 1:
                generation -= 1

        else:

            while [0,0,0,0,0,0,0,0] in master_score_list:
                master_score_list.remove([0,0,0,0,0,0,0,0])

            parent_score = score_list[0]
            b_score = score_list[1]
            c_score = score_list[2]
            d_score = score_list[3]


            score_list = sorted(score_list, reverse=True)

            # checks number of rounds with no improvement and sets annealing
            if parent_score == max(score_list):
                fails += 1
                if fails % 2 == 0:
                    mutation_chance = default_mutation_chance + fails / 2000
                else:
                    mutation_chance = default_mutation_chance - fails / 2000
            else:
                fails = 0
                mutation_chance = default_mutation_chance

            failed = False

            if parent_score == max(score_list):
                failed = True
                winner = copy.deepcopy(ai_parent)
                second_place = copy.deepcopy(ai_parent)
                print("parent won by score: " + str(parent_score/len(master_score_list)))

            elif b_score == max(score_list):
                winner = copy.deepcopy(b)
                print("b won by score: " + str(b_score/len(master_score_list)))

            elif c_score == max(score_list):
                winner = copy.deepcopy(c)
                print("c won by score: " + str(c_score/len(master_score_list)))

            elif d_score == max(score_list):
                winner = copy.deepcopy(d)
                print("d won by score: " + str(d_score/len(master_score_list)))

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
                ai_parent = generate_ai()

def run_vs(ai_parent):

    generation = 0
    #generation = 1
    fails = 0

    score_list = [[0,0,0,0,0,0,0,0]]

    gs = GameSettings(civilisations = ['huns'] * 2, names = ['parent','b'], map_size = 'tiny',  game_time_limit = game_time)

    if generation == 0:
        while score_list == [[0,0,0,0,0,0,0,0]] or score_list == None or score_list == []:
            print("reset")

            ai_parent = []

            ai_parent = generate_ai()

            write_ai(ai_parent, "parent")
            write_ai(ai_parent, "b")

            l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)
            score_list = [game.stats.scores for game in l.launch_games(instances=1) if game.status != GameStatus.EXCEPTED]


    while True:

        generation += 1

        try:

            b = mutate_ai(ai_parent.copy.deepcopy())
            write_ai(ai_parent, "parent")
            write_ai(b, "b")

            failed = False


            l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)
            master_score_list = [game.stats.scores for game in l.launch_games(instances=10, round_robin=False) if game.status != GameStatus.EXCEPTED]
            score_list = [0,0]

            for i in range(len(master_score_list)):
                try:
                    for ai in range(len(ai_names)):
                        score_list[ai] += master_score_list[i][ai]
                except:
                    pass

            else:

                parent_score = score_list[0]
                b_score = score_list[1]

                # checks number of rounds with no improvement and sets annealing
                if parent_score == max(score_list):
                    fails += 1
                    #if fails % 2 == 0:
                    #    mutation_chance = default_mutation_chance + fails / 1000
                    #else:
                    #    mutation_chance = default_mutation_chance - fails / 1000
                    #fail = True
                else:
                    fails = 0
                    #mutation_chance = .05


                if parent_score == max(score_list):
                    winner = ai_parent.copy.deepcopy()
                    print("parent won by score: " + str(parent_score))

                elif b_score == max(score_list):
                    winner = b.copy.deepcopy()
                    print("b won by score: " + str(b_score))


                ai_parent = winner.copy.deepcopy()
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

        except KeyboardInterrupt:
            input("enter anything to continue...")

def run_robin(threshold,load):

    generation = 1
    fails = 0

    mutation_chance = default_mutation_chance

    if load:
        ai_parent = read_ai("best")
    else:
        ai_parent = create_seeds(threshold)

    second_place = copy.deepcopy(ai_parent)

    gs = GameSettings(civilisations = ['huns'] * 5, names = ['parent','b','c','d'], map_size = 'tiny',  game_time_limit = game_time)

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

        for trials in range(3):

            l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)
            #master_score_list = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
            #[p,b],[p,c],[p,d],[b,c],[b,d][c,d]
            games =  l.launch_games(round_robin=True)
            games = [game for game in games if game.status != GameStatus.EXCEPTED]
            master_score_list = []
            times = []

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
                break

        # checks number of rounds with no improvement and sets annealing
        if parent_score == max(score_list):
            fails += 1
            if fails % 2 == 0:
                mutation_chance = default_mutation_chance + fails / 1000
            else:
                mutation_chance = default_mutation_chance - fails / 1000
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
                    return ai_parent

#run_ffa_four(0,False)
#run_vs(ai_parent)
run_robin(0,False)

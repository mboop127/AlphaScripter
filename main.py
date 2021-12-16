import random
import time
import subprocess
import os
import signal
from game_launcher import Launcher, GameSettings, GameStatus
from Functions import *

#controls for algorithm
fails_before_reset = 50
game_time = 1000

#default_mutation_chance = .0
#mutation_chance = .0
#max_fact_length = 6
#max_action_length = 2
#ai_length = 300

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

def run_ffa(ai_parent):
    #global mutation_chance

    generation = 0
    #generation = 1

    score_list = [[0,0,0,0,0,0,0,0]]

    if generation == 0:
        ai_parent = create_seeds()

    gs = GameSettings(civilisations = ['huns'] * 8, names = ai_names,  game_time_limit = game_time)

    second_place = ai_parent.copy()

    generation = 1

    fails = 0

    while True:

        generation += 1

        #b = mutate_ai(crossed)
        #crossed = crossover(ai_parent, second_place)

        #crossed = crossover(ai_parent, second_place)
        #c = mutate_ai(crossed)

        #crossed = crossover(ai_parent, second_place)
        #d = mutate_ai(crossed)

        #crossed = crossover(ai_parent, second_place)
        #e = mutate_ai(crossed)

        #crossed = crossover(ai_parent, second_place)
        #f = mutate_ai(crossed)

        #crossed = crossover(ai_parent, second_place)
        #g = mutate_ai(crossed)

        #crossed = crossover(ai_parent, second_place)
        #h = mutate_ai(crossed)

        b = mutate_ai(ai_parent.copy())
        c = mutate_ai(ai_parent.copy())
        d = mutate_ai(ai_parent.copy())
        e = mutate_ai(ai_parent.copy())
        f = mutate_ai(ai_parent.copy())
        g = mutate_ai(ai_parent.copy())
        h = mutate_ai(ai_parent.copy())

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
            #print("fail")
            if generation == 1:
                generation -= 1
                #ai_parent = generate_ai()

        else:

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
                #if fails % 2 == 0:
                #    mutation_chance = default_mutation_chance + fails / 2000
                #else:
                #    mutation_chance = default_mutation_chance - fails / 2000
            else:
                fails = 0
                #mutation_chance = default_mutation_chance

            failed = False

            if parent_score == max(score_list):
                failed = True
                winner = ai_parent.copy()
                second_place = ai_parent.copy()
                print("parent won by score: " + str(parent_score))

            elif b_score == max(score_list):
                winner = b.copy()
                print("b won by score: " + str(b_score))

            elif c_score == max(score_list):
                winner = c.copy()
                print("c won by score: " + str(c_score))

            elif d_score == max(score_list):
                winner = d.copy()
                print("d won by score: " + str(d_score))

            elif e_score == max(score_list):
                winner = e.copy()
                print("e won by score: " + str(e_score))

            elif f_score == max(score_list):
                winner = f.copy()
                print("f won by score: " + str(f_score))

            elif g_score == max(score_list):
                winner = g.copy()
                print("g won by score: " + str(g_score))

            else:  # h_score == max(score_list):
                winner = h.copy()
                print("h won by score: " + str(h_score))

            # checks if second best for crossover, also gross and needs to be replaced later
            if not failed:

                if parent_score == score_list[1]:
                    second_place = ai_parent.copy()

                elif b_score == score_list[1]:
                    second_place = b.copy()

                elif c_score == score_list[1]:
                    second_place = c.copy()

                elif d_score == score_list[1]:
                    second_place = d.copy()

                elif e_score == score_list[1]:
                    second_place = e.copy()

                elif f_score == score_list[1]:
                    second_place = f.copy()

                elif g_score == score_list[1]:
                    second_place = g.copy()

                else:  # h_score == score_list[1]:
                    second_place = h.copy()


            ai_parent = winner.copy()
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

            b = mutate_ai(ai_parent.copy())
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
                    winner = ai_parent.copy()
                    print("parent won by score: " + str(parent_score))

                elif b_score == max(score_list):
                    winner = b.copy()
                    print("b won by score: " + str(b_score))


                ai_parent = winner.copy()
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

def run_robin(genesParent, rulesParent):
    global mutation_chance

    second_placeRules = rulesParent.copy()
    second_place = genesParent.copy()

    #generation = 0
    generation = 1
    fails = 0

    gs = GameSettings(civilisations = ['huns'] * 4, names = ['parent','b','c','d'], map_size = 'tiny',  game_time_limit = game_time)

    while True:

        generation += 1

        try:

            alphaDNA = genesParent.copy()
            alphaRules = rulesParent.copy()

            crossed_rules, crossed_genes = crossover(rulesParent, second_placeRules, genesParent, second_place)
            betaDNA = mutate_constants(crossed_genes)
            betaRules = mutate_rules(crossed_rules)

            crossed_rules, crossed_genes = crossover(rulesParent, second_placeRules, genesParent, second_place)
            cDNA = mutate_constants(crossed_genes)
            cRules = mutate_rules(crossed_rules)

            crossed_rules, crossed_genes = crossover(rulesParent, second_placeRules, genesParent, second_place)
            dDNA = mutate_constants(crossed_genes)
            dRules = mutate_rules(crossed_rules)

            write_ai(alphaDNA, alphaRules, "parent")
            write_ai(betaDNA, betaRules, "b")
            write_ai(cDNA, cRules, "c")
            write_ai(dDNA, dRules, "d")

            # reads score

            failed = False

            l = Launcher(executable_path = "C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe", settings = gs)
            #master_score_list = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
            #[p,b],[p,c],[p,d],[b,c],[b,d][c,d]
            games =  l.launch_games(round_robin=True)
            games = [game for game in games if game.status != GameStatus.EXCEPTED]
            master_score_list = []
            times = []

            #print(len(games))

            if len(games) == 6:
                for game in games:
                      master_score_list.append(game.stats.scores)
                      times.append(game.stats.elapsed_game_time)

                parent_score, b_score, c_score, d_score = (0,0,0,0)

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

                fail = False

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
                    mutation_chance = .05


                if parent_score == max(score_list) or max(score_list) == 0:
                    winner = genesParent.copy()
                    winnerRules = rulesParent.copy()
                    second_place = genesParent.copy()
                    second_placeRules = rulesParent.copy()
                    print("parent won by score: " + str(parent_score))

                elif b_score == max(score_list):
                    winner = betaDNA.copy()
                    winnerRules = betaRules.copy()
                    print("b won by score: " + str(b_score))

                elif c_score == max(score_list):
                    winner = cDNA.copy()
                    winnerRules = cRules.copy()
                    print("c won by score: " + str(c_score))

                elif d_score == max(score_list):
                    winner = dDNA.copy()
                    winnerRules = dRules.copy()
                    print("d won by score: " + str(d_score))

                if not fail:

                    if parent_score == score_list[1]:
                        second_place = genesParent.copy()
                        second_placeRules = rulesParent.copy()

                    elif b_score == score_list[1]:
                        second_place = betaDNA.copy()
                        second_placeRules = betaRules.copy()

                    elif c_score == score_list[1]:
                        second_place = cDNA.copy()
                        second_placeRules = cRules.copy()

                    elif d_score == score_list[1]:
                        second_place = dDNA.copy()
                        second_placeRules = dRules.copy()

                genesParent = winner.copy()
                rulesParent = winnerRules.copy()
                write_ai(winner, winnerRules, "best", to_ai_folder=False)
                save_ai(winnerRules, winner, "best")

                #restarts after 10 fails
                if fails > fails_before_reset:
                    print("fail threshold exceeded, reseting...")
                    write_ai(winner, winnerRules, str(max(score_list)), to_ai_folder=False)
                    save_ai(winnerRules, winner, str(max(score_list)))
                    fails = 0
                    generation = 0
                    rulesParent, genesParent = generate_script(script_rule_count)

            else:
                print("failed")

        except KeyboardInterrupt:
            input("enter anything to continue...")

def create_seeds():

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

                if max(score_list) > 1161:
                    return ai_parent



#ai_parent = read_ai("best")
ai_parent = generate_ai()

run_ffa(ai_parent)
#run_vs(ai_parent)
#run_robin(genesParent, rulesParent)

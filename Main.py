import random
import time
import subprocess
import os
import signal
from game_launcher import Launcher

#controls for algorithm
fails_before_reset = 20
script_rule_count = 400
mutation_chance = .05

# alphabet = 'abcdefghijklmnopqrstuvwxyz'
# temp = []
# alphavalues = []
# for x in alphabet:
#    for y in alphabet:
#        temp.append(x + y)
#
# for i in range(300):
#    alphavalues.append(temp[i])

alphavalues = ['aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap', 'aq',
               'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'bg', 'bh',
               'bi', 'bj', 'bk', 'bl', 'bm', 'bn', 'bo', 'bp', 'bq', 'br', 'bs', 'bt', 'bu', 'bv', 'bw', 'bx', 'by',
               'bz', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'cg', 'ch', 'ci', 'cj', 'ck', 'cl', 'cm', 'cn', 'co', 'cp',
               'cq', 'cr', 'cs', 'ct', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'da', 'db', 'dc', 'dd', 'de', 'df', 'dg',
               'dh', 'di', 'dj', 'dk', 'dl', 'dm', 'dn', 'do', 'dp', 'dq', 'dr', 'ds', 'dt', 'du', 'dv', 'dw', 'dx',
               'dy', 'dz', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'eg', 'eh', 'ei', 'ej', 'ek', 'el', 'em', 'en', 'eo',
               'ep', 'eq', 'er', 'es', 'et', 'eu', 'ev', 'ew', 'ex', 'ey', 'ez', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff',
               'fg', 'fh', 'fi', 'fj', 'fk', 'fl', 'fm', 'fn', 'fo', 'fp', 'fq', 'fr', 'fs', 'ft', 'fu', 'fv', 'fw',
               'fx', 'fy', 'fz', 'ga', 'gb', 'gc', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gj', 'gk', 'gl', 'gm', 'gn',
               'go', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gv', 'gw', 'gx', 'gy', 'gz', 'ha', 'hb', 'hc', 'hd', 'he',
               'hf', 'hg', 'hh', 'hi', 'hj', 'hk', 'hl', 'hm', 'hn', 'ho', 'hp', 'hq', 'hr', 'hs', 'ht', 'hu', 'hv',
               'hw', 'hx', 'hy', 'hz', 'ia', 'ib', 'ic', 'id', 'ie', 'if', 'ig', 'ih', 'ii', 'ij', 'ik', 'il', 'im',
               'in', 'io', 'ip', 'iq', 'ir', 'is', 'it', 'iu', 'iv', 'iw', 'ix', 'iy', 'iz', 'ja', 'jb', 'jc', 'jd',
               'je', 'jf', 'jg', 'jh', 'ji', 'jj', 'jk', 'jl', 'jm', 'jn', 'jo', 'jp', 'jq', 'jr', 'js', 'jt', 'ju',
               'jv', 'jw', 'jx', 'jy', 'jz', 'ka', 'kb', 'kc', 'kd', 'ke', 'kf', 'kg', 'kh', 'ki', 'kj', 'kk', 'kl',
               'km', 'kn', 'ko', 'kp', 'kq', 'kr', 'ks', 'kt', 'ku', 'kv', 'kw', 'kx', 'ky', 'kz', 'la', 'lb', 'lc',
               'ld', 'le', 'lf', 'lg', 'lh', 'li', 'lj', 'lk', 'll', 'lm', 'ln']

ai_names = ['parent', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# read pre parsed actions
f = open("actions.txt", "r")
actions = f.read().split("\n")
f.close()

# read pre parsed facts
f = open("conditions.txt", "r")
conditions = f.read().split("\n")
f.close()

def setup_ai_files():
    for i in range(len(ai_names)):
        f = open(ai_names[i] + ".ai", "w+")
        f.write("")
        f.close()

def crossover(rule1, rule2, alpha1, alpha2):
    global mutation_chance

    rules_out = []
    for i in range(len(rule1)):

        if random.random() < .5:
            if random.random() < mutation_chance:
                rules_out.append(random.choice(rule1))
            else:
                rules_out.append(rule1[i])
        else:
            if random.random() < mutation_chance:
                rules_out.append(random.choice(rule2))
            else:
                rules_out.append(rule2[i])

    alphas_out = []
    for i in range(len(alpha1)):

        if random.random() < .5:
            if random.random() < mutation_chance:
                alphas_out.append(random.choice(alpha1))
            else:
                alphas_out.append(alpha1[i])
        else:
            if random.random() < mutation_chance:
                alphas_out.append(random.choice(alpha2))
            else:
                alphas_out.append(alpha2[i])

    return rules_out, alphas_out


def read_best():
    f = open("best.txt", "r")

    file = f.read().split("\n")

    f.close()

    file_rules = file[0].split("|")
    file_constants = file[1].split(",")

    constants_out = []
    for i in range(len(file_constants)):
        if file_constants[i] != "":
            constants_out.append(int(file_constants[i]))

    rules_out = []
    for i in range(len(file_rules)):
        if file_rules[i] != "":
            local_rule = file_rules[i].split(",")
            local_conditions = [local_rule[0], local_rule[1], local_rule[2], local_rule[3], local_rule[4]]
            local_actions = [local_rule[5], local_rule[6], local_rule[7], local_rule[8], local_rule[9]]
            local_alphas = [local_rule[10], local_rule[11], local_rule[12], local_rule[13], local_rule[14],
                            local_rule[15], local_rule[16], local_rule[17], local_rule[18], local_rule[19]]
            if_and = int(local_rule[20])
            action_length = int(local_rule[21])
            condition_length = int(local_rule[22])
            age_required = int(local_rule[23])
            # print(local_rule)

            rules_out.append([local_conditions, local_actions, local_alphas, if_and, action_length, condition_length, age_required])

    return rules_out, constants_out


def static_code():
    f = open("Goals.txt", "r")
    goals = f.read()
    f.close()

    f = open("constants.txt", "r")
    statics = f.read()
    f.close()

    return goals + "\n\n\n" + statics


def read_run_length():
    f = open("run_length.txt")
    length = int(f.read())
    f.close()

    return length


def generate_constants():
    temp = []
    for i in range(300):
        temp.append(random.randint(0, 200))
    return temp


def generate_rules(count):
    rules = []

    for i in range(count):
        conditions1 = [random.choice(conditions), random.choice(conditions), random.choice(conditions),
                       random.choice(conditions), random.choice(conditions)]
        actions1 = [random.choice(actions), random.choice(actions), random.choice(actions), random.choice(actions),
                    random.choice(actions)]
        alphavalues1 = [random.choice(alphavalues), random.choice(alphavalues), random.choice(alphavalues),
                        random.choice(alphavalues), random.choice(alphavalues), random.choice(alphavalues),
                        random.choice(alphavalues), random.choice(alphavalues), random.choice(alphavalues),
                        random.choice(alphavalues)]
        if_and = random.randint(1, 3)
        action_length = random.randint(1, 4)
        condition_length = random.randint(1, 4)
        age_required = random.randint(0, 3)

        rules.append([conditions1, actions1, alphavalues1, if_and, action_length, condition_length, age_required])

        # print(conditions1)
    return rules


def mutate_rules(list):
    global mutation_chance

    rules1 = []

    for x in range(len(list)):
        conditions1 = list[x][0].copy()
        actions1 = list[x][1].copy()
        alphavalues1 = list[x][2].copy()
        if_and = list[x][3]
        action_length = list[x][4]
        condition_length = list[x][5]
        age_required = list[x][6]

        for i in range(len(conditions1)):
            conditions1[i] = mutate_single(conditions, conditions1[i])
            actions1[i] = mutate_single(actions, actions1[i])

        for i in range(len(alphavalues1)):
            alphavalues1[i] = mutate_single(alphavalues, alphavalues1[i])

        if random.random() < mutation_chance:
            if_and = random.randint(1, 3)

        if random.random() < mutation_chance:
            action_length = random.randint(1, 5)

        if random.random() < mutation_chance:
            condition_length = random.randint(1, 5)

        if random.random() < mutation_chance:
            age_required = random.randint(0, 3)

        rules1.append([conditions1, actions1, alphavalues1, if_and, action_length, condition_length, age_required])

    return rules1


def mutate_single(list, item):
    global mutation_chance

    if random.random() < mutation_chance:
        return random.choice(list)
    else:
        return item

def save_ai(rules, alphavalues, name):
    f = open(name + ".txt", "w+")
    for i in range(len(rules)):
        conditions1 = rules[i][0].copy()
        actions1 = rules[i][1].copy()
        constants1 = rules[i][2].copy()
        if_and = rules[i][3]
        action_length = rules[i][4]
        condition_length = rules[i][5]
        age_required = rules[i][6]

        f.write("|")
        for x in range(len(conditions1)):
            f.write(conditions1[x] + ",")
        for x in range(len(actions1)):
            f.write(actions1[x] + ",")
        for x in range(len(constants1)):
            f.write(constants1[x] + ",")
        f.write(str(if_and) + ",")
        f.write(str(action_length) + ",")
        f.write(str(condition_length) + ",")
        f.write(str(age_required))

    f.write("\n")
    for i in range(len(alphavalues)):
        f.write(str(alphavalues[i]) + ",")
    f.close()


def write_rules(list):
    string = ""

    # print(list)

    for i in range(len(list)):

        conditions1 = list[i][0].copy()
        actions1 = list[i][1].copy()
        alphavalues1 = list[i][2].copy()
        if_and = list[i][3]
        action_length = list[i][4]
        condition_length = list[i][5]
        age_required = list[i][6]


        load_if_value = ["",""]

        if age_required == 1:
            load_if_value = ["#load-if-not-defined DARK-AGE-END\n","#end-if\n"]

        elif age_required == 2:
            load_if_value = ["#load-if-not-defined FEUDAL-AGE-END\n","#end-if\n"]

        elif age_required == 3:
            load_if_value = ["#load-if-not-defined CASTLE-AGE-END\n","#end-if\n"]

        string += load_if_value[0] + "(defrule\n"
        if_and_value = ["", ""]

        if condition_length == 2:
            if if_and == 1:
                string += "(or"
                if_and_value[0] = "\t"
                if_and_value[1] = ")"

            elif if_and == 2:
                string += "(and"
                if_and_value[0] = "\t"
                if_and_value[1] = ")"

        for i in range(condition_length):
            string += if_and_value[0] + conditions1[i].replace("AlphaMorphValue", alphavalues1[i]) + "\n"

        string += if_and_value[1] + "\n=>\n"

        for i in range(action_length):
            string += actions1[i].replace("AlphaMorphValue", alphavalues1[5 + i]) + "\n"

        string += ")\n" + load_if_value[1] + "\n"

    return string


def mutate_constants(list):
    global mutation_chance

    list2 = list.copy()
    for i in range(len(list2)):

        if random.random() < .01:
            list2[i] = random.randint(0, 200)

        elif random.random() < mutation_chance:
            list2[i] += random.randint(-10, 10)
            list2[i] = max(0, list2[i])

    return list2


def write_ai(list, rules, name: str, to_ai_folder: bool = True):
    constant_write = ""
    for i in range(len(alphavalues)):
        constant_write += "\n(defconst " + alphavalues[i] + " " + str(list[i]) + ")"

    with open(name + ".per", "w+") as ai_file:
        ai_file.write(static_code() + "\n\n\n")
        ai_file.write(constant_write)
        ai_file.write("\n\n\n")
        ai_file.write(write_rules(rules))
        ai_file.write("\n\n\n")

def generate_script(length):

    print("generating new script")
    genesParent = generate_constants()
    rulesParent = generate_rules(length)

    return rulesParent, genesParent

def run_ffa(genesParent, rulesParent):
    global mutation_chance

    second_placeRules = rulesParent.copy()
    second_place = genesParent.copy()

    #generation = 0
    generation = 1
    fails = 0

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

            crossed_rules, crossed_genes = crossover(rulesParent, second_placeRules, genesParent, second_place)
            eDNA = mutate_constants(crossed_genes)
            eRules = mutate_rules(crossed_rules)

            crossed_rules, crossed_genes = crossover(rulesParent, second_placeRules, genesParent, second_place)
            fDNA = mutate_constants(crossed_genes)
            fRules = mutate_rules(crossed_rules)

            crossed_rules, crossed_genes = crossover(rulesParent, second_placeRules, genesParent, second_place)
            gDNA = mutate_constants(crossed_genes)
            gRules = mutate_rules(crossed_rules)

            crossed_rules, crossed_genes = crossover(rulesParent, second_placeRules, genesParent, second_place)
            hDNA = mutate_constants(crossed_genes)
            hRules = mutate_rules(crossed_rules)

            alphaDNA = genesParent.copy()
            alphaRules = rulesParent.copy()

            write_ai(alphaDNA, alphaRules, "parent")
            write_ai(betaDNA, betaRules, "b")
            write_ai(cDNA, cRules, "c")
            write_ai(dDNA, dRules, "d")
            write_ai(eDNA, eRules, "e")
            write_ai(fDNA, fRules, "f")
            write_ai(gDNA, gRules, "g")
            write_ai(hDNA, hRules, "h")

            # reads score
            l = Launcher("C:\\Program Files\\Microsoft Games\\Age of Empires II\\age2_x1.5.exe")
            master_score_list = l.launch_game(ai_names, real_time_limit = 300, game_time_limit = 4000, number_of_instances = 2)
            score_list = [0,0,0,0,0,0,0,0]

            for i in range(len(master_score_list)):
                try:
                    for ai in range(len(ai_names)):
                        score_list[ai] += master_score_list[i]
                except:
                    pass

            if score_list == [0,0,0,0,0,0,0,0] or score_list[0] == None:
                if generation == 1:
                    generation -= 1
                    rulesParent, genesParent = generate_script(script_rule_count)

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
                    mutation_chance += fails / 1000
                else:
                    fails = 0
                    mutation_chance = .05

                failed = False

                if parent_score == max(score_list):
                    failed = True
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

                elif e_score == max(score_list):
                    winner = eDNA.copy()
                    winnerRules = eRules.copy()
                    print("e won by score: " + str(e_score))

                elif f_score == max(score_list):
                    winner = fDNA.copy()
                    winnerRules = fRules.copy()
                    print("f won by score: " + str(f_score))

                elif g_score == max(score_list):
                    winner = gDNA.copy()
                    winnerRules = gRules.copy()
                    print("g won by score: " + str(g_score))

                else:  # h_score == max(score_list):
                    winner = hDNA.copy()
                    winnerRules = hRules.copy()
                    print("h won by score: " + str(h_score))

                # checks if second best for crossover, also gross and needs to be replaced later
                if not failed:

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

                    elif e_score == score_list[1]:
                        second_place = eDNA.copy()
                        second_placeRules = eRules.copy()

                    elif f_score == score_list[1]:
                        second_place = fDNA.copy()
                        second_placeRules = fRules.copy()

                    elif g_score == score_list[1]:
                        second_place = gDNA.copy()
                        second_placeRules = gRules.copy()

                    else:  # h_score == score_list[1]:
                        second_place = hDNA.copy()
                        second_placeRules = hRules.copy()

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

        except KeyboardInterrupt:
            input("enter anything to continue...")

def run_vs(genesParent, rulesParent):
    global mutation_chance

    #generation = 0
    generation = 1
    fails = 0

    while True:

        generation += 1

        try:

            alphaDNA = genesParent.copy()
            alphaRules = rulesParent.copy()

            betaDNA = mutate_constants(genesParent)
            betaRules = mutate_rules(rulesParent)

            write_ai(alphaDNA, alphaRules, "parent")
            write_ai(betaDNA, betaRules, "b")
            # reads score
            master = [0,0]

            failed = False

            success = 0
            fail = 0

            while success < 5:
                l = Launcher()
                score_list = l.launch_game(["parent","b"], real_time_limit = 400, game_time_limit = 3600, number_of_instances=10)

                if score_list == None or score_list[0] == None:

                    if generation == 1:
                        generation -= 1
                        rulesParent, genesParent = generate_script(script_rule_count)
                    fail += 1

                    if fail > 10:
                        break
                        print("killed loop")

                else:
                    success += 1
                    print(str(success))
                    master[0] += score_list[0]
                    master[1] += score_list[1]

                time.sleep(1)



            if not failed:

                parent_score = master[0]
                b_score = master[1]

                score_list = sorted(master, reverse=True)

                # checks number of rounds with no improvement and sets annealing
                if parent_score == max(score_list):
                    fails += 1
                    mutation_chance += fails / 1000
                else:
                    fails = 0
                    mutation_chance = .05


                if parent_score == max(score_list):
                    winner = genesParent.copy()
                    winnerRules = rulesParent.copy()
                    print("parent won by score: " + str(parent_score))

                elif b_score == max(score_list):
                    winner = betaDNA.copy()
                    winnerRules = betaRules.copy()
                    print("b won by score: " + str(b_score))


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

        except KeyboardInterrupt:
            input("enter anything to continue...")

setup_ai_files()

#rulesParent, genesParent = generate_script(script_rule_count)
rulesParent, genesParent = read_best()

#run_vs(genesParent, rulesParent)
# run_score(genesParent, rulesParent)
run_ffa(genesParent, rulesParent)

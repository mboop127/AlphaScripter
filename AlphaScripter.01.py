import random
import cv2
import pytesseract
import pyautogui
import time
import pydirectinput
from collections import OrderedDict
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

pyautogui.failsafe = False

#alphabet = 'abcdefghijklmnopqrstuvwxyz'
#temp = []
#alphavalues = []
#for x in alphabet:
#    for y in alphabet:
#        temp.append(x + y)
#
#for i in range(300):
#    alphavalues.append(temp[i])

alphavalues = ['aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bk', 'bl', 'bm', 'bn', 'bo', 'bp', 'bq', 'br', 'bs', 'bt', 'bu', 'bv', 'bw', 'bx', 'by', 'bz', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'cg', 'ch', 'ci', 'cj', 'ck', 'cl', 'cm', 'cn', 'co', 'cp', 'cq', 'cr', 'cs', 'ct', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'da', 'db', 'dc', 'dd', 'de', 'df', 'dg', 'dh', 'di', 'dj', 'dk', 'dl', 'dm', 'dn', 'do', 'dp', 'dq', 'dr', 'ds', 'dt', 'du', 'dv', 'dw', 'dx', 'dy', 'dz', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'eg', 'eh', 'ei', 'ej', 'ek', 'el', 'em', 'en', 'eo', 'ep', 'eq', 'er', 'es', 'et', 'eu', 'ev', 'ew', 'ex', 'ey', 'ez', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'fg', 'fh', 'fi', 'fj', 'fk', 'fl', 'fm', 'fn', 'fo', 'fp', 'fq', 'fr', 'fs', 'ft', 'fu', 'fv', 'fw', 'fx', 'fy', 'fz', 'ga', 'gb', 'gc', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gj', 'gk', 'gl', 'gm', 'gn', 'go', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gv', 'gw', 'gx', 'gy', 'gz', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'hg', 'hh', 'hi', 'hj', 'hk', 'hl', 'hm', 'hn', 'ho', 'hp', 'hq', 'hr', 'hs', 'ht', 'hu', 'hv', 'hw', 'hx', 'hy', 'hz', 'ia', 'ib', 'ic', 'id', 'ie', 'if', 'ig', 'ih', 'ii', 'ij', 'ik', 'il', 'im', 'in', 'io', 'ip', 'iq', 'ir', 'is', 'it', 'iu', 'iv', 'iw', 'ix', 'iy', 'iz', 'ja', 'jb', 'jc', 'jd', 'je', 'jf', 'jg', 'jh', 'ji', 'jj', 'jk', 'jl', 'jm', 'jn', 'jo', 'jp', 'jq', 'jr', 'js', 'jt', 'ju', 'jv', 'jw', 'jx', 'jy', 'jz', 'ka', 'kb', 'kc', 'kd', 'ke', 'kf', 'kg', 'kh', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kp', 'kq', 'kr', 'ks', 'kt', 'ku', 'kv', 'kw', 'kx', 'ky', 'kz', 'la', 'lb', 'lc', 'ld', 'le', 'lf', 'lg', 'lh', 'li', 'lj', 'lk', 'll', 'lm', 'ln']

mutation_chance = .05

#read pre parsed actions
f = open("mb_actions.txt","r")
actions = f.read().split(",")
f.close()

#remove cheats
temp = []
for i in range(len(actions)):
    if "cc-" not in actions[i]:
        temp.append(actions[i])
    temp.append("\t")

actions = temp

#read pre parsed facts
f = open("mb_conditions.txt","r")
conditions = f.read().split(",")
conditions.append("\t")
f.close()

f = open("resign.txt","r")
resign_script = f.read()
f.close()

#remove dupes
actions = list(OrderedDict.fromkeys(actions))
conditions = list(OrderedDict.fromkeys(conditions))

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

    f = open("best.txt","r")

    file = f.read().split("\n")

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
            local_conditions = [local_rule[0],local_rule[1],local_rule[2]]
            local_actions = [local_rule[3],local_rule[4],local_rule[5]]
            local_alphas = [local_rule[6],local_rule[7],local_rule[8],local_rule[9],local_rule[10],local_rule[11]]

            rules_out.append([local_conditions,local_actions,local_alphas])

    return rules_out, constants_out

def static_code():
    f = open("Goals.txt", "r")
    goals = f.read()
    f.close()

    f = open("constants.txt","r")
    statics = f.read()
    f.close()

    return goals + "\n\n\n" + statics

def read_run_length():
    f = open("run_length.txt")
    length = int(f.read())
    f.close()

    return length

def start_game():
    find_button("play_again.PNG")
    #find_button("ok.PNG")

def clean(string):

    numeric_filter = filter(str.isdigit, string)
    string = "".join(numeric_filter)

    try:
        value = int(string)
    except ValueError:
        value = 0

    return value

def find_button(image):
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence=0.9)
            time.sleep(1)
            pydirectinput.click(x, y)
            break
        except (pyautogui.ImageNotFoundException, TypeError):
            pass

def end_game():
    game_ended = False
    start = time.time()
    current = start

    run_length = read_run_length()

    while not game_ended:
        current = time.time()
        if current - start > run_length:
            find_button("open_menu.PNG")
            find_button("quit.PNG")
            find_button("yes.PNG")
            print("timed out")
            return True
        try:
            x, y = pyautogui.locateCenterOnScreen('leave.png', confidence=0.9)
            pyautogui.click(x, y)
            game_ended = True
            return False
        except (pyautogui.ImageNotFoundException, TypeError):
            pass

def generate_constants():
    temp = []
    for i in range(300):
        temp.append(random.randint(0,200))
    return temp

def generate_rules(count):
    rules = []
    for i in range(count):
        conditions1 = [random.choice(conditions),random.choice(conditions),random.choice(conditions)]
        actions1 = [random.choice(actions),random.choice(actions),random.choice(actions)]
        alphavalues1 = [random.choice(alphavalues),random.choice(alphavalues),random.choice(alphavalues),random.choice(alphavalues),random.choice(alphavalues),random.choice(alphavalues)]

        rules.append([conditions1,actions1,alphavalues1])

        #print(conditions1)
    return rules

def mutate_rules(list):

    rules1 = []

    for x in range(len(list)):
        conditions1 = list[x][0].copy()
        actions1 = list[x][1].copy()
        alphavalues1 = list[x][2].copy()

        for i in range(len(conditions1)):
            conditions1[i] = mutate_single(conditions,conditions1[i])
            actions1[i] = mutate_single(actions,actions1[i])

        for i in range(len(alphavalues1)):
            alphavalues1[i] = mutate_single(alphavalues,alphavalues1[i])

        rules1.append([conditions1,actions1,alphavalues1])

    return rules1

def score_grab(y, bonus):

    military = pyautogui.screenshot(region=(832,y,100,50))
    eco = pyautogui.screenshot(region=(940,y,100,50))
    society = pyautogui.screenshot("try.png",region=(1132,y,100,50))

    eco_score = clean(pytesseract.image_to_string(eco))# ** .5
    military_score = clean(pytesseract.image_to_string(military))# ** .5
    society_score = clean(pytesseract.image_to_string(society))# ** .5

    tscore = military_score + eco_score + society_score + bonus

    return tscore

def mutate_single(list, item):

    global mutation_chance

    if random.random() < mutation_chance:
        return random.choice(list)
    else:
        return item

def save_ai(rules, alphavalues):

    f = open("best.txt","w+")
    for i in range(len(rules)):
        conditions1 = rules[i][0].copy()
        actions1 = rules[i][1].copy()
        constants1 = rules[i][2].copy()

        f.write("|")
        for x in range(len(conditions1)):
            f.write(conditions1[x] + ",")
        for x in range(len(actions1)):
            f.write(actions1[x] + ",")
        for x in range(len(constants1)):
            f.write(constants1[x] + ",")

    f.write("\n")
    for i in range(len(alphavalues)):
        f.write(str(alphavalues[i]) + ",")
    f.close()

def write_rules(list):
    string = ""

    #print(list)

    for i in range(len(list)):

        conditions1 = list[i][0].copy()
        actions1 = list[i][1].copy()
        alphavalues1 = list[i][2].copy()


        string += "(defrule\n"
        string += conditions1[0].replace("AlphaMorphValue",alphavalues1[0]) +"\n"
        string += conditions1[1].replace("AlphaMorphValue",alphavalues1[1]) +"\n"
        string += conditions1[2].replace("AlphaMorphValue",alphavalues1[2]) +"\n"
        string += "\n=>\n"
        string += actions1[0].replace("AlphaMorphValue",alphavalues1[3]) +"\n"
        string += actions1[1].replace("AlphaMorphValue",alphavalues1[4]) +"\n"
        string += actions1[2].replace("AlphaMorphValue",alphavalues1[5]) +"\n"
        string += "\n)\n\n"

    return string

def mutate_constants(list):

    global mutation_chance

    list2 = list.copy()
    for i in range(len(list2)):

        if random.random() < .01:
            list2[i] = random.randint(0,200)

        elif random.random() < mutation_chance:
            list2[i] += random.randint(-10,10)
            list2[i] = max(0, list2[i])

    return list2

def write_ai(list, rules, name):

    constant_write = ""
    for i in range(len(alphavalues)):
        constant_write += "\n(defconst " + alphavalues[i] + " " + str(list[i]) + ")"

    f = open(name + ".per", "w+")
    f.write(static_code() + "\n\n\n")
    f.write(constant_write)
    f.write("\n\n\n")
    f.write(resign_script)
    f.write("\n\n\n")
    f.write(write_rules(rules))
    f.write("\n\n\n")
    f.close()

def run_vs(genesParent, rulesParent):
    global mutation_chance

    time.sleep(1)
    best = 0
    fails = 0
    while True:
        try:

            #alphaDNA = genesParent.copy()
            alphaDNA = mutate_constants(genesParent)
            alphaRules = mutate_rules(rulesParent)

            betaDNA = genesParent.copy()
            betaRules = rulesParent.copy()

            write_ai(alphaDNA, alphaRules, "Alpha")
            write_ai(betaDNA, betaRules, "Beta")

            start_game()
            timed_out = end_game()

            time.sleep(5)

            #finds winner based on crown location in end screen and gives bonus
            try:
                x, y = pyautogui.locateCenterOnScreen('won.PNG', confidence=0.8)
            except (pyautogui.ImageNotFoundException, TypeError):
                y = 0
                print("could not find crown")

            alpha_bonus = 0
            beta_bonus = 0

            if y < 337 and not timed_out:
                winner = alphaDNA
                alpha_bonus = 10000
                print("alpha won")

            elif not timed_out:
                winner = betaDNA
                print("beta won")
                beta_bonus = 10000

            #reads score from screen
            alpha_score = score_grab(290, alpha_bonus)
            beta_score = score_grab(337, beta_bonus)

            if beta_score > alpha_score:
                fails += 1
                mutation_chance += fails/1000
                winner = betaDNA.copy()
                winnerRules = rulesParent.copy()
                print("beta won by score: " + str(beta_score))

            else:
                fails = 0
                mutation_chance = .05
                winner = alphaDNA.copy()
                winnerRules = alphaRules.copy()
                print("alpha won by score: " + str(alpha_score))

            genesParent = winner.copy()
            rulesParent = winnerRules.copy()
            write_ai(winner,winnerRules, "best")
            save_ai(winnerRules,winner)

            #if score > best:
            #    best = score
            #    print("new best: " + str(score))
            #    alpha = write_ai(alphaDNA, "Best")
            #    genesParent = alphaDNA.copy()

        except KeyboardInterrupt:
            input("enter anything to continue...")

def run_score(genesParent, rulesParent):
    time.sleep(1)
    best = 0
    fails = 0

    while True:

        try:


            crossed_rules, crossed_genes = crossover(rulesParent, second_placeRules, genesParent, second_place)

            alphaDNA = mutate_constants(crossed_rules)
            alphaRules = mutate_rules(crossed_genes)
            write_ai(alphaDNA, alphaRules, "Alpha")

            start_game()
            timed_out = end_game()

            time.sleep(5)

            #reads score from screen
            alpha_score = score_grab(337, 0)

            if score > best:
                fails = 0
                mutation_chance = .05
                best = score
                print("new best: " + str(alpha_score))
                write_ai(alphaDNA, alphaRules,"Best")
                save_ai(alphaRules, alphaDNA)
                second_place = genesParent.copy()
                second_placeRules = rulesParent.copy()
                genesParent = alphaDNA.copy()
                rulesParent = alphaRules.copy()
            else:
                fails += 1
                mutation_chance += fails / 1000

        except KeyboardInterrupt:
            input("enter anything to continue...")

    return genesParent, rulesParent


def run_ffa(genesParent, rulesParent):
    global mutation_chance

    time.sleep(1)

    second_placeRules = rulesParent.copy()
    second_place = genesParent.copy()

    best = 0
    fails = 0
    while True:
        try:

            #refector later
            #alphaDNA = genesParent.copy()
            crossed_rules, crossed_genes = crossover(rulesParent, second_placeRules, genesParent, second_place)
            alphaDNA = mutate_constants(crossed_genes)
            alphaRules = mutate_rules(crossed_rules)
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

            betaDNA = genesParent.copy()
            betaRules = rulesParent.copy()

            write_ai(alphaDNA, alphaRules, "Alpha")
            write_ai(betaDNA, betaRules, "Beta")
            write_ai(cDNA, cRules, "c")
            write_ai(dDNA, dRules, "d")
            write_ai(eDNA, eRules, "e")
            write_ai(fDNA, fRules, "f")
            write_ai(gDNA, gRules, "g")
            write_ai(hDNA, hRules, "h")

            start_game()
            timed_out = end_game()

            time.sleep(5)
            pyautogui.click(10,10)

            #reads score from screen
            alpha_score = score_grab(290,0)
            beta_score = score_grab(337,0)
            c_score = score_grab(387,0)
            d_score = score_grab(437,0)
            e_score = score_grab(487,0)
            f_score = score_grab(537,0)
            g_score = score_grab(587,0)
            h_score = score_grab(637,0)

            score_list = [alpha_score,beta_score,c_score,d_score,e_score,f_score,g_score,h_score]

            score_list = sorted(score_list,reverse=True)

            #checks number of rounds with no improvement and sets annealing
            if beta_score == max(score_list):
                fails += 1
                mutation_chance += fails / 1000
            else:
                fails = 0
                mutation_chance = .05

            #checks for unlikely score, need to fix later
            if score_list[0] > score_list[1] * 5:
                winner = genesParent.copy()
                winnerRules = rulesParent.copy()
                print("impossible score, skipping round")

            elif alpha_score == max(score_list):
                winner = alphaDNA.copy()
                winnerRules = alphaRules.copy()
                print("alpha won by score: " + str(alpha_score))

            elif beta_score == max(score_list):
                winner = genesParent.copy()
                winnerRules = rulesParent.copy()
                print("beta won by score: " + str(beta_score))

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

            else: #h_score == max(score_list):
                winner = hDNA.copy()
                winnerRules = hRules.copy()
                print("h won by score: " + str(h_score))

            #checks if second best for crossover, also gross and needs to be replaced later
            if score_list[0] > score_list[1] * 5:
                second_place = genesParent.copy()
                second_placeRules = rulesParent.copy()

            elif alpha_score == score_list[1]:
                second_place = alphaDNA.copy()
                second_placeRules = alphaRules.copy()

            elif beta_score == score_list[1]:
                second_place = genesParent.copy()
                second_placeRules = rulesParent.copy()

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

            else: #h_score == score_list[1]:
                second_place = hDNA.copy()
                second_placeRules = hRules.copy()


            genesParent = winner.copy()
            rulesParent = winnerRules.copy()
            write_ai(winner,winnerRules, "best")
            save_ai(winnerRules, winner)

            #if score > best:
            #    best = score
            #    print("new best: " + str(score))
            #    alpha = write_ai(alphaDNA, "Best")
            #    genesParent = alphaDNA.copy()

        except KeyboardInterrupt:
            input("enter anything to continue...")

#genesParent = generate_constants()
#rulesParent = generate_rules(500)
#genesParent, rulesParent = run_score()
#input("1000 score achieved; enter to continue")
#run_vs(genesParent, rulesParent)

rulesParent, genesParent = read_best()

run_ffa(genesParent,rulesParent)

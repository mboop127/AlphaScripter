import random
import cv2
import pytesseract
import pyautogui
import time
import pydirectinput
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

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

f = open("mb_actions.txt","r")
actions = f.read().split(",")
f.close()

f = open("mb_conditions.txt","r")
conditions = f.read().split(",")
f.close()

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
    find_button("ok.PNG")

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
        rules.append([random.choice(conditions),random.choice(alphavalues),random.choice(actions),random.choice(alphavalues)])
    return rules

def mutate_rules(list):
    list2 = list.copy()
    for i in range(len(list)):
        if random.random() < .05:
            list2[i][0] = random.choice(conditions)
        if random.random() < .05:
            list2[i][1] = random.choice(alphavalues)
        if random.random() < .05:
            list2[i][2] = random.choice(actions)
        if random.random() < .05:
            list2[i][3] = random.choice(alphavalues)

    return list2

def mutate_constants(list):

    list2 = list.copy()
    for i in range(len(list2)):

        if random.random() < .01:
            list2[i] = random.randint(0,200)

        elif random.random() < .05:
            list2[i] += random.randint(-10,10)
            list2[i] = max(0, list2[i])

    return list2

def write_rules(list):
    string = ""

    for i in range(len(list)):
        string += "(defrule\n"
        string += list[i][0].replace("AlphaMorphValue",list[i][1])
        string += "\n=>\n"
        string += list[i][2].replace("AlphaMorphValue",list[i][3])
        string += "\n)\n\n"

    return string

def write_ai(list, rules, name):

    constant_write = ""
    for i in range(len(alphavalues)):
        constant_write += "\n(defconst " + alphavalues[i] + " " + str(list[i]) + ")"

    f = open(name + ".per", "w+")
    f.write(static_code() + "\n\n\n")
    f.write(constant_write)
    f.write("\n\n\n")
    f.write(write_rules(rules))
    f.close()

def vs_run():
    time.sleep(1)
    genesParent = generate()
    best = 0
    while True:
        try:

            #alphaDNA = genesParent.copy()
            alphaDNA = mutate(genesParent)
            write_ai(alphaDNA, "Alpha")
            write_ai(genesParent, "Beta")

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
            military = pyautogui.screenshot(region=(832,290,100,50))
            eco = pyautogui.screenshot("try.png",region=(940,290,100,50))
            eco_score = clean(pytesseract.image_to_string(eco))
            military_score = clean(pytesseract.image_to_string(military))
            alpha_score = military_score + eco_score + beta_bonus

            military = pyautogui.screenshot(region=(832,337,100,50))
            eco = pyautogui.screenshot(region=(940,337,100,50))
            eco_score = clean(pytesseract.image_to_string(eco))
            military_score = clean(pytesseract.image_to_string(military))
            beta_score = military_score + eco_score + alpha_bonus

            if beta_score > alpha_score:
                winner = betaDNA
                print("beta won by score: " + str(beta_score))

            else:
                winner = alphaDNA
                print("alpha won by score: " + str(alpha_score))

            genesParent = winner.copy()
            write_ai(winner, "best")

            #if score > best:
            #    best = score
            #    print("new best: " + str(score))
            #    alpha = write_ai(alphaDNA, "Best")
            #    genesParent = alphaDNA.copy()

        except KeyboardInterrupt:
            input("enter anything to continue...")

def run_score():
    time.sleep(1)
    genesParent = generate()
    best = 0
    while best < 1000:

        try:

            #alphaDNA = genesParent.copy()
            alphaDNA = mutate(genesParent)
            write_ai(alphaDNA, "Alpha")

            start_game()
            timed_out = end_game()

            time.sleep(5)

            #reads score from screen
            military = pyautogui.screenshot(region=(832,337,100,50))
            eco = pyautogui.screenshot(region=(940,337,100,50))
            eco_score = clean(pytesseract.image_to_string(eco))
            military_score = clean(pytesseract.image_to_string(military))
            score = military_score + eco_score

            if score > best:
                best = score
                print("new best: " + str(score))
                write_ai(alphaDNA, "Best")
                genesParent = alphaDNA.copy()

        except KeyboardInterrupt:
            input("enter anything to continue...")

rules = generate_rules(1000)

rules = mutate_rules(rules)

constants = generate_constants()
write_ai(constants, rules, "test")

#run_score()
#input("1000 score achieved; enter to continue")
#run_vs()

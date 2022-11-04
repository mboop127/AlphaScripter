from Functions import *
import tkinter as tk
from main import backup

def write_from_csv(file):
    #parses csv
    f = open(file + ".csv",'r')
    data = f.read()
    f.close()

    #[type,params,threshold,age_required,requirement,requirement_count,gametime]

    data = data.split("|")

    research = data[1].split("\n")
    buildings = data[2].split("\n")
    build_forward = data[3].split("\n")
    units = data[4].split("\n")
    SN = data[5].split("\n")
    distributons = data[6].split("\n")
    attack_rules = data[7].split("\n")

    AI = generate_ai()
    AI[1] = [] #clears simples
    AI[2] = [] #clears complex
    AI[3] = [] #clears attack rules

    #write research rules
    for i in range(2,len(research)-1):
        line = research[i].split(",")

        if line[0] != "":
            temp = generate_simple()
            temp[0] = 'research'
            temp[1]['TechId'] = line[0]
            temp[3] = [line[1]]
            temp[4] = line[2]
            temp[5] = int(line[3])
            temp[6] = int(line[4])
            AI[1] = [temp] + AI[1]


    #[type,params,threshold,age_required,requirement]

    for i in range(2,len(buildings)):
        line = buildings[i].split(",")

        if line[0] != "":
            temp = generate_simple()
            temp[0] = 'build'
            temp[1]['Buildable'] = line[0]
            temp[2] = int(line[2])
            temp[3] = [line[1]]
            temp[4] = line[3]
            temp[5] = int(line[4])
            temp[6] = int(line[5])
            AI[1] = [temp] + AI[1]

    for i in range(2,len(build_forward)):
        line = build_forward[i].split(",")

        if line[0] != "":
            temp = generate_simple()
            temp[0] = 'build-forward'
            temp[1]['Buildable'] = line[0]
            temp[2] = int(line[2])
            temp[3] = [line[1]]
            temp[4] = line[3]
            temp[5] = int(line[4])
            temp[6] = int(line[5])
            AI[1] = [temp] + AI[1]

    for i in range(2,len(units)):
        line = units[i].split(",")

        if line[0] != "":
            temp = generate_simple()
            temp[0] = 'train'
            temp[1]['Trainable'] = line[0]
            temp[2] = int(line[2])
            temp[3] = [line[1]]
            temp[4] = line[3]
            temp[5] = int(line[4])
            temp[6] = int(line[5])
            AI[1] = [temp] + AI[1]

    for i in range(2,len(SN)):
        line = SN[i].split(",")

        if line[0] != "":
            temp = generate_simple()
            temp[0] = 'strategic_number'
            temp[1]['SnId'] = line[0]
            temp[1]['SnValue'] = line[2]
            temp[3] = [line[1]]
            temp[4] = line[3]
            temp[5] = int(line[4])
            temp[6] = int(line[5])
            AI[1] = [temp] + AI[1]

    for i in range(2,len(distributons)):
        line = distributons[i].split(",")

        if line[0] != "":

            for f in range(5):
                line[f] = float(line[f])

            AI[0][i-2] = [line[0],line[1],line[2],line[3],line[4]]

    for i in range(2,len(attack_rules)):
        line = attack_rules[i].split(",")

        if line[0] != "":
            AI[3] = [[line[0],line[1],[line[2],line[3],line[4]],[line[5],line[6],line[7]],[line[8],line[9]],line[10]]] + AI[3]

    backup()
    write_ai(AI,"best")
    save_ai(AI, "best")

def read(string):
    ai = read_ai(string)
    distribution = ai[0]
    simples = ai[1]
    attack_rules = ai[3]


    research = []
    buildings = []
    build_forward = []
    units = []
    SN = []

    #[type,params,threshold,age_required,requirement,requirement_count,gametime]
    for i in range(len(simples)):

        local_simple = simples[i]

        if local_simple[0] == 'research':
            #print(local_simple)
            research.append([local_simple[1]['TechId'],local_simple[3][0],local_simple[4],local_simple[5],local_simple[6]])

        if local_simple[0] == 'build':
            buildings.append([local_simple[1]['Buildable'],local_simple[3][0],local_simple[2],local_simple[4],local_simple[5],local_simple[6]])

        if local_simple[0] == 'build-forward':
            build_forward.append([local_simple[1]['Buildable'],local_simple[3][0],local_simple[2],local_simple[4],local_simple[5],local_simple[6]])

        if local_simple[0] == 'train':
            units.append([local_simple[1]['Trainable'],local_simple[3][0],local_simple[2],local_simple[4],local_simple[5],local_simple[6]])

        if local_simple[0] == 'strategic_number':
            SN.append([local_simple[1]['SnId'],local_simple[3][0],local_simple[1]['SnValue'],local_simple[4],local_simple[5],local_simple[6]])

    f = open("edittable.csv","w+")

    f.write("|Research\n")
    f.write("TechID,age required,required,requirement count,gametime\n")

    write_list(research,f)

    f.write("\n|Building\n")
    f.write("BuildingID,age required,max count,required,requirement count,gametime\n")

    write_list(buildings,f)

    f.write("\n|Build forward\n")
    f.write("BuildingID,age required,max count,required,requirement count,gametime\n")

    write_list(build_forward,f)

    f.write("\n|Unit\n")
    f.write("UnitID,age required,max count,required,requirement count,gametime\n")

    write_list(units,f)

    f.write("\n|Strategic Number\n")
    f.write("SnID,age required,value,required,requirement count,gametime\n")

    write_list(SN,f)

    f.write("\n|Distributions\n")
    f.write("food,wood,gold,stone,attack threshold\n")

    for i in range(len(distribution)):
        line = distribution[i]
        for x in range(len(line)):
            f.write(str(line[x]) + ",")
        f.write("\n")

    f.write("\n|Attack Rules\n")
    f.write("Age required,Enemy Age Required,population1 type,population1 inq,population1 value,population2 type,population2 inq,population2 value,gametime inq,gametime value,attack %\n")

    for i in range(len(attack_rules)):
        line = attack_rules[i]
        f.write(str(line[0]) + "," + str(line[1]) + "," + str(line[2][0]) + "," + str(line[2][1]) + "," + str(line[2][2]) + "," + str(line[3][0]) + "," + str(line[3][1]) + "," + str(line[3][2]) + "," + str(line[4][0]) + "," + str(line[4][1]) + "," + str(line[5]) + "\n")

    f.close()

def write_list(list,f):
    for i in range(len(list)):
        line = list[i]
        for x in range(len(line)):
            f.write(str(line[x]) + ",")
        f.write("\n")

def swap(name1, name2):

    ai1 = read_ai(name1)
    ai2 = read_ai(name2)

    ai1[2] = []
    ai1[2] = ai2[2]

    write_ai(ai1,"best")
    save_ai(ai1, "best")

root = tk.Tk()

inputtxt = tk.Text(root, height = 1, width = 15)
inputtxt.pack()

button1 = tk.Button(root, text = "edit", command = lambda: read(inputtxt.get(1.0, "end-1c")))
button1.pack()

inputtxt2 = tk.Text(root, height = 1, width = 15)
inputtxt2.pack()

button2 = tk.Button(root, text = "commit ai", command = lambda: write_from_csv(inputtxt2.get(1.0, "end-1c")))
button2.pack()

inputtxt3 = tk.Text(root, height = 1, width = 15)
inputtxt3.pack()
inputtxt4 = tk.Text(root, height = 1, width = 15)
inputtxt4.pack()

button2 = tk.Button(root, text = "swap complex", command = lambda: swap(inputtxt3.get(1.0, "end-1c"), inputtxt4.get(1.0, "end-1c")))
button2.pack()


root.mainloop()

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
    #print(data[7])

    research = data[1].split("\n")
    buildings = data[2].split("\n")
    build_forward = data[3].split("\n")
    units = data[4].split("\n")
    SN = data[5].split("\n")
    attack_rules = data[6].split("\n")
    goals = data[7].split("\n")
    DUC = data[8].split("\n")
    goal_actions = data[9].split("\n")

    AI = generate_ai()
    AI[0] = [] #clears simples
    AI[1] = [] #clears complex
    AI[2] = [] #clears attack rules
    AI[3] = []
    AI[4] = []
    AI[5] = []
    AI[6] = []

    simple_dict = {}

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
            temp[8] = int(line[6])
            temp[9] = line[5] == 'TRUE'

            simple_dict[line[7]] = temp


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
            temp[8] = int(line[7])
            temp[9] = line[6] == 'TRUE'
            print(temp[9])

            simple_dict[line[8]] = temp

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
            temp[8] = int(line[7])
            temp[9] = line[6] == 'TRUE'

            simple_dict[line[8]] = temp

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
            temp[8] = int(line[7])
            temp[9] = line[6] == 'TRUE'

            simple_dict[line[8]] = temp

    for i in range(2,len(SN)):
        line = SN[i].split(",")

        if line[0] != "":
            temp = generate_simple()
            temp[0] = 'strategic_number'
            temp[1]['SnId'] = line[0]
            temp[7][temp[1]['SnId']] = line[2]
            temp[3] = [line[1]]
            temp[4] = line[3]
            temp[5] = int(line[4])
            temp[6] = int(line[5])
            temp[8] = int(line[7])
            temp[9] = line[6] == 'TRUE'

            simple_dict[line[8]] = temp

    for item in simple_dict:
        AI[0].append(item)

    for item in simple_dict:
        AI[0][int(item)] = simple_dict[item]



    for i in range(2,len(attack_rules)):
        line = attack_rules[i].split(",")

        if line[0] != "":
            bool = False
            if line[14] == 'TRUE':
                bool = True
            AI[2] = [[line[0],line[1],line[2],[line[3],line[4],line[5]],[line[6],line[7],line[8]],[line[9],line[10]],line[11],line[12],line[13],line[14],bool]] + AI[2]

    for i in range(2,len(goals)):
        line = goals[i].split(",")

        if line[0] != "":
            temp = generate_goal()
            temp[0] = int(line[0])
            temp[1] = int(line[1])
            temp[2] = line[2] == "TRUE"
            temp[3] = int(line[3])
            temp[4] = line[4] == 'TRUE'
            temp[6] = int(line[5])

            for x in range(len(temp[5])):
                temp[5][x][0] = line[6 + x*2]

                local_params = line[7 + x*2].split(";")

                if temp[5][x][0] == 'TRUE':
                    temp[5][x][0] = "true"
                if temp[5][x][0] == 'FALSE':
                    temp[5][x][0] = "false"


                keys = facts[temp[5][x][0]]
                for y in range(len(local_params)):
                    #print(str(keys[y]) + ", " + str(local_params[y-1]))
                    #print(temp[5][x][1][keys[y]])
                    temp[5][x][1][keys[y+1]] = local_params[y]
                    #print(keys[y])
                    #print(temp[5][x][1][keys[y]])


            AI[5] = AI[5] + [temp]

    for i in range(2,len(DUC)):

        #print(DUC[i])
        line = DUC[i].split(",")

        if i % 2 != 1 and line[0] != "":
            temp = generate_DUC_search()
            #print(write_DUC_search(temp))
            temp[0] = line[0]
            temp[1] = int(line[1])
            temp[2] = int(line[2])
            temp[4] = int(line[3])
            for x in range(len(temp[3])):
                local = line[4 + x].split(";")
                temp[3][x] = [int(local[0]),local[1],int(local[2])]
            #print(temp[3])

            AI[3] = AI[3] + [temp]

        elif line[0] != "":

            temp = []
            a = generate_DUC_target()
            a[0] = line[0]
            a[1] = int(line[1])
            a[2] = int(line[3])
            a[4] = int(line[2])

            for x in range(len(a[3])):
                local = line[4 + x].split(";")
                a[3][x] = [int(local[0]),local[1],int(local[2])]

            a[5] = int(line[11])
            a[6] = int(line[12])
            a[7] = int(line[13])
            a[8] = line[14] == 'TRUE'
            a[9] = int(line[15])
            a[10] = int(line[16])
            a[11] = int(line[17])
            a[12] = int(line[18])
            a[13] = int(line[19])
            a[14] = line[20] == 'TRUE'

            AI[4] = AI[4] + [a]


    for i in range(2,len(goal_actions)):
        line = goal_actions[i].split(",")

        if line[0] != "":
            temp = generate_goal_action()

            #count
            temp[3][0] = int(line[0])
            temp[3][1] = int(line[1])

            for x in range(3):
                temp[0][x] = int(line[2+2*x])
                temp[1][x] = int(line[3+2*x])

            for x in range(3):
                action_name = line[8 + 2 * x]
                local_params = line[9 + 2 * x].split(";")

                keys = actions[action_name]
                for y in range(len(local_params)):
                    #print(str(keys[y]) + ", " + str(local_params[y-1]))
                    #print(temp[5][x][1][keys[y]])
                    temp[2][x][0] = action_name
                    temp[2][x][1][keys[y+1]] = local_params[y]


            AI[6] = AI[6] + [temp]

    backup()
    write_ai(AI,"best")
    save_ai(AI, "best")

def read(string):
    ai = read_ai(string)
    simples = ai[0]
    attack_rules = ai[2]
    DUC_search = ai[3]
    DUC_target = ai[4]
    goals = ai[5]
    goal_actions = ai[6]

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
            research.append([local_simple[1]['TechId'],local_simple[3][0],local_simple[4],local_simple[5],local_simple[6],local_simple[9],local_simple[8],i])

        if local_simple[0] == 'build':
            buildings.append([local_simple[1]['Buildable'],local_simple[3][0],local_simple[2],local_simple[4],local_simple[5],local_simple[6],local_simple[9],local_simple[8],i])

        if local_simple[0] == 'build-forward':
            build_forward.append([local_simple[1]['Buildable'],local_simple[3][0],local_simple[2],local_simple[4],local_simple[5],local_simple[6],local_simple[9],local_simple[8],i])

        if local_simple[0] == 'train':
            units.append([local_simple[1]['Trainable'],local_simple[3][0],local_simple[2],local_simple[4],local_simple[5],local_simple[6],local_simple[9],local_simple[8],i])

        if local_simple[0] == 'strategic_number':
            SN.append([local_simple[1]['SnId'],local_simple[3][0],local_simple[7][local_simple[1]['SnId']],local_simple[4],local_simple[5],local_simple[6],local_simple[9],local_simple[8],i])

    f = open("edittable.csv","w+")

    f.write("|Research\n")
    f.write("TechID,age required,required,requirement count,gametime,goal_checked,goal_id,order\n")

    write_list(research,f)

    f.write("\n|Building\n")
    f.write("BuildingID,age required,max count,required,requirement count,gametime,goal_checked,goal_id,order\n")

    write_list(buildings,f)

    f.write("\n|Build forward\n")
    f.write("BuildingID,age required,max count,required,requirement count,gametime,goal_checked,goal_id,order\n")

    write_list(build_forward,f)

    f.write("\n|Unit\n")
    f.write("UnitID,age required,max count,required,requirement count,gametime,goal_checked,goal_id,order\n")

    write_list(units,f)

    f.write("\n|Strategic Number\n")
    f.write("SnID,age required,value,required,requirement count,gametime,goal_checked,goal_id,order\n")

    write_list(SN,f)

    f.write("\n|Attack Rules\n")
    f.write("Type,Age required,Enemy Age Required,population1 type,population1 inq,population1 value,population2 type,population2 inq,population2 value,gametime inq,gametime value,attack %,retreat units,retreat location,goal_id,goal_checked\n")

    for i in range(len(attack_rules)):
        line = attack_rules[i]
        f.write(str(line[0])+ "," + str(line[1]) + "," + str(line[2]) + "," + str(line[3][0]) + "," + str(line[3][1]) + "," + str(line[3][2]) + "," + str(line[4][0]) + "," + str(line[4][1]) + "," + str(line[4][2]) + "," + str(line[5][0]) + "," + str(line[5][1]) + "," + str(line[6]) + "," + str(line[7]) + "," + str(line[8]) + "," + str(line[9]) + "," + str(line[10]) + "\n")

    f.write("\n|Goals\n")
    f.write("Goal ID,value,disable after use,checked goal,checked goal value,number of facts used,fact1,params1,fact2,params2,fact3,params3,fact4,params4\n")

    for i in range(len(goals)):
        line = goals[i]
        f.write(str(line[0])+ "," + str(line[1]) + "," + str(line[2]) + "," + str(line[3])+ "," + str(line[4]) + "," + str(line[6]) + ",")

        for x in range(len(line[5])):
            local = line[5][x]
            fact_name = local[0]
            params = local[1]
            f.write(local[0] + "," + str(params[facts[fact_name][1]]) + ";" + str(params[facts[fact_name][2]]) + ";" + str(params[facts[fact_name][3]]) + ";" + str(params[facts[fact_name][4]]) + ",")
        f.write("\n")

    f.write("\n|DUC\n")
    f.write("lol I will add a descripter later leave this line\n")
    for i in range(len(DUC_search)):
        f.write(write_DUC_search_local(DUC_search[i]))
        f.write(write_DUC_target_local(DUC_target[i]))

    f.write("\n|Goal actions\n")
    f.write("goal_count,action_count,goal1,goal_value1,goal2,goal_value2,goal3,goal_value3,action1,action1_parameters,action2,action2_parameters,action3,action3_parameters\n")

    for i in range(len(goal_actions)):

        goals = goal_actions[i][0]
        values = goal_actions[i][1]
        action = goal_actions[i][2]
        count = goal_actions[i][3]

        f.write(str(count[0]) + ",")
        f.write(str(count[1]) + ",")

        for x in range(len(goals)):
            f.write(str(goals[x]) + ",")
            f.write(str(values[x]) + ",")

        for x in range(len(action)):
            local = action[x]
            action_name = local[0]
            params = local[1]
            sns = local[2]
            f.write(local[0] + "," + str(params[actions[action_name][1]]) + ";" + str(params[actions[action_name][2]]) + ";" + str(params[actions[action_name][3]]) + ";" + str(params[actions[action_name][4]]) + ",")

        f.write("\n")


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

    ai1[1] = []
    ai1[1] = ai2[1]

    write_ai(ai1,"best")
    save_ai(ai1, "best")

def write_DUC_search_local(search):
    self_selected = search[0]
    self_selected_max = search[1]
    used_filters = search[2]
    filters = search[3]
    group_id = search[4]

    string = ""

    string += str(self_selected) + "," + str(self_selected_max) + "," + str(used_filters) + "," + str(group_id) + ","

    for i  in range(len(filters)):

        filter_object = filters[i][0]
        filter_compare = filters[i][1]
        filter_value = filters[i][2]
        string += str(filter_object) + ";" + str(filter_compare) + ";" + str(filter_value) + ","

    string += "\n"

    return string

def write_DUC_target_local(target):

    selected = target[0]
    selected_max = target[1]
    used_filters = target[2]
    filters = target[3]
    group_id = target[4]
    action = target[5]
    position = target[6]
    targeted_player = target[7]
    target_position = target[8]
    formation = target[9]
    stance = target[10]
    timer_id = target[11]
    if timer_id == 0:
        timer_id == 1
    timer_time = target[12]
    if len(target) > 13:
        goal = target[13]
        use_goal = target[14]
    else:
        goal = 1
        use_goal = False

    string = str(selected) + "," + str(selected_max) + "," + str(group_id) + "," + str(used_filters) + ","

    for i  in range(len(filters)):
        filter_object = filters[i][0]
        filter_compare = filters[i][1]
        filter_value = filters[i][2]
        string += str(filter_object) + ";" + str(filter_compare) + ";" + str(filter_value) + ","

    string += str(action) + "," + str(position) + "," + str(targeted_player) + "," + str(target_position) + "," + str(formation) + "," + str(stance) + "," + str(timer_id) + "," + str(timer_time) + "," + str(goal) + "," + str(use_goal) + "\n"

    return string

#a = generate_ai()
#save_ai(a,"test")
#read("test")
#write_from_csv("edittable")

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

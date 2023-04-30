from Functions import *
from main import *

#get_single_ai_data(['huns']*2,'best',list(eloDict.keys()),eloDict,3)

#benchmarker("best","Shadow 3.1",7,['huns','huns'])

#ai = read_ai("best")

ai = generate_ai()

ab = mutate_ai(ai,.05)
ab = crossover(ai,ab,.05)
write_ai(ab,"test")
save_ai(ab,"test")

#benchmarker("test","Shadow 3.1",7,['huns','huns'])

#from elosports.elo import Elo
#eloLeague = Elo(k= 10, g = 1)
#
#working_ais = ['Tlamacazqui','Wartron','Cyan','Eidolon','Odette_AI','Maximus 2_2a','RehoboamUP50%','Goths92602','Viper','Anti_TRiBaL','BTGBestStrats','Crusade 4.42c','Rhapsody0004','Ace','Ahulane UP','AllianceThundaEmpire','Alphav4','Arabian_Knight',"ARFFI-De'gel_ver_1_65",'ARFFI_05_107_50_rules','BambiV030','BambiV030dot2','best','Binary','BooM II','Boss_321','BruteForce3.1','Chameleon','CPS_Alexander','Cyan','Demon','Esty the TutoMaster','Faradol','fire2.3 DC-Final-#01','GamesGod','Grasshopper007','Grasshopper008AOC','II2N Rattlehead','Illuminati','Immortal v0.9c (beta)','IMP_CAES_MIRO III Azt_Teut','IS_UPMachine','John_Mendl','Juggernaut','Junior','Kosmos3.00beta2','Leif Ericson 1.32','Maiar','Miggins','Mini Eel 1.7','Mininati','Mininaut 1.4','No Limits','Pantheon','Pharaon DE','Phyrexx UP','Promi','PUMA Dreadnought','PUMA Lade13','PUMA Promi','PUMA Snake BF','rAge__(fixed)','Ranger 3.04','Rattlehead','Reactionaryv19 UP','Shadow 4.11','Snake #8.5','Subjugator','Ternary','The General','The Horde','best','The Khanate','Thermopylai v1.3','The_Unknown3','Tlamacazqui','Torisan_bc','TRiBaL_Warrior','TRON','UlyssesWK','UnfairSteel','Valkyrie Warriors','VetrixDE Final','Vicky','VNS_Chris_Tournament','Yggdrasil']
#
#for x in range(len(working_ais)):
#    eloLeague.addPlayer(working_ais[x], rating = 1600)
#
#f = open("data.csv","r")
#data = f.read().split("\n")
#f.close()
#
#for i in range(1,len(data)-1):
#    line = data[i].split(",")
#    AI = line[0]
#    opponent = line[6]
#    result = line[2]
#
#    if result == "win":
#        eloLeague.gameOver(winner = AI, loser = opponent,winnerHome = False)
#    elif result == "loss":
#        eloLeague.gameOver(winner = opponent, loser = AI,winnerHome = False)
#
#for entry in eloLeague.ratingDict:
#    print(entry + "," + str(eloLeague.ratingDict[entry]))


#ai = generate_ai()
#write_ai(ai,"best")
#save_ai(ai,"best")
#
#while True:
#    DUC_search = []
#    DUC_target = []
#    for i in range(5):
#        DUC_search.append(generate_DUC_search())
#        DUC_target.append(generate_DUC_target())
#
#    ai = read_ai("best")
#    ai[3] = DUC_search
#    ai[4] = DUC_target
#    write_ai(ai,"test")
#
#    wins = basic_benchmarker("test", "BambiV030", 7, ['huns']*2)
#    print(wins)
#    if wins > 2:
#        save_ai(ai,str(wins))
#        write_ai(ai,str(wins))
#        break
#

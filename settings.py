
fails_before_reset = 1000
#game_time = 3000
game_time = 7800

default_mutation_chance = .01
anneal_amount = 5 #bigger = less annealing
max_fact_length = 4
max_action_length = 3
ai_length = 0 #normal rules
simple_count = 100
attack_rule_count = 0
DUC_count = 10
goal_rule_count = 25
goal_action_count = 5

#network_drive = "C:/Users/mboop/Desktop/Shared/"
network_drive = "C:/Program Files/Microsoft Games/Age of Empires II/AI/"
local_drive = "C:/Program Files/Microsoft Games/Age of Empires II/AI/"

working_ais = ['Tlamacazqui','Wartron','Cyan','Eidolon','Odette_AI','Maximus 2_2a','RehoboamUP50%','Goths92602','Viper','Anti_TRiBaL','BTGBestStrats','Crusade 4.42c','Rhapsody0004','Ace','Ahulane UP','AllianceThundaEmpire','Alphav4','Arabian_Knight',"ARFFI-De'gel_ver_1_65",'ARFFI_05_107_50_rules','BambiV030','BambiV030dot2','best','Binary','BooM II','Boss_321','BruteForce3.1','Chameleon','CPS_Alexander','Cyan','Demon','Esty the TutoMaster','Faradol','fire2.3 DC-Final-01','GamesGod','Grasshopper007','Grasshopper008AOC','II2N Rattlehead','Illuminati','Immortal v0.9c (beta)','IMP_CAES_MIRO III Azt_Teut','IS_UPMachine','John_Mendl','Juggernaut','Junior','Kosmos3.00beta2','Leif Ericson 1.32','Maiar','Miggins','Mini Eel 1.7','Mininati','Mininaut 1.4','No Limits','Pantheon','Pharaon DE','Phyrexx UP','Promi','PUMA Dreadnought','PUMA Lade13','PUMA Promi','PUMA Snake BF','rAge__(fixed)','Ranger 3.04','Rattlehead','Reactionaryv19 UP','Shadow 4.11','Snake 8.5','Subjugator','Ternary','The General','The Horde','best','The Khanate','Thermopylai v1.3','The_Unknown3','Tlamacazqui','Torisan_bc','TRiBaL_Warrior','TRON','UlyssesWK','UnfairSteel','Valkyrie Warriors','VetrixDE Final','Vicky','VNS_Chris_Tournament','Yggdrasil']

eloDict = {'Hun Krush': 1745.128208, 'BambiV030': 1843.355396, 'UCS': 1669.937395, 'The Horde': 2008.261136, 'GamesGod': 1751.458229, 'Shadow 1': 1130.270815, 'Alphav4': 1490.374699, 'Subjugator': 1847.823758, 'VNS_Chris_Tournament': 1687.102006, 'Vicky': 1707.662764, 'Ace': 1672.926251, 'Alphav3': 1211.091988, 'Shadow 0': 1081.197184, 'Barbarian': 2063.981729, 'kt_trainer': 803.970408, 'Flying_Monk': 1500.779466, 'Crusade 4.42c': 2253.207843, 'Reactionaryv9': 1672.520563, 'MDE': 861.9773302, 'VNS_Halen_': 1834.394246, 'The_Unknown3': 2062.802085, 'The Khanate': 1777.137909, 'Shadow 2': 1302.087291, 'king': 914.8197984, 'Arabian_Knight': 1848.035116, 'Shadow 4.11': 2167.584068, 'Cal': 1301.195953, 'alpha_drush': 862.7897774, 'Vermin Supreme': 1654.355526, 'Ranger 3.04': 1929.164509, 'TRiBaL_Warrior': 2312.385075, 'Shadow 3.1': 1492.129188, 'CD': 1166.636131, 'AT_Scout_Rush': 1314.765075, 'UnfairSteel': 2293.514252, 'Rhapsody0004': 1429.094763, 'UlyssesWK': 2025.904929, 'Alphav2': 1072.367715}

arenaDict =   {
    "king": 985.3409644,
    "Shadow 0": 1117.177414,
    "Shadow 1": 1128.097398,
    "Shadow 2": 1198.126926,
    "CD": 1214.674512,
    "Shadow 3.1": 1335.581095,
    "Flying_Monk": 1373.37178,
    "Ace": 1383.680611,
    "Reactionaryv9": 1417.378483,
    "Subjugator": 1478.669299,
    "VNS_Chris_Tournament": 1522.210848,
    "Arabian_Knight": 1543.749224,
    "Vicky": 1583.402538,
    "Shadow 4.11": 1702.629269,
    "GamesGod": 1724.124926,
    "VNS_Halen_": 1782.395163,
    "BambiV030": 1819.853665,
    "Ranger 3.04": 1831.743734,
    "Crusade 4.42c": 1846.222101,
    "UlyssesWK": 1875.358588,
    "The_Unknown3": 1926.96583,
    "The Khanate": 1958.862525,
    "UnfairSteel": 2014.75918,
    "TRiBaL_Warrior": 2074.795807,
    "Barbarian": 2198.621863,
    "The Horde": 2206.336696
  }

#ai_ladder = ["Shadow 3.1","NightMare3","farmertron"]
ai_ladder = ["BambiV030","UlyssesWK","Barbarian","Promi"]
#ai_ladder = ['The_Unknown3','Vicky','GamesGod','BambiV030','Ranger 3.04','VNS_Halen_','Shadow 4.11','Crusade 4.42c','UlyssesWK','The Khanate','UnfairSteel','TRiBaL_Warrior','Barbarian','The Horde']
#ai_ladder = ['Reactionaryv9', 'Arabian_Knight', 'BambiV030', 'Barbarian', 'Crusade 4.42c', 'GamesGod', 'Ranger 3.04', 'Shadow 4.11', 'Subjugator', 'The Horde', 'The Khanate', 'The_Unknown3', 'TRiBaL_Warrior', 'UlyssesWK', 'UnfairSteel', 'Vicky', 'VNS_Chris_Tournament', 'VNS_Halen_']

all_ai_list = ['Ace', 'Alphav2', 'Alphav3', 'Alphav4', 'alpha_drush', 'Arabian_Knight', 'AT_Scout_Rush', 'BambiV030', 'Barbarian', 'best', 'Cal', 'CD', 'Crusade 4.42c', 'Flying_Monk', 'GamesGod', 'Hun Krush', 'king', 'Ranger 3.04', 'Reactionaryv9', 'Rhapsody0004', 'Shadow 0', 'Shadow 1', 'Shadow 2', 'Shadow 3.1', 'Shadow 4.11', 'Subjugator', 'The Horde', 'The Khanate', 'The_Unknown3', 'TRiBaL_Warrior', 'UCS', 'UlyssesWK', 'UnfairSteel', 'Vermin Supreme', 'Vicky', 'VNS_Chris_Tournament', 'VNS_Halen_']

civ = 'huns'
restart = False

force_age_up = False
allow_complex = False
force_house = True
allow_DUC = True

if restart:
    villager_preset = True
    force_imperial_age = False
    force_barracks = True
    force_resign = False
    force_scout = True
    allow_attack_rules = False
    force_castle_age_units = False

    allow_units = True
    allow_towers = False

else:
    villager_preset = True
    force_imperial_age = False
    force_barracks = True
    force_resign = True
    force_scout = True
    allow_attack_rules = True
    force_castle_age_units = False


allow_units = True
allow_towers = True

#DUC
#villager_preset = False
#force_imperial_age = False
#force_barracks = False
#force_resign = False
#force_scout = False
#allow_attack_rules = True
#force_castle_age_units = False
#
#allow_units = False
#allow_towers = False

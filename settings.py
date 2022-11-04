
fails_before_reset = 1000
#game_time = 3000
game_time = 6000

default_mutation_chance = .01
anneal_amount = 4 #bigger = less annealing
max_fact_length = 4
max_action_length = 3
ai_length = 0 #normal rules
simple_count = 150
attack_rule_count = 1

#network_drive = "C:/Users/mboop/Desktop/Shared/"
network_drive = "C:/Program Files/Microsoft Games/Age of Empires II/AI/"

eloDict = {'Hun Krush': 1745.128208, 'BambiV030': 1843.355396, 'UCS': 1669.937395, 'The Horde': 2008.261136, 'GamesGod': 1751.458229, 'Shadow 1': 1130.270815, 'Alphav4old': 1490.374699, 'Subjugator': 1847.823758, 'VNS_Chris_Tournament': 1687.102006, 'Vicky': 1707.662764, 'Ace': 1672.926251, 'Alphav3': 1211.091988, 'Shadow 0': 1081.197184, 'Barbarian': 2063.981729, 'kt_trainer': 803.970408, 'Flying_Monk': 1500.779466, 'Crusade 4.42c': 2253.207843, 'Reactionaryv9': 1672.520563, 'MDE': 861.9773302, 'VNS_Halen_': 1834.394246, 'The_Unknown3': 2062.802085, 'The Khanate': 1777.137909, 'Shadow 2': 1302.087291, 'king': 914.8197984, 'Arabian_Knight': 1848.035116, 'Shadow 4.11': 2167.584068, 'Cal': 1301.195953, 'alpha_drush': 862.7897774, 'Vermin Supreme': 1654.355526, 'Ranger 3.04': 1929.164509, 'TRiBaL_Warrior': 2312.385075, 'Shadow 3.1': 1492.129188, 'CD': 1166.636131, 'AT_Scout_Rush': 1314.765075, 'UnfairSteel': 2293.514252, 'Rhapsody0004': 1429.094763, 'UlyssesWK': 2025.904929, 'Alphav2': 1072.367715}

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

#ai_ladder = ["Vicky","Arabian_Knight","VNS_Chris_Tournament"]
ai_ladder = ["The_Unknown3","BambiV030"]
#ai_ladder = ['The_Unknown3','Vicky','GamesGod','BambiV030','Ranger 3.04','VNS_Halen_','Shadow 4.11','Crusade 4.42c','UlyssesWK','The Khanate','UnfairSteel','TRiBaL_Warrior','Barbarian','The Horde']
#ai_ladder = ['Reactionaryv9', 'Arabian_Knight', 'BambiV030', 'Barbarian', 'Crusade 4.42c', 'GamesGod', 'Ranger 3.04', 'Shadow 4.11', 'Subjugator', 'The Horde', 'The Khanate', 'The_Unknown3', 'TRiBaL_Warrior', 'UlyssesWK', 'UnfairSteel', 'Vicky', 'VNS_Chris_Tournament', 'VNS_Halen_']

all_ai_list = ['Ace', 'Alphav2', 'Alphav3', 'Alphav4', 'alpha_drush', 'Arabian_Knight', 'AT_Scout_Rush', 'BambiV030', 'Barbarian', 'best', 'Cal', 'CD', 'Crusade 4.42c', 'Flying_Monk', 'GamesGod', 'Hun Krush', 'king', 'Ranger 3.04', 'Reactionaryv9', 'Rhapsody0004', 'Shadow 0', 'Shadow 1', 'Shadow 2', 'Shadow 3.1', 'Shadow 4.11', 'Subjugator', 'The Horde', 'The Khanate', 'The_Unknown3', 'TRiBaL_Warrior', 'UCS', 'UlyssesWK', 'UnfairSteel', 'Vermin Supreme', 'Vicky', 'VNS_Chris_Tournament', 'VNS_Halen_']

civ = 'franks'
restart = False

allow_complex = True
force_house = True
force_buildings = False

if restart:
    villager_preset = True
    force_age_up = True
    force_imperial_age = False
    force_barracks = True
    force_resign = True
    force_scout = True
    force_attack_type_1 = False
    force_attack_type_2 = False
    allow_attack_rules = False
    force_castle_age_units = True

    allow_units = False
    allow_towers = False

else:
    villager_preset = True
    force_age_up = True
    force_imperial_age = False
    force_barracks = True
    force_resign = True
    force_scout = True
    force_attack_type_1 = False
    force_attack_type_2 = False
    allow_attack_rules = True
    force_castle_age_units = False

    allow_units = True
    allow_towers = True

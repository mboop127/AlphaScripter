import random
import json

#for testing
mutation_chance = .05
max_fact_length = 6
max_action_length = 3
ai_length = 500

paramdict = {'ActionId': '-1;600;601;602;603;604;605;606;607;608;609;610;611;612;613;614;615;616;617;618;619;620;621;631', 'Age': '0;1;2;3', 'AllyPlayer': '1;2;3;4;5;6;7;8;my-player-number;target-player;focus-player;-101;-103;-108;-201', 'AnyPlayer': '0;1;2;3;4;5;6;7;8;my-player-number;target-player;focus-player;-101;-102;-103;-104;-105;-106;-107;-108;-109;-110;-111;-201;-202;-203;-204;-205', 'BuildingId': '10;12;14;18;19;20;30;31;32;45;47;49;51;68;70;71;82;84;86;87;101;103;104;109;116;129;130;131;132;133;137;141;142;153;209;210;276;463;464;465;481;482;483;498;562;563;564;565;584;585;586;587;598;611;612;613;614;615;616;618;619;620;621;624;625;626;712;713;714;715;716;717;718;719;734;1189;1251', 'Civ': '0|18', 'ClassId': '-1;900;901;902;903;904;905;906;907;908;909;910;911;912;913;914;915;918;919;920;921;922;923;927;930;932;933;935;936;939;942;943;944;947;949;951;952;954;955;958;959', 'CmdId': '-1|10', 'ColorId': '1|8', 'Commodity': '0;1;2', 'compareOp': '>;>=;<;<=;==;!=;c:>;c:>=;c:<;c:<=;c:==;c:!=;g:>;g:>=;g:<;g:<=;g:==;g:!=;s:>;s:>=;s:<;s:<=;s:==;s:!=', 'ComputerAllyPlayer': '1;2;3;4;5;6;7;8;my-player-number;target-player;focus-player;-103', 'CustomResource': '0;1;2;3;907;908;909;910;915;932;933;958', 'difficulty': '0;1;2;3;4', 'DiffParameterId': '0;1', 'ElapsedTime': '1|120000', 'EscrowState': '0|512', 'ESPlayerStance': '0;1;3', 'EventID': '0|255', 'EventType': '0', 'ExploredState': '0;15;128', 'FactId': '0|54', 'FindPlayerMethod': '0;1;2;3', 'GameType': '0;1;2;3;5;6;7;8', 'GarrisonableUnitId': '35;422;548;545;141;481;482;612;483;82;79;234;236;235', 'GoalId': '1|512', 'GroupId': '0|9', 'GroupType': '100|109', 'Id': '0|32000', 'IdleType': '0;1;2;3', 'MapSize': '0|5', 'MapType': '-1;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;25;26;27;28;29;30;31;32;33;34;35;36;37;38;39;40;41;42;43;44', 'mathOp': '0|35', 'MaxDistance': '-1|32767', 'MaxGarrison': '-1|32767', 'MinDistance': '-1|32767', 'MinGarrison': '-1|32767', 'ObjectData': '-1|82', 'ObjectList': '0;1', 'ObjectStatus': '0;2;3;4;5', 'OnMainland': '-1;0;1', 'OrderId': '-1;700;701;702;703;704;705;706;707;708;709;710;711;712;713;714;715;716;717;718;719;720;721;731', 'Perimeter': '1;2', 'PlacementType': '0;1;2;3', 'PlayerId': '0|8', 'PlayerStance': '0;1;2;3', 'Point': '41|510', 'PositionType': '0|13', 'ProjectileType': '0|7', 'ResearchState': '0;1;2;3', 'Resource': '0;1;2;3', 'ResourceAmount': '0|224', 'SearchOrder': '0;1;2', 'SearchSource': '1;2', 'SharedGoalId': '1|256', 'SignalId': '0|255', 'SnId': '0;1;2;3;5;16;18;19;20;22;23;25;26;28;29;32;34;35;36;38;41;42;43;44;50;51;52;54;56;57;72;73;74;75;77;78;79;80;81;82;83;86;87;88;89;90;92;93;94;98;99;100;101;103;104;105;106;107;108;109;110;114;115;117;118;119;120;122;123;131;134;138;139;140;141;142;143;144;145;146;148;149;156;157;158;159;160;163;164;165;166;167;168;169;179;184;185;194;198;201;202;203;204;216;218;219;225;226;227;228;229;230;231;232;233;234;235;237;238;239;242;243;244;245;246;247;248;249;250;251;252;253;254;255;256;257;258;259;260;261;262;263;264;265;266;267;268;269;270;271;272;273;274;275;276;277;278;279;280;281;282;283;284;285;286;287;288;291;292;293;294;295', 'StartingResources': '1;2;3', 'State': '-1;0;1', 'Strict': '0;1', 'TauntId': '1|255', 'TechId': '2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;19;21;22;23;24;27;34;35;37;39;45;47;48;49;50;51;52;54;55;59;60;61;63;64;67;68;74;75;76;77;80;81;82;83;90;93;96;98;100;101;102;103;140;182;194;197;199;200;201;202;203;207;209;211;212;213;215;217;218;219;221;222;230;231;233;236;237;239;244;246;249;252;254;255;257;264;265;278;279;280;315;316;319;320;321;322;360;361;362;363;364;365;366;367;368;369;370;371;372;373;374;375;376;377;379;380;398;408;428;429;432;434;435;436;437;438;439;440;441;445;448;450;457', 'Terrain': '0|41', 'TimerId': '1|50', 'TimerState': '0;1;2', 'typeOp': 'c:;g:;s:', 'UnitId': '-299;-298;-297;-296;-295;-294;-293;-292;-291;-290;-289;-288;-287;-286;-285;-284;-283;-282;-281;-280;-279;-278;-277;-276;-275;-274;-273;-272;-271;-270;-269;-268;-267;-266;-265;-264;-1;4;5;6;7;8;11;13;17;21;24;25;35;36;38;39;40;41;42;46;56;57;73;74;75;77;83;93;106;114;118;120;122;123;124;125;128;156;183;184;185;203;204;207;208;212;214;216;218;220;222;223;230;232;239;250;259;260;279;280;281;282;283;286;291;293;329;330;331;354;358;359;418;420;422;440;441;442;448;453;459;467;473;474;492;494;527;528;529;530;531;532;533;534;539;542;545;546;548;553;554;555;556;557;558;559;560;561;567;569;579;581;588;590;592;653;691;692;694;701;725;726;732;751;752;753;755;757;759;760;761;762;763;765;766;771;773;774;775;782;784;811;823;827;829;830;831;832;836;861;866;868;869;871;873;875;876;878;879;881;882;886;887;891;900;901;902;903;904;905;906;907;908;909;910;911;912;913;914;915;918;919;920;921;922;923;927;930;932;933;935;936;939;942;943;944;947;949;951;952;954;955;958;959', 'UnitIdStrict': '4;5;6;7;8;11;13;17;21;24;25;35;36;38;39;40;41;42;46;56;57;73;74;75;77;83;93;106;114;118;120;122;123;124;125;128;156;183;184;185;203;204;207;208;212;214;216;218;220;222;223;230;232;239;250;259;260;279;280;281;282;283;286;291;293;329;330;331;354;358;359;418;420;422;440;441;442;448;453;459;467;473;474;492;494;527;528;529;530;531;532;533;534;539;542;545;546;548;553;554;555;556;557;558;559;560;561;567;569;579;581;588;590;592;653;691;692;694;701;725;726;732;751;752;753;755;757;759;760;761;762;763;765;766;771;773;774;775;782;784;811;823;827;829;830;831;832;836;861;866;868;869;871;873;875;876;878;879;881;882;886;887;891', 'value256': '0|255', 'value32': '-32768|32767', 'value32Positive': '1|32767', 'Victory': '0;1;2;3;4', 'WallId': '72;117;155;-399', 'RuleId': '0|32767', 'PriorityType': '0;1', 'ResetMode': '0;1', 'OnOff': '0;1', 'ObjectId': '-299;-298;-297;-296;-295;-294;-293;-292;-291;-290;-289;-288;-287;-286;-285;-284;-283;-282;-281;-280;-279;-278;-277;-276;-275;-274;-273;-272;-271;-270;-269;-268;-267;-266;-265;-264;-1;4;5;6;7;8;11;13;17;21;24;25;35;36;38;39;40;41;42;46;56;57;73;74;75;77;83;93;106;114;118;120;122;123;124;125;128;156;183;184;185;203;204;207;208;212;214;216;218;220;222;223;230;232;239;250;259;260;279;280;281;282;283;286;291;293;329;330;331;354;358;359;418;420;422;440;441;442;448;453;459;467;473;474;492;494;527;528;529;530;531;532;533;534;539;542;545;546;548;553;554;555;556;557;558;559;560;561;567;569;579;581;588;590;592;653;691;692;694;701;725;726;732;751;752;753;755;757;759;760;761;762;763;765;766;771;773;774;775;782;784;811;823;827;829;830;831;832;836;861;866;868;869;871;873;875;876;878;879;881;882;886;887;891;900;901;902;903;904;905;906;907;908;909;910;911;912;913;914;915;918;919;920;921;922;923;927;930;932;933;935;936;939;942;943;944;947;949;951;952;954;955;958;959,10;12;14;18;19;20;30;31;32;45;47;49;51;68;70;71;82;84;86;87;101;103;104;109;116;129;130;131;132;133;137;141;142;153;209;210;276;463;464;465;481;482;483;498;562;563;564;565;584;585;586;587;598;611;612;613;614;615;616;618;619;620;621;624;625;626;712;713;714;715;716;717;718;719;734;1189;1251', 'ScoutMethod': '0;1;2;3;4;5;6', 'AttackStance': '0;1;2;3', 'TargetAction': '0|18', 'Formation': '-1;2;4;7;8', '0|240': '0|240','0|40' : '0|40','0|239' : '0|239','83;293' : '83;293','EventType' : '0;0','-254|254' : '-254|254','-1|11' : '-1|11','0|100' : '0|100', '-1|250' : '-1|250', '1' : '1|1','GoalId2': '1|512'
}

facts = {'attack-soldier-count': ['2', 'compareOp', 'value32', '', ''], 'building-available': ['1', 'BuildingId', '', '', ''], 'building-count': ['2', 'compareOp', 'value32', '', ''], 'building-count-total': ['2', 'compareOp', 'value32', '', ''], 'building-type-count': ['3', 'BuildingId', 'compareOp', 'value32', ''], 'building-type-count-total': ['3', 'BuildingId', 'compareOp', 'value32', ''], 'can-afford-building': ['1', 'BuildingId', '', '', ''], 'can-afford-complete-wall': ['2', 'Perimeter', 'WallId', '', ''], 'can-afford-research': ['1', 'TechId', '', '', ''], 'can-afford-unit': ['1', 'UnitId', '', '', ''], 'can-build': ['1', 'BuildingId', '', '', ''], 'can-build-with-escrow': ['1', 'BuildingId', '', '', ''], 'can-build-gate': ['1', 'Perimeter', '', '', ''], 'can-build-gate-with-escrow': ['1', 'Perimeter', '', '', ''], 'can-build-wall': ['2', 'Perimeter', 'WallId', '', ''], 'can-build-wall-with-escrow': ['2', 'Perimeter', 'WallId', '', ''], 'can-buy-commodity': ['1', 'Commodity', '', '', ''], 'can-research': ['1', 'TechId', '', '', ''], 'can-research-with-escrow': ['1', 'TechId', '', '', ''], 'can-sell-commodity': ['1', 'Commodity', '', '', ''], 'can-spy': ['0', '', '', '', ''], 'can-spy-with-escrow': ['0', '', '', '', ''], 'can-train': ['1', 'UnitId', '', '', ''], 'can-train-with-escrow': ['1', 'UnitId', '', '', ''], 'civilian-population': ['2', 'compareOp', 'value32', '', ''], 'civ-selected': ['1', 'Civ', '', '', ''], 'commodity-buying-price': ['3', 'Commodity', 'compareOp', 'value32', ''], 'commodity-selling-price': ['3', 'Commodity', 'compareOp', 'value32', ''], 'current-age': ['1', 'typeOp', 'Age', '', ''], 'current-age-time': ['2', 'compareOp', 'value32', '', ''], 'current-score': ['2', 'compareOp', 'value32', '', ''], 'death-match-game': ['0', '', '', '', ''], 'defend-soldier-count': ['2', 'compareOp', 'value32', '', ''], 'defend-warboat-count': ['2', 'compareOp', 'value32', '', ''], 'difficulty': ['2', 'compareOp', 'difficulty', '', ''], 'doctrine': ['1', 'value32', '', '', ''], 'dropsite-min-distance': ['3', 'Resource', 'compareOp', 'value32', ''], 'enemy-buildings-in-town': ['0', '', '', '', ''], 'enemy-captured-relics': ['0', '', '', '', ''], 'escrow-amount': ['3', 'Resource', 'compareOp', 'value32', ''], 'event-detected': ['2', 'EventType', 'EventID', '', ''], 'false': ['0', '', '', '', ''], 'food-amount': ['2', 'compareOp', 'value32', '', ''], 'game-time': ['2', 'compareOp', 'value32', '', ''], 'game-type': ['2', 'compareOp', 'GameType', '', ''], 'gate-count': ['3', 'Perimeter', 'compareOp', 'value32', ''], 'goal': ['2', 'GoalId', 'value32', '', ''], 'gold-amount': ['2', 'compareOp', 'value32', '', ''], 'hold-koh-ruin': ['0', '', '', '', ''], 'hold-relics': ['0', '', '', '', ''], 'housing-headroom': ['2', 'compareOp', 'value32', '', ''], 'idle-farm-count': ['2', 'compareOp', 'value32', '', ''], 'map-size': ['1', 'MapSize', '', '', ''], 'map-type': ['1', 'MapType', '', '', ''], 'military-population': ['2', 'compareOp', 'value32', '', ''], 'player-computer': ['1', 'AnyPlayer', '', '', ''], 'player-human': ['1', 'AnyPlayer', '', '', ''], 'player-in-game': ['1', 'AnyPlayer', '', '', ''], 'player-number': ['1', 'AnyPlayer', '', '', ''], 'player-resigned': ['1', 'AnyPlayer', '', '', ''], 'player-valid': ['1', 'AnyPlayer', '', '', ''], 'players-building-count': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-building-type-count': ['4', 'AnyPlayer', 'BuildingId', 'compareOp', 'value32'], 'players-civ': ['2', 'AnyPlayer', 'Civ', '', ''], 'players-civilian-population': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-current-age': ['3', 'AnyPlayer', 'compareOp', 'Age', ''], 'players-current-age-time': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-military-population': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-population': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-score': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-stance': ['2', 'AnyPlayer', 'ESPlayerStance', '', ''], 'players-unit-count': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-unit-type-count': ['4', 'AnyPlayer', 'UnitId', 'compareOp', 'value32'], 'population': ['2', 'compareOp', 'value32', '', ''], 'population-cap': ['2', 'compareOp', 'value32', '', ''], 'population-headroom': ['2', 'compareOp', 'value32', '', ''], 'random-number': ['2', 'compareOp', 'value32', '', ''], 'research-available': ['1', 'TechId', '', '', ''], 'research-completed': ['1', 'TechId', '', '', ''], 'resource-found': ['1', 'Resource', '', '', ''], 'shared-goal': ['2', 'SharedGoalId', 'value32', '', ''], 'sheep-and-forage-too-far': ['0', '', '', '', ''], 'soldier-count': ['2', 'compareOp', 'value32', '', ''], 'stance-toward': ['2', 'AnyPlayer', 'ESPlayerStance', '', ''], 'starting-age': ['2', 'compareOp', 'Age', '', ''], 'starting-resources': ['2', 'compareOp', 'StartingResources', '', ''], 'stone-amount': ['2', 'compareOp', 'value32', '', ''], 'strategic-number': ['3', 'SnId', 'compareOp', 'value32', ''], 'timer-triggered': ['1', 'TimerId', '', '', ''], 'town-under-attack': ['0', '', '', '', ''], 'true': ['0', '', '', '', ''], 'unit-available': ['1', 'UnitId', '', '', ''], 'unit-count': ['2', 'compareOp', 'value32', '', ''], 'unit-count-total': ['2', 'compareOp', 'value32', '', ''], 'unit-type-count': ['3', 'UnitId', 'compareOp', 'value32', ''], 'unit-type-count-total': ['3', 'UnitId', 'compareOp', 'value32', ''], 'victory-condition': ['1', 'Victory', '', '', ''], 'wall-completed-percentage': ['3', 'Perimeter', 'compareOp', 'value32', ''], 'wall-invisible-percentage': ['3', 'Perimeter', 'compareOp', 'value32', ''], 'warboat-count': ['2', 'compareOp', 'value32', '', ''], 'wood-amount': ['2', 'compareOp', 'value32', '', ''], 'up-add-object-by-id': ['3', 'SearchSource', 'typeOp', 'Id', ''], 'up-allied-goal': ['4', 'ComputerAllyPlayer', 'GoalId', 'compareOp', 'value32'], 'up-allied-resource-amount': ['4', 'AllyPlayer', 'ResourceAmount', 'compareOp', 'value32'], 'up-allied-sn': ['4', 'ComputerAllyPlayer', 'SnId', 'compareOp', 'value32'], 'up-attacker-class': ['2', 'compareOp', 'ClassId', '', ''], 'up-building-type-in-town': ['4', 'typeOp', 'BuildingId', 'compareOp', 'value32'], 'up-can-build': ['3', 'EscrowState', 'typeOp', 'BuildingId', ''], 'up-can-build-line': ['4', 'EscrowState', 'Point', 'typeOp', 'BuildingId'], 'up-can-research': ['3', 'EscrowState', 'typeOp', 'TechId', ''], 'up-can-search': ['1', 'SearchSource', '', '', ''], 'up-can-train': ['3', 'EscrowState', 'typeOp', 'UnitId', ''], 'up-compare-const': ['3', 'value32', 'compareOp', 'value32', ''], 'up-compare-goal': ['3', 'GoalId', 'compareOp', 'value32', ''], 'up-compare-sn': ['3', 'SnId', 'compareOp', 'value32', ''], 'up-defender-count': ['2', 'compareOp', 'value32', '', ''], 'up-enemy-buildings-in-town': ['2', 'compareOp', 'value32', '', ''], 'up-enemy-units-in-town': ['2', 'compareOp', 'value32', '', ''], 'up-enemy-villagers-in-town': ['2', 'compareOp', 'value32', '', ''], 'up-find-remote': ['4', 'typeOp', 'UnitId', 'typeOp', '0|40'], 'up-find-resource': ['4', 'typeOp', 'CustomResource', 'typeOp', '0|240'], 'up-find-status-remote': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240'], 'up-gaia-type-count': ['4', 'typeOp', 'CustomResource', 'compareOp', 'value32'], 'up-gaia-type-count-total': ['4', 'typeOp', 'CustomResource', 'compareOp', 'value32'], 'up-get-object-data': ['2', 'ObjectData', 'GoalId', '', ''], 'up-get-object-target-data': ['2', 'ObjectData', 'GoalId', '', ''], 'up-get-point-contains': ['4', 'Point', 'GoalId', 'typeOp', 'ObjectId'], 'up-group-size': ['4', 'typeOp', 'GroupId', 'compareOp', 'value32'], 'up-idle-unit-count': ['3', 'IdleType', 'compareOp', 'value32', ''], 'up-modify-goal': ['3', 'GoalId', 'mathOp', 'value32', ''], 'up-object-data': ['3', 'ObjectData', 'compareOp', 'value32', ''], 'up-object-target-data': ['3', 'ObjectData', 'compareOp', 'value32', ''], 'up-object-type-count': ['4', 'typeOp', 'ObjectId', 'compareOp', 'value32'], 'up-object-type-count-total': ['4', 'typeOp', 'ObjectId', 'compareOp', 'value32'], 'up-path-distance': ['4', 'Point', 'Strict', 'compareOp', 'value32'], 'up-pending-objects': ['4', 'typeOp', 'ObjectId', 'compareOp', 'value32'], 'up-pending-placement': ['2', 'typeOp', 'BuildingId', '', ''], 'up-player-distance': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'up-players-in-game': ['3', 'PlayerStance', 'compareOp', 'value32', ''], 'up-point-contains': ['3', 'Point', 'typeOp', 'ObjectId', ''], 'up-point-distance': ['4', 'Point', 'Point', 'compareOp', 'value32'], 'up-point-elevation': ['4', 'Point', 'compareOp', 'value32', ''], 'up-point-explored': ['3', 'Point', 'typeOp', 'ExploredState', ''], 'up-point-terrain': ['3', 'Point', 'compareOp', 'Terrain', ''], 'up-point-zone': ['3', 'Point', 'compareOp', 'value32', ''], 'up-projectile-detected': ['3', 'ProjectileType', 'compareOp', 'ElapsedTime', ''], 'up-projectile-target': ['3', 'ProjectileType', 'compareOp', 'ClassId', ''], 'up-remaining-boar-amount': ['2', 'compareOp', 'value32', '', ''], 'up-research-status': ['4', 'typeOp', 'TechId', 'compareOp', 'ResearchState'], 'up-resource-amount': ['3', 'ResourceAmount', 'compareOp', 'value32', ''], 'up-resource-percent': ['3', 'ResourceAmount', 'compareOp', 'value32', ''], 'up-set-target-by-id': ['2', 'typeOp', 'Id', '', ''], 'up-set-target-object': ['3', 'SearchSource', 'typeOp', '0|239', ''], 'up-timer-status': ['3', 'TimerId', 'compareOp', 'TimerState', ''], 'up-train-site-ready': ['2', 'typeOp', 'UnitIdStrict', '', ''], 'up-unit-type-in-town': ['3', 'typeOp', 'UnitId', 'compareOp', 'value32'], 'up-villager-type-in-town': ['4', 'typeOp', '83;293', 'compareOp', 'value32'], 'up-allied-resource-percent': ['4', 'AllyPlayer', 'ResourceAmount', 'compareOp', 'value32'], 'up-find-local': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240']}

actions = {'acknowledge-event': ['2', 'EventType', 'EventID', '', ''], 'attack-now': ['0', '', '', '', ''], 'build': ['1', 'BuildingId', '', '', ''], 'build-forward': ['1', 'BuildingId', '', '', ''], 'build-gate': ['1', 'Perimeter', '', '', ''], 'build-wall': ['2', 'Perimeter', 'WallId', '', ''], 'buy-commodity': ['1', 'Commodity', '', '', ''], 'clear-tribute-memory': ['2', 'AnyPlayer', 'Resource', '', ''], 'delete-building': ['1', 'BuildingId', '', '', ''], 'delete-unit': ['1', 'UnitIdStrict', '', '', ''], 'disable-timer': ['1', 'TimerId', '', '', ''], 'do-nothing': ['0', '', '', '', ''], 'enable-timer': ['2', 'TimerId', 'value32Positive', '', ''], 'enable-wall-placement': ['1', 'Perimeter', '', '', ''], 'generate-random-number': ['1', 'value32Positive', '', '', ''], 'release-escrow': ['1', 'Resource', '', '', ''], 'research': ['1', 'TechId', '', '', ''], 'sell-commodity': ['1', 'Commodity', '', '', ''], 'set-difficulty-parameter': ['2', 'DiffParameterId', '0|100', '', ''], 'set-doctrine': ['1', 'value32', '', '', ''], 'set-escrow-percentage': ['2', 'Resource', 'value32', '', ''], 'set-goal': ['2', 'GoalId', 'value32', '', ''], 'set-shared-goal': ['2', 'SharedGoalId', 'value32', '', ''], 'set-signal': ['1', 'SignalId', '', '', ''], 'set-stance': ['2', 'AnyPlayer', 'ESPlayerStance', '', ''], 'set-strategic-number': ['2', 'SnId', 'value32', '', ''], 'spy': ['0', '', '', '', ''], 'train': ['1', 'UnitId', '', '', ''], 'tribute-to-player': ['3', 'AnyPlayer', 'Resource', 'value32Positive', ''], 'up-add-cost-data': ['3', 'GoalId', 'typeOp', 'value32', ''], 'up-add-object-by-id': ['3', 'SearchSource', 'typeOp', 'Id', ''], 'up-add-point': ['4', 'Point', 'Point', 'typeOp', 'value32'], 'up-add-research-cost': ['4', 'typeOp', 'TechId', 'typeOp', 'value32'], 'up-assign-builders': ['4', 'typeOp', 'BuildingId', 'typeOp', '-1|250'], 'up-bound-point': ['2', 'Point', 'Point', '', ''], 'up-bound-precise-point': ['4', 'Point', '1', 'typeOp', 'value32Positive'], 'up-build': ['4', 'PlacementType', 'EscrowState', 'typeOp', 'BuildingId'], 'up-build-line': ['4', 'Point', 'Point', 'typeOp', 'BuildingId'], 'up-buy-commodity': ['4', 'typeOp', 'ResourceAmount', 'typeOp', 'value32Positive'], 'up-clean-search': ['3', 'SearchSource', 'ObjectData', 'SearchOrder', ''], 'up-copy-point': ['2', 'Point', 'Point', '', ''], 'up-create-group': ['4', 'GoalId', 'GoalId2', 'typeOp', 'GroupId'], 'up-cross-tiles': ['4', 'Point', 'Point', 'typeOp', 'value32'], 'up-delete-distant-farms': ['2', 'typeOp', 'value256', '', ''], 'up-delete-idle-units': ['1', 'IdleType', '', '', ''], 'up-delete-objects': ['4', 'typeOp', 'UnitIdStrict', 'typeOp', 'value32Positive'], 'up-disband-group-type': ['1', 'GroupType', '', '', ''], 'up-drop-resources': ['3', 'Resource', 'typeOp', 'value32Positive', ''], 'up-filter-distance': ['4', 'typeOp', 'MinDistance', 'typeOp', 'MaxDistance'], 'up-filter-exclude': ['4', 'CmdId', 'ActionId', 'OrderId', 'ClassId'], 'up-filter-garrison': ['4', 'typeOp', 'MinGarrison', 'typeOp', 'MaxGarrison'], 'up-filter-include': ['4', 'CmdId', 'ActionId', 'OrderId', 'OnMainland'], 'up-filter-range': ['4', 'MinGarrison', 'MaxGarrison', 'MinDistance', 'MaxDistance'], 'up-filter-status': ['4', 'typeOp', 'ObjectStatus', 'typeOp', 'ObjectList'], 'up-find-local': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240'], 'up-find-next-player': ['3', 'PlayerStance', 'FindPlayerMethod', 'PlayerId', ''], 'up-find-player': ['3', 'PlayerStance', 'FindPlayerMethod', 'PlayerId', ''], 'up-find-remote': ['4', 'typeOp', 'UnitId', 'typeOp', '0|40'], 'up-find-resource': ['4', 'typeOp', 'Resource', 'typeOp', '0|240'], 'up-find-status-local': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240'], 'up-find-status-remote': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240'], 'up-full-reset-search': ['0', '', '', '', ''], 'up-garrison': ['3', 'GarrisonableUnitId', 'typeOp', 'UnitId', ''], 'up-gather-inside': ['4', 'typeOp', 'BuildingId', 'typeOp', 'State'], 'up-get-attacker-class': ['1', 'GoalId', '', '', ''], 'up-get-cost-delta': ['1', 'GoalId', '', '', ''], 'up-get-event': ['3', 'typeOp', 'EventID', 'GoalId', ''], 'up-get-group-size': ['3', 'typeOp', 'GroupId', 'GoalId', ''], 'up-get-indirect-goal': ['3', 'typeOp', 'GoalId', 'GoalId2', ''], 'up-get-object-data': ['2', 'ObjectData', 'GoalId', '', ''], 'up-get-object-target-data': ['2', 'ObjectData', 'GoalId', '', ''], 'up-get-path-distance': ['3', 'Point', 'Strict', 'GoalId', ''], 'up-get-player-color': ['2', 'AnyPlayer', 'ColorId', '', ''], 'up-get-point': ['2', 'PositionType', 'GoalId', '', ''], 'up-get-point-contains': ['4', 'GoalId', 'GoalId2', 'typeOp', 'ObjectId'], 'up-get-point-distance': ['3', 'Point', 'Point', 'GoalId', ''], 'up-get-point-elevation': ['2', 'Point', 'GoalId', '', ''], 'up-get-point-terrain': ['2', 'Point', 'Terrain', '', ''], 'up-get-point-zone': ['2', 'Point', 'GoalId', '', ''], 'up-get-precise-time': ['2', 'GoalId', 'GoalId2', '', ''], 'up-get-projectile-player': ['2', 'ProjectileType', 'PlayerId', '', ''], 'up-get-rule-id': ['1', 'RuleId', '', '', ''], 'up-get-search-state': ['1', 'GoalId', '', '', ''], 'up-get-shared-goal': ['3', 'typeOp', 'SharedGoalId', 'GoalId', ''], 'up-get-signal': ['3', 'typeOp', 'SignalId', 'GoalId', ''], 'up-get-threat-data': ['4', 'GoalId', 'PlayerId', 'GoalId', 'GoalId2'], 'up-get-timer': ['3', 'typeOp', 'TimerId', 'GoalId', ''], 'up-guard-unit': ['3', 'ObjectId', 'typeOp', 'UnitId', ''], 'up-jump-direct': ['2', 'typeOp', 'RuleId', '', ''], 'up-jump-dynamic': ['2', 'typeOp', 'value32', '', ''], 'up-jump-rule': ['1', 'value32', '', '', ''], 'up-lerp-percent': ['4', 'Point', 'Point', 'typeOp', 'value32'], 'up-lerp-tiles': ['4', 'Point', 'Point', 'typeOp', 'value32'], 'up-modify-escrow': ['3', 'Resource', 'mathOp', 'value32', ''], 'up-modify-goal': ['3', 'GoalId', 'mathOp', 'value32', ''], 'up-modify-group-flag': ['3', 'OnOff', 'typeOp', 'GroupId', ''], 'up-modify-sn': ['3', 'SnId', 'mathOp', 'value32', ''], 'up-release-escrow': ['0', '', '', '', ''], 'up-remove-objects': ['4', 'SearchSource', 'ObjectData', 'typeOp', 'value32'], 'up-request-hunters': ['2', 'typeOp', 'value32Positive', '', ''], 'up-research': ['3', 'EscrowState', 'typeOp', 'TechId', ''], 'up-reset-attack-now': ['0', '', '', '', ''], 'up-reset-building': ['3', 'OnOff', 'typeOp', 'BuildingId', ''], 'up-reset-cost-data': ['1', 'GoalId', '', '', ''], 'up-reset-filters': ['0', '', '', '', ''], 'up-reset-group': ['2', 'typeOp', 'GroupId', '', ''], 'up-reset-placement': ['2', 'typeOp', 'BuildingId', '', ''], 'up-reset-scouts': ['0', '', '', '', ''], 'up-reset-search': ['4', 'OnOff', 'OnOff', 'OnOff', 'OnOff'], 'up-reset-target-priorities': ['2', 'OnOff', 'OnOff', '', ''], 'up-reset-unit': ['2', 'typeOp', 'UnitId', '', ''], 'up-retask-gatherers': ['3', 'Resource', 'typeOp', 'value32Positive', ''], 'up-retreat-now': ['0', '', '', '', ''], 'up-retreat-to': ['3', 'ObjectId', 'typeOp', 'UnitId', ''], 'up-sell-commodity': ['4', 'typeOp', 'ResourceAmount', 'typeOp', 'value32Positive'], 'up-send-scout': ['2', 'GroupType', 'ScoutMethod', '', ''], 'up-set-attack-stance': ['3', 'UnitId', 'typeOp', 'AttackStance', ''], 'up-set-defense-priority': ['4', 'typeOp', 'BuildingId', 'typeOp', 'value32'], 'up-set-group': ['3', 'SearchSource', 'typeOp', 'GroupId', ''], 'up-set-indirect-goal': ['4', 'typeOp', 'GroupId', 'typeOp', 'value32'], 'up-set-offense-priority': ['4', 'typeOp', 'ObjectId', 'typeOp', '-1|11'], 'up-set-placement-data': ['4', 'AllyPlayer', 'ObjectId', 'typeOp', '-254|254'], 'up-set-precise-target-point': ['1', 'Point', '', '', ''], 'up-set-shared-goal': ['4', 'typeOp', 'SharedGoalId', 'typeOp', 'value32'], 'up-set-signal': ['4', 'typeOp', 'SignalId', 'typeOp', 'value32'], 'up-set-target-by-id': ['2', 'typeOp', 'Id', '', ''], 'up-set-target-object': ['3', 'SearchSource', 'typeOp', '0|239', ''], 'up-set-target-point': ['1', 'Point', '', '', ''], 'up-set-timer': ['4', 'typeOp', 'TimerId', 'typeOp', 'value32Positive'], 'up-setup-cost-data': ['2', 'OnOff', 'GoalId', '', ''], 'up-store-map-name': ['1', 'OnOff', '', '', ''], 'up-store-object-name': ['0', '', '', '', ''], 'up-store-player-name': ['1', 'AnyPlayer', '', '', ''], 'up-store-tech-name': ['1', 'typeOp', 'TechId', '', ''], 'up-target-point': ['4', 'Point', 'TargetAction', 'Formation', 'AttackStance'], 'up-train': ['3', 'EscrowState', 'typeOp', 'UnitId', ''], 'up-tribute-to-player': ['4', 'AnyPlayer', 'ResourceAmount', 'typeOp', 'value32Positive'], 'up-ungarrison': ['2', 'typeOp', 'ObjectId', '', ''], 'up-update-targets': ['0', '', '', '', '']}

paramkeys = list(paramdict.keys())
fact_list = list(facts.keys())
action_list = list(actions.keys())

def parse_params():
    f = open("params.csv","r")
    params = f.read().split("\n")
    f.close()

    paramdict = {}
    for i in range(len(params)):
        temp = params[i].split(",")
        if len(temp) > 1:
            paramdict[temp[0]] = temp[1]

    print(paramdict)

def mutate_parameters(parameters):

    for key in parameters:

        if key != '':
            mutation_rules = paramdict[key]

            if "|" in mutation_rules:
                mutation_rules = mutation_rules.split("|")
                if random.random() < mutation_chance:
                    parameters[key] = str(random.randint(int(mutation_rules[0]),int(mutation_rules[1])))

            elif ";" in mutation_rules:
                mutation_rules = mutation_rules.split(";")
                if random.random() < mutation_chance:
                    parameters[key] = random.choice(mutation_rules)


    return parameters

def generate_parameters():

    out = {'':''}

    for i in range(len(paramkeys)):

        mutation_rules = paramdict[paramkeys[i]]

        if "|" in mutation_rules:
            mutation_rules = mutation_rules.split("|")
            out[paramkeys[i]] = (random.randint(int(mutation_rules[0]),int(mutation_rules[1])))

        elif ";" in mutation_rules:
            mutation_rules = mutation_rules.split(";")
            out[paramkeys[i]] = random.choice(mutation_rules)


    return out

def generate_fact():

    fact_name = random.choice(fact_list)
    is_not = random.randint(0,1)
    params = generate_parameters()
    and_or = random.choice(["and","or","nand","nor"])

    fact = [fact_name, is_not, params, and_or]

    return fact

def generate_action():
    action_name = random.choice(action_list)
    params = generate_parameters()

    action = [action_name, params]

    return action

def mutate_fact(fact):

    fact_name = fact[0]
    is_not = fact[1]
    params = fact[2].copy()
    and_or = fact[3]

    if random.random() < mutation_chance:
        fact_name = random.choice(fact_list)

    if random.random() < mutation_chance:
        is_not = random.randint(0,1)

    params = mutate_parameters(params)

    if random.random() < mutation_chance:
        and_or = random.choice(["and","or","nand","nor"])

    fact = [fact_name, is_not, params, and_or]

    return fact

def mutate_action(action):

    action_name = action[0]
    params = action[1]

    if random.random() < mutation_chance:
        action_name = random.choice(action_list)

    params = mutate_parameters(params)

    action = [action_name, params]

    return action

def generate_rule():

    fact_length = random.randint(1,max_fact_length)
    action_length = random.randint(1,max_action_length)
    age_required = random.choice([["",""],["#load-if-not-defined DARK-AGE-END","#end-if"],["#load-if-not-defined FEUDAL-AGE-END","#end-if"],["#load-if-not-defined CASTLE-AGE-END","#end-if"],["#load-if-not-defined IMPERIAL-AGE-START","#end-if"]])

    local_facts = []
    local_actions = []

    for i in range(max_fact_length):
        local_facts.append(generate_fact())
        local_actions.append(generate_action())

    rule = [fact_length, action_length, age_required, local_facts, local_actions]

    return rule

def mutate_rule(rule):

    fact_length = rule[0]
    action_length = rule[1]
    age_required = rule[2]
    local_facts = rule[3]
    local_actions = rule[4]

    if random.random() < mutation_chance:
        fact_length = random.randint(1,max_fact_length)

    if random.random() < mutation_chance:
        action_length = random.randint(1,max_action_length)

    if random.random() < mutation_chance:
        age_required = random.choice([["",""],["#load-if-not-defined DARK-AGE-END","#end-if"],["#load-if-not-defined FEUDAL-AGE-END","#end-if"],["#load-if-not-defined CASTLE-AGE-END","#end-if"],["#load-if-not-defined IMPERIAL-AGE-START","#end-if"]])

    for i in range(len(local_facts)):
        local_facts[i] = mutate_fact(local_facts[i])
        local_actions[i] = mutate_action(local_actions[i])

    rule = [fact_length, action_length, age_required, local_facts, local_actions]

    return rule

def generate_ai():
    ai = []
    for i in range(ai_length):
        ai.append(generate_rule())

    return ai

def mutate_ai(ai):

    local = ai.copy()
    for i in range(len(ai)):
        local[i] = mutate_rule(local[i])

    return local

def crossover(ai_one, ai_two):

    out = []

    for i in range(len(ai_one)):
        out.append(random.choice([ai_one[i],ai_two[i]]))

    return out

def write_fact(local_facts, fact_length):

    string = "    "

    for i in range(fact_length):

        fact = local_facts[i]
        fact_name = fact[0]
        is_not = fact[1]
        params = fact[2]
        and_or = fact[3]

        string += "\n"


        if i < fact_length - 1:

            for l in range(i):
                string += "    "
            string += "    (" + and_or + " "

            if is_not == 1:
                string += "(not "

            string += " (" + fact_name + " " + str(params[facts[fact_name][1]]) + " " + str(params[facts[fact_name][2]]) + " " + str(params[facts[fact_name][3]]) + " " + str(params[facts[fact_name][4]]) + ")"

        else:
            for i in range(fact_length):
                string += "    "

            if is_not == 1:
                string += "(not "
            string += "(" + fact_name + " " + str(params[facts[fact_name][1]]) + " " + str(params[facts[fact_name][2]]) + " " + str(params[facts[fact_name][3]]) + " " + str(params[facts[fact_name][4]]) + ")\n"


            for i in range(fact_length-1):
                string += ")"

        if is_not == 1:
            string += ")"

    return string

def write_action(local_actions, action_length):

    string = "    "

    for i in range(action_length):

        action = local_actions[i]
        action_name = action[0]
        params = action[1]

        string += "\n"

        string += " (" + action_name + " " + str(params[actions[action_name][1]]) + " " + str(params[actions[action_name][2]]) + " " + str(params[actions[action_name][3]]) + " " + str(params[actions[action_name][4]]) + ")"


    return string

def write_rule(rule):

    fact_length = rule[0]
    action_length = rule[1]
    age_required = rule[2]
    local_facts = rule[3]
    local_actions = rule[4]

    string = ""
    string += "\n" + age_required[0] + "\n"
    string += "(defrule"
    string += write_fact(local_facts, fact_length)
    string += "\n=>"
    string += write_action(local_actions, action_length)
    string += ")\n" + age_required[1] + "\n\n"

    check = string.split(" ")
    while '' in check:
        check.remove('')

    if len(check) > 20:
        string = ""

    return string

def write_ai(ai, ai_name):

    f = open(ai_name + ".per","w+")
    for i in range(len(ai)):
        c = write_rule(ai[i])
        f.write(c)
    f.close()

def save_ai(ai, file):

    temp = {'lazy' : ai}

    with open(file + ".txt", 'w+') as outfile:
        json.dump(temp, outfile)

def read_ai(file):

    with open(file + '.txt') as json_file:
        data = json.load(json_file)

    out = data['lazy']

    return out
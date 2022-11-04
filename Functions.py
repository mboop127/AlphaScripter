import random
import copy
import json
from settings import *

paramdict = {
    "ActionId": "-1;600;601;602;603;604;605;606;607;608;609;610;611;612;613;614;615;616;617;618;619;620;621;631",
    "Age": "0;1;2;3",
    "AllyPlayer": "1;2;3;4;5;6;7;8;my-player-number;target-player;focus-player;-101;-103;-108;-201",
    "AnyPlayer": "0;1;2;3;4;5;6;7;8;my-player-number;target-player;focus-player;-101;-102;-103;-104;-105;-106;-107;-108;-109;-110;-111;-201;-202;-203;-204;-205",
    "BuildingId": "10;12;14;18;19;20;30;31;32;45;47;49;51;68;70;71;82;84;86;87;101;103;104;109;116;129;130;131;132;133;137;141;142;153;209;210;276;463;464;465;481;482;483;498;562;563;564;565;584;585;586;587;598;611;612;613;614;615;616;618;619;620;621;624;625;626;712;713;714;715;716;717;718;719;734;1189;1251",
    "Civ": "0|18",
    "ClassId": "-1;900;901;902;903;904;905;906;907;908;909;910;911;912;913;914;915;918;919;920;921;922;923;927;930;932;933;935;936;939;942;943;944;947;949;951;952;954;955;958;959",
    "CmdId": "-1|10",
    "ColorId": "1|8",
    "Commodity": "0;1;2",
    "compareOp": ">=;<=;==;!=;c:>;c:>=;c:<;c:<=;c:==;c:!=;g:>;g:>=;g:<;g:<=;g:==;g:!=;s:>;s:>=;s:<;s:<=;s:==;s:!=;<;>",
    "ComputerAllyPlayer": "1;2;3;4;5;6;7;8;my-player-number;target-player;focus-player;-103",
    "CustomResource": "0;1;2;3;907;908;909;910;915;932;933;958",
    "difficulty": "0;1;2;3;4",
    "DiffParameterId": "0;1",
    "ElapsedTime": "1|120000",
    "EscrowState": "0|512",
    "ESPlayerStance": "0;1;3",
    "EventID": "0|255",
    "EventType": "0",
    "ExploredState": "0;15;128",
    "FactId": "0|54",
    "FindPlayerMethod": "0;1;2;3",
    "GameType": "0;1;2;3;5;6;7;8",
    "GarrisonableUnitId": "35;422;548;545;141;481;482;612;483;82;79;234;236;235",
    "GoalId": "1|512",
    "GroupId": "0|9",
    "GroupType": "100|109",
    "Id": "0|32000",
    "IdleType": "0;1;2;3",
    "MapSize": "0|5",
    "MapType": "-1;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;25;26;27;28;29;30;31;32;33;34;35;36;37;38;39;40;41;42;43;44",
    "mathOp": "0|35",
    "MaxDistance": "-1|32767",
    "MaxGarrison": "-1|32767",
    "MinDistance": "-1|32767",
    "MinGarrison": "-1|32767",
    "ObjectData": "-1|82",
    "ObjectList": "0;1",
    "ObjectStatus": "0;2;3;4;5",
    "OnMainland": "-1;0;1",
    "OrderId": "-1;700;701;702;703;704;705;706;707;708;709;710;711;712;713;714;715;716;717;718;719;720;721;731",
    "Perimeter": "1;2",
    "PlacementType": "0;1;2;3",
    "PlayerId": "0|8",
    "PlayerStance": "0;1;2;3",
    "Point": "41|510",
    "PositionType": "0|13",
    "ProjectileType": "0|7",
    "ResearchState": "0;1;2;3",
    "Resource": "0;1;2;3",
    "ResourceAmount": "0|224",
    "SearchOrder": "0;1;2",
    "SearchSource": "1;2",
    "SharedGoalId": "1|256",
    "SignalId": "0|255",
    "SnValue": "-100|100",
    "2": "2;2",
    "SnId": "0;1;2;3;5;16;19;20;22;23;25;26;28;29;32;34;35;36;38;41;43;44;50;51;52;54;56;57;72;73;74;75;77;78;79;80;81;82;83;86;87;88;89;90;92;93;94;98;99;100;101;103;105;106;107;108;109;110;114;115;117;118;119;120;122;123;131;134;142;143;144;145;146;148;149;156;157;158;159;160;163;164;165;166;167;168;169;179;184;185;194;198;201;202;203;204;216;218;219;225;226;227;228;229;230;231;232;233;234;235;237;238;239;242;243;244;245;246;247;248;249;250;251;252;253;254;255;256;257;258;259;260;261;262;263;264;265;266;267;268;269;270;271;272;273;274;275;276;277;278;279;280;281;282;283;284;285;286;287;288;291;292;293;294;295", #removed 42 and 18 to prevent exploration rules change,
    "StartingResources": "1;2;3",
    "State": "-1;0;1",
    "Strict": "0;1",
    "TauntId": "1|255",
    "Terrain": "0|41",
    "TimerId": "1|50",
    "TimerState": "0;1;2",
    "typeOp": "c:;g:;s:",
    "UnitId": "-299;-298;-297;-296;-295;-294;-293;-292;-291;-290;-289;-288;-287;-286;-285;-284;-283;-282;-281;-280;-279;-278;-277;-276;-275;-274;-273;-272;-271;-270;-269;-268;-267;-266;-265;-264;-1;4;5;6;7;8;11;13;17;21;24;25;35;36;38;39;40;41;42;46;56;57;73;74;75;77;83;93;106;114;118;120;122;123;124;125;128;156;183;184;185;203;204;207;208;212;214;216;218;220;222;223;230;232;239;250;259;260;279;280;281;282;283;286;291;293;329;330;331;354;358;359;418;420;422;440;441;442;448;453;459;467;473;474;492;494;527;528;529;530;531;532;533;534;539;542;545;546;548;553;554;555;556;557;558;559;560;561;567;569;579;581;588;590;592;653;691;692;694;701;725;726;732;751;752;753;755;757;759;760;761;762;763;765;766;771;773;774;775;782;784;811;823;827;829;830;831;832;836;861;866;868;869;871;873;875;876;878;879;881;882;886;887;891;900;901;902;903;904;905;906;907;908;909;910;911;912;913;914;915;918;919;920;921;922;923;927;930;932;933;935;936;939;942;943;944;947;949;951;952;954;955;958;959",
    "UnitIdStrict": "4;5;6;7;8;11;13;17;21;24;25;35;36;38;39;40;41;42;46;56;57;73;74;75;77;83;93;106;114;118;120;122;123;124;125;128;156;183;184;185;203;204;207;208;212;214;216;218;220;222;223;230;232;239;250;259;260;279;280;281;282;283;286;291;293;329;330;331;354;358;359;418;420;422;440;441;442;448;453;459;467;473;474;492;494;527;528;529;530;531;532;533;534;539;542;545;546;548;553;554;555;556;557;558;559;560;561;567;569;579;581;588;590;592;653;691;692;694;701;725;726;732;751;752;753;755;757;759;760;761;762;763;765;766;771;773;774;775;782;784;811;823;827;829;830;831;832;836;861;866;868;869;871;873;875;876;878;879;881;882;886;887;891",
    "value256": "0|255",
    "value32": "-32768|32767",
    "value32Positive": "1|32767",
    "Victory": "0;1;2;3;4",
    "WallId": "72;117;155;-399",
    "RuleId": "0|32767",
    "PriorityType": "0;1",
    "ResetMode": "0;1",
    "OnOff": "0;1",
    "ObjectId": "-299;-298;-297;-296;-295;-294;-293;-292;-291;-290;-289;-288;-287;-286;-285;-284;-283;-282;-281;-280;-279;-278;-277;-276;-275;-274;-273;-272;-271;-270;-269;-268;-267;-266;-265;-264;-1;4;5;6;7;8;11;13;17;21;24;25;35;36;38;39;40;41;42;46;56;57;73;74;75;77;83;93;106;114;118;120;122;123;124;125;128;156;183;184;185;203;204;207;208;212;214;216;218;220;222;223;230;232;239;250;259;260;279;280;281;282;283;286;291;293;329;330;331;354;358;359;418;420;422;440;441;442;448;453;459;467;473;474;492;494;527;528;529;530;531;532;533;534;539;542;545;546;548;553;554;555;556;557;558;559;560;561;567;569;579;581;588;590;592;653;691;692;694;701;725;726;732;751;752;753;755;757;759;760;761;762;763;765;766;771;773;774;775;782;784;811;823;827;829;830;831;832;836;861;866;868;869;871;873;875;876;878;879;881;882;886;887;891;900;901;902;903;904;905;906;907;908;909;910;911;912;913;914;915;918;919;920;921;922;923;927;930;932;933;935;936;939;942;943;944;947;949;951;952;954;955;958;959,10;12;14;18;19;20;30;31;32;45;47;49;51;68;70;71;82;84;86;87;101;103;104;109;116;129;130;131;132;133;137;141;142;153;209;210;276;463;464;465;481;482;483;498;562;563;564;565;584;585;586;587;598;611;612;613;614;615;616;618;619;620;621;624;625;626;712;713;714;715;716;717;718;719;734;1189;1251",
    "ScoutMethod": "0;1;2;3;4;5;6",
    "AttackStance": "0;1;2;3",
    "TargetAction": "0|18",
    "Formation": "-1;2;4;7;8",
    "0|240": "0|240",
    "0|40": "0|40",
    "0|239": "0|239",
    "83;293": "83;293",
    "EventType": "0;0",
    "-254|254": "-254|254",
    "-1|11": "-1|11",
    "0|100": "0|100",
    "-1|250": "-1|250",
    "1": "1|1",
    "GoalId2": "1|512",
    #"Trainable": "759;militiaman-line;spearman-line;battering-ram-line;mangonel-line;scorpion-line;villager;trebuchet;petard;5;monk;886;36;huskarl-line",
    "Trainable": "archer-line;cavalry-archer-line;skirmisher-line;militiaman-line;spearman-line;battering-ram-line;mangonel-line;scorpion-line;camel-line;knight-line;scout-cavalry-line;tarkan-line;villager;trebuchet;petard;5;monk;886;36;huskarl-line",
    "Buildable": "town-center;farm;house;mill;mining-camp;lumber-camp;dock;blacksmith;market;monastery;university;wonder;barracks;archery-range;stable;siege-workshop;outpost;castle;stone-wall;palisade-wall;gate",
    "TechId":"2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;19;21;22;23;24;27;34;35;37;39;45;47;48;49;50;51;52;54;55;59;60;61;63;64;67;68;74;75;76;77;80;81;82;83;90;93;96;98;100;101;102;103;140;182;194;197;199;200;201;202;203;207;209;211;212;213;215;217;218;219;221;222;230;231;233;236;237;239;244;246;249;252;254;255;257;264;265;278;279;280;315;316;319;320;321;322;360;361;362;363;364;365;366;367;368;369;370;371;372;373;374;375;376;377;379;380;398;408;428;429;432;434;435;436;437;438;439;440;441;445;448;450;457",
    #"TechId": "2;6;7;8;9;10;11;12;13;14;15;16;17;19;21;22;23;39;45;47;48;50;51;52;54;55;59;63;64;67;68;74;75;76;77;80;81;82;83;90;93;96;98;100;101;102;103;140;182;194;197;199;200;201;202;203;207;209;211;212;213;215;217;218;219;221;222;230;231;233;236;237;239;249;252;254;255;257;264;265;278;279;280;315;316;319;320;321;322;377;379;380;408;428;429;435;437;438;439;441;445;457",
    "0|10": "0|10",
    "0|200": "0|200",
    "0|50000": "0|50000",
    "0|50": "0|50",
    "0|20000": "0|20000",
    "0|170": "0|170",
    "14|1000": "14|1000",
    "25|1000": "25|1000",
}


facts = {
    "attack-soldier-count": ["2", "compareOp", "0|200", "", ""],
    "building-available": ["1", "BuildingId", "", "", ""],
    "building-count": ["2", "compareOp", "0|50", "", ""],
    "building-count-total": ["2", "compareOp", "0|200", "", ""],
    "building-type-count": ["3", "BuildingId", "compareOp", "0|50", ""],
    "building-type-count-total": ["3", "BuildingId", "compareOp", "0|50", ""],
    "can-afford-building": ["1", "BuildingId", "", "", ""],
    "can-afford-complete-wall": ["2", "Perimeter", "WallId", "", ""],
    "can-afford-research": ["1", "TechId", "", "", ""],
    "can-afford-unit": ["1", "UnitId", "", "", ""],
    "can-build": ["1", "BuildingId", "", "", ""],
    "can-build-with-escrow": ["1", "BuildingId", "", "", ""],
    "can-build-gate": ["1", "Perimeter", "", "", ""],
    "can-build-gate-with-escrow": ["1", "Perimeter", "", "", ""],
    "can-build-wall": ["2", "Perimeter", "WallId", "", ""],
    "can-build-wall-with-escrow": ["2", "Perimeter", "WallId", "", ""],
    "can-buy-commodity": ["1", "Commodity", "", "", ""],
    "can-research": ["1", "TechId", "", "", ""],
    "can-research-with-escrow": ["1", "TechId", "", "", ""],
    "can-sell-commodity": ["1", "Commodity", "", "", ""],
    "can-spy": ["0", "", "", "", ""],
    "can-spy-with-escrow": ["0", "", "", "", ""],
    "can-train": ["1", "UnitId", "", "", ""],
    "can-train-with-escrow": ["1", "UnitId", "", "", ""],
    "civilian-population": ["2", "compareOp", "0|200", "", ""],
    "civ-selected": ["1", "Civ", "", "", ""],
    "commodity-buying-price": ["3", "Commodity", "compareOp", "25|1000", ""],
    "commodity-selling-price": ["3", "Commodity", "compareOp", "14|1000", ""],
    "current-age": ["1", "compareOp", "Age", "", ""], #maybe cause issues
    "current-age-time": ["2", "compareOp", "0|20000", "", ""],
    "current-score": ["2", "compareOp", "0|50000", "", ""],
    "death-match-game": ["0", "", "", "", ""],
    "defend-soldier-count": ["2", "compareOp", "0|200", "", ""],
    "difficulty": ["2", "compareOp", "difficulty", "", ""],
    "doctrine": ["1", "value32", "", "", ""],
    "dropsite-min-distance": ["3", "Resource", "compareOp", "0|170", ""],
    "enemy-buildings-in-town": ["0", "", "", "", ""],
    "enemy-captured-relics": ["0", "", "", "", ""],
    "escrow-amount": ["3", "Resource", "compareOp", "0|50000", ""],
    "event-detected": ["2", "EventType", "EventID", "", ""],
    "false": ["0", "", "", "", ""],
    "food-amount": ["2", "compareOp", "0|50000", "", ""],
    "game-time": ["2", "compareOp", "0|20000", "", ""],
    "game-type": ["2", "compareOp", "GameType", "", ""],
    "gate-count": ["3", "Perimeter", "compareOp", "0|50", ""],
    "goal": ["2", "GoalId", "value32", "", ""],
    "gold-amount": ["2", "compareOp", "0|50000", "", ""],
    "hold-koh-ruin": ["0", "", "", "", ""],
    "hold-relics": ["0", "", "", "", ""],
    "housing-headroom": ["2", "compareOp", "0|200", "", ""],
    "idle-farm-count": ["2", "compareOp", "0|50", "", ""],
    "map-size": ["1", "MapSize", "", "", ""],
    "map-type": ["1", "MapType", "", "", ""],
    "military-population": ["2", "compareOp", "0|200", "", ""],
    "player-computer": ["1", "AnyPlayer", "", "", ""],
    "player-human": ["1", "AnyPlayer", "", "", ""],
    "player-in-game": ["1", "AnyPlayer", "", "", ""],
    "player-number": ["1", "AnyPlayer", "", "", ""],
    "player-resigned": ["1", "AnyPlayer", "", "", ""],
    "player-valid": ["1", "AnyPlayer", "", "", ""],
    "players-building-count": ["3", "AnyPlayer", "compareOp", "0|50", ""],
    "players-building-type-count": [
        "4",
        "AnyPlayer",
        "BuildingId",
        "compareOp",
        "0|50",
    ],
    "players-civ": ["2", "AnyPlayer", "Civ", "", ""],
    "players-civilian-population": ["3", "AnyPlayer", "compareOp", "0|200", ""],
    "players-current-age": ["3", "AnyPlayer", "compareOp", "Age", ""],
    "players-current-age-time": ["3", "AnyPlayer", "compareOp", "0|20000", ""],
    "players-military-population": ["3", "AnyPlayer", "compareOp", "0|200", ""],
    "players-population": ["3", "AnyPlayer", "compareOp", "0|200", ""],
    "players-score": ["3", "AnyPlayer", "compareOp", "0|50000", ""],
    "players-stance": ["2", "AnyPlayer", "ESPlayerStance", "", ""],
    "players-unit-count": ["3", "AnyPlayer", "compareOp", "0|200", ""],
    "players-unit-type-count": ["4", "AnyPlayer", "UnitId", "compareOp", "0|200"],
    "population": ["2", "compareOp", "0|200", "", ""],
    "population-cap": ["2", "compareOp", "0|200", "", ""],
    "population-headroom": ["2", "compareOp", "0|200", "", ""],
    "random-number": ["2", "compareOp", "value32", "", ""],
    "research-available": ["1", "TechId", "", "", ""],
    "research-completed": ["1", "TechId", "", "", ""],
    "resource-found": ["1", "Resource", "", "", ""],
    "shared-goal": ["2", "SharedGoalId", "value32", "", ""],
    "sheep-and-forage-too-far": ["0", "", "", "", ""],
    "soldier-count": ["2", "compareOp", "0|200", "", ""],
    "stance-toward": ["2", "AnyPlayer", "ESPlayerStance", "", ""],
    "starting-age": ["2", "compareOp", "Age", "", ""],
    "starting-resources": ["2", "compareOp", "StartingResources", "", ""],
    "stone-amount": ["2", "compareOp", "0|50000", "", ""],
    "strategic-number": ["3", "SnId", "compareOp", "value32", ""],
    "timer-triggered": ["1", "TimerId", "", "", ""],
    "town-under-attack": ["0", "", "", "", ""],
    "true": ["0", "", "", "", ""],
    "unit-available": ["1", "UnitId", "", "", ""],
    "unit-count": ["2", "compareOp", "0|200", "", ""],
    "unit-count-total": ["2", "compareOp", "0|200", "", ""],
    "unit-type-count": ["3", "UnitId", "compareOp", "0|200", ""],
    "unit-type-count-total": ["3", "UnitId", "compareOp", "0|200", ""],
    "victory-condition": ["1", "Victory", "", "", ""],
    "wall-completed-percentage": ["3", "Perimeter", "compareOp", "0|100", ""],
    "wall-invisible-percentage": ["3", "Perimeter", "compareOp", "0|100", ""],
    "wood-amount": ["2", "compareOp", "0|50000", "", ""],
    "up-add-object-by-id": ["3", "SearchSource", "typeOp", "Id", ""],
    "up-allied-goal": ["4", "ComputerAllyPlayer", "GoalId", "compareOp", "value32"],
    "up-allied-resource-amount": [
        "4",
        "AllyPlayer",
        "ResourceAmount",
        "compareOp",
        "value32",
    ],
    "up-allied-sn": ["4", "ComputerAllyPlayer", "SnId", "compareOp", "value32"],
    "up-attacker-class": ["2", "compareOp", "ClassId", "", ""],
    "up-building-type-in-town": ["4", "typeOp", "BuildingId", "compareOp", "0|50"],
    "up-can-build": ["3", "EscrowState", "typeOp", "BuildingId", ""],
    "up-can-build-line": ["4", "EscrowState", "Point", "typeOp", "BuildingId"],
    "up-can-research": ["3", "EscrowState", "typeOp", "TechId", ""],
    "up-can-search": ["1", "SearchSource", "", "", ""],
    "up-can-train": ["3", "EscrowState", "typeOp", "UnitId", ""],
    "up-compare-const": ["3", "value32", "compareOp", "value32", ""],
    "up-compare-goal": ["3", "GoalId", "compareOp", "value32", ""],
    "up-compare-sn": ["3", "SnId", "compareOp", "value32", ""],
    "up-defender-count": ["2", "compareOp", "0|200", "", ""],
    "up-enemy-buildings-in-town": ["2", "compareOp", "0|50", "", ""],
    "up-enemy-units-in-town": ["2", "compareOp", "0|200", "", ""],
    "up-enemy-villagers-in-town": ["2", "compareOp", "0|200", "", ""],
    "up-find-remote": ["4", "typeOp", "UnitId", "typeOp", "0|40"],
    "up-find-resource": ["4", "typeOp", "CustomResource", "typeOp", "0|240"],
    "up-find-status-remote": ["4", "typeOp", "UnitId", "typeOp", "0|240"],
    "up-gaia-type-count": ["4", "typeOp", "CustomResource", "compareOp", "0|200"],
    "up-gaia-type-count-total": [
        "4",
        "typeOp",
        "CustomResource",
        "compareOp",
        "0|200",
    ],
    "up-get-object-data": ["2", "ObjectData", "GoalId", "", ""],
    "up-get-object-target-data": ["2", "ObjectData", "GoalId", "", ""],
    "up-get-point-contains": ["4", "Point", "GoalId", "typeOp", "ObjectId"],
    "up-group-size": ["4", "typeOp", "GroupId", "compareOp", "0|200"],
    "up-idle-unit-count": ["3", "IdleType", "compareOp", "0|200", ""],
    "up-modify-goal": ["3", "GoalId", "mathOp", "value32", ""],
    "up-object-data": ["3", "ObjectData", "compareOp", "value32", ""],
    "up-object-target-data": ["3", "ObjectData", "compareOp", "value32", ""],
    "up-object-type-count": ["4", "typeOp", "ObjectId", "compareOp", "value32"],
    "up-object-type-count-total": ["4", "typeOp", "ObjectId", "compareOp", "value32"],
    "up-path-distance": ["4", "Point", "Strict", "compareOp", "0|170"],
    "up-pending-objects": ["4", "typeOp", "ObjectId", "compareOp", "value32"],
    "up-pending-placement": ["2", "typeOp", "BuildingId", "", ""],
    "up-player-distance": ["3", "AnyPlayer", "compareOp", "0|170", ""],
    "up-players-in-game": ["3", "PlayerStance", "compareOp", "2", ""],
    "up-point-contains": ["3", "Point", "typeOp", "ObjectId", ""],
    "up-point-distance": ["4", "Point", "Point", "compareOp", "0|170"],
    "up-point-elevation": ["4", "Point", "compareOp", "value32", ""],
    "up-point-explored": ["3", "Point", "typeOp", "ExploredState", ""],
    "up-point-terrain": ["3", "Point", "compareOp", "Terrain", ""],
    "up-point-zone": ["3", "Point", "compareOp", "value32", ""],
    "up-projectile-detected": ["3", "ProjectileType", "compareOp", "ElapsedTime", ""],
    "up-projectile-target": ["3", "ProjectileType", "compareOp", "ClassId", ""],
    "up-remaining-boar-amount": ["2", "compareOp", "0|10", "", ""],
    "up-research-status": ["4", "typeOp", "TechId", "compareOp", "ResearchState"],
    "up-resource-amount": ["3", "ResourceAmount", "compareOp", "0|50000", ""],
    "up-resource-percent": ["3", "ResourceAmount", "compareOp", "0|100", ""],
    "up-set-target-by-id": ["2", "typeOp", "Id", "", ""],
    "up-set-target-object": ["3", "SearchSource", "typeOp", "0|239", ""],
    "up-timer-status": ["3", "TimerId", "compareOp", "TimerState", ""],
    "up-train-site-ready": ["2", "typeOp", "UnitIdStrict", "", ""],
    "up-unit-type-in-town": ["3", "typeOp", "UnitId", "compareOp", "0|200"],
    "up-villager-type-in-town": ["4", "typeOp", "83;293", "compareOp", "0|200"],
    "up-allied-resource-percent": [
        "4",
        "AllyPlayer",
        "ResourceAmount",
        "compareOp",
        "0|100",
    ],
    "up-find-local": ["4", "typeOp", "UnitId", "typeOp", "0|240"],
}

#facts = {'attack-soldier-count': ['2', 'compareOp', 'value32', '', ''], 'building-available': ['1', 'BuildingId', '', '', ''], 'building-count': ['2', 'compareOp', 'value32', '', ''], 'building-count-total': ['2', 'compareOp', 'value32', '', ''], 'building-type-count': ['3', 'BuildingId', 'compareOp', 'value32', ''], 'building-type-count-total': ['3', 'BuildingId', 'compareOp', 'value32', ''], 'can-afford-building': ['1', 'BuildingId', '', '', ''], 'can-afford-complete-wall': ['2', 'Perimeter', 'WallId', '', ''], 'can-afford-research': ['1', 'TechId', '', '', ''], 'can-afford-unit': ['1', 'UnitId', '', '', ''], 'can-build': ['1', 'BuildingId', '', '', ''], 'can-build-with-escrow': ['1', 'BuildingId', '', '', ''], 'can-build-gate': ['1', 'Perimeter', '', '', ''], 'can-build-gate-with-escrow': ['1', 'Perimeter', '', '', ''], 'can-build-wall': ['2', 'Perimeter', 'WallId', '', ''], 'can-build-wall-with-escrow': ['2', 'Perimeter', 'WallId', '', ''], 'can-buy-commodity': ['1', 'Commodity', '', '', ''], 'can-research': ['1', 'TechId', '', '', ''], 'can-research-with-escrow': ['1', 'TechId', '', '', ''], 'can-sell-commodity': ['1', 'Commodity', '', '', ''], 'can-spy': ['0', '', '', '', ''], 'can-spy-with-escrow': ['0', '', '', '', ''], 'can-train': ['1', 'UnitId', '', '', ''], 'can-train-with-escrow': ['1', 'UnitId', '', '', ''], 'civilian-population': ['2', 'compareOp', 'value32', '', ''], 'civ-selected': ['1', 'Civ', '', '', ''], 'commodity-buying-price': ['3', 'Commodity', 'compareOp', 'value32', ''], 'commodity-selling-price': ['3', 'Commodity', 'compareOp', 'value32', ''], 'current-age': ['1', 'typeOp', 'Age', '', ''], 'current-age-time': ['2', 'compareOp', 'value32', '', ''], 'current-score': ['2', 'compareOp', 'value32', '', ''], 'death-match-game': ['0', '', '', '', ''], 'defend-soldier-count': ['2', 'compareOp', 'value32', '', ''], 'defend-warboat-count': ['2', 'compareOp', 'value32', '', ''], 'difficulty': ['2', 'compareOp', 'difficulty', '', ''], 'doctrine': ['1', 'value32', '', '', ''], 'dropsite-min-distance': ['3', 'Resource', 'compareOp', 'value32', ''], 'enemy-buildings-in-town': ['0', '', '', '', ''], 'enemy-captured-relics': ['0', '', '', '', ''], 'escrow-amount': ['3', 'Resource', 'compareOp', 'value32', ''], 'event-detected': ['2', 'EventType', 'EventID', '', ''], 'false': ['0', '', '', '', ''], 'food-amount': ['2', 'compareOp', 'value32', '', ''], 'game-time': ['2', 'compareOp', 'value32', '', ''], 'game-type': ['2', 'compareOp', 'GameType', '', ''], 'gate-count': ['3', 'Perimeter', 'compareOp', 'value32', ''], 'goal': ['2', 'GoalId', 'value32', '', ''], 'gold-amount': ['2', 'compareOp', 'value32', '', ''], 'hold-koh-ruin': ['0', '', '', '', ''], 'hold-relics': ['0', '', '', '', ''], 'housing-headroom': ['2', 'compareOp', 'value32', '', ''], 'idle-farm-count': ['2', 'compareOp', 'value32', '', ''], 'map-size': ['1', 'MapSize', '', '', ''], 'map-type': ['1', 'MapType', '', '', ''], 'military-population': ['2', 'compareOp', 'value32', '', ''], 'player-computer': ['1', 'AnyPlayer', '', '', ''], 'player-human': ['1', 'AnyPlayer', '', '', ''], 'player-in-game': ['1', 'AnyPlayer', '', '', ''], 'player-number': ['1', 'AnyPlayer', '', '', ''], 'player-resigned': ['1', 'AnyPlayer', '', '', ''], 'player-valid': ['1', 'AnyPlayer', '', '', ''], 'players-building-count': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-building-type-count': ['4', 'AnyPlayer', 'BuildingId', 'compareOp', 'value32'], 'players-civ': ['2', 'AnyPlayer', 'Civ', '', ''], 'players-civilian-population': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-current-age': ['3', 'AnyPlayer', 'compareOp', 'Age', ''], 'players-current-age-time': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-military-population': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-population': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-score': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-stance': ['2', 'AnyPlayer', 'ESPlayerStance', '', ''], 'players-unit-count': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'players-unit-type-count': ['4', 'AnyPlayer', 'UnitId', 'compareOp', 'value32'], 'population': ['2', 'compareOp', 'value32', '', ''], 'population-cap': ['2', 'compareOp', 'value32', '', ''], 'population-headroom': ['2', 'compareOp', 'value32', '', ''], 'random-number': ['2', 'compareOp', 'value32', '', ''], 'research-available': ['1', 'TechId', '', '', ''], 'research-completed': ['1', 'TechId', '', '', ''], 'resource-found': ['1', 'Resource', '', '', ''], 'shared-goal': ['2', 'SharedGoalId', 'value32', '', ''], 'sheep-and-forage-too-far': ['0', '', '', '', ''], 'soldier-count': ['2', 'compareOp', 'value32', '', ''], 'stance-toward': ['2', 'AnyPlayer', 'ESPlayerStance', '', ''], 'starting-age': ['2', 'compareOp', 'Age', '', ''], 'starting-resources': ['2', 'compareOp', 'StartingResources', '', ''], 'stone-amount': ['2', 'compareOp', 'value32', '', ''], 'strategic-number': ['3', 'SnId', 'compareOp', 'value32', ''], 'timer-triggered': ['1', 'TimerId', '', '', ''], 'town-under-attack': ['0', '', '', '', ''], 'true': ['0', '', '', '', ''], 'unit-available': ['1', 'UnitId', '', '', ''], 'unit-count': ['2', 'compareOp', 'value32', '', ''], 'unit-count-total': ['2', 'compareOp', 'value32', '', ''], 'unit-type-count': ['3', 'UnitId', 'compareOp', 'value32', ''], 'unit-type-count-total': ['3', 'UnitId', 'compareOp', 'value32', ''], 'victory-condition': ['1', 'Victory', '', '', ''], 'wall-completed-percentage': ['3', 'Perimeter', 'compareOp', 'value32', ''], 'wall-invisible-percentage': ['3', 'Perimeter', 'compareOp', 'value32', ''], 'warboat-count': ['2', 'compareOp', 'value32', '', ''], 'wood-amount': ['2', 'compareOp', 'value32', '', ''], 'up-add-object-by-id': ['3', 'SearchSource', 'typeOp', 'Id', ''], 'up-allied-goal': ['4', 'ComputerAllyPlayer', 'GoalId', 'compareOp', 'value32'], 'up-allied-resource-amount': ['4', 'AllyPlayer', 'ResourceAmount', 'compareOp', 'value32'], 'up-allied-sn': ['4', 'ComputerAllyPlayer', 'SnId', 'compareOp', 'value32'], 'up-attacker-class': ['2', 'compareOp', 'ClassId', '', ''], 'up-building-type-in-town': ['4', 'typeOp', 'BuildingId', 'compareOp', 'value32'], 'up-can-build': ['3', 'EscrowState', 'typeOp', 'BuildingId', ''], 'up-can-build-line': ['4', 'EscrowState', 'Point', 'typeOp', 'BuildingId'], 'up-can-research': ['3', 'EscrowState', 'typeOp', 'TechId', ''], 'up-can-search': ['1', 'SearchSource', '', '', ''], 'up-can-train': ['3', 'EscrowState', 'typeOp', 'UnitId', ''], 'up-compare-const': ['3', 'value32', 'compareOp', 'value32', ''], 'up-compare-goal': ['3', 'GoalId', 'compareOp', 'value32', ''], 'up-compare-sn': ['3', 'SnId', 'compareOp', 'value32', ''], 'up-defender-count': ['2', 'compareOp', 'value32', '', ''], 'up-enemy-buildings-in-town': ['2', 'compareOp', 'value32', '', ''], 'up-enemy-units-in-town': ['2', 'compareOp', 'value32', '', ''], 'up-enemy-villagers-in-town': ['2', 'compareOp', 'value32', '', ''], 'up-find-remote': ['4', 'typeOp', 'UnitId', 'typeOp', '0|40'], 'up-find-resource': ['4', 'typeOp', 'CustomResource', 'typeOp', '0|240'], 'up-find-status-remote': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240'], 'up-gaia-type-count': ['4', 'typeOp', 'CustomResource', 'compareOp', 'value32'], 'up-gaia-type-count-total': ['4', 'typeOp', 'CustomResource', 'compareOp', 'value32'], 'up-get-object-data': ['2', 'ObjectData', 'GoalId', '', ''], 'up-get-object-target-data': ['2', 'ObjectData', 'GoalId', '', ''], 'up-get-point-contains': ['4', 'Point', 'GoalId', 'typeOp', 'ObjectId'], 'up-group-size': ['4', 'typeOp', 'GroupId', 'compareOp', 'value32'], 'up-idle-unit-count': ['3', 'IdleType', 'compareOp', 'value32', ''], 'up-modify-goal': ['3', 'GoalId', 'mathOp', 'value32', ''], 'up-object-data': ['3', 'ObjectData', 'compareOp', 'value32', ''], 'up-object-target-data': ['3', 'ObjectData', 'compareOp', 'value32', ''], 'up-object-type-count': ['4', 'typeOp', 'ObjectId', 'compareOp', 'value32'], 'up-object-type-count-total': ['4', 'typeOp', 'ObjectId', 'compareOp', 'value32'], 'up-path-distance': ['4', 'Point', 'Strict', 'compareOp', 'value32'], 'up-pending-objects': ['4', 'typeOp', 'ObjectId', 'compareOp', 'value32'], 'up-pending-placement': ['2', 'typeOp', 'BuildingId', '', ''], 'up-player-distance': ['3', 'AnyPlayer', 'compareOp', 'value32', ''], 'up-players-in-game': ['3', 'PlayerStance', 'compareOp', 'value32', ''], 'up-point-contains': ['3', 'Point', 'typeOp', 'ObjectId', ''], 'up-point-distance': ['4', 'Point', 'Point', 'compareOp', 'value32'], 'up-point-elevation': ['4', 'Point', 'compareOp', 'value32', ''], 'up-point-explored': ['3', 'Point', 'typeOp', 'ExploredState', ''], 'up-point-terrain': ['3', 'Point', 'compareOp', 'Terrain', ''], 'up-point-zone': ['3', 'Point', 'compareOp', 'value32', ''], 'up-projectile-detected': ['3', 'ProjectileType', 'compareOp', 'ElapsedTime', ''], 'up-projectile-target': ['3', 'ProjectileType', 'compareOp', 'ClassId', ''], 'up-remaining-boar-amount': ['2', 'compareOp', 'value32', '', ''], 'up-research-status': ['4', 'typeOp', 'TechId', 'compareOp', 'ResearchState'], 'up-resource-amount': ['3', 'ResourceAmount', 'compareOp', 'value32', ''], 'up-resource-percent': ['3', 'ResourceAmount', 'compareOp', 'value32', ''], 'up-set-target-by-id': ['2', 'typeOp', 'Id', '', ''], 'up-set-target-object': ['3', 'SearchSource', 'typeOp', '0|239', ''], 'up-timer-status': ['3', 'TimerId', 'compareOp', 'TimerState', ''], 'up-train-site-ready': ['2', 'typeOp', 'UnitIdStrict', '', ''], 'up-unit-type-in-town': ['3', 'typeOp', 'UnitId', 'compareOp', 'value32'], 'up-villager-type-in-town': ['4', 'typeOp', '83;293', 'compareOp', 'value32'], 'up-allied-resource-percent': ['4', 'AllyPlayer', 'ResourceAmount', 'compareOp', 'value32'], 'up-find-local': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240']}

actions = {
'acknowledge-event': ['2', 'EventType', 'EventID', '', ''], 'attack-now': ['0', '', '', '', ''], 'build': ['1', 'Buildable', '', '', ''], 'build-forward': ['1', 'Buildable', '', '', ''], 'build-gate': ['1', 'Perimeter', '', '', ''], 'build-wall': ['2', 'Perimeter', 'WallId', '', ''], 'buy-commodity': ['1', 'Commodity', '', '', ''], 'clear-tribute-memory': ['2', 'AnyPlayer', 'Resource', '', ''], 'delete-building': ['1', 'BuildingId', '', '', ''], 'delete-unit': ['1', 'UnitIdStrict', '', '', ''], 'disable-timer': ['1', 'TimerId', '', '', ''], 'disable-self': ['0', '', '', '', ''], 'do-nothing': ['0', '', '', '', ''], 'enable-timer': ['2', 'TimerId', 'value32Positive', '', ''], 'enable-wall-placement': ['1', 'Perimeter', '', '', ''], 'generate-random-number': ['1', 'value32Positive', '', '', ''], 'release-escrow': ['1', 'Resource', '', '', ''], 'research': ['1', 'TechId', '', '', ''], 'sell-commodity': ['1', 'Commodity', '', '', ''], 'set-difficulty-parameter': ['2', 'DiffParameterId', '0|100', '', ''], 'set-doctrine': ['1', 'value32', '', '', ''], 'set-escrow-percentage': ['2', 'Resource', 'value32', '', ''], 'set-goal': ['2', 'GoalId', 'value32', '', ''], 'set-shared-goal': ['2', 'SharedGoalId', 'value32', '', ''], 'set-signal': ['1', 'SignalId', '', '', ''], 'spy': ['0', '', '', '', ''], 'train': ['1', 'Trainable', '', '', ''], 'tribute-to-player': ['3', 'AnyPlayer', 'Resource', 'value32Positive', ''], 'up-add-cost-data': ['3', 'GoalId', 'typeOp', 'value32', ''], 'up-add-object-by-id': ['3', 'SearchSource', 'typeOp', 'Id', ''], 'up-add-point': ['4', 'Point', 'Point', 'typeOp', 'value32'], 'up-add-research-cost': ['4', 'typeOp', 'TechId', 'typeOp', 'value32'], 'up-assign-builders': ['4', 'typeOp', 'Buildable', 'typeOp', '-1|250'], 'up-bound-point': ['2', 'Point', 'Point', '', ''], 'up-bound-precise-point': ['4', 'Point', '1', 'typeOp', 'value32Positive'], 'up-build': ['4', 'PlacementType', 'EscrowState', 'typeOp', 'Buildable'], 'up-build-line': ['4', 'Point', 'Point', 'typeOp', 'Buildable'], 'up-buy-commodity': ['4', 'typeOp', 'ResourceAmount', 'typeOp', 'value32Positive'], 'up-clean-search': ['3', 'SearchSource', 'ObjectData', 'SearchOrder', ''], 'up-copy-point': ['2', 'Point', 'Point', '', ''], 'up-create-group': ['4', 'GoalId', 'GoalId2', 'typeOp', 'GroupId'], 'up-cross-tiles': ['4', 'Point', 'Point', 'typeOp', 'value32'], 'up-delete-distant-farms': ['2', 'typeOp', 'value256', '', ''], 'up-delete-idle-units': ['1', 'IdleType', '', '', ''], 'up-delete-objects': ['4', 'typeOp', 'UnitIdStrict', 'typeOp', 'value32Positive'], 'up-disband-group-type': ['1', 'GroupType', '', '', ''], 'up-drop-resources': ['3', 'Resource', 'typeOp', 'value32Positive', ''], 'up-filter-distance': ['4', 'typeOp', 'MinDistance', 'typeOp', 'MaxDistance'], 'up-filter-exclude': ['4', 'CmdId', 'ActionId', 'OrderId', 'ClassId'], 'up-filter-garrison': ['4', 'typeOp', 'MinGarrison', 'typeOp', 'MaxGarrison'], 'up-filter-include': ['4', 'CmdId', 'ActionId', 'OrderId', 'OnMainland'], 'up-filter-range': ['4', 'MinGarrison', 'MaxGarrison', 'MinDistance', 'MaxDistance'], 'up-filter-status': ['4', 'typeOp', 'ObjectStatus', 'typeOp', 'ObjectList'], 'up-find-local': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240'], 'up-find-next-player': ['3', 'PlayerStance', 'FindPlayerMethod', 'PlayerId', ''], 'up-find-player': ['3', 'PlayerStance', 'FindPlayerMethod', 'PlayerId', ''], 'up-find-remote': ['4', 'typeOp', 'UnitId', 'typeOp', '0|40'], 'up-find-resource': ['4', 'typeOp', 'Resource', 'typeOp', '0|240'], 'up-find-status-local': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240'], 'up-find-status-remote': ['4', 'typeOp', 'UnitId', 'typeOp', '0|240'], 'up-full-reset-search': ['0', '', '', '', ''], 'up-garrison': ['3', 'GarrisonableUnitId', 'typeOp', 'UnitId', ''], 'up-gather-inside': ['4', 'typeOp', 'BuildingId', 'typeOp', 'State'], 'up-get-attacker-class': ['1', 'GoalId', '', '', ''], 'up-get-cost-delta': ['1', 'GoalId', '', '', ''], 'up-get-event': ['3', 'typeOp', 'EventID', 'GoalId', ''], 'up-get-group-size': ['3', 'typeOp', 'GroupId', 'GoalId', ''], 'up-get-indirect-goal': ['3', 'typeOp', 'GoalId', 'GoalId2', ''], 'up-get-object-data': ['2', 'ObjectData', 'GoalId', '', ''], 'up-get-object-target-data': ['2', 'ObjectData', 'GoalId', '', ''], 'up-get-path-distance': ['3', 'Point', 'Strict', 'GoalId', ''], 'up-get-player-color': ['2', 'AnyPlayer', 'ColorId', '', ''], 'up-get-point': ['2', 'PositionType', 'GoalId', '', ''], 'up-get-point-contains': ['4', 'GoalId', 'GoalId2', 'typeOp', 'ObjectId'], 'up-get-point-distance': ['3', 'Point', 'Point', 'GoalId', ''], 'up-get-point-elevation': ['2', 'Point', 'GoalId', '', ''], 'up-get-point-terrain': ['2', 'Point', 'Terrain', '', ''], 'up-get-point-zone': ['2', 'Point', 'GoalId', '', ''], 'up-get-precise-time': ['2', 'GoalId', 'GoalId2', '', ''], 'up-get-projectile-player': ['2', 'ProjectileType', 'PlayerId', '', ''], 'up-get-rule-id': ['1', 'RuleId', '', '', ''], 'up-get-search-state': ['1', 'GoalId', '', '', ''], 'up-get-shared-goal': ['3', 'typeOp', 'SharedGoalId', 'GoalId', ''], 'up-get-signal': ['3', 'typeOp', 'SignalId', 'GoalId', ''], 'up-get-threat-data': ['4', 'GoalId', 'PlayerId', 'GoalId', 'GoalId2'], 'up-get-timer': ['3', 'typeOp', 'TimerId', 'GoalId', ''], 'up-guard-unit': ['3', 'ObjectId', 'typeOp', 'UnitId', ''], 'up-jump-direct': ['2', 'typeOp', 'RuleId', '', ''], 'up-jump-dynamic': ['2', 'typeOp', 'value32', '', ''], 'up-jump-rule': ['1', 'value32', '', '', ''], 'up-lerp-percent': ['4', 'Point', 'Point', 'typeOp', 'value32'], 'up-lerp-tiles': ['4', 'Point', 'Point', 'typeOp', 'value32'], 'up-modify-escrow': ['3', 'Resource', 'mathOp', 'value32', ''], 'up-modify-goal': ['3', 'GoalId', 'mathOp', 'value32', ''], 'up-modify-group-flag': ['3', 'OnOff', 'typeOp', 'GroupId', ''], 'up-modify-sn': ['3', 'SnId', 'mathOp', 'value32', ''], 'up-release-escrow': ['0', '', '', '', ''], 'up-remove-objects': ['4', 'SearchSource', 'ObjectData', 'typeOp', 'value32'], 'up-request-hunters': ['2', 'typeOp', 'value32Positive', '', ''], 'up-research': ['3', 'EscrowState', 'typeOp', 'TechId', ''], 'up-reset-attack-now': ['0', '', '', '', ''], 'up-reset-building': ['3', 'OnOff', 'typeOp', 'BuildingId', ''], 'up-reset-cost-data': ['1', 'GoalId', '', '', ''], 'up-reset-filters': ['0', '', '', '', ''], 'up-reset-group': ['2', 'typeOp', 'GroupId', '', ''], 'up-reset-placement': ['2', 'typeOp', 'BuildingId', '', ''], 'up-reset-search': ['4', 'OnOff', 'OnOff', 'OnOff', 'OnOff'], 'up-reset-target-priorities': ['2', 'OnOff', 'OnOff', '', ''], 'up-reset-unit': ['2', 'typeOp', 'UnitId', '', ''], 'up-retask-gatherers': ['3', 'Resource', 'typeOp', 'value32Positive', ''], 'up-retreat-now': ['0', '', '', '', ''], 'up-retreat-to': ['3', 'ObjectId', 'typeOp', 'UnitId', ''], 'up-sell-commodity': ['4', 'typeOp', 'ResourceAmount', 'typeOp', 'value32Positive'], 'up-set-attack-stance': ['3', 'UnitId', 'typeOp', 'AttackStance', ''], 'up-set-defense-priority': ['4', 'typeOp', 'BuildingId', 'typeOp', 'value32'], 'up-set-group': ['3', 'SearchSource', 'typeOp', 'GroupId', ''], 'up-set-indirect-goal': ['4', 'typeOp', 'GroupId', 'typeOp', 'value32'], 'up-set-offense-priority': ['4', 'typeOp', 'ObjectId', 'typeOp', '-1|11'], 'up-set-placement-data': ['4', 'AllyPlayer', 'ObjectId', 'typeOp', '-254|254'], 'up-set-precise-target-point': ['1', 'Point', '', '', ''], 'up-set-shared-goal': ['4', 'typeOp', 'SharedGoalId', 'typeOp', 'value32'], 'up-set-signal': ['4', 'typeOp', 'SignalId', 'typeOp', 'value32'], 'up-set-target-by-id': ['2', 'typeOp', 'Id', '', ''], 'up-set-target-object': ['3', 'SearchSource', 'typeOp', '0|239', ''], 'up-set-target-point': ['1', 'Point', '', '', ''], 'up-set-timer': ['4', 'typeOp', 'TimerId', 'typeOp', 'value32Positive'], 'up-setup-cost-data': ['2', 'OnOff', 'GoalId', '', ''], 'up-store-map-name': ['1', 'OnOff', '', '', ''], 'up-store-object-name': ['0', '', '', '', ''], 'up-store-player-name': ['1', 'AnyPlayer', '', '', ''], 'up-store-tech-name': ['1', 'typeOp', 'TechId', '', ''], 'up-target-point': ['4', 'Point', 'TargetAction', 'Formation', 'AttackStance'], 'up-train': ['3', 'EscrowState', 'typeOp', 'Trainable', ''], 'up-tribute-to-player': ['4', 'AnyPlayer', 'ResourceAmount', 'typeOp', 'value32Positive'], 'up-ungarrison': ['2', 'typeOp', 'ObjectId', '', ''], 'up-update-targets': ['0', '', '', '', ''], 'up-reset-scouts': ['0', '', '', '', ''],'set-strategic-number':['2','SnId','SnValue','','']
}

buildings_text = "(defrule\n	(can-build mill)\n	(building-type-count mill < 1)\n=>\n	(build mill)\n)\n\n(defrule\n	(can-build lumber-camp)\n	(building-type-count lumber-camp < 1)\n=>\n	(build lumber-camp)\n)\n\n(defrule\n	(can-build barracks)\n	(building-type-count barracks < 1)\n=>\n	(build barracks)\n)\n\n(defrule\n	(can-build mining-camp)\n	(building-type-count mining-camp < 1)\n=>\n	(build mining-camp)\n)\n\n(defrule\n	(can-build stable)\n	(building-type-count stable < 1)\n=>\n	(build stable)\n)\n\n(defrule\n	(can-build archery-range)\n	(building-type-count archery-range < 1)\n=>\n	(build archery-range)\n)\n\n(defrule\n	(can-build market)\n	(building-type-count market < 1)\n=>\n	(build market)\n)\n\n(defrule\n	(can-build blacksmith)\n	(building-type-count blacksmith < 1)\n=>\n	(build blacksmith)\n)\n\n(defrule\n	(can-build monastery)\n	(building-type-count monastery < 1)\n=>\n	(build monastery)\n)\n\n(defrule\n	(can-build university)\n	(building-type-count university < 1)\n=>\n	(build university)\n)\n\n(defrule\n	(can-build siege-workshop)\n	(building-type-count siege-workshop < 1)\n=>\n	(build siege-workshop)\n)\n\n(defrule\n	(can-build castle)\n	(building-type-count castle < 1)\n=>\n	(build castle)\n)"

if allow_towers:
    paramdict['Buildable'] += ';watch-tower;guard-tower'

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

def mutate_parameters(parameters, mutation_chance):

    out = parameters.copy()

    for key in parameters:

        if key != '':
            mutation_rules = paramdict[key]

            if "|" in mutation_rules:
                mutation_rules = mutation_rules.split("|")
                if random.random() < mutation_chance:
                    out[key] = str(random.randint(int(mutation_rules[0]),int(mutation_rules[1])))

            elif ";" in mutation_rules:
                mutation_rules = mutation_rules.split(";")
                if random.random() < mutation_chance:
                    out[key] = random.choice(mutation_rules)


    return out

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
    #if action_name == 'train':
    #    print("train!")

    return action

def mutate_fact(fact, mutation_chance):

    fact_name = fact[0]
    is_not = fact[1]
    params = fact[2].copy()
    and_or = fact[3]

    if random.random() < mutation_chance:
        fact_name = random.choice(fact_list)

    if random.random() < mutation_chance:
        is_not = random.randint(0,1)

    params = mutate_parameters(params, mutation_chance)

    if random.random() < mutation_chance:
        and_or = random.choice(["and","or","nand","nor"])

    fact = [fact_name, is_not, params, and_or]

    return fact

def mutate_action(action, mutation_chance):

    action_name = action[0]
    params = action[1].copy()

    if random.random() < mutation_chance:
        action_name = random.choice(action_list)
        #if action_name == 'train':
        #    print("train!")

    params = mutate_parameters(params, mutation_chance)

    action = [action_name, params]

    return action

def generate_rule():

    fact_length = random.randint(1,max_fact_length)
    action_length = random.randint(1,max_action_length)
    #age_required = random.choice([["","","#load-if-not-defined DARK-AGE-END","#end-if","#load-if-not-defined FEUDAL-AGE-END","#end-if","#load-if-not-defined CASTLE-AGE-END","#end-if","#load-if-not-defined IMPERIAL-AGE-START","#end-if"]])
    age_required = ["",""]

    local_facts = []
    local_actions = []

    for i in range(max_fact_length):
        local_facts.append(generate_fact())
        local_actions.append(generate_action())

    rule = [fact_length, action_length, age_required, local_facts, local_actions]

    return rule

def mutate_rule(rule, mutation_chance):

    fact_length = rule[0]
    action_length = rule[1]
    age_required = rule[2]
    local_facts = rule[3].copy()
    local_actions = rule[4].copy()

    if random.random() < mutation_chance:
        fact_length = random.randint(1,max_fact_length)

    if random.random() < mutation_chance:
        action_length = random.randint(1,max_action_length)

    if random.random() < mutation_chance:
        age_required = random.choice([["","","#load-if-not-defined DARK-AGE-END","#end-if","#load-if-not-defined FEUDAL-AGE-END","#end-if","#load-if-not-defined CASTLE-AGE-END","#end-if","#load-if-not-defined IMPERIAL-AGE-START","#end-if"]])

    for i in range(len(local_facts)):
        local_facts[i] = mutate_fact(local_facts[i], mutation_chance)
        local_actions[i] = mutate_action(local_actions[i], mutation_chance)

    rule = [fact_length, action_length, age_required, local_facts, local_actions]

    if random.random() < mutation_chance / 5:
        rule = generate_rule()

    return rule

def simple_to_complex(simple):
    rule = generate_rule()

    type = simple[0]
    params = simple[1].copy()
    threshold = simple[2]
    simple_age_required = simple[3].copy()
    requirement = simple[4]

    fact_length = rule[0]
    action_length = rule[1]
    age_required = rule[2]
    local_facts = rule[3].copy()
    local_actions = rule[4].copy()

    for i in range(len(local_facts)):
        local_facts[i][1] = 0
        local_facts[i][3] = "and"

    action_length = 1
    fact_length = 0

    #fact = [fact_name, is_not, params, and_or]
    first_fact = 0

    if simple_age_required != [""]:
        fact_length += 1
        local_facts[first_fact][0] = "current-age"

        simple_age_required[0] = simple_age_required[0].replace("   "," ")
        simple_age_required[0] = simple_age_required[0].replace("  "," ")

        temp = simple_age_required[0].split(" ")

        local_facts[first_fact][2]['compareOp'] = temp[1]

        if temp[2] in ["0","1","2","3","4","5"]:
            local_facts[first_fact][2]['Age'] = temp[2]
        else:
            local_facts[first_fact][2]['Age'] = "2"

        first_fact += 1

    if type == 'train':
        fact_length += 2

        local_facts[first_fact][0] = "can-train"
        local_facts[first_fact][2]["UnitId"] = params["Trainable"]

        local_facts[first_fact + 1][0] = "unit-type-count"
        local_facts[first_fact + 1][2]["compareOp"] = "<"
        local_facts[first_fact + 1][2]["UnitId"] = params["Trainable"]
        local_facts[first_fact + 1][2]["0|50"] = threshold

        local_actions[0][0] = 'train'
        local_actions[0][1]["Trainable"] = params["Trainable"]

    elif type == 'build':
        fact_length += 2

        local_facts[first_fact][0] = "can-build"
        local_facts[first_fact][2]["BuildingId"] = params["Buildable"]

        local_facts[first_fact + 1][0] = "building-type-count"
        local_facts[first_fact + 1][2]["compareOp"] = "<"
        local_facts[first_fact + 1][2]["BuildingId"] = params["Buildable"]

        if params["Buildable"] != "farm":
            local_facts[first_fact + 1][2]["0|50"] = threshold%10
        else:
            local_facts[first_fact + 1][2]["0|50"] = threshold

        local_actions[0][0] = 'build'
        local_actions[0][1]["Buildable"] = params["Buildable"]

    elif type == 'research':
        fact_length += 1

        local_facts[first_fact][0] = "can-research"
        local_facts[first_fact][2]["TechId"] = params["TechId"]
        local_actions[0][0] = 'research'
        local_actions[0][1]["TechId"] = params["TechId"]

    elif type == 'strategic_number':
        fact_length += 1
        local_facts[first_fact][0] = "true"
        action_length = 2
        local_actions[0][0] = 'set-strategic-number'
        local_actions[0][1]["SnId"] = params["SnId"]
        local_actions[0][1]["SnValue"] = params["SnValue"]
        local_actions[1][0] = 'disable-self'



    rule = [fact_length, action_length, age_required, local_facts, local_actions]

    return rule

def generate_ai():

    #print("generating")

    simple_list = []
    ai = []

    villager_distribution = generate_distribution()

    if villager_preset:
        #build villagers
        temp = generate_simple()
        temp[0] = 'train'
        temp[1]['Trainable'] = '83'
        temp[2] = 30
        temp[3] = ["current-age  == 0"]

        simple_list.append(temp)

        temp = generate_simple()
        temp[0] = 'train'
        temp[1]['Trainable'] = '83'
        temp[2] = 80
        temp[3] = ["current-age  == 1"]

        simple_list.append(temp)

    for i in range(simple_count):
        simple_list.append(generate_simple())

    for i in range(ai_length):
        ai.append(generate_rule())

    attack_rules = []
    for i in range(attack_rule_count):
        attack_rules.append(generate_attack_rule())

    return [villager_distribution,simple_list,ai,attack_rules]

def mutate_ai(ai, mutation_chance):

    local = copy.deepcopy(ai)

    local[0] = mutate_distribution(local[0].copy(), mutation_chance)

    remove_list = []
    add_list = []

    for i in range(len(ai[1])):
        local[1][i] = mutate_simple(ai[1][i], mutation_chance)

        if allow_complex:
            if random.random() < mutation_chance / 2:
                add_list.append(simple_to_complex(local[1][i]))
                remove_list.append(local[1][i])

    for i in range(len(remove_list)):
        local[1].remove(remove_list[i])

    if random.random() < mutation_chance * 2:
        local[1].append(generate_simple())
    if random.random() < mutation_chance / 2:
        local[1].remove(random.choice(local[1]))

    for i in range(len(ai[2])):
        local[2][i] = mutate_rule(ai[2][i], mutation_chance)

    if random.random() < mutation_chance / 2:
        local[2].append(generate_rule())
    if random.random() < mutation_chance / 2:
        if len(local[2]) > 0:
            local[2].remove(random.choice(local[2]))

    for i in range(len(ai[3])):
        local[3][i] = mutate_attack_rule(ai[3][i], mutation_chance)

    if random.random() < mutation_chance:
        local[3].append(generate_attack_rule())
    if random.random() < mutation_chance:
        if len(local[3]) > 0:
            local[3].remove(random.choice(local[3]))


    if random.random() < mutation_chance / 3:
        random.shuffle(local[1])

    if random.random() < mutation_chance / 3:
        random.shuffle(local[2])

    while local == ai:
        local[0] = mutate_distribution(local[0].copy(), mutation_chance)

        for i in range(len(ai[1])):
            local[1][i] = mutate_simple(ai[1][i], mutation_chance)

        for i in range(len(ai[2])):
            local[2][i] = mutate_rule(ai[2][i], mutation_chance)

    local[2] = add_list + local[2]

    return local

def crossover(ai_one, ai_two, mutation_chance):

    out0 = random.choice([ai_one[0],ai_two[0]])
    out1 = []
    out2 = []
    out3 = []

    for i in range(len(ai_one[1])):

        try:
            if random.random() < mutation_chance/5:

                    if random.random() < .5:
                        out1.append(random.choice(ai_one[1]))

                    else:
                        out1.append(random.choice(ai_two[1]))

            else:
                out1.append(random.choice([ai_one[1][i],ai_two[1][i]]))


        except IndexError:
            out1.append(random.choice(ai_one[1]))

    for i in range(len(ai_one[2])):

        try:
            if random.random() < mutation_chance/5:

                if random.random() < .5:
                    out2.append(random.choice(ai_one[2]))

                else:
                    out2.append(random.choice(ai_two[2]))

            else:
                out2.append(random.choice([ai_one[2][i],ai_two[2][i]]))

        except IndexError:
            out2.append(random.choice(ai_one[2]))


    for i in range(len(ai_one[3])):

        try:
            if random.random() < mutation_chance/5:

                if random.random() < .5:
                    out3.append(random.choice(ai_one[3]))

                else:
                    out3.append(random.choice(ai_two[3]))

            else:
                out3.append(random.choice([ai_one[3][i],ai_two[3][i]]))

        except IndexError:
            out2.append(random.choice(ai_one[2]))

    return [out0,out1,out2,out3]

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
    string += "\n"
    string += "(defrule"
    string += write_fact(local_facts, fact_length)
    string += "\n=>"
    string += write_action(local_actions, action_length)
    string += ")\n"

    check = string.split(" ")
    while '' in check:
        check.remove('')

    if len(check) > 20:
        string = ""

    return string

def write_ai(ai, ai_name):

    f = open(ai_name + ".per","w+")

    #default = "(defrule\n(true)\n=>\n(set-strategic-number sn-cap-civilian-builders -1)\n(set-strategic-number sn-cap-civilian-gatherers 0)\n(set-strategic-number sn-cap-civilian-explorers 0)\n(set-strategic-number sn-initial-exploration-required 0)\n(set-strategic-number sn-maximum-food-drop-distance -2)\n(set-strategic-number sn-maximum-gold-drop-distance -2)\n(set-strategic-number sn-maximum-hunt-drop-distance -2)\n(set-strategic-number sn-maximum-stone-drop-distance -2)\n(set-strategic-number sn-maximum-wood-drop-distance -2)\n(set-strategic-number sn-disable-villager-garrison 3)\n(disable-self))\n\n"

    default = "(defrule\n(true)\n=>\n(set-strategic-number sn-cap-civilian-explorers 0)\n(set-strategic-number sn-initial-exploration-required 10)\n(disable-self))\n\n"
    #default = ""

    if force_house:
        default += "(defrule \n(building-type-count-total town-center > 0)\n(housing-headroom < 5)\n(population-headroom > 0)\n(can-build house)\n=>\n(build house))\n\n"

    if force_age_up:
        default += "(defrule\n(true)\n=>\n(research 101))\n(defrule\n(true)\n=>\n(research 102))\n\n"

    if force_imperial_age:
        default +="(defrule\n(true)\n=>\n(research 103))\n"

    if force_buildings:
        default += buildings_text

    if force_barracks:
        default += "(defrule\n	(can-build barracks)\n	(building-type-count barracks < 1)\n=>\n	(build barracks)\n)\n\n"

    if force_resign:
        default += "(defrule\n\t(true)\n=>\n\t(up-get-fact-min any-enemy 20 0 21)\n\t(up-get-fact 20 0 19))\n"
        default += "(defrule\n\t(up-compare-goal 19 g:< 21)\n\t(unit-type-count villager < 15)\n\t(current-age >= feudal-age)\n=>\n\t(resign)\n\t(disable-self))\n\n"
        default += "(defrule\n\t(up-compare-goal 19 g:< 21)\n\t(building-type-count town-center < 1)\n\t(current-age < feudal-age)\n=>\n\t(resign)\n\t(disable-self))\n\n"

    if force_scout:
        default += '\n(defrule\n\t(true)\n=>\n\t(set-strategic-number sn-total-number-explorers 1)\n\t(set-strategic-number sn-number-explore-groups 1)\n\t(up-send-scout 101 1)\n\t(disable-self)\n)\n\n'

    f.write(default)

    for i in range(len(ai[1])):
        c = write_simple(ai[1][i])
        f.write(c)

    c = write_distribution(ai[0].copy())
    f.write(c)

    if allow_attack_rules:
        for i in range(len(ai[3])):
            c = write_attack_rule(ai[3][i])
            f.write(c)

    if allow_complex:
        for i in range(len(ai[2])):
            c = write_rule(ai[2][i])
            f.write(c)

    f.close()

def save_ai(ai, file):

    saved = False

    while not saved:
        try:
            temp = {'lazy' : ai}

            with open(file + ".txt", 'w+') as outfile:
                json.dump(temp, outfile)

            saved = True

        except KeyboardInterrupt:
            print("saving!")
            saved = False

def read_ai(file):

    with open(file + '.txt') as json_file:
        data = json.load(json_file)

    out = data['lazy']

    return out

def generate_simple():

    type = random.choice(['train','research','strategic_number','build','build-forward'])
    #type = random.choice(['train','build','research','research'])

    requirement = "none"

    params = generate_parameters()

    threshold = random.randint(0,200)

    if force_castle_age_units and params['Trainable'] != '83' and type == 'train':
        age_required = ["current-age  >= 3"]
    else:
        age_required = random.choice([[""],["current-age > 0"],["current-age != 0"],["current-age == 0"],["current-age >= 0"],["current-age < 0"],["current-age <= 1"],["current-age > 1"],["current-age == 1"],["current-age >= 1"],["current-age < 1"],["current-age <= 1"],["current-age != 1"],["current-age <= 2"],["current-age > 2"],["current-age == 2"],["current-age >= 2"],["current-age < 2"],["current-age <= 3"],["current-age != 3"],["current-age <= 3"],["current-age > 3"],["current-age == 3"],["current-age >= 3"],["current-age < 3"],["current-age <= 3"],["current-age != 3"]])

    gametime = random.randint(0,7200)
    requirement_count = random.randint(0,10)

    return [type,params,threshold,age_required,requirement,requirement_count,game_time]

def mutate_simple(simple, mutation_chance):

    type = simple[0]
    params = simple[1].copy()
    threshold = simple[2]
    age_required = simple[3].copy()
    requirement = simple[4]
    if len(simple) > 5:
        requirement_count = simple[5]
        gametime = simple[6]
    else:
        requirement_count = 0
        gametime = 0

    if random.random() < mutation_chance:
        if allow_units:
            type = random.choice(['train','research','strategic_number','build','build-forward'])
        else:
            type = random.choice(['research','strategic_number','build','build-forward'])

    params = mutate_parameters(params.copy(), mutation_chance)

    if random.random() < mutation_chance:
        if random.random() < .25:
            threshold = random.randint(0,200)
        else:
            threshold += random.randint(-10,10)

    if force_castle_age_units and params['Trainable'] != '83' and type == 'train':
        age_required = ["current-age  >= 2"]
    elif random.random() < mutation_chance:
        age_required = random.choice([[""],["current-age > 0"],["current-age  != 0"],["current-age  == 0"],["current-age  >= 0"],["current-age < 0"],["current-age  <= 1"],["current-age > 1"],["current-age  == 1"],["current-age  >= 1"],["current-age < 1"],["current-age  <= 1"],["current-age  != 1"],["current-age  <= 2"],["current-age > 2"],["current-age  == 2"],["current-age  >= 2"],["current-age < 2"],["current-age  <= 3"],["current-age  != 3"],["current-age  <= 3"],["current-age > 3"],["current-age  == 3"],["current-age  >= 3"],["current-age < 3"],["current-age  <= 3"],["current-age  != 3"]])

    if random.random() < mutation_chance:
        requirement = random.choice(["none","town-center","farm","house","mill","mining-camp","lumber-camp","dock","blacksmith","market","monastery","university","wonder","barracks","archery-range","stable","siege-workshop","outpost","castle","stone-wall","palisade-wall","gate"])

    if random.random() < mutation_chance:
        if random.random() < .25:
            gametime = random.randint(0,7200)
        else:
            gametime += random.randint(-100,100)

    if random.random() < mutation_chance:
        if random.random() < .25:
            requirement_count = random.randint(0,10)
        else:
            requirement_count += random.randint(-1,1)

    return [type,params,threshold,age_required,requirement,requirement_count,gametime]

def write_simple(simple):

    type = simple[0]
    params = simple[1].copy()
    threshold = simple[2]
    age_required = simple[3]
    requirement = simple[4]
    if len(simple) > 5:
        requirement_count = simple[5]
        gametime = simple[6]
    else:
        requirement_count = 0
        gametime = 0

    string = ""
    string += "\n" #+ age_required[0] + "\n"
    string += "(defrule"

    if age_required[0] != "":
        string += "\n\t(" + age_required[0] + ")"

    if gametime > 0:
        string += "\n\t(game-time > " + str(gametime) + ")"

    if requirement != "none" and requirement != "":
        string += "\n\t(building-type-count " + requirement + " > " + str(requirement_count) + ")"

    if type == 'train':
        string += "\n\t(can-train " + str(params['Trainable'] + ")")
        string += "\n\t(unit-type-count " + str(params['Trainable'] + " < " + str(threshold) + ")")

    if type == 'build' or type == 'build-forward':

        string += "\n\t(can-build " + str(params['Buildable'] + ")")

        if params['Buildable'] != 'farm':
            string += "\n\t(building-type-count " + params['Buildable'] + " < " + str(threshold%10) + ")"
        else:
            string += "\n\t(building-type-count " + params['Buildable'] + " < " + str(threshold%100) + ")"

    if type == 'research':
        string += "\n\t(can-research " + str(params['TechId'] + ")")

    if type == 'strategic_number':
        string += "\n\t(true)"

    string += "\n=>"

    if type == 'train':
        string += "\n\t(train " + str(params['Trainable'] + ")")

    if type == 'build':
        string += "\n\t(build " + str(params['Buildable'] + ")")

    if type == 'build-forward':
        string += "\n\t(build-forward " + str(params['Buildable'] + ")")

    if type == 'research':
        string += "\n\t(research " + str(params['TechId'] + ")")

    if type == 'strategic_number':
        string += "\n\t(set-strategic-number " + str(params['SnId']) + " " + str(params['SnValue']) + ")\n\t(disable-self)"

    string += ")\n" #+ age_required[1]

    return string

def generate_distribution():

    villager_distribution = [[.25,.25,.25,.25,.2],[.25,.25,.25,.25,.2],[.25,.25,.25,.25,.2],[.25,.25,.25,.25,.2]]

    #for i in range(5):
    #    villager_distribution.append(random.uniform(0,1))

    return villager_distribution

def mutate_distribution(villager_distribution, mutation_chance):

    for x in range(len(villager_distribution)):
        for i in range(5):
            if random.random() < mutation_chance:
                villager_distribution[x][i] *= random.uniform(.95,1.05)
                villager_distribution[x][i] = min(1,max(0,villager_distribution[x][i]))
            elif random.random() < mutation_chance:
                villager_distribution[x][i] = random.uniform(0,.3)

    return villager_distribution

def write_distribution(villager_distribution):

    v = copy.deepcopy(villager_distribution)

    string = ""

    for x in range(len(v)):
        total = v[x][0] + v[x][1] + v[x][2] + v[x][3]

        for i in range(4):
            v[x][i] = int(v[x][i]/total * 100)

        string += "\n(defrule\n\t(current-age == " + str(x) + " )\n=>"
        string += "\n\t(set-strategic-number sn-food-gatherer-percentage " + str(v[x][0]) + ")"
        string += "\n\t(set-strategic-number sn-wood-gatherer-percentage " + str(v[x][1]) + ")"
        string += "\n\t(set-strategic-number sn-gold-gatherer-percentage " + str(v[x][2]) + ")"
        string += "\n\t(set-strategic-number sn-stone-gatherer-percentage " + str(v[x][3]) + ")\n\t(disable-self))\n"

        if force_attack_type_1:
            string += "\n(defrule\n\t(current-age == " + str(x) + " )\n\t(defend-soldier-count >= " + str(int(v[x][4]*100)) + ")\n=>\n\t(set-strategic-number sn-maximum-town-size 1000)\n\t(disable-self))\n"

        if force_attack_type_2:
            string += "\n(defrule\n\t(current-age == " + str(x) + " )\n\t(defend-soldier-count >= " + str(int(v[x][4]*100))  + ")\n=>\n\t(set-strategic-number sn-percent-attack-soldiers 100)\n\t(attack-now))\n"

    return string

def generate_attack_rule():

    age_required = random.choice(["","current-age > 0","current-age != 0","current-age == 0","current-age >= 0","current-age < 0","current-age <= 1","current-age > 1","current-age == 1","current-age >= 1","current-age < 1","current-age <= 1","current-age != 1","current-age <= 2","current-age > 2","current-age == 2","current-age >= 2","current-age < 2","current-age <= 3","current-age != 3","current-age <= 3","current-age > 3","current-age == 3","current-age >= 3","current-age < 3","current-age <= 3","current-age != 3"])

    enemy_age_required = random.choice(["","players-current-age any-enemy > 0","players-current-age any-enemy != 0","players-current-age any-enemy == 0","players-current-age any-enemy >= 0","players-current-age any-enemy < 0","players-current-age any-enemy <= 1","players-current-age any-enemy > 1","players-current-age any-enemy == 1","players-current-age any-enemy >= 1","players-current-age any-enemy < 1","players-current-age any-enemy <= 1","players-current-age any-enemy != 1","players-current-age any-enemy <= 2","players-current-age any-enemy > 2","players-current-age any-enemy == 2","players-current-age any-enemy >= 2","players-current-age any-enemy < 2","players-current-age any-enemy <= 3","players-current-age any-enemy != 3","players-current-age any-enemy <= 3","players-current-age any-enemy > 3","players-current-age any-enemy == 3","players-current-age any-enemy >= 3","players-current-age any-enemy < 3","players-current-age any-enemy <= 3","players-current-age any-enemy != 3"])

    population1 = ["","",0]
    population1[0] = random.choice(["population","civilian-population","military-population","defend-soldier-count",""])
    population1[1] = random.choice(["<",">","==","!=","<=",">="])
    population1[2] = random.randint(0,200)

    population2 = ["","",0]
    population2[0] = random.choice(["population","civilian-population","military-population","defend-soldier-count",""])
    population2[1] = random.choice(["<",">","==","!=","<=",">="])
    population2[2] = random.randint(0,200)

    gametime = ["",0]
    gametime[0] = random.choice(["<",">","==","!=","<=",">=",""])
    gametime[1] = random.randint(0,7200)

    #set-strategic-number sn-percent-attack-soldiers
    attack_percent = random.randint(0,100)

    rule = [age_required, enemy_age_required, population1, population2, gametime, attack_percent]

    return rule

def mutate_attack_rule(rule, mutation_chance):

    age_required = rule[0]
    enemy_age_required = rule[1]
    population1 = rule[2]
    population2 = rule[3]
    gametime = rule[4]
    attack_percent = rule[5]

    if random.random() < mutation_chance:
        age_required = random.choice(["","current-age > 0","current-age != 0","current-age == 0","current-age >= 0","current-age < 0","current-age <= 1","current-age > 1","current-age == 1","current-age >= 1","current-age < 1","current-age <= 1","current-age != 1","current-age <= 2","current-age > 2","current-age == 2","current-age >= 2","current-age < 2","current-age <= 3","current-age != 3","current-age <= 3","current-age > 3","current-age == 3","current-age >= 3","current-age < 3","current-age <= 3","current-age != 3"])

    if random.random() < mutation_chance:
        enemy_age_required = random.choice(["","players-current-age any-enemy > 0","players-current-age any-enemy != 0","players-current-age any-enemy == 0","players-current-age any-enemy >= 0","players-current-age any-enemy < 0","players-current-age any-enemy <= 1","players-current-age any-enemy > 1","players-current-age any-enemy == 1","players-current-age any-enemy >= 1","players-current-age any-enemy < 1","players-current-age any-enemy <= 1","players-current-age any-enemy != 1","players-current-age any-enemy <= 2","players-current-age any-enemy > 2","players-current-age any-enemy == 2","players-current-age any-enemy >= 2","players-current-age any-enemy < 2","players-current-age any-enemy <= 3","players-current-age any-enemy != 3","players-current-age any-enemy <= 3","players-current-age any-enemy > 3","players-current-age any-enemy == 3","players-current-age any-enemy >= 3","players-current-age any-enemy < 3","players-current-age any-enemy <= 3","players-current-age any-enemy != 3"])

    if random.random() < mutation_chance:
        population1[0] = random.choice(["population","civilian-population","military-population","defend-soldier-count",""])
    if random.random() < mutation_chance:
        population1[1] = random.choice(["<",">","==","!=","<=",">="])
    if random.random() < mutation_chance:
        population1[2] = random.randint(0,200)

    if random.random() < mutation_chance:
        population2[0] = random.choice(["population","civilian-population","military-population","defend-soldier-count",""])
    if random.random() < mutation_chance:
        population2[1] = random.choice(["<",">","==","!=","<=",">="])
    if random.random() < mutation_chance:
        population2[2] = random.randint(0,200)

    if random.random() < mutation_chance:
        gametime[0] = random.choice(["<",">","==","!=","<=",">=",""])
    if random.random() < mutation_chance:
        gametime[1] = random.randint(0,7200)

    if random.random() < mutation_chance:
        attack_percent = random.randint(0,100)

    rule = [age_required, enemy_age_required, population1, population2, gametime, attack_percent]

    return rule

def write_attack_rule(rule):

    string = ""
    string += "\n" #+ age_required[0] + "\n"
    string += "(defrule \n"

    age_required = rule[0]
    enemy_age_required = rule[1]
    population1 = rule[2]
    population2 = rule[3]
    gametime = rule[4]
    attack_percent = rule[5]

    if age_required == "" and enemy_age_required == "" and population1[0] == "" and population2[0] == "" and gametime[0] == "" and population1[1] != "" and population2[1] != "":
        string += "\n\t(true)"
    else:

        if age_required != "" and age_required != [""]:
            try:
                string += "\n\t(" + age_required + ")"
                string += "\n\t"
            except TypeError:
                string += "\n\t(" + age_required[0] + ")"
                string += "\n\t"

        if enemy_age_required != "" and enemy_age_required != [""]:
            try:
                string += "\n\t(" + enemy_age_required + ")"
                string += "\n\t"
            except TypeError:
                string += "\n\t(" + enemy_age_required[0] + ")"
                string += "\n\t"


        if population1[0] != "" and population1[1] != "":
            string += "(" + population1[0] + " " + population1[1] + " " + str(population1[2]) + ")\n\t"

        if population2[0] != "" and population2[1] != "":
            string += "(" + population2[0] + " " + population2[1] + " " + str(population2[2]) + ")\n\t"

        if gametime[0] != "":
            string += "(game-time " + gametime[0] + " " + str(gametime[1]) + ")\n\t"

    string += "\n=>\n\t"

    string += "(set-strategic-number sn-percent-attack-soldiers " + str(attack_percent)
    string += ")\n\t(attack-now)\n)"

    return string

#a = read_ai("b4")
#temp = generate_simple()
#temp[0] = 'train'
#temp[1]['Trainable'] = 'knight-line'
#temp[2] = 50
#temp[3] = [""]
#a[1] = [temp] + a[1]
#save_ai(a,"best")
#write_ai(a,"best")
#
#a = read_ai("b5")
#temp = generate_simple()
#temp[0] = 'train'
#temp[1]['Trainable'] = '759'
#temp[2] = 50
#temp[3] = ["current-age  >= 2"]
#a[1] = [temp] + a[1]
#temp = generate_simple()
#temp[0] = 'train'
#temp[1]['Trainable'] = 'huskarl-line'
#temp[2] = 50
#temp[3] = ["current-age  >= 2"]
#a[1] = [temp] + a[1]
#
#temp = generate_simple()
#temp[0] = 'build'
#temp[1]['Buildable'] = 'lumber-camp'
#temp[2] = 1
#temp[3] = [""]
#a[1] = [temp] + a[1]
#
#temp = generate_simple()
#temp[0] = 'build'
#temp[1]['Buildable'] = 'mining-camp'
#temp[2] = 1
#temp[3] = [""]
#a[1] = [temp] + a[1]
#
#temp = generate_simple()
#temp[0] = 'build'
#temp[1]['Buildable'] = 'mill'
#temp[2] = 1
#temp[3] = [""]
#a[1] = [temp] + a[1]
#
#temp = generate_simple()
#temp[0] = 'build'
#temp[1]['Buildable'] = 'castle'
#temp[2] = 1
#temp[3] = [""]
#a[1] = [temp] + a[1]
#
#temp = generate_simple()
#temp[0] = 'build'
#temp[1]['Buildable'] = 'market'
#temp[2] = 2
#temp[3] = [""]
#a[1] = [temp] + a[1]


#a = read_ai("b5")
#temp = generate_simple()
#temp[0] = 'research'
#temp[1]['TechId'] = 'anarchy'
#temp[2] = 2
#temp[3] = [""]
#a[1] = [temp] + a[1]
#
#save_ai(a,"best")
#write_ai(a,"best")

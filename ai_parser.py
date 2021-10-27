import os
import re
import pickle
from dataclasses import dataclass, field

fact_names = {'attack-soldier-count', 'building-available', 'building-count', 'building-count-total',
              'building-type-count', 'building-type-count-total', 'can-afford-building', 'can-afford-complete-wall',
              'can-afford-research', 'can-afford-unit', 'can-build', 'can-build-with-escrow', 'can-build-gate',
              'can-build-gate-with-escrow', 'can-build-wall', 'can-build-wall-with-escrow', 'can-buy-commodity',
              'can-research', 'can-research-with-escrow', 'can-sell-commodity', 'can-spy', 'can-spy-with-escrow',
              'can-train', 'can-train-with-escrow', 'civilian-population', 'civ-selected', 'commodity-buying-price',
              'commodity-selling-price', 'current-age', 'current-age-time', 'current-score', 'death-match-game',
              'defend-soldier-count', 'defend-warboat-count', 'difficulty', 'doctrine', 'dropsite-min-distance',
              'enemy-buildings-in-town', 'enemy-captured-relics', 'escrow-amount', 'event-detected', 'FALSE',
              'food-amount', 'game-time', 'game-type', 'gate-count', 'goal', 'gold-amount', 'hold-koh-ruin',
              'hold-relics', 'housing-headroom', 'idle-farm-count', 'map-size', 'map-type', 'military-population',
              'player-computer', 'player-human', 'player-in-game', 'player-number', 'player-resigned', 'player-valid',
              'players-building-count', 'players-building-type-count', 'players-civ', 'players-civilian-population',
              'players-current-age', 'players-current-age-time', 'players-military-population', 'players-population',
              'players-score', 'players-stance', 'players-unit-count', 'players-unit-type-count', 'population',
              'population-cap', 'population-headroom', 'random-number', 'research-available', 'research-completed',
              'resource-found', 'shared-goal', 'sheep-and-forage-too-far', 'soldier-count', 'stance-toward',
              'starting-age', 'starting-resources', 'stone-amount', 'strategic-number', 'taunt-detected',
              'timer-triggered', 'town-under-attack', 'TRUE', 'unit-available', 'unit-count', 'unit-count-total',
              'unit-type-count', 'unit-type-count-total', 'victory-condition', 'wall-completed-percentage',
              'wall-invisible-percentage', 'warboat-count', 'wood-amount', 'up-add-object-by-id', 'up-allied-goal',
              'up-allied-resource-amount', 'up-allied-sn', 'up-attacker-class', 'up-building-type-in-town',
              'up-can-build', 'up-can-build-line', 'up-can-research', 'up-can-search', 'up-can-train',
              'up-compare-const', 'up-compare-flag', 'up-compare-goal', 'up-compare-sn', 'up-compare-text',
              'up-defender-count', 'up-enemy-buildings-in-town', 'up-enemy-units-in-town', 'up-enemy-villagers-in-town',
              'up-find-remote', 'up-find-resource', 'up-find-status-local', 'up-find-status-remote',
              'up-gaia-type-count', 'up-gaia-type-count-total', 'up-get-fact', 'up-get-fact-max', 'up-get-fact-min',
              'up-get-fact-sum', 'up-get-focus-fact', 'up-get-object-data', 'up-get-object-target-data',
              'up-get-player-fact', 'up-get-point-contains', 'up-get-target-fact', 'up-group-size',
              'up-idle-unit-count', 'up-modify-goal', 'up-object-data', 'up-object-target-data', 'up-object-type-count',
              'up-object-type-count-total', 'up-path-distance', 'up-pending-objects', 'up-pending-placement',
              'up-player-distance', 'up-players-in-game', 'up-point-contains', 'up-point-distance',
              'up-point-elevation', 'up-point-explored', 'up-point-terrain', 'up-point-zone', 'up-projectile-detected',
              'up-projectile-target', 'up-remaining-boar-amount', 'up-research-status', 'up-resource-amount',
              'up-resource-percent', 'up-set-target-by-id', 'up-set-target-object', 'up-timer-status',
              'up-train-site-ready', 'up-unit-type-in-town', 'up-villager-type-in-town', 'up-allied-resource-percent',
              'up-find-local'}


# ========== Utility Functions ============

def dir_exists(path: str, raise_exception: bool = False) -> bool:
    if os.path.isdir(path):
        return True
    elif raise_exception:
        raise Exception(f"Directory {path} does not exist!")
    return False


def file_exists(path: str, raise_exception: bool = False) -> bool:
    if os.path.isfile(path):
        return True
    elif raise_exception:
        raise Exception(f"File {path} does not exist!")
    return False


def write_to_file(path: str, contents: str, create_if_not_exists=False, append=False):
    if not create_if_not_exists and not os.path.isfile(path):
        print(f"File writing failed: {path} does not exist!")
    mode = "a" if append else "w+"
    with open(path, mode) as file:
        file.write(contents)


def read_file_raw(path: str) -> str:
    file_exists(path, raise_exception=True)
    with open(path, mode="r") as file:
        return file.read()


def str_to_int(string: str, allow_negative: bool = True) -> tuple:
    if string.isdigit():
        return True, int(string)
    if allow_negative and string.startswith("-"):
        return True, -int(string[1:])
    # print(f"String '{string}' cannot be converted to int, returning the string instead.")
    return False, string


def inside_outer_parentheses(string: str):
    first_parenthesis_index = string.find("(") + 1
    last_parenthesis_index = string.rfind(")")
    return string[first_parenthesis_index:last_parenthesis_index]


# =========================================

operators = {"and": "&", "or": "|", "not": '#', "nand": '$', "nor": '@'}


@dataclass
class FactBase:
    name: str  # For a simple, this the name of the fact. For a Complex, this is an operator.
    depth: int = field(init=False, default=0)

    @property
    def is_simple(self) -> bool:
        return self.name not in operators

    @property
    def is_complex(self) -> bool:
        return not self.is_simple

    def set_depth(self, value: int):
        self.depth = value


@dataclass
class Simple(FactBase):
    params: list
    length: int
    relevant_length: int

    def __init__(self, params, *args):
        if isinstance(params, str):
            self.name = params
            if args:
                self.params = self.__get_params(args)
        if isinstance(params, (list, tuple)):
            if len(params) > 5:
                raise Exception("A Simple only take a name and a maximum of 4 arguments.")
            self.name = params[0]
            self.params = self.__get_params(list(params)[1:])

        if self.params:
            self.length = self.relevant_length = len(params)

        self.depth = 0

    @staticmethod
    def __get_params(params: list) -> list:
        if params is None:
            return None
        # If the params passed through are a list or tuple, we just use that one.
        if isinstance(params, list) or isinstance(params, tuple) or isinstance(params, set):
            if len(params) > 4:
                raise Exception("Cannot create Simple with more than 4 parameters!")
            return [str(x) for x in params]
        raise Exception("Arguments passed to the Simple init should be either a single list or multiple int and string")

    def __str__(self):
        string = f"({self.name} "
        if self.params:
            string += ' '.join(self.params[:self.relevant_length])

        return string + ")"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.length


@dataclass
class Complex(FactBase):
    param1: FactBase
    param2: FactBase = None

    def __init__(self, name: str, param1: FactBase, param2: FactBase = None):
        self.name = name
        self.param1 = param1
        self.param2 = param2
        self.set_depth(0)  # Set the depths recursively

    def __str__(self):
        name_tabs = '\t' * (1 if len(self.name) > 2 else 2)
        result = f"({self.name}{name_tabs}{self.param1}"
        if self.param2:
            tabs = '\t' * (self.param2.depth * 2 + 1)  # The plus 1 is because every rule has every line indented 1 tab
            result += f"\n{tabs}{self.param2}"
        return result + ")"

    def set_depth(self, value: int):
        self.depth = value
        self.param1.set_depth(value + 1)
        if self.param2:
            self.param2.set_depth(value + 1)


@dataclass
class Rule:
    facts: list[FactBase]
    primary_facts: list[FactBase]
    actions: list[Simple]
    actions_length: int
    comment_unused: bool  # If this is True, during printing, this rule will comment out the 'unused' actions and facts

    def __init__(self, facts: list[FactBase], actions: list, facts_length: int = None, actions_length: int = None,
                 comment_unused: bool = False):
        if not facts:
            raise Exception("Cannot create a rule without any facts!")
        elif not actions:
            raise Exception("Cannot create a rule without any actions!")

        self.facts = facts
        self.primary_facts = self.get_facts(depth=0)
        self.actions = actions

        if facts_length is not None and facts_length < 0:
            print(f"Warning! Facts length cannot be smaller than zero. Defaulting to None.")
            facts_length = None

        if actions_length is not None and (actions_length < 0 or actions_length > 4):
            print(f"Warning! Action length cannot be smaller than zero or greater than 4.")
            actions_length = None

        self.facts_length = facts_length if facts_length is not None else len(self.facts)
        self.actions_length = actions_length if actions_length is not None else len(self.actions)
        self.comment_unused = comment_unused

    def get_facts(self, depth: int = None):
        if depth is None:
            return self.facts[:]
        elif depth == 1:
            return self.primary_facts[:]
        return [fact for fact in self.facts if fact.depth == depth]

    def __str__(self):
        string = "(defrule\n"

        if self.comment_unused:
            for index, fact in enumerate(self.facts):
                string += f"{index:{';' if index >= self.facts_length else ''}\t}{fact}\n"
            string += "=>\n"
            for index, action in enumerate(self.actions):
                string += f"{index:{';' if index >= self.actions_length else ''}\t}{action}\n"
        else:
            for fact in self.primary_facts[:self.facts_length]:
                string += f"\t{fact}\n"
            string += "=>\n"
            for action in self.actions[:self.actions_length]:
                string += f"\t{action}\n"

        string += ")"
        return string

    def __repr__(self):
        return str(self)


class AIParser:
    @staticmethod
    def read_single(path: str = "C:\\Program Files\\Microsoft Games\\age of empires ii\\Ai\\Alpha.per",
                    raise_exception: bool = True):
        """
        Read a single .per file and return the AI.

        :param path: The path to the .per file.
        :param raise_exception: Whether to raise Exceptions if for example a file cannot be found.
        :return: An instance of the AI class if found, else None.
        """

        if os.path.isfile(path):
            if path.endswith(".per"):
                return AI(path=path)
            elif path.endswith(".pickle"):
                ai = open(path, "rb")
                return pickle.load(ai)
            elif raise_exception:
                raise Exception(f"Cannot read from {path}. The file is not a .per file.")
        elif raise_exception:
            raise Exception(f"Cannot read from {path}. No file found at that path.")
        return None

    @staticmethod
    def read_multiple(path: str, names: set[str] = None, as_dict: bool = True):
        """
        Read multiple AI .per files in a directory and return a list containing the found AI's.

        :param path: The path to the directory containing the .per files.
        :param names: An optional set of names that will act as a filter when reading AIs.
        :param as_dict: Whether to return the result as a dictionary. If False, returns the AI's in a list instead.
        :return: A dict (keys are AI names) or list containing all the AIs, depending on the value of 'as_dict'.
        """

        if not os.path.isdir(path):
            raise Exception(f"The path {path} does not exist or is not a directory.")

        result = dict() if as_dict else []
        found = set()
        for file in os.listdir(path):

            if file.endswith(".per"):
                name = file.removesuffix(".per")
            elif file.endswith(".pickle"):
                name = file.removesuffix(".pickle")
            else:
                continue

            if names and name not in names:
                continue
            ai = AIParser.read_single(os.path.join(path, file), raise_exception=False)
            if ai:
                if as_dict:
                    result[name] = ai
                else:
                    result.append(ai)
                found.add(name)

        if len(found) != len(names):
            print(f"We did not find all the AI's you were looking for: \n Query={names} \n Found={found}.")

        return result

    @staticmethod
    def write_single(ai, target_directory, pickled: bool = True) -> bool:
        if not dir_exists(target_directory, raise_exception=True) or not isinstance(ai, AI):
            print(f"Warning! Writing AI {ai} failed.")
            return False
        if pickled:
            pickle.dump(ai, os.path.join(target_directory, ai.name + ".pickle"))
            return True
        else:
            ai.write()


class AI:
    def __init__(self, path: str):
        self.path = self.__repair_path(path)  # The path to the AI .per file
        # The directory in which this AI's .per file is located & The name of this AI.
        self.parent_directory, self.name = os.path.split(path)
        self.name = self.name.removesuffix(".per")
        # Whether this AI is visible in the selection dropdown in-game
        self.visible = os.path.isfile(os.path.join(self.parent_directory, (self.name + ".ai")))
        self.raw_content = read_file_raw(path)
        self.simple_indicator = '*'
        self.complex_indicator = '%'
        self.operators = {"and": "&", "or": "|", "not": '#', "nand": '$', "nor": '@'}
        self.operators_inverse = dict()
        for operator_name, operator_symbol in self.operators.items():
            self.operators_inverse[operator_symbol] = operator_name

        self.constants, self.rules = self._parse_raw_content(content=self.raw_content)
        x = 0

    @staticmethod
    def __repair_path(path: str) -> str:
        if os.path.isfile(path) and path.endswith(".per"):
            return path
        raise Exception(f"Cannot instance AI with incorrect path {path}. \n There could be a few reasons for this. \n"
                        f"1. The path specified does not reference to a valid location / file. \n"
                        f"2. The path specified does not reference to a .per file but some type of file. \n"
                        f"3. Between pickling and unpickling this AI, the corresponding .per file has been deleted.")

    def _parse_raw_content(self, content):
        constants = dict()
        current_rule_lines = None
        rules = []

        for line in content.split("\n"):
            line = line.strip()

            comment_index = line.find(";")
            if comment_index == 0:  # This line is a comment.
                continue
            elif comment_index > 0:  # This line contains a comment.
                line = line[:comment_index].strip()

            # Skip empty lines.
            if len(line) == 0:
                continue

            if line.startswith("(defrule"):
                # If we found the beginning of a rule and we are not busy with another rule,
                if current_rule_lines is None:
                    current_rule_lines = []
                else:
                    rules.append(self._lines_to_rule(current_rule_lines[:]))
                    current_rule_lines = []

            elif line.startswith("(load"):  # We need to load a different file as well!
                extra_file = line.split(' "')[1].removesuffix('")').strip()
                loaded_raw_content = read_file_raw(os.path.join(self.parent_directory, (extra_file + ".per")))
                loaded, _ = self._parse_raw_content(loaded_raw_content)
                constants.update(loaded)

                if current_rule_lines is not None:
                    rules.append(self._lines_to_rule(current_rule_lines[:]))
                    current_rule_lines = None

            elif line.startswith("(defconst"):  # This line is a constant
                name, value = self._line_to_constant(line)
                is_digit, value = str_to_int(value, allow_negative=True)

                # If our constant value is a string, it must be an existing constants' value
                if not is_digit and value in constants.keys():
                    value = constants[value]
                constants[name] = value

                if current_rule_lines is not None:
                    # TODO : convert list to string here, instead of later in the function
                    rules.append(self._lines_to_rule(current_rule_lines[:]))
                    current_rule_lines = None

            # If we are currently working on a rule, add the current line, unless it's the trailing parenthesis
            elif current_rule_lines is not None and len(line.strip()) > 0:
                current_rule_lines.append(line.strip())

        return constants, rules

    @staticmethod
    def _line_to_constant(line: str) -> tuple:
        clean = inside_outer_parentheses(line)
        clean = clean.split(" ")
        if clean[0] != "defconst":
            raise Exception(f"Line '{line}'is not a constant!")
        return clean[1], clean[2]

    def _lines_to_rule(self, lines: list[str]):
        splitter_index = lines.index("=>")
        fact_lines = lines[:splitter_index]
        facts = self._lines_to_facts(fact_lines)
        # TODO parse actions correctly
        action_lines = lines[splitter_index + 1:]
        actions = self._lines_to_actions(action_lines)
        return Rule(facts, actions)

    @staticmethod
    def _lines_to_actions(lines: list[str]):
        actions = []
        string = "".join(lines)
        string = re.sub(r"[\s\t\n\r]*\([\s\t\n\r]*", "(", string)  # Remove whitespace
        string = re.sub(r"[\s\t\n\r]*\)[\s\t\n\r]*", ")", string)  # Remove whitespace
        pattern = r"\([a-zA-Z0-9\- ><=!:\+]+\)"
        for action_string in re.findall(pattern, string):
            action_string = action_string.removesuffix(")")
            action_string = action_string.removeprefix("(")
            if len(action_string) > 0:
                actions.append(Simple(action_string.split()))
        return actions

    def _lines_to_facts(self, lines: list[str]):
        string = "".join(lines)
        string = re.sub(r"[\s\t\n\r]*\([\s\t\n\r]*", "(", string)  # Remove all irrelevant whitespace
        string = re.sub(r"[\s\t\n\r]*\)[\s\t\n\r]*", ")", string)  # Remove all irrelevant whitespace

        # Replace all operator keywords for symbols
        for operator, value in self.operators.items():
            string = re.sub(r"\(\s*" + operator + r"\s*\(", f"({value}(", string)

        simples, string, without_globals = self._extract_simple_facts(string)
        complexes = self._extract_complex_facts(without_globals, simples)
        simples.extend(complexes)
        return simples

    def _extract_simple_facts(self, string: str):
        without_globals = string
        simples = []
        pattern = r"\([a-zA-Z0-9\- ><=!:]+\)"
        match = re.search(pattern, string)
        while match:
            depth = string.count("(", 0, match.start())
            depth -= string.count(")", 0, match.start())
            simple_as_list = match[0][1:-1].split()  # Remove the parenthesis TODO Maybe remove using regex.
            simples.append(Simple(simple_as_list))
            string = string.replace(match[0], f"({self.simple_indicator}{len(simples) - 1})")
            if depth == 0:
                without_globals = without_globals.replace(match[0], "")
            else:
                without_globals = without_globals.replace(match[0], f"({self.simple_indicator}{len(simples) - 1})")
            match = re.search(pattern, string)
        return simples, string, without_globals

    def _extract_complex_facts(self, string: str, simples: list) -> list:
        if len(string) == 0:
            return []

        pattern = r"\([&|#@$](\((\*|\%)[0-9]+\)){1,2}\)"
        match = re.search(pattern, string)
        complexes = []
        # If we find a match, we most certainly have a valid complex fact
        while match:
            s = match[0]
            complexes.append(self.string_to_complex(s, simples, complexes))
            string = string.replace(match[0], f"({self.complex_indicator}{len(complexes) - 1})")
            match = re.search(pattern, string)
        return complexes

    def string_to_complex(self, string: str, simples: list, complexes: list) -> Complex:
        string = string.removesuffix(")")
        string = string.removeprefix("(")
        # The operator symbol, followed by the simple/complex indicator and then the index
        end = string.find(")")
        index1 = int(string[3:end])
        param1 = simples[index1] if (string[2] == self.simple_indicator) else complexes[index1]
        if string[0] == self.operators['not']:
            return Complex(name="not", param1=param1)

        elif string[0] in self.operators.values():
            start = string.rfind("(")
            end = string.rfind(")")
            index2 = int(string[7:end])
            param2 = simples[index2] if (string[start + 1] == self.simple_indicator) else complexes[index2]
            return Complex(name=self.operators_inverse[string[0]], param1=param1, param2=param2)

        raise Exception(f"{string[0]} is not a valid operator symbol!")

    def write(self, target_directory: str = None):
        destination: str = ""
        if target_directory is not None and dir_exists(target_directory, raise_exception=True):
            destination = os.path.join(target_directory, self.name + ".per")
        elif file_exists(self.path, raise_exception=True):
            destination = self.path
        else:
            raise Exception(f"AI {self.name} couldn't write its content to {destination}, destination doesn't exist!")

        with open(destination, 'w') as file:
            # Write constants
            for constant_name, constant_value in self.constants.items():
                file.write(f"(defconst {constant_name} {constant_value}) \n")

            # Write rules
            for rule in self.rules:
                file.write(str(rule) + "\n\n")

# ai_path = "C:\\Program Files\\Microsoft Games\\age of empires ii\\Ai"
# example_path = "C:\\Program Files\\Microsoft Games\\age of empires ii\\Ai\\Alpha.per"
# ai = AIParser.read_single(example_path)
# ai.write("C:\\Users\\Gabi\\Documents\\GitHub\\AlphaScripter")
# names = {"parent", "a", "b", "c", "d", "e", "f"}

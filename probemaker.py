#!', 'usr', 'bin', 'env python
# -*- coding: utf-8 -*-

import os
import json
from random import randint
from pathlib import Path
import warnings
from typing import List
from settings import debug

if debug:
    print(os.listdir())
    print(os.getcwd())

if "settings.py" in os.listdir():
    from settings import *
else:
    # fallback if no custom settings are provided
    from settings_template import *


class Hero:
    """ Class to create an Hero object from heros .json file

    file -- .json file name from Optolith containing hero's data_folder
    show_values -- If set, show all character values when load hero

    """

    def __init__(self, file, show_values=False):

        # Prepare and load hero's .json file
        f = open(file)
        h_data = json.load(f)
        self.name = h_data['name']
        print('=======================')
        print('The great hero called ' + self.name + ' is being summoned into the working memory.')
        print('=======================')

        # Basic attributs
        attr = h_data['attr']['values']  # Get data from .json file
        attr_dict = {}
        for a in attr:
            attr_dict[a['id']] = a['value']

        self.attr = dict()  # Dict to collect all attributs
        self.attr['MU'] = attr_dict['ATTR_1'] if 'ATTR_1' in attr_dict else 8
        self.attr['KL'] = attr_dict['ATTR_2'] if 'ATTR_2' in attr_dict else 8
        self.attr['IN'] = attr_dict['ATTR_3'] if 'ATTR_3' in attr_dict else 8
        self.attr['CH'] = attr_dict['ATTR_4'] if 'ATTR_4' in attr_dict else 8
        self.attr['FF'] = attr_dict['ATTR_5'] if 'ATTR_5' in attr_dict else 8
        self.attr['GE'] = attr_dict['ATTR_6'] if 'ATTR_6' in attr_dict else 8
        self.attr['KO'] = attr_dict['ATTR_7'] if 'ATTR_7' in attr_dict else 8
        self.attr['KK'] = attr_dict['ATTR_8'] if 'ATTR_8' in attr_dict else 8

        # Get race and compute derived stats
        self.ap = h_data['ap']
        self.LP_max = 2 * self.attr['KO']
        self.race = h_data['r']
        if self.race == 'R_1':
            self.race == 'Human'
            self.LP_max = self.LP_max + 5
        elif self.race == 'R_2':
            self.race == 'Halfelf'
            self.LP_max = self.LP_max + 5
        elif self.race == 'R_3':
            self.race == 'Elf'
            self.LP_max = self.LP_max + 2
        elif self.race == 'R_4':
            self.race == 'Dwarf'
            self.LP_max = self.LP_max + 8

        # Talents
        talents = h_data['talents']  # Get data from .json file
        self.tal = dict()  # Dict to collent all talents
        self.tal['Fliegen'] = ['MU', 'IN', 'GE', talents['TAL_1'] if 'TAL_1' in talents else 0]
        self.tal['Gaukeleien'] = ['MU', 'CH', 'FF', talents['TAL_2'] if 'TAL_2' in talents else 0]
        self.tal['Klettern'] = ['MU', 'GE', 'KK', talents['TAL_3'] if 'TAL_3' in talents else 0]
        self.tal['Koerperbeherrschung'] = ['GE', 'GE', 'KO', talents['TAL_4'] if 'TAL_4' in talents else 0]
        self.tal['Kraftakt'] = ['KO', 'KK', 'KK', talents['TAL_5'] if 'TAL_5' in talents else 0]
        self.tal['Reiten'] = ['CH', 'GE', 'KK', talents['TAL_6'] if 'TAL_6' in talents else 0]
        self.tal['Schwimmen'] = ['GE', 'KO', 'KK', talents['TAL_7'] if 'TAL_7' in talents else 0]
        self.tal['Selbstbeherrschung'] = ['MU', 'MU', 'KO', talents['TAL_8'] if 'TAL_8' in talents else 0]
        self.tal['Singen'] = ['KL', 'CH', 'KO', talents['TAL_1'] if 'TAL_1' in talents else 0]
        self.tal['Sinnesschaerfe'] = ['KL', 'IN', 'IN', talents['TAL_9'] if 'TAL_9' in talents else 0]
        self.tal['Tanzen'] = ['KL', 'CH', 'GE', talents['TAL_10'] if 'TAL_10' in talents else 0]
        self.tal['Taschendiebstahl'] = ['MU', 'FF', 'GE', talents['TAL_1'] if 'TAL_1' in talents else 0]
        self.tal['Verbergen'] = ['MU', 'IN', 'GE', talents['TAL_11'] if 'TAL_11' in talents else 0]
        self.tal['Zechen'] = ['KL', 'KO', 'KK', talents['TAL_12'] if 'TAL_12' in talents else 0]

        self.tal['Bekehren u Ueberzeugen'] = ['MU', 'KL', 'CH', talents['TAL_13'] if 'TAL_13' in talents else 0]
        self.tal['Betoeren'] = ['MU', 'CH', 'CH', talents['TAL_14'] if 'TAL_14' in talents else 0]
        self.tal['Einschuechtern'] = ['MU', 'IN', 'CH', talents['TAL_15'] if 'TAL_15' in talents else 0]
        self.tal['Etikette'] = ['KL', 'IN', 'CH', talents['TAL_16'] if 'TAL_16' in talents else 0]
        self.tal['Gassenwissen'] = ['KL', 'IN', 'CH', talents['TAL_17'] if 'TAL_17' in talents else 0]
        self.tal['Menschenkenntnis'] = ['KL', 'IN', 'CH', talents['TAL_18'] if 'TAL_18' in talents else 0]
        self.tal['Ueberreden'] = ['MU', 'IN', 'CH', talents['TAL_19'] if 'TAL_19' in talents else 0]
        self.tal['Verkleiden'] = ['IN', 'CH', 'GE', talents['TAL_20'] if 'TAL_20' in talents else 0]
        self.tal['Willenskraft'] = ['MU', 'IN', 'CH', talents['TAL_21'] if 'TAL_21' in talents else 0]

        self.tal['Faehrtensuchen'] = ['MU', 'IN', 'GE', talents['TAL_22'] if 'TAL_23' in talents else 0]
        self.tal['Fesseln'] = ['KL', 'FF', 'KK', talents['TAL_24'] if 'TAL_24' in talents else 0]
        self.tal['Fischen u Angeln'] = ['FF', 'GE', 'KO', talents['TAL_25'] if 'TAL_25' in talents else 0]
        self.tal['Orientierung'] = ['KL', 'IN', 'IN', talents['TAL_26'] if 'TAL_26' in talents else 0]
        self.tal['Pflanzenkunde'] = ['KL', 'FF', 'KO', talents['TAL_27'] if 'TAL_27' in talents else 0]
        self.tal['Tierkunde'] = ['MU', 'MU', 'CH', talents['TAL_28'] if 'TAL_28' in talents else 0]
        self.tal['Wildnisleben'] = ['MU', 'GE', 'KO', talents['TAL_29'] if 'TAL_29' in talents else 0]

        self.tal['Brett- u Gluecksspiel'] = ['KL', 'KL', 'IN', talents['TAL_30'] if 'TAL_30' in talents else 0]
        self.tal['Geographie'] = ['KL', 'KL', 'IN', talents['TAL_31'] if 'TAL_31' in talents else 0]
        self.tal['Geschichtswissen'] = ['KL', 'KL', 'IN', talents['TAL_32'] if 'TAL_32' in talents else 0]
        self.tal['Goetter u Kulte'] = ['KL', 'KL', 'IN', talents['TAL_33'] if 'TAL_33' in talents else 0]
        self.tal['Kriegskunst'] = ['MU', 'KL', 'IN', talents['TAL_34'] if 'TAL_34' in talents else 0]
        self.tal['Magiekunde'] = ['KL', 'KL', 'IN', talents['TAL_35'] if 'TAL_35' in talents else 0]
        self.tal['Mechanik'] = ['KL', 'KL', 'FF', talents['TAL_36'] if 'TAL_36' in talents else 0]
        self.tal['Rechnen'] = ['KL', 'KL', 'IN', talents['TAL_37'] if 'TAL_37' in talents else 0]
        self.tal['Rechtskunde'] = ['KL', 'KL', 'IN', talents['TAL_37'] if 'TAL_37' in talents else 0]
        self.tal['Sagen u Legenden'] = ['KL', 'KL', 'IN', talents['TAL_38'] if 'TAL_38' in talents else 0]
        self.tal['Sphaerenkunde'] = ['KL', 'KL', 'IN', talents['TAL_39'] if 'TAL_39' in talents else 0]
        self.tal['Sternkunde'] = ['KL', 'KL', 'IN', talents['TAL_40'] if 'TAL_40' in talents else 0]

        self.tal['Alchimie'] = ['MU', 'KL', 'FF', talents['TAL_41'] if 'TAL_41' in talents else 0]
        self.tal['Boote u Schiffe'] = ['FF', 'GE', 'KK', talents['TAL_42'] if 'TAL_42' in talents else 0]
        self.tal['Fahrzeuge'] = ['CH', 'FF', 'KO', talents['TAL_43'] if 'TAL_43' in talents else 0]
        self.tal['Handel'] = ['KL', 'IN', 'CH', talents['TAL_44'] if 'TAL_44' in talents else 0]
        self.tal['Heilkunde Gift'] = ['MU', 'KL', 'IN', talents['TAL_45'] if 'TAL_45' in talents else 0]
        self.tal['Heilkunde Krankheiten'] = [' MU', 'IN', 'KO', talents['TAL_46'] if 'TAL_46' in talents else 0]
        self.tal['Heilkunde Seele'] = ['IN', 'CH', 'KO', talents['TAL_47'] if 'TAL_47' in talents else 0]
        self.tal['Heilkunde Wunden'] = ['KL', 'FF', 'FF', talents['TAL_48'] if 'TAL_48' in talents else 0]
        self.tal['Holzbearbeitung'] = ['FF', 'GE', 'KK', talents['TAL_49'] if 'TAL_49' in talents else 0]
        self.tal['Lebensmittelbearbeitung'] = ['IN', 'FF', 'FF', talents['TAL_50'] if 'TAL_50' in talents else 0]
        self.tal['Lederbearbeitung'] = ['FF', 'GE', 'KO', talents['TAL_51'] if 'TAL_51' in talents else 0]
        self.tal['Malen u Zeichnen'] = ['IN', 'FF', 'FF', talents['TAL_52'] if 'TAL_52' in talents else 0]
        self.tal['Metallbearbeitung'] = ['FF', 'KO', 'KK', talents['TAL_53'] if 'TAL_53' in talents else 0]
        self.tal['Musizieren'] = ['CH', 'FF', 'KO', talents['TAL_54'] if 'TAL_54' in talents else 0]
        self.tal['Schloesserknacken'] = ['IN', 'FF', 'FF', talents['TAL_55'] if 'TAL_55' in talents else 0]
        self.tal['Steinbearbeitung'] = ['FF', 'FF', 'KK', talents['TAL_56'] if 'TAL_56' in talents else 0]
        self.tal['Stoffbearbeitung'] = ['KL', 'FF', 'FF ', talents['TAL_57'] if 'TAL_57' in talents else 0]
        self.tal['wichsen'] = ['MU', 'IN', 'KK', 5000]

        if show_values:
            print('These are ' + self.name + "'s basic atrributes:")
            print('=======================')

            for att in self.attr:
                print(att + ': ' + str(self.attr[att]))
            print('=======================')
            print('These are ' + self.name + "'s derived atrributes:")
            print(f'LP: {self.LP_max}')
            print('=======================')
            print(f"These are {self.name}'s talents:")
            print('=======================')
            print(self.tal)
            print('=======================')

        # Get everything that can be probed on
        self.possible_probes = list()
        # Talents
        for key in self.tal.keys():
            self.possible_probes.append(key)
        # Attributes
        for key in self.attr.keys():
            self.possible_probes.append(key)

    def perform_attr_probe(self, attr: str, mod: int = 0):
        print(f"The mighty {self.name} has incredible {self.attr[attr]} points in {attr}," +
              f"the modifier for this probe is {mod}")
        roll = randint(1, 20)
        res = self.attr[attr] - roll + mod
        print(f'The die shows a {roll}')
        if res >= 0 and roll != 20:
            print(f"{self.name} has passed")
            if roll == 1:
                print('Will it be meisterlich?')
                roll2 = randint(1, 20)
                res2 = self.attr[attr] - roll2 + mod
                if res >= 0:
                    print('Yes!')
                else:
                    print('No :(')
        elif roll != 20:
            print(f"{self.name} has failed")

        if roll == 20:
            print(f"{self.name} has failed, will it be a complete disaster?")
            roll2 = randint(1, 20)
            res2 = self.attr[attr] - roll2 + mod
            if res <= 0:
                print("Yes....")
            else:
                print("No")

    def talent_probe(self, talent: str, mod: int = 0):
        """Method to perform a talent probe

        talent -- name of talent to probe
        mod -- modifier on probe

        """

        # Boolean whether something critical occured
        patz = False
        mega_patz = False
        meister = False
        mega_meister = False

        points_left = self.tal[talent][3]  # Get number of talent points

        print('=======================')
        print('The mighty ' + self.name + ' has ' + str(points_left) + ' talent points when he tries to ' +
              talent + '.')
        if mod != 0:
            print('Probe modified by ' + str(mod) + '.')
            if mod > 0:
                str_mod = ' + ' + str(mod)
            elif mod < 0:
                str_mod = ' - ' + str(abs(mod))
        else:
            str_mod = ' +- ' + str(mod)

        rolls = [randint(1, 20), randint(1, 20), randint(1, 20)]
        print('Rolls:')

        print(self.tal[talent][0] + ': ' + str(rolls[0]) + ' (' + str(self.attr[self.tal[talent][0]]) + str_mod + ')')
        print(self.tal[talent][1] + ': ' + str(rolls[1]) + ' (' + str(self.attr[self.tal[talent][1]]) + str_mod + ')')
        print(self.tal[talent][2] + ': ' + str(rolls[2]) + ' (' + str(self.attr[self.tal[talent][2]]) + str_mod + ')')

        if rolls.count(20) >= 2:
            patz = True
            if rolls.count(20) == 3:
                mega_patz = True
        if rolls.count(1) >= 2:
            meister = True
            if rolls.count(1) == 3:
                mega_meister = True

        res1 = self.attr[self.tal[talent][0]] - rolls[0] + mod
        res2 = self.attr[self.tal[talent][1]] - rolls[1] + mod
        res3 = self.attr[self.tal[talent][2]] - rolls[2] + mod

        # Check single rolls
        if res1 < 0:
            points_left = points_left + res1
        if res2 < 0:
            points_left = points_left + res2
        if res3 < 0:
            points_left = points_left + res3

        # Check whether probe was passed and give corresponding message
        # Fail message
        if not patz and not mega_patz and points_left < 0:
            print(self.name + ' failed with ' + str(points_left) + '.')
        # Success messages
        elif not patz and not mega_patz and points_left >= 0:
            print(self.name + ' passed with ' + str(points_left) + '.')
        elif meister and not mega_meister and points_left < 0:
            print('Though ' + self.name + 'should have failed with ' + str(points_left) +
                  ', our hero was struck by the Gods and passed meisterlich.')
        elif mega_meister and points_left < 0:
            print('Though ' + self.name + 'should have failed with ' + str(points_left) +
                  ', our hero was struck by the Gods and passed mega meisterlich.')

        # Extra messages for meisterlich and patzing
        if meister and not mega_meister:
            print('... and it was meisterlich!')
        elif mega_meister:
            print('... and it was mega meisterlich!')
        elif patz and not mega_patz:
            print(self.name + ' is an idiot and patzed.')
        elif mega_patz:
            print(self.name + ' is an idiot and mega patzed.')

    def export(self, mode: str = "object"):
        """Method to export the hero either in JSON for Optolith or as an pickled object.
        The idea is that the history of Proben can be tracked and analysed so that the corresponding
        talents or attributes can be leveled ;-)
        """

    def perform_action(self, user_action: str, modifier: int = 0) -> bool:
        # Quitting program
        if user_action == 'feddich':
            if len(group) == 1:
                print(self.name + ' has left the building.')
            else:
                for h in names:
                    print(h + ' has left the building.')
            return False

        # Perform probe
        else:
            if user_action in self.tal:
                self.talent_probe(user_action, modifier)
            elif user_action in self.attr:
                self.perform_attr_probe(user_action, modifier)
            else:
                raise ValueError('Talent ' + user_action + " not found, enter 'feddich' to quit")
            return True


def run(group: List[Hero]):
    # Playing loop asking for names and modifiers for talent probes
    # TODO never do an endless while loop, use a max_round = 10000 or so
    playing = True  # Check whether playing loop shall be stopped
    while playing:
        modifier = 0
        if len(group) == 1:
            name, stuff = list(group.items())[0]
        else:
            while True:
                name = input(
                     'Who wants to perform something(' + str(names) + ')? '
                     '(Enter "feddich" to quit.) '
                )
                if name not in group and name != "feddich":
                    warnings.warn("This hero is not known!")
                    print("Please provide a valid hero name!!!")
                else:
                    break
        if name != 'feddich':
            Digga = group[name]
            while True:
                user_action_and_mod = input(
                    "Oh mighty " + Digga.name + ', what are you trying to accomplish ' +
                    'next? (Enter talent or attribute name, optional modifier separated by a comma,' +
                    ' enter "feddich" to quit.) '
                )
                if ',' in user_action_and_mod:
                    user_action = user_action_and_mod.split(',')[0].replace(' ', '')
                    modifier = int(user_action_and_mod.split(',')[1].replace(' ', ''))
                else:
                    user_action = user_action_and_mod
                if debug and user_action != "feddich":
                    print(f"You are trying to perform {user_action} with modifier {modifier}...")

                if user_action not in Digga.possible_probes and user_action != "feddich":
                    warnings.warn(f"This action is not known! ({user_action})")
                    print("Misspelled? Try again ;-)")
                else:
                    break
            playing = Digga.perform_action(user_action, modifier)
        else:
            playing = False


if __name__ == "__main__":

    hfiles = dict()  # Dict for heros' .json files
    group = dict()  # Dict to collect all Hero objects
    names = list()  # List to collect all names of heros in group

    # Create total path to hero files
    for hero in heros:
        hfiles[hero] = (data_folder / hero).resolve()

    if debug:
        print(heros)
        print("Data folder", data_folder)
        print(hfiles)

    # Create Hero objects
    for h in hfiles:
        Digga = Hero(hfiles[h], show_values)
        names.append(Digga.name)
        group[Digga.name] = Digga

    run(group)

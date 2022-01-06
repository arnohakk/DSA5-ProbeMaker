#!', 'usr', 'bin', 'env python
# -*- coding: utf-8 -*-

import os
import json
import logging
from random import randint
from pathlib import Path
import warnings
from typing import List
from difflib import get_close_matches

if "settings.py" in os.listdir():
    from settings import *
else:
    # fallback if no custom settings are provided
    from settings_template import *

if debug:
    print(os.listdir())
    print(os.getcwd())


class Hero:
    """ Class to create an Hero object from heros .json file

    file -- .json file name from Optolith containing hero's data_folder
    show_values -- If set, show all character values when load hero

    """

    def __init__(self, file, logger, show_values=False):

        # Prepare and load hero's .json file
        f = open(file)
        h_data = json.load(f)
        self.name = h_data['name']
        self.logger = logger
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

        print('These are ' + self.name + "'s basic atrributes:")
        print('=======================')

        for att in self.attr:
            print(att + ': ' + str(self.attr[att]))
        print('=======================')

        # Get race and compute derived stats
        self.ap = h_data['ap']
        self.LP_max = 2 * self.attr['KO']

        self.race = h_data['r']
        if self.race == 'R_1':
            self.race = 'Human'
            self.LP_max = self.LP_max + 5
        elif self.race == 'R_2':
            self.race = 'Halfelf'
            self.LP_max = self.LP_max + 5
        elif self.race == 'R_3':
            self.race = 'Elf'
            self.LP_max = self.LP_max + 2
        elif self.race == 'R_4':
            self.race = 'Dwarf'
            self.LP_max = self.LP_max + 8
        print(f'{self.name} is a cute {self.race}!')

        # Get leiteigenschaft
        LEG = h_data['attr']['attributeAdjustmentSelected']
        attr_dict = {'ATTR_1': 'MU', 'ATTR_2': 'KL', 'ATTR_3': 'IN', 'ATTR_4': 'CH', 'ATTR_5': 'FF',
                     'ATTR_6': 'GE', 'ATTR_7': 'KO', 'ATTR_8': 'KK'}
        self.leiteigenschaft = [attr_dict[LEG], self.attr[attr_dict[LEG]]]
        print(f'{self.name}`s leiteigenschaft is {self.leiteigenschaft[0]}.')

        self.LP = self.LP_max
        print(f'{self.name} has {self.LP} of {self.LP_max} LP')

        # Wundschwellen
        print(self.LP_max/4)
        print("===================")
        aa

        # Talents
        talents = h_data['talents']  # Get data from .json file
        self.skills = dict()  # Dict to collect all talents
        self.skills['Fliegen'] = ['MU', 'IN', 'GE', talents['TAL_1'] if 'TAL_1' in talents else 0, 'talent']
        self.skills['Gaukeleien'] = ['MU', 'CH', 'FF', talents['TAL_2'] if 'TAL_2' in talents else 0, 'talent']
        self.skills['Klettern'] = ['MU', 'GE', 'KK', talents['TAL_3'] if 'TAL_3' in talents else 0, 'talent']
        self.skills['Koerperbeherrschung'] = ['GE', 'GE', 'KO', talents['TAL_4'] if 'TAL_4' in talents else 0, 'talent']
        self.skills['Kraftakt'] = ['KO', 'KK', 'KK', talents['TAL_5'] if 'TAL_5' in talents else 0, 'talent']
        self.skills['Reiten'] = ['CH', 'GE', 'KK', talents['TAL_6'] if 'TAL_6' in talents else 0, 'talent']
        self.skills['Schwimmen'] = ['GE', 'KO', 'KK', talents['TAL_7'] if 'TAL_7' in talents else 0, 'talent']
        self.skills['Selbstbeherrschung'] = ['MU', 'MU', 'KO', talents['TAL_8'] if 'TAL_8' in talents else 0, 'talent']
        self.skills['Singen'] = ['KL', 'CH', 'KO', talents['TAL_9'] if 'TAL_9' in talents else 0, 'talent']
        self.skills['Sinnesschaerfe'] = ['KL', 'IN', 'IN', talents['TAL_10'] if 'TAL_10' in talents else 0, 'talent']
        self.skills['Tanzen'] = ['KL', 'CH', 'GE', talents['TAL_11'] if 'TAL_11' in talents else 0, 'talent']
        self.skills['Taschendiebstahl'] = ['MU', 'FF', 'GE', talents['TAL_12'] if 'TAL_12' in talents else 0, 'talent']
        self.skills['Verbergen'] = ['MU', 'IN', 'GE', talents['TAL_13'] if 'TAL_13' in talents else 0, 'talent']
        self.skills['Zechen'] = ['KL', 'KO', 'KK', talents['TAL_14'] if 'TAL_14' in talents else 0, 'talent']

        self.skills['Bekehren u Ueberzeugen'] = ['MU', 'KL', 'CH', talents['TAL_15'] if 'TAL_15' in talents else 0, 'talent']
        self.skills['Betoeren'] = ['MU', 'CH', 'CH', talents['TAL_16'] if 'TAL_16' in talents else 0, 'talent']
        self.skills['Einschuechtern'] = ['MU', 'IN', 'CH', talents['TAL_17'] if 'TAL_17' in talents else 0, 'talent']
        self.skills['Etikette'] = ['KL', 'IN', 'CH', talents['TAL_18'] if 'TAL_18' in talents else 0, 'talent']
        self.skills['Gassenwissen'] = ['KL', 'IN', 'CH', talents['TAL_19'] if 'TAL_19' in talents else 0, 'talent']
        self.skills['Menschenkenntnis'] = ['KL', 'IN', 'CH', talents['TAL_20'] if 'TAL_20' in talents else 0, 'talent']
        self.skills['Ueberreden'] = ['MU', 'IN', 'CH', talents['TAL_21'] if 'TAL_21' in talents else 0, 'talent']
        self.skills['Verkleiden'] = ['IN', 'CH', 'GE', talents['TAL_22'] if 'TAL_22' in talents else 0, 'talent']
        self.skills['Willenskraft'] = ['MU', 'IN', 'CH', talents['TAL_23'] if 'TAL_23' in talents else 0, 'talent']

        self.skills['Faehrtensuchen'] = ['MU', 'IN', 'GE', talents['TAL_24'] if 'TAL_24' in talents else 0, 'talent']
        self.skills['Fesseln'] = ['KL', 'FF', 'KK', talents['TAL_25'] if 'TAL_25' in talents else 0, 'talent']
        self.skills['Fischen u Angeln'] = ['FF', 'GE', 'KO', talents['TAL_26'] if 'TAL_26' in talents else 0, 'talent']
        self.skills['Orientierung'] = ['KL', 'IN', 'IN', talents['TAL_27'] if 'TAL_27' in talents else 0, 'talent']
        self.skills['Pflanzenkunde'] = ['KL', 'FF', 'KO', talents['TAL_28'] if 'TAL_28' in talents else 0, 'talent']
        self.skills['Tierkunde'] = ['MU', 'MU', 'CH', talents['TAL_29'] if 'TAL_29' in talents else 0, 'talent']
        self.skills['Wildnisleben'] = ['MU', 'GE', 'KO', talents['TAL_30'] if 'TAL_30' in talents else 0, 'talent']

        self.skills['Brett- u Gluecksspiel'] = ['KL', 'KL', 'IN', talents['TAL_31'] if 'TAL_31' in talents else 0, 'talent']
        self.skills['Geographie'] = ['KL', 'KL', 'IN', talents['TAL_32'] if 'TAL_32' in talents else 0, 'talent']
        self.skills['Geschichtswissen'] = ['KL', 'KL', 'IN', talents['TAL_33'] if 'TAL_33' in talents else 0, 'talent']
        self.skills['Goetter u Kulte'] = ['KL', 'KL', 'IN', talents['TAL_34'] if 'TAL_34' in talents else 0, 'talent']
        self.skills['Kriegskunst'] = ['MU', 'KL', 'IN', talents['TAL_35'] if 'TAL_35' in talents else 0, 'talent']
        self.skills['Magiekunde'] = ['KL', 'KL', 'IN', talents['TAL_36'] if 'TAL_36' in talents else 0, 'talent']
        self.skills['Mechanik'] = ['KL', 'KL', 'FF', talents['TAL_37'] if 'TAL_37' in talents else 0, 'talent']
        self.skills['Rechnen'] = ['KL', 'KL', 'IN', talents['TAL_38'] if 'TAL_38' in talents else 0, 'talent']
        self.skills['Rechtskunde'] = ['KL', 'KL', 'IN', talents['TAL_39'] if 'TAL_39' in talents else 0, 'talent']
        self.skills['Sagen u Legenden'] = ['KL', 'KL', 'IN', talents['TAL_40'] if 'TAL_40' in talents else 0, 'talent']
        self.skills['Sphaerenkunde'] = ['KL', 'KL', 'IN', talents['TAL_41'] if 'TAL_41' in talents else 0, 'talent']
        self.skills['Sternkunde'] = ['KL', 'KL', 'IN', talents['TAL_42'] if 'TAL_42' in talents else 0, 'talent']

        self.skills['Alchimie'] = ['MU', 'KL', 'FF', talents['TAL_43'] if 'TAL_43' in talents else 0, 'talent']
        self.skills['Boote u Schiffe'] = ['FF', 'GE', 'KK', talents['TAL_44'] if 'TAL_44' in talents else 0, 'talent']
        self.skills['Fahrzeuge'] = ['CH', 'FF', 'KO', talents['TAL_45'] if 'TAL_45' in talents else 0, 'talent']
        self.skills['Handel'] = ['KL', 'IN', 'CH', talents['TAL_46'] if 'TAL_46' in talents else 0, 'talent']
        self.skills['Heilkunde Gift'] = ['MU', 'KL', 'IN', talents['TAL_47'] if 'TAL_47' in talents else 0, 'talent']
        self.skills['Heilkunde Krankheiten'] = [' MU', 'IN', 'KO', talents['TAL_48'] if 'TAL_48' in talents else 0, 'talent']
        self.skills['Heilkunde Seele'] = ['IN', 'CH', 'KO', talents['TAL_49'] if 'TAL_49' in talents else 0, 'talent']
        self.skills['Heilkunde Wunden'] = ['KL', 'FF', 'FF', talents['TAL_50'] if 'TAL_50' in talents else 0, 'talent']
        self.skills['Holzbearbeitung'] = ['FF', 'GE', 'KK', talents['TAL_51'] if 'TAL_51' in talents else 0, 'talent']
        self.skills['Lebensmittelbearbeitung'] = ['IN', 'FF', 'FF', talents['TAL_52'] if 'TAL_52' in talents else 0, 'talent']
        self.skills['Lederbearbeitung'] = ['FF', 'GE', 'KO', talents['TAL_53'] if 'TAL_53' in talents else 0, 'talent']
        self.skills['Malen u Zeichnen'] = ['IN', 'FF', 'FF', talents['TAL_54'] if 'TAL_54' in talents else 0, 'talent']
        self.skills['Metallbearbeitung'] = ['FF', 'KO', 'KK', talents['TAL_55'] if 'TAL_55' in talents else 0, 'talent']
        self.skills['Musizieren'] = ['CH', 'FF', 'KO', talents['TAL_56'] if 'TAL_56' in talents else 0, 'talent']
        self.skills['Schloesserknacken'] = ['IN', 'FF', 'FF', talents['TAL_57'] if 'TAL_57' in talents else 0, 'talent']
        self.skills['Steinbearbeitung'] = ['FF', 'FF', 'KK', talents['TAL_58'] if 'TAL_58' in talents else 0, 'talent']
        self.skills['Stoffbearbeitung'] = ['KL', 'FF', 'FF ', talents['TAL_59'] if 'TAL_59' in talents else 0, 'talent']
        self.skills['wichsen'] = ['MU', 'IN', 'KK', 5000, 'talent']

        # Magic
        spells = h_data['spells']
        if len(spells) > 0:
            self.AE_max = 20 + self.leiteigenschaft[1]
            self.AE = self.AE_max
            print(f'{self.name} has {self.AE} of {self.AE_max} AE')
            if 'SPELL_367' in spells:
                self.skills['Schelmenkleister'] = ['KL', 'IN', 'GE', spells['SPELL_367'], 'magic', 8]
            #######################
            # ADD MORE MAGIC HERE #
            #######################
        else:
            print(f'{self.name} does not know any magic.')

        # Liturgies
        liturgies = h_data['liturgies']
        if len(liturgies) > 0:
            print('liturgies not implemented')
            ###########################
            # ADD MORE liturgies HERE #
            ###########################
        else:
            print(f'{self.name} does not know any liturgies.')

        if show_values:
            print('=======================')
            print(f"These are {self.name}'s talents:")
            print('=======================')
            print(self.skills)
        print('=======================')

        # Get everything that can be probed on
        self.possible_probes = list()
        self.possible_probes.append('take_hit')
        self.possible_probes.append('give_hit')
        self.possible_probes.append('sLP')
        self.possible_probes.append('sAE')
        self.possible_probes.append('cLP')
        self.possible_probes.append('cAE')

        # Talents
        for key in self.skills.keys():
            self.possible_probes.append(key)
        # Attributes
        for key in self.attr.keys():
            self.possible_probes.append(key)

    def set_LP(self, value):
        old = self.LP
        self.LP = value
        print(f'LP set to {self.LP}')
        self.logger.info(f'reg_event;set_LP;{self.name};{old};{self.LP}')

    def set_AE(self, value):
        old = self.AE
        self.AE = value
        print(f'AE set to {self.AE}')
        self.logger.info(f'reg_event;set_AE;{self.name};{old};{self.AE}')

    def change_AE(self, value):
        old = self.AE
        self.AE = min(self.AE + value, self.AE_max)
        print(f'AE has changed from {old} to {self.AE}')
        self.logger.info(f'reg_event;change_AE;{self.name};{old};{self.AE}')

    def change_LP(self, value):
        old = self.LP
        self.LP = min(self.LP + value, self.LP_max)
        print(f'LP has changed from {old} to {self.LP}')
        self.logger.info(f'reg_event;change_LP;{self.name};{old};{self.LP}')

    def perform_attr_probe(self, attr: str, mod: int = 0):
        print(f"The mighty {self.name} has incredible {self.attr[attr]} points in {attr}," +
              f"the modifier for this probe is {mod}")
        meist = False
        patz = False

        roll = randint(1, 20)
        res = self.attr[attr] - roll + mod
        print(f'The die shows a {roll}')

        if res >= 0 and roll != 20:
            print(f"{self.name} has passed")
            passed = True
            if roll == 1:
                print('Will it be meisterlich?')
                roll2 = randint(1, 20)
                res2 = self.attr[attr] - roll2 + mod
                if res >= 0:
                    print('Yes!')
                    meist = True
                else:
                    print('No :(')
        elif roll != 20:
            passed = False
            print(f"{self.name} has failed")
        elif roll == 20:
            print(f"{self.name} has failed, but will it be a complete disaster?")
            roll2 = randint(1, 20)
            res2 = self.attr[attr] - roll2 + mod
            if res <= 0:
                print("Yes....")
                patz = True
            else:
                print("No, thanks to the Twelve")
        else:
            print('This should never happen :(')

        self.logger.info(f'attr_probe;{self.name};{attr};{self.attr[attr]};{mod};{roll};{res};{passed};{meist};{patz}')

    def skill_probe(self, skill: str, mod: int = 0):
        """Method to perform a skill probe

        skill -- name of talent, magic, or liturgie to probe
        mod -- modifier on probe

        """

        # Booleans whether something critical occured
        patz = False
        mega_patz = False
        meister = False
        mega_meister = False

        points_left = self.skills[skill][3]  # Get number of skill points

        print('=======================')
        print(f'The mighty {self.name} has {points_left} skill points when he tries to {skill}.')
        if mod != 0:
            print(f'Probe modified by {mod}.')
            if mod > 0:
                str_mod = ' + ' + str(mod)
            elif mod < 0:
                str_mod = ' - ' + str(abs(mod))
        else:
            str_mod = ' +- ' + str(mod)

        rolls = [randint(1, 20), randint(1, 20), randint(1, 20)]
        print('Die rolls:')

        print(self.skills[skill][0] + ': ' + str(rolls[0]) + ' (' + str(self.attr[self.skills[skill][0]]) + str_mod + ')')
        print(self.skills[skill][1] + ': ' + str(rolls[1]) + ' (' + str(self.attr[self.skills[skill][1]]) + str_mod + ')')
        print(self.skills[skill][2] + ': ' + str(rolls[2]) + ' (' + str(self.attr[self.skills[skill][2]]) + str_mod + ')')

        if rolls.count(20) >= 2:
            patz = True
            if rolls.count(20) == 3:
                mega_patz = True
        if rolls.count(1) >= 2:
            meister = True
            if rolls.count(1) == 3:
                mega_meister = True

        res1 = self.attr[self.skills[skill][0]] - rolls[0] + mod
        res2 = self.attr[self.skills[skill][1]] - rolls[1] + mod
        res3 = self.attr[self.skills[skill][2]] - rolls[2] + mod

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
            print(f'{self.name} failed with {points_left}.')
            passed = False
        # Success messages
        elif not patz and not mega_patz and points_left >= 0:
            print(f'{self.name} passed with {points_left}.')
            passed = True
        elif meister and not mega_meister and points_left < 0:
            print(f'Though {self.name} should have failed with {points_left} our hero was struck by the Gods' +
                  'and passed meisterlich.')
            passed = True
        elif mega_meister and points_left < 0:
            print('Though ' + self.name + 'should have failed with ' + str(points_left) +
                  ', our hero was struck by the Gods and passed mega meisterlich.')
            passed = True

        # Extra messages for meisterlich and patzing
        if meister and not mega_meister:
            print('... and it was meisterlich!')
        elif mega_meister:
            print('... and it was mega meisterlich!')
        elif patz and not mega_patz:
            print(f'{self.name} is an idiot and patzed.')
        elif mega_patz:
            print(f'{self.name} is an gigantic idiot and mega patzed.')

        if self.skills[skill][4] == 'talent':
            self.logger.info(f'tal_probe;{self.name};{skill};{self.skills[skill]};{mod};{rolls};{res1};{res2};'
                             f'{res3};{points_left};{passed};{meister};{patz};{mega_meister};{mega_patz}')
        elif self.skills[skill][4] == 'magic':
            self.change_AE(-self.skills[skill][5])
            self.logger.info(f'mag_probe;{self.name};{skill};{self.skills[skill]};{mod};{rolls};{res1};{res2};'
                             f'{res3};{points_left};{passed};{meister};{patz};{mega_meister};{mega_patz}')

    def export(self, mode: str = "object"):
        """Method to export the hero either in JSON for Optolith or as an pickled object.
        The idea is that the history of Proben can be tracked and analysed so that the corresponding
        talents or attributes can be leveled ;-)
        """

    def take_a_hit(self):
        enemy = input(f'Aua! What has hit {self.name}? ')
        damage = int(input(f'How much damage did {enemy} inflict? '))
        self.change_LP(-damage)
        source = input(f'How did {enemy} hit {self.name}? ')
        source_class = input(f'What is the general class of {source}? ')
        print(f'OMG! {self.name} was hit by a {enemy} and suffered {damage} damge from this brutal attack with a '
              f'{source} ({source_class}).')
        self.logger.info(f'hit_taken;{self.name};{enemy};{damage};{source};{source_class}')

    def give_a_hit(self):
        enemy = input(f'SCHWUSSS! What did {self.name} hit? ')
        damage = int(input(f'How much damage did {self.name} inflict on {enemy}? '))
        source = input(f'How did {self.name} hit {enemy}? ')
        source_class = input(f'What is the general class of {source}? ')
        print(f'N1! A {enemy} was hit by a {self.name} and suffered {damage} damage from this brutal attack with a '
              f' {source} ({source_class}).')
        self.logger.info(f'hit_given;{self.name};{enemy};{damage};{source};{source_class}')

    def perform_action(self, user_action: str, modifier: int = 0) -> bool:
        # Quitting program
        if user_action == 'feddich':
            if len(group) == 1:
                print(f'{self.name} has left the building.')
            else:
                for h in names:
                    print(f'{h} has left the building.')
            return False
        # Perform probe
        else:
            if user_action in self.skills:
                self.skill_probe(user_action, modifier)
            elif user_action in self.attr:
                self.perform_attr_probe(user_action, modifier)
            elif user_action == 'take_hit':
                self.take_a_hit()
            elif user_action == 'give_hit':
                self.give_a_hit()
            elif user_action == 'sLP':
                self.set_LP(modifier)
            elif user_action == 'sAE':
                self.set_AE(modifier)
            elif user_action == 'cLP':
                self.change_LP(modifier)
            elif user_action == 'cAE':
                self.change_AE(modifier)
            else:
                raise ValueError('Keyword ' + user_action + " not found, enter 'feddich' to quit")
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
                    matches = get_close_matches(name, list(group.keys()) + ["feddich"], cutoff=.6)
                    if len(matches) == 1:
                        yes_no = input(f"Misspelled? Did you mean {matches[0]}? (y/n) ")
                        if yes_no == "y":
                            name = matches[0]
                            break
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
                    matches = get_close_matches(user_action, list(Digga.possible_probes) + ["feddich"], cutoff=.3)
                    if len(matches) == 1:
                        yes_no = input(f"Misspelled? Did you mean {matches[0]}? (y/n) ")
                        if yes_no == "y":
                            user_action = matches[0]
                            break
                    elif len(matches) > 1:
                        print(f"Probably you meant any of {matches}. Please try again.")
                    else:
                        warnings.warn(f"This action is not known! ({user_action})")
                        print("Misspelled? Try again ;-)")
                else:
                    break
            playing = Digga.perform_action(user_action, modifier)
        else:
            playing = False
    logger.info('Probemaker is feddich')


if __name__ == "__main__":
    logging.basicConfig(filename='probe.log',
                        # encoding='utf-8',
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S;', level=logging.DEBUG)
    logger = logging.getLogger("Basic Logger")
    logger.info('Probemaker started')

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
        Digga = Hero(hfiles[h], logger, show_values)
        names.append(Digga.name)
        group[Digga.name] = Digga
        logger.info(f'{Digga.name} loaded')

    run(group)

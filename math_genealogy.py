#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 21:28:50 2018

@author: benjaminlucas
"""

import json
from enum import Enum

root_directory = '/users/benjaminlucas/Documents/Math_Genealogy/'

class MathematicianGroup(Enum):
    fields_medalists = "fields_medalists"
    nobel_economists = "economists"

def main(root_directory, mathematician_class = MathematicianGroup.fields_medalists):
    math_dict = Load_Math_Data(root_directory)
    
    if(mathematician_class == MathematicianGroup.fields_medalists):
        fields_medalists = ['Lars Ahlfors', 'Jesse Douglas',
                            'Laurent Schwartz', 'Atle Selberg', 'Kunihiko Kodaira','Jean-Pierre Serre'
                            ,'Klaus Roth', u'René Thom',u'Lars Hörmander','John Milnor','Michael Atiyah'
                            ,'Paul Joseph Cohen','Alexander Grothendieck','Stephen Smale','Alan Baker'
                            ,'Heisuke Hironaka','John Griggs Thompson','Sergey Petrovich Novikov','Enrico Bombieri'
                            ,'David Mumford','Pierre Deligne','Charles Fefferman','Daniel Quillen'
                            ,'Gregory Aleksandrovic Margulis','Alain Connes','William Thurston','Shing-Tung Yau'
                            ,'Simon Donaldson','Gerd Faltings','Michael Freedman','Vladimir Drinfeld'
                            ,'Vaughan Jones','Shigefumi Mori','Edward Witten','Jean Bourgain'
                            ,'Pierre-Louis Lions','Jean-Christophe Yoccoz','Efim Zelmanov','Richard Borcherds'
                            ,'William Timothy Gowers','Maxim Kontsevich','Curtis McMullen','Laurent Lafforgue'
                            ,'Vladimir Voevodsky','Andrei Okounkov','Grigorii Yakovlevich Perelman','Terence Tao'
                            ,'Wendelin Werner','Elon Lindenstrauss',u'Bảo Châu Ngô','Stanislav Smirnov'
                            ,u'Cédric Villani','Artur Avila','Manjul Bhargava','Martin Hairer'
                            ,'Maryam Mirzakhani']
    else:
        # Nobel Econonmists
        fields_medalists =['Ragnar Frisch', 'Jan Tinbergen','Paul Samuelson',
                           'Simon Kuznets','John Hicks','Kenneth Arrow','Wassily Leontief',
                           'Friedrich Hayek','Leonid Kantorovich',
                           'Tjalling Koopmans','Milton Friedman',
                           'Herbert Alexander Simon','Theodore Schultz','Arthur Lewis','Lawrence Klein','James Tobin',
                           'George Stigler', u'Gérard Debreu','Richard Stone',
                           'Franco Modigliani','Robert Solow',
                           'Harry Markowitz','Merton Miller','Gary Becker',
                           'Robert Fogel', 'John Harsanyi',
                           'John Forbes Nash, Jr.','Reinhard Selten','Robert Emerson Lucas',
                           'James Mirrlees','William Vickrey','Robert Cox Merton',
                           'Amartya Sen','Robert Mundell',
                           'James Heckman','Daniel McFadden','George Akerlof','A. Michael (Andrew) Spence',
                           'Joseph Eugene Stiglitz','Vernon Lomax Smith', 'Robert Engle',
                           'Clive Granger','Finn Kydland','Edward Prescott','Robert Aumann',
                           'Thomas Schelling','Edmund Phelps','Leonid Hurwicz',
                           'Eric Maskin','Roger Myerson','Paul Krugman',
                           'Peter Diamond','Dale Mortensen','Christopher Pissarides',
                           'Thomas Sargent','Christopher Albert Sims','Alvin Elliot Roth','Lloyd Stowell Shapley',
                           'Eugene Francis Fama','Lars Peter Hansen','Jean Tirole']
            

    fields_medalist_entries = [FindMathematicianID(winner, math_dict) for winner in fields_medalists]
    
    
    # Find the fraction of medalists that share a lineage with historical figures
    liebniz_fraction = sum([ContainsPerson(u'Friedrich Leibniz', [entry], math_dict) for entry in fields_medalist_entries])/(1.0*len(fields_medalist_entries))
    print('The fraction on Fields Medalists whose lineage contains Liebniz: ' + str(round(liebniz_fraction,3)))
    euler_fraction = sum([ContainsPerson(u'Leonhard Euler', [entry], math_dict) for entry in fields_medalist_entries])/(1.0*len(fields_medalist_entries))
    print('The fraction on Fields Medalists whose lineage contains Euler: ' + str(round(euler_fraction,3)))
    gauss_fraction = sum([ContainsPerson(u'Carl Friedrich Gauß', [entry], math_dict) for entry in fields_medalist_entries])/(1.0*len(fields_medalist_entries))
    print('The fraction on Fields Medalists whose lineage contains Gauss: ' + str(round(gauss_fraction,3)))  
    copernicus_fraction = sum([ContainsPerson(u'Nicolaus (Mikołaj Kopernik) Copernicus', [entry], math_dict) for entry in fields_medalist_entries])/(1.0*len(fields_medalist_entries))
    print('The fraction on Fields Medalists whose lineage contains Copernicus: ' + str(round(copernicus_fraction,3)))
    
    # Find the oldest ancestor for a given medalist
    oldest_ancestor_list = [FindOldestAncestors([entry], math_dict)[0] for entry in fields_medalist_entries]
    entry_name = [entry['name'] for entry in fields_medalist_entries]
    medalist_ancestor_pairs = sorted(zip(entry_name, oldest_ancestor_list))
    
    unique_ancestors = list(set(oldest_ancestor_list))
    ancestor_count = [sum([x == a for x in oldest_ancestor_list]) for a in unique_ancestors]
    ancestor_count_pairs = zip(unique_ancestors, ancestor_count)
    ancestor_count_pairs = sorted(ancestor_count_pairs, key=lambda x: x[1], reverse = True)
    print('The fraction of Fields Medalist whose oldest ancestor is ' + ancestor_count_pairs[0][0] + ": " + str(round(1.0*ancestor_count_pairs[0][1]/(1.0*len(fields_medalists)),3)))
    
    # Find the set of all progenitors
    ancestor_list = [FindAllAncestors([entry], math_dict) for entry in fields_medalist_entries]
    pacioli_list = [entry['name'] for entry in fields_medalist_entries if 'Luca Pacioli' in FindAllAncestors([entry], math_dict)]
    ancestors_all = []
    for a in ancestor_list:
        ancestors_all.extend(a)
    unique_ancestor = list(set(ancestors_all))
    count = [sum([x == a for x in ancestors_all]) for a in unique_ancestor]
    ancestor_count_pairs= zip(unique_ancestor, count)
    ancestor_count_pairs = sorted(ancestor_count_pairs, key=lambda x: x[1], reverse = True)
    print('The fraction of Fields Medalist whose oldest ancestor is ' + ancestor_count_pairs[0][0] + ": " + str(round(1.0*ancestor_count_pairs[0][1]/(1.0*len(fields_medalists)),3)))




def Load_Math_Data(root_dir):
    filename = root_dir + '/data.json'
    with open(filename, 'r') as f:
        math_data = json.load(f)
    f.close()
    math_data = math_data['nodes']
    # make a dictionary to look up data
    math_dict = {}
    for m in math_data:
        math_dict[m['id']] = m
    return math_dict


def FindMathematicianID(name, math_dict):
    for m in math_dict.itervalues():
        try:
            full_name = m['name'].split(' ')
        except:
            full_name = ['','']
        if(name == m['name']):
            return m
            break
        elif((full_name[0] + ' ' + full_name[-1]) == name):
            return m
            break
    return False



def FindOldestAncestors(persons, math_dict):
    search_ids = [person['advisors'] for person in persons]
    if (len(filter(lambda x: x != [], search_ids)) == 0):
        return list(set([person['name'] for person in persons]))
    else:
        ancestors = []
        advisors = []
        for person in persons:
            if(person['advisors'] == []):
                ancestors.append(person)
            else:
                for ind in person['advisors']:
                    advisors.append(math_dict[ind])
        if(len(advisors) > 0):
            return FindOldestAncestors(advisors, math_dict)
        else:
            return FindOldestAncestors(ancestors, math_dict)

def FindAllAncestors(persons, math_dict):
    search_ids = [person['advisors'] for person in persons]
    if (len(filter(lambda x: x != [], search_ids)) == 0):
        return list(set([person['name'] for person in persons]))
    else:
        advisors = []
        for person in persons:
            if(person['advisors'] == []):
                advisors.append(person)
            else:
                for ind in person['advisors']:
                    advisors.append(math_dict[ind])
        return FindAllAncestors(advisors, math_dict)


def ContainsPerson(target_person, start_persons, math_dict):
    names = [x['name'] for x in start_persons]
    if(len(filter(lambda x: x == target_person, names)) > 0):
        return True
    search_ids = [person['advisors'] for person in start_persons]
    if (len(filter(lambda x: x != [], search_ids)) == 0):
        return False
    else:
        advisors = []
        for person in start_persons:
            if(person['advisors'] == []):
                advisors.append(person)
            else:
                for ind in person['advisors']:
                    advisors.append(math_dict[ind])
        return ContainsPerson(target_person, advisors, math_dict)

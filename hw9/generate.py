'''
Copyright (C) 2022 BUAA
Author: Hyggge, <czh20020503@buaa.edu.com>

You can use this program to generate test data, which can be used in homework9 of BUAA-OO
'''


import random
import sys
import names

instr_list = ['ap', 'ar', 'qv', 'qps', 'qci', 'qbs', 'ag', 'atg', 'dfg']
person_id_set = set()
group_id_set = set()
link_map = {}
group_map = {}


def get_unexist_id(id_set) :
    id = random.randint(-2147483648, 2147483647)
    while (id in id_set) :
        id = random.randint(-2147483648, 2147483647)
    return str(id)

def get_exist_id(id_set) :
    id = random.choice(list(id_set))
    return str(id)

def get_name() :
    name = names.get_first_name()
    while (len(name) > 10) :
        name = names.get_first_name()
    return name

def get_age() :
    age = random.randint(0, 200)
    return str(age)

def get_value() :
    value = random.randint(0, 1000)
    return str(value)

def get_instr() :
    instr = random.choice(instr_list)
    if (instr == 'ap') :
        return add_person(instr)
    elif (instr == 'ar') :
        return add_relation(instr)
    elif (instr == 'qv') :
        return query_value(instr)
    elif (instr == 'qps') :
        return instr
    elif (instr == 'qci') :
        return query_circle(instr)
    elif (instr == 'qbs') :
        return instr 
    elif (instr == 'ag') :
        return add_group(instr)
    elif (instr == 'atg') :
        return add_to_group(instr)
    elif (instr == 'dfg') :
        return del_from_group(instr)


def add_person(instr) :
    prob = random.uniform(0, 1)
    id = get_unexist_id(person_id_set)
    if (prob < 0.4) :
        if (person_id_set) :
            id = get_exist_id(person_id_set)
    else :
        id = get_unexist_id(person_id_set)
        person_id_set.add(id)
        link_map[id] = []
    return instr + " " + id + " " + get_name() + " " + get_age()

def add_relation(instr) :
    prob = random.uniform(0, 1)
    id1 = get_unexist_id(person_id_set)
    id2 = get_unexist_id(person_id_set)
    if (prob < 0.2) :
        id1 = get_unexist_id(person_id_set)
        id2 = str(random.randint(-2147483648, 2147483647))
    elif (prob < 0.4) :
        if (person_id_set) :
            id1 = get_exist_id(person_id_set)
        id2 = get_unexist_id(person_id_set)
    elif (prob < 0.6) :
        if (person_id_set) :
            id1 = get_exist_id(person_id_set)
            if (link_map[id1]) :
                id2 = random.choice(link_map[id1])
            else :
                id2 = id1
        
    else :
        if (person_id_set) :
            id1 = get_exist_id(person_id_set)
            id2 = get_exist_id(person_id_set)
            if (len(link_map[id1]) + 1 < len(person_id_set)) :
                while (id2 in link_map[id1]) :
                    id2 = get_exist_id(person_id_set)
                link_map[id1].append(id2)
                link_map[id2].append(id1)
    return instr + " " + id1 + " " + id2 + " " + get_value()

def query_value(instr) :
    prob = random.uniform(0, 1)
    id1 = get_unexist_id(person_id_set)
    id2 = get_unexist_id(person_id_set)
    if (prob < 0.2) :
        id1 = get_unexist_id(person_id_set)
        id2 = str(random.randint(-2147483648, 2147483647))
    elif (prob < 0.4) :
        if (person_id_set) :
            id1 = get_exist_id(person_id_set)
        id2 = get_unexist_id(person_id_set)
    elif (prob < 0.6) :
        if (person_id_set) :
            id1 = get_exist_id(person_id_set)
            id2 = get_exist_id(person_id_set)
            if (len(link_map[id1]) + 1 < len(person_id_set)) :
                while (id2 in link_map[id1]) :
                    id2 = get_exist_id(person_id_set)
    else :
        if (person_id_set) :
            id1 = get_exist_id(person_id_set)
            if (link_map[id1]) :
                id2 = random.choice(link_map[id1])
            else :
                id2 = id1 
    return instr + " " + id1 + " " + id2 

def query_circle(instr) :
    prob = random.uniform(0, 1)
    id1 = get_unexist_id(person_id_set)
    id2 = get_unexist_id(person_id_set)
    if (prob < 0.2) :
        id1 = get_unexist_id(person_id_set)
        id2 = str(random.randint(-2147483648, 2147483647))
    elif (prob < 0.4) :
        if (person_id_set) :
            id1 = get_exist_id(person_id_set)
        id2 = get_unexist_id(person_id_set)
    else :
        if (person_id_set) :
            id1 = get_exist_id(person_id_set)
            id2 = get_exist_id(person_id_set)
    return instr + " " + id1 + " " + id2 

def add_group(instr) :
    prob = random.uniform(0, 1)
    id = get_unexist_id(group_id_set)
    if (prob < 0.4) :
        if (group_id_set) :
            id = get_exist_id(group_id_set)
    else :
        id = get_unexist_id(group_id_set)
        group_id_set.add(id)
        group_map[id] = []
    return instr + " " + id 

def add_to_group(instr) :
    prob = random.uniform(0, 1)
    group_id = get_unexist_id(group_id_set)
    person_id = get_unexist_id(person_id_set)
    if (prob < 0.2) :
        group_id = get_unexist_id(group_id_set)
        person_id = str(random.randint(-2147483648, 2147483647))
    elif (prob < 0.4) :
        if (group_id_set):
            group_id = get_exist_id(group_id_set)
        person_id = get_unexist_id(person_id_set)
    elif (prob < 0.6) :
        for it in group_id_set:
            if (group_map[it]) :
                group_id = it
                person_id = random.choice(group_map[group_id])
                break    
    else :
        if (person_id_set and group_id_set) :
            group_id = get_exist_id(group_id_set)
            person_id = get_exist_id(person_id_set)
            if (len(group_map[group_id]) < len(person_id_set)) : 
                while (person_id in group_map[group_id]) :
                    person_id = get_exist_id(person_id_set)
                group_map[group_id].append(person_id)
    return instr + " " + person_id + " " + group_id

def del_from_group(instr) :
    prob = random.uniform(0, 1)
    group_id = get_unexist_id(group_id_set)
    person_id = get_unexist_id(person_id_set)
    if (prob < 0.2) :
        group_id = get_unexist_id(group_id_set)
        person_id = str(random.randint(-2147483648, 2147483647))
    elif (prob < 0.4) :
        if (group_id_set):
            group_id = get_exist_id(group_id_set)
        person_id = get_unexist_id(person_id_set)
    elif (prob < 0.6) :
        if (person_id_set and group_id_set) :
            group_id = get_exist_id(group_id_set)
            person_id = get_exist_id(person_id_set)
            if (len(group_map[group_id]) < len(person_id_set)) :
                while (person_id in group_map[group_id]) :
                    person_id = get_exist_id(person_id_set)
    else :
        for it in group_id_set:
            if (group_map[it]) :
                group_id = it
                person_id = random.choice(group_map[group_id])
                group_map[group_id].remove(person_id)
                break    

    return instr + " " + person_id + " " + group_id


if __name__ == '__main__':
    # f = open("data.txt", "w")
    # sys.stdout = f
    n = 100000
    for i in range(1) :
        for i in range(n) :
            instr = get_instr()
            print(instr)
            # print(person_id_set)
            # print(link_map)
            # print(group_id_set)
            # print(group_map)

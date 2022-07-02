'''
Copyright (C) 2022 BUAA FTT Company
Author: Hyggge, <czh20020503@buaa.edu.com>

You can use this program to generate test data, which can be used in Unit 6 of BUAA-OO.
Before run it, you should choose a operatatin mode based on your need. To change the mode, 
you need modify the values of "mode" . The introduction is shown below.
'''

from distutils.filelist import glob_to_re
import random
from xmlrpc.client import MAXINT


# defination of const value
MAX_FLOOR = 10 
MAX_TIME = 45
MAX_REQ_NUM = 50
MAX_E_NUM = 20
MAX_E_NUM_PER_BUILDING = 3
MAX_E_NUM_PER_FLOOR = 3


SINGLE = True
MULTIPLE = False


#sets of people and elevator  
p_id_set = set()
e_id_set = {1, 2, 3, 4, 5, 6}

#number of elevators per building or per floor
building_acess_map = {'A':1, 'B':1, 'C':1, 'D':1, 'E':1}
floor_acess_map = {i:0 for i in range(2, MAX_FLOOR + 1)}
floor_acess_map[1] = 1

# tags of building and floor
building_tags = ['A', 'B', 'C', 'D', 'E']
floor_tags = [i for i in range(1, MAX_FLOOR+1)]
speed_list = [0.2, 0.4, 0.6]
capacity_list = [4, 6, 8]

#initial data
time = 1.0
e_num = 5
req_num = 0

# choice of mode
mode = SINGLE
certain_building = [random.choice(building_tags), random.choice(building_tags)]
certain_floor = random.choice(floor_tags)

# 1：请求时间上密集
# 2：请求时间上稀疏
# 3；请求时间上疏密交替
TIME_GAP_MODE = 1

'''
Functions for get relative information 
'''
def get_p_id() :
    id = random.randint(1, MAXINT)
    while (id in p_id_set) :
        id = random.randint(1, MAXINT)
    p_id_set.add(id)
    return id

def get_e_id() :
    id = random.randint(1, MAXINT)
    while (id in e_id_set) :
        id = random.randint(1, MAXINT)
    e_id_set.add(id)
    return id

def get_time_gap() :
    chance = random.randint(0, MAXINT) % 100
    if TIME_GAP_MODE == 1:
        if chance < 15 or chance > 85:
            return random.uniform(0.0, 0.2)
        elif chance < 60 and chance > 40:
            return random.uniform(0.7, 1.5)
        else:
            return random.uniform(0.2, 0.7)
    elif TIME_GAP_MODE == 2:
        if chance < 10 or chance > 90:
            return random.uniform(0.2, 2.0)
        elif chance < 60 and chance > 40:
            return random.uniform(8.0, 15.0)
        else:
            return random.uniform(2.0, 8.0)
    else:
        if chance < 5 or chance > 95:
            return random.uniform(5.0, 12.0)
        elif chance < 60 and chance > 40:
            return random.uniform(0.0, 0.3)
        else:
            return random.uniform(0.3, 0.8)
    
def get_building(new_set = None) :
    if (new_set == None) :
        return random.choice(list(building_tags))
    return random.choice(list(new_set))

def get_floor(new_set = None) :
    if (new_set == None) :
        return random.choice(list(floor_tags))
    return random.choice(list(new_set))

def get_switch_info() :
    switch_info = random.randint(1, 31)
    sum = 0
    for i in range(5) :
        sum += ((switch_info >> i) & 1)

    while (sum < 2) :
        switch_info = random.randint(1, 31)
        sum = 0
        for i in range(5) :
            sum += ((switch_info >> i) & 1)
    
    return switch_info

def get_capacity() :
    return random.choice(capacity_list)

def get_speed() :
    return random.choice(speed_list)

'''
Functions for checking 
'''
def check_floor_can_add() :
    new_set = set()
    for it in floor_acess_map.keys() :
        if (floor_acess_map.get(it) < MAX_E_NUM_PER_FLOOR) :
            new_set.add(it)
    if (not new_set) :
        return False, None
    return True, new_set

def check_building_can_add() :
    new_set = set()
    for it in building_acess_map.keys() :
        if (building_acess_map.get(it) < MAX_E_NUM_PER_BUILDING) :
            new_set.add(it)
    if (not new_set) :
        return False, None
    return True, new_set


'''
Functions for generating person requests or elevator requests
'''

def gener_p() :
    global time, req_num
    time_gap = get_time_gap()

    if (mode == SINGLE) :
        from_building = random.choice(certain_building)
        to_building = random.choice(certain_building)
    else :
        from_building = get_building()
        to_building = get_building()
    
    time += time_gap
    if (time > MAX_TIME) : return 

    id = str(get_p_id())
    from_floor = str(get_floor())
    to_floor = str(get_floor())
    
    if (from_building == to_building) :
        while (to_floor == from_floor) :
            to_floor = str(get_floor())
    
    print('[' + str(format(time, '.1f')) + ']' + id + '-FROM-' + from_building + '-' + from_floor + '-TO-' + 
                        to_building + '-' + to_floor)
    req_num += 1
    


def gener_virtical_e() :
    global time, req_num
    check_res, new_set = check_building_can_add()
    if (not check_res) : return

    if (mode == SINGLE) : 
        building = random.choice(certain_building)
        if (building_acess_map[building] >= MAX_E_NUM_PER_BUILDING) : return 
    else:
        building = get_building(new_set)
    building_acess_map[building] += 1
    
    time += get_time_gap()
    if (time > MAX_TIME) : return 

    id = str(get_p_id())
    building = str(building)
    capacity = str(get_capacity())
    speed = str(get_speed())
    print('[' + str(format(time, '.1f')) + ']' +'ADD-building-' + id + '-' + building + '-' + capacity + '-' + speed)
    req_num += 1


def gener_lateral_e() :
    global time, req_num
    check_res, new_set = check_floor_can_add()
    if (not check_res) : return

    if (mode == SINGLE) :
        floor = certain_floor
        if (floor_acess_map[floor] >= MAX_E_NUM_PER_FLOOR) : return
    else :
        floor = get_floor(new_set)
    floor_acess_map[floor] += 1

    time += get_time_gap()
    if (time > MAX_TIME) : return 

    id = str(get_p_id())
    floor = str(floor)
    capacity = str(get_capacity())
    speed = str(get_speed())
    switch_info = str(get_switch_info())
    print('[' + str(format(time, '.1f')) + ']' +'ADD-floor-' + id + '-' + floor + '-' + capacity + '-' + speed + '-' + switch_info)
    req_num += 1


def gener_e() :
    if (random.randint(0, 1)) :
        gener_virtical_e()
    else :
        gener_lateral_e()
    


def generate(num) :
    global time, e_num, req_num
    time = 1.0

    while (req_num < num and time < MAX_TIME):
        choice = random.randint(0, 5)
        if (choice > 0 or choice == 0 and e_num >= MAX_E_NUM) :
            gener_p()
        else :
            gener_e()
            e_num += 1


if __name__ == '__main__':

    num = random.randint(20, MAX_REQ_NUM)
    # num = 10
    generate(num)




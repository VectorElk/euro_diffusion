from constants import MAX_SIZE, MAX_COUNTRIES, REPRESENTATIVE_COEF, STARTING_CAPITAL
from copy import deepcopy
from enum import Enum
from itertools import product

class CountryData(Enum): #used to navigate in 3d array
    X1 = "x1"
    Y1 = "y1"
    X2 = "x2"
    Y2 = "y2"

#input array of strings and current case number
#output dictionary, 0 for eof, -1 for error
def get_data(_input, case): 
    line_num = 0

    for i in range(case-1):
        try:
            line_num = line_num + int(_input[line_num]) + 1
        except (ValueError, EOFError):
            print("Input error - bad number of countries")
            return -1

    countries_count = _input[line_num]
    try:
        countries_count = int(countries_count)
    except ValueError:
        print("Input error - bad number of countries")
        return -1

    if countries_count == 0:
        return 0

    if countries_count < 0 or countries_count > MAX_COUNTRIES:
        print("Input error - bad number of countries")
        return -1

    countries_list = [dict() for country in range(countries_count)]
    for i in range(line_num+1, line_num+countries_count+1):
        curr_line = _input[i].split()
        curr_country = i - line_num - 1 #number of current parsed country
        countries_list[curr_country]["name"] = curr_line[0]

        if not check_input_validity(countries_list, curr_line, curr_country):
            print("Input error - bad data at country ", curr_country+1)
            return -1

    return countries_list


def check_input_validity(countries_list, curr_line, curr_country): #return False if input file is invalid in any way
    try:
        for output_index, input_index in zip(CountryData, range(1,5)):
            countries_list[curr_country][output_index] = int(curr_line[input_index])-1
        for i in CountryData:
            if  not (0 <= countries_list[curr_country][i] <= MAX_SIZE-1):
                return False
    except (ValueError, IndexError):
            return False
    if countries_list[curr_country][CountryData.Y2] < countries_list[curr_country][CountryData.Y1] \
                         or countries_list[curr_country][CountryData.X2] < countries_list[curr_country][CountryData.X1]:
        return False
    return True


def check_overlap(countries_list): #return True if any overlap
    if len(countries_list) == 1:
        return False
    for i in range(len(countries_list)-1):
        for j in range(i+1, len(countries_list)):
            if countries_list[i][CountryData.X1] <= countries_list[j][CountryData.X2] and \
                    countries_list[i][CountryData.X2] >= countries_list[j][CountryData.X1] and \
                    countries_list[i][CountryData.Y1] <= countries_list[j][CountryData.Y2] and \
                    countries_list[i][CountryData.Y2] >= countries_list[j][CountryData.Y1]:
                return True
    return False

 
def get_full_countries(_map, x_max, y_max, _count,): #returns vector of full countries
    country_status = [1 for k in range(_count)]
    for x,y,z in product(range(x_max), range(y_max), range(1, _count+1)):
        if _map[x][y][0] != 0 and _map[x][y][z] == 0:
            country_status[_map[x][y][0]-1] = 0
    return country_status


def main():
    case = 1
    _input = []
    _file_mode = True
    file_location = ""
    print("Choose preferd input method (file/console). F/c")
    value = input()
    if (value == "c" or value == "C"):
        _file_mode = False
        print("Please, input your data")
        while True:
            value = input()
            _input.append(value)
            if value == "0":
                break
    else:
        print("Please, enter relative file location")
        value = input()
        file_location = value
        try:
            _file = open(file_location,"r")
            with _file as f:
                _input = f.readlines()
            _file.close()
            _input = [x.strip() for x in _input]
        except IOError:
            print("File not found")
            return -1

    while(True):
        countries_list = 0
        #dictionary filled with data with keys
        #"name" - country name
        #CountryData.X1 - starting coor x
        #CountryData.Y1 - starting coor y
        #CountryData.X2 - finish coor x
        #CountryData.Y2 - finish coor y
        countries_list = get_data(_input, case)
        
        if (countries_list == 0):
            return 0
        if (countries_list == -1):
            print("Problem in case", case)
            return -1

        if check_overlap(countries_list):
            print("Countries overlap in case", case, "\nMay lead to unexpected results")

        countries_count = len(countries_list)

        x_max = 1
        y_max = 1
        #crop array size to maximum needed for time saving
        for i in range(countries_count):
            if countries_list[i][CountryData.X2] > x_max: 
                x_max = countries_list[i][CountryData.X2]
            if countries_list[i][CountryData.Y2] > y_max: 
                y_max = countries_list[i][CountryData.Y2]
        #3d array with spacial x and y, and z rezerved for currency "pockets"
        #0 for non-european, 1-25 each european country
        europe_map = [[[0 for k in range(countries_count+1)] \
                            for j in range(y_max+1)]\
                            for i in range(x_max+1)]
        #fill initial map
        #europe_map[x][y][0] - country index in dictionaries array
        #europe_map[x][y][europe_map[x][y][0]] - currency of this country
        for x, y, z in product(range(x_max+1), range(y_max+1), range(countries_count)):
            if x >= countries_list[z][CountryData.X1] \
                    and y >= countries_list[z][CountryData.Y1] \
                    and x <= countries_list[z][CountryData.X2] \
                    and y <= countries_list[z][CountryData.Y2]:
                europe_map[x][y][0] = z+1 
                europe_map[x][y][z+1] = STARTING_CAPITAL
        days_without_change = 0
        day = 0
        country_status = [0 for k in range(countries_count)]
        print("Case Number", case)
        while(sum(country_status) != countries_count):
            if days_without_change > 10000:
                print("Seemingly infinite loop, taking next case")
                break
            new_country_status = get_full_countries(europe_map, x_max+1, y_max+1, countries_count)
            if country_status != new_country_status:
                days_without_change = 0
                diff = list(x-y for x,y in zip(country_status,new_country_status))
                filled_list = []
                for i in range(countries_count):
                    if diff[i] != 0:
                        filled_list.append(countries_list[i]["name"])
                        filled_list.sort() #sort newly filled alphabetically
                for i in range(len(filled_list)):
                    print(filled_list[i], day)
            #regular copy by reference wouldn't work, using deepcopy()
            country_status = deepcopy(new_country_status)
            europe_map_copy = deepcopy(europe_map)
            for x, y, z in product(range(x_max+1), range(y_max+1), range(1, countries_count+1)):
                if(europe_map[x][y][0] != 0):
                    neighbor_counter = 0
                    #representative number of coins of country z in city xy
                    representative_count = int(europe_map_copy[x][y][z]*REPRESENTATIVE_COEF) 
                    if x != 0 and europe_map[x-1][y][0] != 0:
                        neighbor_counter += 1
                        europe_map[x-1][y][z] += representative_count
                    if x != x_max and europe_map[x+1][y][0] != 0:
                        neighbor_counter += 1
                        europe_map[x+1][y][z] += representative_count
                    if y != 0 and europe_map[x][y-1][0] != 0:
                        neighbor_counter += 1
                        europe_map[x][y-1][z] += representative_count
                    if y != y_max and europe_map[x][y+1][0] != 0:
                        neighbor_counter += 1
                        europe_map[x][y+1][z] += representative_count
                    europe_map[x][y][z] -= neighbor_counter*representative_count
            day += 1
            days_without_change += 1
        case += 1


main()

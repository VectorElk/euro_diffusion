import constants
from copy import deepcopy

#take array of strings and current case number
#return dictionary, 0 for eof, -1 for error
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

    if countries_count < 0 or countries_count > 25:
        print("Input error - bad number of countries")
        return -1

    countries_list = [dict() for country in range(countries_count)]
    for i in range(line_num+1, line_num+countries_count+1):
        curr_line = _input[i].split()
        try:
            curr_country = i - line_num - 1 #number of current parsed country
            countries_list[curr_country]["name"] = curr_line[0]
            countries_list[curr_country]["x1"] = int(curr_line[1])-1 
            countries_list[curr_country]["y1"] = int(curr_line[2])-1
            countries_list[curr_country]["x2"] = int(curr_line[3])-1
            countries_list[curr_country]["y2"] = int(curr_line[4])-1 
        except (ValueError, IndexError):
            print("Input error - bad data at country ", curr_country+1)
            return -1

        if not (0 <= countries_list[curr_country]["x1"] <= constants.MAX_SIZE-1) \
                or not (0 <= countries_list[curr_country]["x2"] <= constants.MAX_SIZE-1) \
                or not (0 <= countries_list[curr_country]["y1"] <= constants.MAX_SIZE-1) \
                or not (0 <= countries_list[curr_country]["x2"] <= constants.MAX_SIZE-1) \
                or countries_list[curr_country]["y2"] < countries_list[curr_country]["y1"] \
                or countries_list[curr_country]["x2"] < countries_list[curr_country]["x1"]:
            print("Input error - bad coordinates")
            return -1
    return countries_list


def check_overlap(countries_list): #return True if any overlap
    if len(countries_list) == 1:
        return False
    for i in range(len(countries_list)-1):
        for j in range(i+1, len(countries_list)):
            if countries_list[i]["x1"] <= countries_list[j]["x2"] and \
                    countries_list[i]["x2"] >= countries_list[j]["x1"] and \
                    countries_list[i]["y1"] <= countries_list[j]["y2"] and \
                    countries_list[i]["y2"] >= countries_list[j]["y1"]:
                return True
    return False

 
def check_fill(_map, x_max, y_max, _count,): #returns vector of full countries
    country_status = [1 for k in range(_count)]
    for x in range(x_max):
            for y in range(y_max):
                if _map[x][y][0] != 0:
                    for z in range(1, _count+1):
                        if _map[x][y][z] == 0:
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
        #"x1" - starting coor x
        #"y1" - starting coor y
        #"x2" - finish coor x
        #"y2" - finish coor y
        countries_list = get_data(_input, case)
        
        if (countries_list == 0):
            return 0
        if (countries_list == -1):
            print("Problem in case", case)
            return -1

        if check_overlap(countries_list):
            print("Countries overlap in case", case, "\nMay lead to unexpected results")

        countries_count = len(countries_list)

        x_max = 0 
        y_max = 0
        #crop array size to maximum needed for time saving
        for i in range(countries_count):
            if countries_list[i]["x2"] > x_max: 
                x_max = countries_list[i]["x2"]
            if countries_list[i]["y2"] > y_max: 
                y_max = countries_list[i]["y2"]
        #3d array with spacial x and y, and z rezerved for currency "pockets"
        #0 for non-european, 1-25 each european country
        europe_map = [[[0 for k in range(countries_count+1)] \
                            for j in range(y_max+1)]\
                            for i in range(x_max+1)]
        #fill initial map
        #europe_map[x][y][0] - country index in dictionaries array
        #europe_map[x][y][europe_map[x][y][0]] - currency of this country
        for x in range(x_max+1):
            for y in range(y_max+1):
                for z in range(countries_count):
                    if x >= countries_list[z]["x1"] \
                            and y >= countries_list[z]["y1"] \
                            and x <= countries_list[z]["x2"] \
                            and y <= countries_list[z]["y2"]:
                        europe_map[x][y][0] = z+1 
                        europe_map[x][y][z+1] = constants.STARTING_CAPITAL
        days_without_change = 0
        day = 0
        country_status = [0 for k in range(countries_count)]
        print("Case Number", case)
        while(sum(country_status) != countries_count):
            if days_without_change > 10000:
                print("Seemingly infinite loop, taking next case")
                break
            new_country_status = check_fill(europe_map, x_max+1, y_max+1, countries_count)
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
            for x in range(x_max+1):
                for y in range(y_max+1):
                    if(europe_map[x][y][0] != 0):
                        for z in range(1, countries_count+1):
                            neighbor_counter = 0
                            #representative number of coins of country z in city xy
                            representative_count = int(europe_map_copy[x][y][z]*constants.REPRESENTATIVE_COEF) 
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

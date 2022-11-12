import pandas as pd
import datetime
import re
import DataStructures as ds
import classroomMechanics as mech
import sys
import get_bmc_info as bmc


def parse_bmc_constraints(file_name):
    data_li = bmc.get_data_list_of_lists(file_name)
    room_sizes = bmc.get_room_sizes(data_li)
    rooms = []
    count = 1

    for room_name in room_sizes:
        new_room = mech.Room(room_name, count, room_sizes[room_name])
        rooms.append(new_room)
        count += 1
    
    mergeSort(rooms, 0)
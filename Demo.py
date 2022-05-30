import sc2reader
import os
import csv
import math

# playerName = ""
# playerName = input("Please enter the player's name:")

# 一些自定义functions
def remove_id(temp):
    name_id = str(temp)
    name = ""
    open = False
    for i in name_id:
        if (i == ' '):
            open = True
        elif (i == '[') and (open == True):
            break
        else:
            name += i
    return name

# 将地图分为四个区域
def location(x, y, height, width):
    size_x = math.ceil(width / 4)
    size_y = math.ceil(height / 4)
    if (x <= size_x and y <= size_y):
        return str("11")
    elif (size_x < x <= size_x * 2 and y <= size_y):
        return str("21")
    elif (size_x * 2 < x <= size_x * 3 and y <= size_y):
        return str("31")
    elif (size_x * 3 < x <= size_x * 4 and y <= size_y):
        return str("41")
    elif (x <= size_x and size_y < y <= size_y * 2):
        return str("12")
    elif (size_x < x <= size_x * 2 and size_y < y <= size_y * 2):
        return str("22")
    elif (size_x * 2 < x <= size_x * 3 and size_y < y <= size_y * 2):
        return str("32")
    elif (size_x * 3 < x <= size_x * 4 and size_y < y <= size_y * 2):
        return str("42")
    elif (x <= size_x and size_y * 2 < y <= size_y * 3):
        return str("13")
    elif (size_x < x <= size_x * 2 and size_y * 2 < y <= size_y * 3):
        return str("23")
    elif (size_x * 2 < x <= size_x * 3 and size_y * 2 < y <= size_y * 3):
        return str("33")
    elif (size_x * 3 < x <= size_x * 4 and size_y * 2 < y <= size_y * 3):
        return str("43")
    elif (x <= size_x and size_y * 3 < y <= size_y * 4):
        return str("14")
    elif (size_x < x <= size_x *2 and size_y * 3 < y <= size_y * 4):
        return str("24")
    elif (size_x * 2 < x <= size_x * 3 and size_y * 3 < y <= size_y * 4):
        return str("34")
    else:
        return str("44")

# 处理游戏时长，将其转换成秒
def seconds(time):
    times = str(time)
    times += '.'
    count = 0
    secs = 0
    temp = ""
    for i in range(len(times)):
        if(times[i] == '.'):
            count += 1
    for i in range(len(times)):
        temp += times[i]
        if (temp[-1] == '.'):
            temp = temp[:-1]
            count -= 1
            if(count == 2):
                secs += int(temp) * 3600
                temp = ""
            elif (count == 1):
                secs += int(temp) * 60
                temp = ""
            elif (count == 0):
                secs += int(temp)
                temp = ""
    return secs

# 处理游戏时长，将其转换成stage
# def stage(time, secs):
#     if (time <= int(secs / 3)):
#         return 1
#     elif (int(secs / 3) < time <= int(secs / 3 * 2)):
#         return 2
#     else:
#         return 3

# 处理游戏时长，将其转换成stage
def stage(time, secs):
    if (time <= 420):
        return 1
    elif (420 < time <= 900):
        return 2
    else:
        return 3

# 放入replay名字(56003:73829)
for pa in range(800, 801):
    path = 'D:/SC/HeroMarine/' + str(pa) + '.SC2Replay'
    deter = False
    while(deter == False):
        if os.path.exists(path):
            path = 'D:/SC/HeroMarine/' + str(pa) + '.SC2Replay'
            break
        else:
            pa += 1
            path = 'D:/SC/HeroMarine/' + str(pa) + '.SC2Replay'

    # 导入replay
    sc2reader.configure(debug=True)
    replay = None
    try:
        replay = sc2reader.load_replay(path, load_level=4)
        replay.load_map()
    except:
        print("Replay: ", pa)
        print(replay.player)
        continue

    # 一些比赛的信息。
    # print(replay.start_time)
    # print(replay.end_time)
    # print(replay.map_name)
    # print(replay.map.map_info.height)
    # print(replay.map.map_info.width)
    # print(replay.real_type)
    # print(replay.real_length)
    # print(replay.player)
    if str(replay.winner.players[0].name) == str(replay.player[1].name):
        print("The WINNER is: Player 1")
        print("The LOSER is: Player 2")
    else:
        print("The WINNER is: Player 2")
        print("The LOSER is: Player 1")
    # 提取到地图的长宽数值
    height = replay.map.map_info.height
    width = replay.map.map_info.width
    secs = seconds(replay.real_length)
    playerID = 0
    # DPGZest, Maru, PtitDrogo
    if (replay.player[1].name == "HeroMarine") or (replay.player[1].name == "Neeb") or (replay.player[1].name == "Elazer") or (replay.player[1].name == "HeRoMaRinE"):
        playerID = 0
    else:
        playerID = 1

    out_string = []
    list1 = []
    list2 = []
    Search = dict()
    for event in replay.events:
       #  将所有生成单位存入字典（死亡事件需要进行比较）
       if (((event.name == "UnitBornEvent") or (event.name == "UnitInitEvent"))):
           Search[event.unit_id] = event.control_pid

       #  除去地图加载生成的事件信息
       if (event.second > 0):
           # 将选中的部队存入一个列表（根据选中的部队进行“进攻”单位的判断）
           if (event.name == "SelectionEvent") and (event.player != None):
               # if (event.player.sid == 0) or (event.player.sid == 1):
               if (event.player.sid == playerID):
                   if len(event.new_units):
                       if event.player.sid == 0:
                           list1.clear()
                           for num in event.new_units:
                               list1.append(num)
                       elif event.player.sid == 1:
                           list2.clear()
                           for num in event.new_units:
                               list2.append(num)

           if event.name == "TargetUnitCommandEvent":
               if (event.ability_name == "UnloadTargetWarpPrism") or (event.ability_name == "UnloadTargetMedivac") or (event.ability_name == "UnloadTargetOverlord"):
                    if event.player.sid == playerID:
                       time = stage(event.second, secs)
                       area = location(event.x, event.y, height, width)
                       # string = "Player " + str(event.player.sid + 1) + " " + event.target.name + " is Unloading at area " + str(area) + " in stage " + str(time)
                       string = event.target.name + " is Unloading at area " + str(area) + " in stage " + str(time)
                       out_string.append(string)
                       # print(string)
               # 输出进攻事件（右键攻击也包括在内）
               # if (event.ability_name == "Attack") or (event.ability_name == "RightClick"):
               #     if (event.target.race != "None") and (event.target.race != "Neutral"):
               #         # 去除迷雾中的未知单位和去除相同阵营击杀
               #         if (event.player.sid != int(event.control_player_id)) and (event.target_unit_id != 0):
               #             if event.player.sid == 0:
               #                 #  每一个单位的进攻事件输出
               #                 for temp in list1:
               #                     time = stage(event.second, secs)
               #                     area = location(event.x, event.y, height, width)
               #                     string = "Player " + str(event.player.sid+1) + " " + remove_id(temp) + " is Attacking Player " + str(event.control_player_id) + " " + remove_id(event.target) + " at area " + str(area) + " in stage " + str(time)
               #                     # out_string.append(string)
               #                     # print(string)
               #             elif event.player.sid == 1:
               #                 for temp in list2:
               #                     time = stage(event.second, secs)
               #                     area = location(event.x, event.y, height, width)
               #                     string = "Player " + str(event.player.sid+1) + " " + remove_id(temp) + " is Attacking Player " + str(event.control_player_id) + " " + remove_id(event.target) + " at area " + str(area) + " in stage " + str(time)
               #                     # out_string.append(string)
               #                     # print(string)

            # 输出移动事件
           if (event.name == "TargetPointCommandEvent") and (event.player != None):
               if event.player.sid == playerID:
                   for temp in list1:
                       if temp.is_army == True:
                           time = stage(event.second, secs)
                           area = location(event.x, event.y, height, width)
                           # string = "Player " + str(event.player.sid+1) + " " + remove_id(temp) + " Moves to area " + str(area) + " in stage " + str(time)
                           string = remove_id(temp) + " Moves to area " + str(area) + " in stage " + str(time)
                           out_string.append(string)
                           # print(string)

               # 单选一方选手而comment掉
               # elif event.player.sid == 1:
               #     for temp in list2:
               #         if temp.is_army == True:
               #             time = stage(event.second, secs)
               #             area = location(event.x, event.y, height, width)
               #             string = "Player " + str(event.player.sid+1) + " " + remove_id(temp) + " Moves to area " + str(area) + " in stage " + str(time)
               #             out_string.append(string)
               #             print(string)

            # 输出创建建筑事件
           if (event.name == "UnitInitEvent"):
               if (event.unit.race != "None") and (event.unit.race != "Neutral") and (event.unit.is_building == True):
                   if event.control_pid == (playerID+1):
                       secs = seconds(replay.real_length)
                       area = location(event.x, event.y, height, width)
                       time = stage(event.second, secs)
                       # string = "Player " + str(event.control_pid) + " Build a " + remove_id(event.unit_type_name) + " at area " + str(area) + " in stage " + str(time)
                       string = "Build a " + remove_id(event.unit_type_name) + " at area " + str(area) + " in stage " + str(time)
                       out_string.append(string)
                       # print(string)

               if (event.unit.race != "None") and (event.unit.race != "Neutral") and (event.unit.is_army == True):
                   if event.control_pid == (playerID + 1):
                       secs = seconds(replay.real_length)
                       area = location(event.x, event.y, height, width)
                       time = stage(event.second, secs)
                       # string = "Player " + str(event.control_pid) + " Generate a " + remove_id(event.unit_type_name) + " at area " + str(area) + " in stage " + str(time)
                       string = "Generate a " + remove_id(event.unit_type_name) + " at area " + str(area) + " in stage " + str(time)
                       out_string.append(string)
                       # print(string)

           # 输出创建单位事件
           if (event.name == "UnitBornEvent"):
               if (event.unit.race != "None") and (event.unit.race != "Neutral") and (event.unit.is_army == True):
                   if event.control_pid == (playerID + 1):
                       secs = seconds(replay.real_length)
                       area = location(event.x, event.y, height, width)
                       time = stage(event.second, secs)
                       # string = "Player " + str(event.control_pid) + " Generate a " + remove_id(event.unit_type_name) + " at area " + str(area) + " in stage " + str(time)
                       string = "Generate a " + remove_id(event.unit_type_name) + " at area " + str(area) + " in stage " + str(time)
                       out_string.append(string)
                       # print(string)

           # 输出死亡事件
           if ((event.name == "UnitDiedEvent") and ((event.killing_player_id  == 1) or (event.killing_player_id  == 2))):
               if event.killing_player_id == 1:
                   for temp in list2:
                       if (temp == event.unit):
                           list2.remove(temp)

               elif event.killing_player_id == 2:
                   for temp in list1:
                       if (temp == event.unit):
                           list1.remove(temp)

               # 过滤掉中立单位
               if (event.unit.race != "Neutral") and (event.unit.race != "None") and (event.unit.owner != "None"):
                   if event.killing_player_id != Search[event.unit_id]:
                       if (event.unit.is_building == True):
                           if remove_id(event.killing_unit) != "None":
                               if event.killing_player_id == (playerID+1):
                                   secs = seconds(replay.real_length)
                                   area = location(event.x, event.y, height, width)
                                   time = stage(event.second, secs)
                                   # string = "Player " + str(event.killing_player_id) + " " + remove_id(event.killing_unit) + " Destroyed" + " Player 2 " + remove_id(event.unit) + " at area " + str(area) + " in stage " + str(time)
                                   string = remove_id(event.killing_unit) + " Destroyed" + remove_id(event.unit) + " at area " + str(area) + " in stage " + str(time)
                                   out_string.append(string)
                                   # print(string)

                               # elif (event.killing_player_id == 2):
                               #     secs = seconds(replay.real_length)
                               #     area = location(event.x, event.y, height, width)
                               #     time = stage(event.second, secs)
                               #     string = "Player " + str(event.killing_player_id) + " " + remove_id(event.killing_unit) + " Destroyed" + " Player 1 " + remove_id(event.unit) + " at area " + str(area) + " in stage " + str(time)
                               #     out_string.append(string)
                                   # print(string)

                       else:
                           if remove_id(event.killing_unit) != "None":
                               if event.killing_player_id == (playerID+1):
                                   secs = seconds(replay.real_length)
                                   area = location(event.x, event.y, height, width)
                                   time = stage(event.second, secs)
                                   # string = "Player " + str(event.killing_player_id) + " " + remove_id(event.killing_unit) + " Killed" + " Player 2 " + remove_id(event.unit) + " at area " + str(area) + " in stage " + str(time)
                                   string = remove_id(event.killing_unit) + " Killed" + remove_id(event.unit) + " at area " + str(area) + " in stage " + str(time)
                                   out_string.append(string)
                                   # print(string)

                               # elif (event.killing_player_id == 2):
                               #     secs = seconds(replay.real_length)
                               #     area = location(event.x, event.y, height, width)
                               #     time = stage(event.second, secs)
                               #     string = "Player " + str(event.killing_player_id) + " " + remove_id(event.killing_unit) + " Killed" + " Player 1 " + remove_id(event.unit) + " at area " + str(area) + " in stage " + str(time)
                               #     out_string.append(string)
                               #     # print(string)

    write = 'D:/SC/HeroMarinec/' + str(pa) + '.csv'
    f = open(write, 'w', encoding='utf-8')
    csv_write = csv.writer(f)
    for i in out_string:
        csv_write.writerow([i])

    # print(write)


import sc2reader
import os
import csv
import math

# 一些自定义functions
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
    elif (size_x < x <= size_x * 2 and size_y * 3 < y <= size_y * 4):
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
    elif (420 < time <= 960):
        return 2
    else:
        return 3

player_names = []
# 放入replay名字(56003:73829)
for pa in range(0, 226):
    path = 'D:/Final/Hellion/' + str(pa) + '.SC2Replay'
    deter = False
    while(deter == False):
        if os.path.exists(path):
            path = 'D:/Final/Hellion/' + str(pa) + '.SC2Replay'
            break
        else:
            pa += 1
            path = 'D:/Final/Hellion/' + str(pa) + '.SC2Replay'

    # 导入replay
    sc2reader.configure(debug=True)
    replay = None
    try:
        replay = sc2reader.load_replay(path, load_level=4)
        replay.load_map()
    except:
        print("Replay: ", pa)
        # print(replay.player)
        os.remove(path)
        continue

    print(replay.player[1].name, replay.player[2].name)
    # 一些比赛的信息。
    player_names.append(replay.player[1].name)
    player_names.append(replay.player[2].name)

    if str(replay.winner.players[0].name) == str(replay.player[1].name):
        print("The WINNER is: Player 1 " + str(replay.winner.players[0].play_race))
        print("The LOSER is: Player 2")
        print()
    else:
        print("The WINNER is: Player 2 " + str(replay.winner.players[0].play_race))
        print("The LOSER is: Player 1")
        print()

    # # 区分player的名字
    # if "Maru" in player_names[1]:
    #     player_id = 1
    # else:
    #     player_id = 2

    # # 区分胜利者的名字
    if replay.winner.players[0] == replay.player[1].name:
        player_id = 1
    else:
        player_id = 2

    # print(type(replay.player[1].name))
    # print(type(str(replay.winner.players[0])))
    # print(type(replay.winner.players[0].play_race))

    # 区分策略种族的名字
    # if (replay.player[1].name == str(replay.winner.players[0])) and (replay.winner.players[0].play_race == "Terran"):
    #     player_id = 1
    # elif (replay.player[2].name == str(replay.winner.players[0])) and (replay.winner.players[0].play_race != "Terran"):
    #     player_id = 1
    # else:
    #     player_id = 2

    # 提取到地图的长宽数值
    height = replay.map.map_info.height
    width = replay.map.map_info.width
    secs = seconds(replay.real_length)

    units_record = dict()
    building_record = dict()
    out_string = []
    out_string1 = []
    out_string2 = []
    Search = dict()
    for event in replay.events:
        #  将所有生成单位存入字典（死亡事件需要进行比较）
        if (((event.name == "UnitBornEvent") or (event.name == "UnitInitEvent"))):
           Search[event.unit_id] = event.control_pid

        #  除去地图加载生成的事件信息
        if (event.second > 0):
            # 输出创建建筑事件
            if (event.name == "UnitInitEvent"):
                if (event.unit.race != "None") and (event.unit.race != "Neutral") and (event.unit.is_building == True):
                    secs = seconds(replay.real_length)
                    area = location(event.x, event.y, height, width)
                    time = stage(event.second, secs)
                    string = "Player " + str(event.control_pid) + " Build a " + event.unit.name + " at area " + str(area) + " in stage " + str(time)

                    if event.control_pid == 1:
                        if player_id == 1:
                            out_string1.append(string)
                        else:
                            out_string2.append(string)
                        out_string.append(string)

                    elif event.control_pid == 2:
                        if player_id == 2:
                            out_string1.append(string)
                        else:
                            out_string2.append(string)
                        out_string.append(string)

                    building_record[event.unit.id] = event.unit.name
                    # print(string)

                if (event.unit.race != "None") and (event.unit.race != "Neutral") and (event.unit.is_army == True):
                    secs = seconds(replay.real_length)
                    area = location(event.x, event.y, height, width)
                    time = stage(event.second, secs)
                    string = "Player " + str(event.control_pid) + " Generate a " + event.unit.name + " at area " + str(area) + " in stage " + str(time)

                    if event.control_pid == 1:
                        if player_id == 1:
                            out_string1.append(string)
                        else:
                            out_string2.append(string)
                        out_string.append(string)

                    elif event.control_pid == 2:
                        if player_id == 2:
                            out_string1.append(string)
                        else:
                            out_string2.append(string)
                        out_string.append(string)

                    units_record[event.unit.id] = event.unit.name
                    # print(string)

           # 输出创建单位事件
            if (event.name == "UnitBornEvent"):
                if (event.unit.race != "None") and (event.unit.race != "Neutral") and (event.unit.is_army == True):
                    # if event.control_pid == (playerID + 1):
                    secs = seconds(replay.real_length)
                    area = location(event.x, event.y, height, width)
                    time = stage(event.second, secs)
                    string = "Player " + str(event.control_pid) + " Generate a " + event.unit.name + " at area " + str(area) + " in stage " + str(time)
                    if event.control_pid == 1:
                        if player_id == 1:
                            out_string1.append(string)
                        else:
                            out_string2.append(string)
                        out_string.append(string)

                    elif event.control_pid == 2:
                        if player_id == 2:
                            out_string1.append(string)
                        else:
                            out_string2.append(string)
                        out_string.append(string)

                    units_record[event.unit.id] = event.unit.name
                    # print(string)

           # 输出死亡事件
            if (event.name == "UnitDiedEvent") and ((event.killing_player_id  == 1) or (event.killing_player_id == 2)) and (hasattr(event.unit, 'killed_by') == True):
                # 过滤掉中立单位
                if (event.unit.race != "Neutral") and (event.unit.race != "None") and (event.unit.owner != "None") and (event.unit.killed_by != 'None'):
                    if event.killing_player_id != Search[event.unit_id]:
                        if hasattr(event.killing_unit, 'name') == True:
                            if event.unit.is_building == True:
                                secs = seconds(replay.real_length)
                                area = location(event.x, event.y, height, width)
                                time = stage(event.second, secs)

                                if event.killing_player_id == 1:
                                    string = "Player " + str(event.killing_player_id) + " " + event.killing_unit.name + " Destroyed" + " Player 2 " + event.unit.name + " at area " + str(area) + " in stage " + str(time)
                                    if player_id == 1:
                                        out_string1.append(string)
                                    else:
                                        out_string2.append(string)
                                    out_string.append(string)

                                elif event.killing_player_id == 2:
                                    string = "Player " + str(event.killing_player_id) + " " + event.killing_unit.name + " Destroyed" + " Player 1 " + event.unit.name + " at area " + str(area) + " in stage " + str(time)
                                    if player_id == 2:
                                        out_string1.append(string)
                                    else:
                                        out_string2.append(string)
                                    out_string.append(string)

                                if building_record.__contains__(event.unit.id) == True:
                                    del building_record[event.unit.id]
                                # out_string.append(string)
                                # print(string)

                            elif event.unit.is_army == True:
                                secs = seconds(replay.real_length)
                                area = location(event.x, event.y, height, width)
                                time = stage(event.second, secs)

                                if event.killing_player_id == 1:
                                    string = "Player " + str(event.killing_player_id) + " " + event.killing_unit.name + " Killed" + " Player 2 " + event.unit.name + " at area " + str(area) + " in stage " + str(time)
                                    if player_id == 1:
                                        out_string1.append(string)
                                    else:
                                        out_string2.append(string)
                                    out_string.append(string)

                                elif event.killing_player_id == 2:
                                    string = "Player " + str(event.killing_player_id) + " " + event.killing_unit.name + " Killed" + " Player 1 " + event.unit.name + " at area " + str(area) + " in stage " + str(time)
                                    if player_id == 2:
                                        out_string1.append(string)
                                    else:
                                        out_string2.append(string)
                                    out_string.append(string)

                                if units_record.__contains__(event.unit.id) == True:
                                    del units_record[event.unit.id]
                                # out_string.append(string)
                                # print(string)
    # print()
    # print("Building list:")
    # print(building_record)
    # print()
    # print("Units list:")
    # print(units_record)

    # 所有过滤后的事件被写入csv文件(random & concept)
    # if replay.player[1].name == 'Serral' or (replay.player[1].name == 'Serral'):
    #     write1 = 'D:/SC2/Serral_Gate/' + str(pa) + str(replay.player[1].name) + '.csv'
    # else:
    #     write1 = 'D:/SC2/Serral_Gate/' + str(pa) + '.csv'
    # write1 = 'D:/SC2/Win/' + str(pa) + 'Win.csv'
    # f1 = open(write1, 'w', encoding='utf-8')
    # csv_write = csv.writer(f1)
    # for i in out_string1:
    #     csv_write.writerow([i])
    # print(write1)
    #
    #
    # if (replay.player[2].name == 'Serral') or (replay.player[2].name == 'Serral'):
    #     write2 = 'D:/SC2/Serral_Gate/' + str(pa) + str(replay.player[2].name) + '.csv'
    # else:
    #     write2 = 'D:/SC2/Serral_Gate/' + str(pa) + '.csv'
    # write2 = 'D:/SC2/Lose/' + str(pa) + 'Lose.csv'
    # f2 = open(write2, 'w', encoding='utf-8')
    # csv_write = csv.writer(f2)
    # for i in out_string2:
    #     csv_write.writerow([i])
    # print(write2)

    # if str(replay.winner.players[0].name) == str(replay.player[1].name):
    #     # dirswin = 'D:/SC2/Win/' + str(replay.player[1].name)
    #     # if not os.path.exists(dirswin):
    #     #     os.makedirs(dirswin)
    #     # write1 = dirswin + str(pa) + str(replay.player[1].name) + 'Win.csv'
    #     write1 = 'D:/SC2/Win/' + str(pa) + str(replay.player[1].name) + 'Win.csv'
    #     # dirslose = 'D:/SC2/Lose/' + str(replay.player[2].name)
    #     # if not os.path.exists(dirslose):
    #     #     os.makedirs(dirslose)
    #     # write2 = dirslose + str(pa) + str(replay.player[2].name) + 'Lose.csv'
    #     write2 = 'D:/SC2/Lose/' + str(pa) + str(replay.player[2].name) + 'Lose.csv'
    #
    # else:
    #     write1 = 'D:/SC2/Win/' + str(pa) + str(replay.player[2].name) + 'Win.csv'
    #     write2 = 'D:/SC2/Lose/' + str(pa) + str(replay.player[1].name) + 'Lose.csv'

    write1 = 'D:/Final/Hellion/Win/' + str(pa) + '.csv'
    f1 = open(write1, 'w', encoding='utf-8')
    csv_write = csv.writer(f1)
    for i in out_string1:
        csv_write.writerow([i])
    print(write1)
    # if player_id == 1:
    #     for i in out_string1:
    #         csv_write.writerow([i])
    #     print(write1)
    # else:
    #     for i in out_string2:
    #         csv_write.writerow([i])
    #     print(write1)



    write2 = 'D:/Final/Hellion/Lose/' + str(pa) + '.csv'
    f2 = open(write2, 'w', encoding='utf-8')
    csv_write = csv.writer(f2)
    for i in out_string2:
        csv_write.writerow([i])
    print(write2)




    # 所有过滤后的事件被写入csv文件(target)
    # write = 'D:/SC2/Strategycsv/' + str(pa) + '.csv'
    # f = open(write, 'w', encoding='utf-8')
    # csv_write = csv.writer(f)
    # for i in out_string:
    #     csv_write.writerow([i])
    # print(write)




# print()
# print("Players names")
# print(player_names)
# print()
# print("Players names (without repeated names)")
# print(set(player_names))
# print()


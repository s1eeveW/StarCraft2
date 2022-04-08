import sc2reader
import os
import csv

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

def location(x, y, height, width):
    size = max(width, height)
    size4 = size / 2
    if (x < size4 and y < size4):
        return int(1)
    elif (x < size4 and y > size4):
        return int(2)
    elif (x > size4 and y < size4):
        return int(3)
    else:
        return int(4)

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
def stage(time, secs):
    if (time <= int(secs / 3)):
        return 1
    elif (int(secs / 3) < time <= int(secs / 3 * 2)):
        return 2
    else:
        return 3

# 特定识别矿场信息
def Lab(unit):
    temp = str(unit)
    if (temp[0] == 'L' and temp[3] == 'M' and temp[10] == 'F'):
        return True
    elif (temp[0] == 'M' and temp[7] == 'F'):
        return True
    else:
        return False

# 特定识别中立生物信息
def Clean(unit):
    temp = str(unit)
    if (temp[0] == 'C' and temp[8] == 'B'):
        return True
    else:
        return False




# 放入replay名字
for pa in range(72678, 73830):
    path = 'D:/SC2/SC/' + str(pa) + '.SC2Replay'
    deter = False
    while(deter == False):
        if os.path.exists(path):
            path = 'D:/SC2/SC/' + str(pa) + '.SC2Replay'
            break
        else:
            pa += 1
            path = 'D:/SC2/SC/' + str(pa) + '.SC2Replay'

    # 导入replay
    sc2reader.configure(debug=True)
    replay = sc2reader.load_replay(path, load_level=4)
    replay.load_map()

    # 一些比赛的信息。
    # print(replay.start_time)
    # print(replay.end_time)
    # print(replay.map_name)
    # print(replay.map.map_info.height)
    # print(replay.map.map_info.width)
    # print(replay.real_type)
    # print(replay.real_length)

    # 提取到地图的长宽数值
    height = replay.map.map_info.height
    width = replay.map.map_info.width
    secs = seconds(replay.real_length)

    out_string = []
    list = []
    Search = dict()
    for event in replay.events:
       #  将所有生成单位存入字典（死亡事件需要进行比较）
       if (((event.name == "UnitBornEvent") or (event.name == "UnitInitEvent"))):
           Search[event.unit_id] = event.control_pid

       #  除去地图加载生成的事件信息
       if (event.second > 0):
           # 将选中的部队存入一个列表（根据选中的部队进行“进攻”单位的判断）
           if((event.name == "SelectionEvent") and ((event.pid == 1) or (event.pid == 2))):
               if(len(event.new_units)):
                   list = []
                   for num in event.new_units:
                       list.append(num)


           if ((event.name == "TargetUnitCommandEvent") and ((event.pid == 1) or (event.pid == 2))):
               # 输出进攻事件（右键攻击也包括在内）
               if ((event.ability_name == "Attack") or (event.ability_name == "RightClick")):
                   if ((event.control_player_id > 0) and (int(event.pid) != int(event.control_player_id)) and (event.target_unit_id != 0)):
                       #  每一个单位的进攻事件输出
                       for temp in list:
                           time = stage(event.second, secs)
                           area = location(event.x, event.y, height, width)
                           string = "Player " + str(event.pid) + " " + remove_id(temp) + " is Attacking Player " + str(event.control_player_id) + " " + remove_id(event.target) + " at area " + str(area) + " in stage " + str(time)
                           out_string.append(string)
                           print(string)

                # 输出移动事件
               if (event.ability_name == "RightClick"):
                   for temp in list:
                       if (Lab(temp) == False):
                           time = stage(event.second, secs)
                           area = location(event.x, event.y, height, width)
                           string = "Player " + str(event.pid) + " " + remove_id(temp) + " Move at area " + str(area) + " in stage " + str(time)
                           out_string.append(string)
                           print(string)

            # 输出创建建筑事件
           if (event.name == "UnitInitEvent"):
               secs = seconds(replay.real_length)
               area = location(event.x, event.y, height, width)
               time = stage(event.second, secs)
               string = "Player " + str(event.control_pid) + " Build a " + remove_id(event.unit_type_name) + " at area " + str(area) + " in stage " + str(time)
               out_string.append(string)
               print(string)

           # 输出死亡事件
           if ((event.name == "UnitDiedEvent") and ((event.killing_player_id  == 1) or (event.killing_player_id  == 2))):
               for temp in list:
                   if (temp == event.unit):
                       list.remove(temp)
               if (Lab(event.unit)):
                   secs = seconds(replay.real_length)
                   area = location(event.x, event.y, height, width)
                   time = stage(event.second, secs)
                   string = str(event.unit) + remove_id(event.unit_id_index) + " is depleted by Player " + str(event.killing_player_id) + " at area " + str(area) + " in stage " + str(time)
                   print(string)

               # 处理中立生物
               elif (Clean(event.unit)):
                   secs = seconds(replay.real_length)
                   area = location(event.x, event.y, height, width)
                   time = stage(event.second, secs)
                   string = remove_id(event.unit) + " is Killed by Player " + str(event.killing_player_id) + str(event.killing_unit) + " at area " + str(area) + " in stage " + str(time)
                   print(string)

               # 输出玩家单位死亡事件
               else:
                   if(event.killing_player_id != Search[event.unit_id]):
                       if (event.killing_player_id == 1):
                           secs = seconds(replay.real_length)
                           area = location(event.x, event.y, height, width)
                           time = stage(event.second, secs)
                           string = "Player " + str(event.killing_player_id) + " " + remove_id(event.killing_unit) + " Killed" + " Player 2 " + remove_id(event.unit) + " at area " + str(area) + " in stage " + str(time)
                           out_string.append(string)
                           print(string)

                       elif (event.killing_player_id == 2):
                           secs = seconds(replay.real_length)
                           area = location(event.x, event.y, height, width)
                           time = stage(event.second, secs)
                           string = "Player " + str(event.killing_player_id) + " " + remove_id(event.killing_unit) + " Killed" + " Player 1 " + remove_id(event.unit) + " at area " + str(area) + " in stage " + str(time)
                           out_string.append(string)
                           print(string)

    write = 'D:/SC2/SCIII/' + str(pa) + '.csv'
    f = open(write, 'w', encoding='utf-8')
    csv_write = csv.writer(f)
    for i in out_string:
        csv_write.writerow([i])

    print(write)


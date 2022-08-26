import requests
import re
import json
import os
from random import randint

url = 'https://jwxt.sias.edu.cn/eams/courseTableForStd!courseTable.action'
cookie = {
    'cookie': ''
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.0.0 Safari/537.36 '
}
data = {
    'ignoreHead': '1',
    'setting.kind': 'std',
    'startWeek': '',
    'project.id': '1',
    'semester.id': '123',
    'ids': '167851'
}

classList = list()
class_box = list()
response = requests.post(url, cookies=cookie, data=data, headers=headers).text
result = re.findall('activity = (.+)', response)
a = 0
for i in range(len(result)):
    # print("Data %d" % i)
    str_result = str(result[i])
    str_result = str_result.strip('new TaskActivity(null,null,')
    str_result = str_result.strip(',null,"",assistantName,"","");')
    list_result = str_result.split('"')
    del list_result[1]
    del list_result[2]
    del list_result[3]
    del list_result[4]
    del list_result[5]
    del list_result[6]
    del list_result[7]
    find_file = list_result[3]
    # print(find_file)
    classID = re.findall('[0-9]+\((.+)\)', find_file)
    # print(classID[0])
    find_teacher = re.findall('{}</a>\n</td><td>([\u4e00-\u9fa5]+)</td>'.format(classID[0]), response)
    # print(find_teacher)
    list_result.append(find_teacher[0])
    class_box.append(list_result)
    # print(list_result)
# print(class_box)
# print(len(class_box))
for y in range(len(class_box)):
    # print(class_box[y])
    box_list = class_box[y]
    class_name = box_list[2]
    class_data = box_list[0]
    class_start = float(str(re.findall('([0-9]*)-', class_data)[0]))
    class_end = float(str(re.findall('-([0-9]*)', class_data)[0]))
    # print(box_list[7])
    weekday = float(box_list[1])
    class_room = box_list[6]
    classID = str(re.findall('[0-9]+\((.+)\)', box_list[3])[0])
    class_teacher = box_list[-1]
    list_code = []
    for m in range(len(box_list[7])):
        list_code.append(box_list[7][m])
    # print(list_code)
    week_code = []
    for x in range(len(box_list[7])):
        # print(x)
        if list_code[x] == '1':
            week_code.append(x)
    # print(week_code)
    if len(week_code) == (int(week_code[-1]) - int(week_code[0])) + 1:
        week_status = 0.0
        # print(week_status)
    else:
        if int(week_code[0]) % 2 == 1:
            week_status = 1.0
        else:
            week_status = 2.0
    start_week = float(int(week_code[0]))
    end_week = float(int(week_code[-1]))
    classList.append(dict())
    classList[a].setdefault("ClassName", class_name)
    classList[a].setdefault("StartWeek", start_week)
    classList[a].setdefault("EndWeek", end_week)
    classList[a].setdefault("WeekStatus", week_status)
    classList[a].setdefault("Weekday", weekday)
    classList[a].setdefault("ClassStartTimeId", class_start)
    classList[a].setdefault("ClassEndTimeId", class_end)
    classList[a].setdefault("Classroom", class_room)
    classList[a].setdefault("ClassSerial", classID)
    classList[a].setdefault("Teacher", class_teacher)
    a = a + 1
    # print("第%d条："%a+box_list[7]+"  "+box_list[2]+box_list[1])


def write_data(self):
    if os.path.exists("conf_classInfo.json"):
        print("已存在 JSON 文件，使用随机文件名，请手动修改！")
        filename = "conf_classInfo_" + str(randint(100, 999)) + ".json"
    else:
        filename = "conf_classInfo.json"
    with open(filename, 'w', encoding='UTF-8') as json_file:
        json_str = json.dumps(self, ensure_ascii=False, indent=4)
        json_file.write(json_str)
        json_file.close()


write_data(classList)

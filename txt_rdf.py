path = '/home/cys/Desktop/tutor_info.txt'
teacher_name = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#teacher_name> \"%s\" ."
major_course = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#major_course> <http://www.kbpa.com/%s> ."
course_name = "<http://www.kbpa.com/%s> <http://www.kbqa.com/properties#course_name> \"%s\" ."
tutor_type = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#teacher_type> <http://www.kbpa.com/%s> ."
type_name = "<http://www.kbpa.com/%s> <http://www.kbqa.com/properties#type_name> \"%s\" ."
position = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#position> <http://www.kbpa.com/%s> ."
position_name = "<http://www.kbpa.com/%s> <http://www.kbqa.com/properties#position_name> \"%s\" ."
department = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#department> <http://www.kbpa.com/%s> ."
department_name = "<http://www.kbpa.com/%s> <http://www.kbqa.com/properties#department_name> \"%s\" ."
de_cla = "<http://www.kbpa.com/%s> <http://www.kbqa.com/properties#establish> <http://www.kbpa.com/%s> ."
info = {}
with open(path,'r+') as f:
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split(' ')
        info[line[0]] = {}
with open(path, 'r+') as f:
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split(' ')

        if line[1] == '职称':
            if '\n' in line[2]: line[2] = line[2].replace('\n', '')
            info[line[0]]['职称'] = line[2]
        if line[1] == '所在系别':
            if '\n' in line[2]: line[2] = line[2].replace('\n', '')
            info[line[0]]['所在系别'] = line[2]
        if line[1] == '主讲课程':
            if '\n' in line[2]: line[2] = line[2].replace('\n', '')
            if '、'  in line[2] :
                line[2] = line[2].split('、')
            elif '，' in line[2]:
                line[2] = line[2].split('，')

            info[line[0]]['主讲课程'] = line[2]
        if line[1] == '导师类型':
            if '\n' in line[2]: line[2] = line[2].replace('\n', '')
            info[line[0]]['导师类型'] = line[2]

with open('tutor_info.nt', 'a+') as f1:
    for i, name in enumerate(info.keys()):
        # print(i+1 ,name)
        print(teacher_name % (i+1, name), file=f1)
        if isinstance(info[name]['主讲课程'], list):
            print('list')
            for cla in info[name]['主讲课程']:
                print(major_course % (i + 1, cla), file=f1)
                print(course_name % (cla, cla), file=f1)
                print(de_cla % (info[name]['所在系别'], cla), file=f1)
        else:
            print(major_course % (i+1, info[name]['主讲课程']), file=f1)
            print(course_name % (info[name]['主讲课程'], info[name]['主讲课程']), file=f1)
            print(de_cla % (info[name]['所在系别'], info[name]['主讲课程']), file=f1)
        if '博' in info[name]['导师类型']:
            print(tutor_type % (i + 1, '硕士生导师'), file=f1)
        print(tutor_type % (i+1, info[name]['导师类型']), file=f1)
        print(type_name % (info[name]['导师类型'], info[name]['导师类型']), file=f1)
        print(position % (i+1, info[name]['职称']), file=f1)
        print(position_name % (info[name]['职称'], info[name]['职称']), file=f1)
        print(department % (i+1, info[name]['所在系别']), file=f1)
        print(department_name % (info[name]['所在系别'], info[name]['所在系别']), file=f1)


        # print(de_cla % (info[name]['所在系别'], info[name]['主讲课程']), file=f1)

with open('../untitled1/dict.txt', 'a+') as f:
    for k in info.keys():
        print("%s nr" % k, file=f)
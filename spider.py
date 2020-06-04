# author:cys
'''
Spider for TJU supervisor(info _ Tutor)
URL:http://cic.tju.edu.cn/jyjx/yjsjy/yjsdsml.htm
Return the txt .(It contains the info of TJU tutor. The txt format in follow)
'''
import requests
import re
from bs4 import BeautifulSoup
def getResponse(url):
    '''
    :param url:
    :return:  tutor_info data (Type of it is dict)
    '''
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        raise requests.HTTPError

def getPersonHref(resp):
    '''
    :param resp:
    :return: tutor_name + href
    '''
    tutor_href = set([])
    soup = BeautifulSoup(resp, 'html.parser')
    for i in soup.find_all('td'):
        # print(i.a, i.string)
        if i.a and i.string:
            tutor_href.add(i.a.get('href'))
    return tutor_href
    pass

def parserHtml(url_list, path):
    '''
    :param url_list:
    :return:tutor + operation + something (txt)
    '''

    num = 0

    teacher_name = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#teacher_name> \"%s\" ."

    major_course = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#major_course> <http://www.kbpa.com/%s> ."
    course_name = "<http://www.kbpa.com/%s> <http://www.kbqa.com/properties#course_name> \"%s\" ."

    tutor_type = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#teacher_type> <http://www.kbpa.com/%s> ."
    type_name = "<http://www.kbpa.com/%s> <http://www.kbqa.com/properties#type_name> \"%s\" ."

    position = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#position> <http://www.kbpa.com/%s> ."
    position_name = "<http://www.kbpa.com/%s> <http://www.kbqa.com/properties#position_name> \"%s\" ."

    department = "<http://www.kbqa.com/teacher_%02d> <http://www.kbqa.com/properties#department> <http://www.kbpa.com/%s> ."
    department_name = "<http://www.kbpa.com/%s> <http://www.kbqa.com/properties#department_name> \"%s\" ."
    info = {}

    for i, link in enumerate(url_list):
        try:
            link_html = getResponse(link)
            # Type-1
            name_pat_1 = re.compile("<strong>姓名</strong>：(.*)<br><strong>职称")
            w_s_p_1 = re.compile("职称</strong>：(.*)<br><strong>所在系别")
            sub_p_1 = re.compile("<strong>所在系别</strong>：(.*)<br><strong>主讲课程")
            cla_p_1 = re.compile("主讲课程</strong>:(.*)<br><strong>导师类型")
            type_p_1 = re.compile("导师类型</strong>：(.*)<br><strong>电子邮件")
            email_p_1 = re.compile("电子邮件</strong>：<a href=(.*)>(.*)</a> <br><strong>研究领域")
            location_p_1 = re.compile("研究领域</strong>：(.*)<br><strong>研究方向")
            aim_p_1 = re.compile("研究方向</strong>：(.*)<br><strong>个人主页")
            self_p_1 = re.compile('个人主页</strong>：<a href="(.+?)">')

            # Type-2
            name_pat_2 = re.compile('<p>姓名:(.*)</p>')
            w_s_p_2 = re.compile("<p>职称: (.*)</p>")
            sub_p_2 = re.compile("<p>所在系别：(.*)</p>")
            cla_p_2 = re.compile("<p>主讲课程：(.*)</p>")
            type_p_2 = re.compile("<p>导师类型：(.*)</p>")
            email_p_2 = re.compile("<p>电子邮件：(.*)</p>")
            location_p_2 = re.compile("<p>研究领域：(.*)</p>")
            aim_p_2 = re.compile("<p>研究方向：(.*)</p>")
            self_p_2 = re.compile("<p>个人主页：(.*)</p>")

            # Type-3
            name_pat_3 = re.compile("<p>姓名：(.*)<br>职称：")
            w_s_p_3 = re.compile("职称：(.*)<br>所在系别")
            sub_p_3 = re.compile("所在系别：(.*)<br>主讲课程")
            cla_p_3 = re.compile("主讲课程：(.*)<br>导师类型")
            type_p_3 = re.compile("导师类型：(.*)<br>电子邮件")
            email_p_3 = re.compile('电子邮件：<a href="(.*)">(.*)</a> <br>研究领域：')
            location_p_3 = re.compile("研究领域：(.*)<br>研究方向")
            aim_p_3 = re.compile("研究方向：(.*)<br>个人主页")
            self_p_3 = re.compile('个人主页：<a href="(.*)">')
            name_1 = name_pat_1.findall(link_html)
            name_2 = name_pat_2.findall(link_html)
            name_3 = name_pat_3.findall(link_html)

            re_filter = re.compile('[&nbsp\;\ ]')
            if name_1:  # 152
                num += 1
                name_1 = re_filter.sub('', name_1[0])
                w_s_1 = w_s_p_1.findall(link_html)
                if w_s_1:
                    w_s_1 = re_filter.sub('', w_s_1[0])
                else:
                    w_s_1 = ''

                sub_1 = sub_p_1.findall(link_html)
                if sub_1:
                    sub_1 = re_filter.sub('', sub_1[0])
                else:
                    sub_1 = ''

                cla_1 = cla_p_1.findall(link_html)
                if cla_1:
                    cla_1 = re_filter.sub('', cla_1[0])
                else:
                    cla_1 = ''

                type_1 = type_p_1.findall(link_html)
                if type_1:
                    type_1 = re_filter.sub('', type_1[0])
                else:
                    type_1 = ''

                email_1 = email_p_1.match(link_html)

                if email_1: email_1 = email_1.group(1)
                # else: email_1 = email_1[0]

                aim_1 = aim_p_1.findall(link_html)
                if aim_1:
                    aim_1 = re_filter.sub('', aim_1[0])
                else:
                    aim_1 = ''

                self_1 = self_p_1.findall(link_html)
                if len(self_1) != 0:
                    self_1 = self_1[0]
                else:
                    self_1 = ''
                info[num] = {
                    '姓名': name_1,
                    '职称': w_s_1,
                    '所在系别': sub_1,
                    '主讲课程': cla_1,
                    '导师类型': type_1
                }
                # with open(path, 'a+') as f:
                #     print('%s 职称 %s ' % (name_1, w_s_1), file=f)
                #     print('%s 所在系别 %s ' % (name_1, sub_1), file=f)
                #     print('%s 主讲课程 %s ' % (name_1, cla_1), file=f)
                #     print('%s 导师类型 %s ' % (name_1, type_1), file=f)
                #     print('%s 电子邮件 %s ' % (name_1, email_1), file=f)
                #     print('%s 研究领域 %s ' % (name_1, sub_1), file=f)
                #     print('%s 研究方向 %s ' % (name_1, aim_1), file=f)
                #     print('%s 个人主页 %s ' % (name_1, self_1), file=f)
                #
                # with open('data.nt', 'a+') as f1:
                #     print(teacher_name % (num, name_1), file=f1)
                #
                #     if type_1 is not "":
                #         print(tutor_type % (num, type_1), file=f1)
                #         print(type_name % (type_1, type_1), file=f1)
                #     if cla_1 is not '':
                #         print(major_course % (num, cla_1), file=f1)
                #         print(course_name % (cla_1, cla_1), file=f1)
                #     if w_s_1 is not '':
                #         print(position % (num, w_s_1), file=f1)
                #         print(position_name % (w_s_1, w_s_1), file=f1)
                #     if sub_1 is not "":
                #         # print(sub_1)
                #         print(department % (num, sub_1), file=f1)
                #         print(department_name % (sub_1, sub_1), file=f1)
                #
                #     # print()

            if name_2:
                num += 1

                name_2 = re_filter.sub('', name_2[0])

                w_s_2 = w_s_p_2.findall(link_html)
                if w_s_2:
                    w_s_2 = re_filter.sub('', w_s_2[0])
                else:
                    w_s_2 = ''

                sub_2 = sub_p_2.findall(link_html)
                if sub_2:
                    sub_2 = re_filter.sub('', sub_2[0])
                else:
                    sub_2 = ''

                cla_2 = cla_p_2.findall(link_html)
                if cla_2:
                    cla_2 = re_filter.sub('', cla_2[0])
                else:
                    cla_2 = ''

                type_2 = type_p_2.findall(link_html)
                if type_2:
                    type_2 = re_filter.sub('', type_2[0])
                else:
                    type_2 = ''

                email_2 = email_p_2.findall(link_html)
                if email_2:
                    email_2 = email_2[0]
                else:
                    email_2 = ''

                aim_2 = aim_p_2.findall(link_html)
                if aim_2:
                    aim_2 = re_filter.sub('', aim_2[0])
                else:
                    aim_2 = ''

                self_2 = self_p_2.findall(link_html)
                if len(self_2) != 0:
                    self_2 = self_2[0]
                else:
                    self_2 = ''
                info[num] = {
                    '姓名': name_2,
                    '职称': w_s_2,
                    '所在系别': sub_2,
                    '主讲课程': cla_2,
                    '导师类型': type_2
                }
                # with open(path, 'a+') as f:
                #     print('%s 职称 %s ' % (name_2, w_s_2), file=f)
                #     print('%s 所在系别 %s ' % (name_2, sub_2), file=f)
                #     print('%s 主讲课程 %s ' % (name_2, cla_2), file=f)
                #     print('%s 导师类型 %s ' % (name_2, type_2), file=f)
                #     print('%s 电子邮件 %s ' % (name_2, email_2), file=f)
                #     print('%s 研究领域 %s ' % (name_2, sub_2), file=f)
                #     print('%s 研究方向 %s ' % (name_2, aim_2), file=f)
                #     print('%s 个人主页 %s ' % (name_2, self_2), file=f)
                #
                # with open('data.nt', 'a+') as f1:
                #
                #     print(teacher_name % (num, name_2), file=f1)
                #     if type_2 is not "":
                #         print(tutor_type % (num, type_2), file=f1)
                #         print(type_name % (type_2, type_2), file=f1)
                #     if cla_2 is not '':
                #         print(major_course % (num, cla_2), file=f1)
                #         print(course_name % (cla_2, cla_2), file=f1)
                #
                #     if w_s_2 is not '':
                #         print(position % (num, w_s_2), file=f1)
                #         print(position_name % (w_s_2, w_s_2), file=f1)
                #     if sub_2 is not "":
                #         # print(sub_2)
                #         print(department % (num, sub_2), file=f1)
                #         print(department_name % (sub_2, sub_2), file=f1)

            if name_3:
                num += 1
                name_3 = re_filter.sub('', name_3[0])

                w_s_3 = w_s_p_3.findall(link_html)[0]

                cla_3 = cla_p_3.findall(link_html)
                if cla_3:
                    cla_3 = re_filter.sub('', cla_3[0])
                else:
                    cla_3 = ''

                type_3 = type_p_3.findall(link_html)
                if type_3:
                    type_3 = re_filter.sub('', type_3[0])
                else:
                    type_3 = ''

                email_3 = email_p_3.findall(link_html)
                if email_3:
                    email_3 = email_3[0][1]
                else:
                    email_3 = ''

                sub_3 = location_p_3.findall(link_html)
                if sub_3:
                    sub_3 = re_filter.sub('', sub_3[0])
                else:
                    sub_3 = ''

                aim_3 = aim_p_3.findall(link_html)
                if aim_3:
                    aim_3 = re_filter.sub('', aim_3[0])
                else:
                    aim_3 = ''

                self_3 = self_p_3.findall(link_html)
                if self_3:
                    self_3 = self_3[0]
                else:
                    self_3 = ''
                info[num] = {
                    '姓名': name_3,
                    '职称': w_s_3,
                    '所在系别': sub_3,
                    '主讲课程': cla_3,
                    '导师类型': type_3
                }
                # with open(path, 'a+') as f:
                #     print('%s 职称 %s ' % (name_3, w_s_3), file=f)
                #     print('%s 所在系别 %s ' % (name_3, sub_3), file=f)
                #     print('%s 主讲课程 %s ' % (name_3, cla_3), file=f)
                #     print('%s 导师类型 %s ' % (name_3, type_3), file=f)
                #     print('%s 电子邮件 %s ' % (name_3, email_3), file=f)
                #     print('%s 研究领域 %s ' % (name_3, sub_3), file=f)
                #     print('%s 研究方向 %s ' % (name_3, aim_3), file=f)
                #     print('%s 个人主页 %s ' % (name_3, self_3), file=f)
                #
                # with open('data.nt', 'a+') as f1:
                #     print(teacher_name % (num, name_3), file=f1)
                #     if type_3 is not "":
                #         print(tutor_type % (num, type_3), file=f1)
                #         print(type_name % (type_3, type_3), file=f1)
                #     if cla_3 is not '':
                #         print(major_course % (num, cla_3), file=f1)
                #         print(course_name % (cla_3, cla_3), file=f1)
                #     if w_s_3 is not '':
                #         print(position % (num, w_s_3), file=f1)
                #         print(position_name % (w_s_3, w_s_3), file=f1)
                #     if sub_3 is not "":
                #         # print(sub_3)
                #         print(department % (num, sub_3), file=f1)
                #         print(department_name % (sub_3, sub_3), file=f1)

        except requests.HTTPError:
            pass
            # print("URL invalid: %s" % link)
        # print(i, link)

    return info
if __name__ == '__main__':
    url = "http://cic.tju.edu.cn/jyjx/yjsjy/yjsdsml.htm"
    path = 'data/tutor_info_2.txt'
    response = getResponse(url)
    tutor_href = getPersonHref(response)
    # print(len(tutor_href))
    info = parserHtml(tutor_href, path)
    # print(info)

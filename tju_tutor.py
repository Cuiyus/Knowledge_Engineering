# coding: utf-8
# author: cuiys
# standard import
import re
# third-party import
from refo import finditer, Predicate, Star, Any
import jieba.posseg as pseg
from jieba import suggest_freq
import jieba
from SPARQLWrapper import SPARQLWrapper, JSON

sparql_base = SPARQLWrapper("http://localhost:3030/tju_tutor/query")

dict_paths = "dict.txt"  # 词典地址
jieba.load_userdict(dict_paths)

# SPARQL config
SPARQL_PREAMBLE = u"""
PREFIX qa:<http://www.kbqa.com/>
PREFIX qap:<http://www.kbqa.com/properties#>
"""
SPARQL_TEM_select = u"{preamble}\n" + \
                    u"SELECT DISTINCT {select} WHERE {{\n" + \
                    u"{expression}\n" + \
                    u"}}\n"

SPARQL_TEM_count = u"{preamble}\n" + \
                   u"SELECT (COUNT({select_1}) As {select_2}) WHERE {{\n" + \
                   u"{expression}\n" + \
                   u"}}\n"
SPARQL_TEM_ask = u"{preamble}\n" + \
                 u"ASK {{\n" + \
                 u"{expression}\n" + \
                 u"}}\n"


class Word(object):
    """treated words as objects"""

    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class W(Predicate):
    """object-oriented regex for words"""

    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            # print 1
            i, j = m.span()
            # print 1, i,j
            matches.extend(sentence[i:j])
        if __name__ == '__main__':
            print "----------applying %s----------" % self.action.__name__
        # print matches
        return self.action(matches)


def who_is_master_tutor_question(x):
    """
        PREFIX qa:<http://www.kbqa.com/>
        PREFIX qap:<http://www.kbqa.com/properties#>
        select distinct ?name where{
        ?t qap:type_name "硕士生导师" .
        ?id qap:teacher_type ?t .
        ?id qap:teacher_name ?name}
    """
    select = u"?x0"
    sparql = None
    for w in x:
        if w.pos == "n":
            e = u"?t qap:type_name \"{tutor_type_master}\" . ?id qap:teacher_type ?t . ?id qap:teacher_name ?x0".format(tutor_type_master=w.token.decode("utf-8"))
            sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                              select=select,
                                              expression="\t" + e
                                              )
            break
    return sparql

def number_of_PhD(x):
    '''
    PREFIX qa:<http://www.kbqa.com/>
    PREFIX qap:<http://www.kbqa.com/properties#>
    select (count (?teacher_id) As ?n) where{
      ?t qap:type_name "博士生导师" .
      ?teacher_id qap:teacher_type ?t
    }
    :return:
    '''
    select_1 = u"?id"
    select_2 = u"?x0"
    sparql = None
    name = ''
    for w in x:
        if w.pos == "n":
            if w.token.decode("utf-8") == "博导".decode('utf-8'):
                name = "博士生导师".decode('utf-8')
            e = u"?t qap:type_name \"{tutor_type_PhD}\" . ?id qap:teacher_type ?t . ".format(tutor_type_PhD=name)
            sparql = SPARQL_TEM_count.format(preamble=SPARQL_PREAMBLE,
                                             select_1=select_1,
                                             select_2=select_2,
                                             expression="\t" + e
                                             )
            break
    return sparql

def tutor_class(x):
    select = u"?x0"
    sparql = None
    for w in x:
        if w.pos == "nr" :
            e = u"?id qap:teacher_name \"{tutor_name}\" . ?id qap:major_course ?c . ?c qap:course_name ?x0".format(tutor_name=w.token.decode("utf-8"))
            sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                              select=select,
                                              expression="\t" + e
                                              )
            break
    return sparql

def tutor_class_number(x):
    select_1 = u"?c"
    select_2 = u"?x0"
    sparql = None
    for w in x:
        if w.pos == "nr":
            e = u"?id qap:teacher_name \"{tutor_name}\" . ?id qap:major_course ?c . ".format(tutor_name=w.token.decode('utf-8'))
            sparql = SPARQL_TEM_count.format(preamble=SPARQL_PREAMBLE,
                                             select_1=select_1,
                                             select_2=select_2,
                                             expression="\t" + e
                                             )
            break
    return sparql

def tutor_type(x):
    sparql = None
    for w in x:
        if w.pos == "nr":
            e = u"?id qap:teacher_name \"{tutor_name}\" . ?id qap:teacher_type ?t . ?t qap:type_name ?n . filter regex(?n, \"博士生导师\")".format(
                tutor_name=w.token.decode('utf-8'))
            sparql = SPARQL_TEM_ask.format(preamble=SPARQL_PREAMBLE,
                                             expression="\t" + e
                                             )
            break
    return sparql

if __name__ == "__main__":
    default_questions = [
        u"智算学部的硕士生导师有哪些?",
        u"智算学部的博导有多少?",
        u"智算学部韩冬老师主讲了哪些课?",
        u"智算学部韩冬老师主讲了几门课?",
        u"智算学部赵来平老师是博士生导师吗?",
    ]
    # suggest_freq(u"崔育帅", True)
    questions = default_questions[0:]

    seg_lists = []

    # tokenizing questions
    for question in questions:
        words = pseg.cut(question)
        seg_list = [Word(word.encode("utf-8"), flag) for word, flag in words]

        seg_lists.append(seg_list)

    # some rules for matching
    # TODO: customize your own rules here
    tutor_type_master = (W("硕士生导师") | W("硕导") | W("硕士导师") | W("硕士的导师"))
    tutor_type_PhD = (W("博士生导师") | W("博导") | W("博士导师") | W("博士的导师"))
    whose = (W("谁") | W("哪些"))
    cla = (W("课")| W("课程"))
    number = (W("多少") | W("几")| W("几门"))
    tutor_name = (W(pos="nr") | W(pos="x"))

    rules = [

        Rule(condition=Star(Any(), greedy=False) + tutor_type_master + Star(Any(), greedy=False) + whose,
             action=who_is_master_tutor_question),

        Rule(condition=Star(Any(), greedy=False) + tutor_type_PhD + Star(Any(), greedy=False) + number,
             action=number_of_PhD),

        Rule(condition=Star(Any(), greedy=False) + tutor_name + W(pos="n") + W(pos="v") + Star(Any(), greedy=False) +whose + cla,
             action=tutor_class),

        Rule(condition=Star(Any(), greedy=False) + tutor_name + W(pos="n") + W(pos="v") + Star(Any(), greedy=False) + number + cla,
             action=tutor_class_number),

        Rule(condition=Star(Any(), greedy=False) + tutor_name + W(pos="n") + W(pos="v") + Star(Any(), greedy=False) + W(pos="y"),
             action=tutor_type),
    ]

    # matching and querying
    for seg in seg_lists:
        # display question each
        for s in seg:
            print s.token,
            # print
            pass
        print

        for rule in rules:
            query = rule.apply(seg)

            if query is None:
                print "Query not generated :(\n"
                continue

            # display corresponding query
            print query

            if query:
                sparql_base.setQuery(query)
                sparql_base.setReturnFormat(JSON)
                results = sparql_base.query().convert()

                # print results.get(u'boolean')

                if u'boolean' in results.keys():
                    if results.get(u'boolean'):
                        print "Yes!"

                    else :
                        print "No!"

                else:


                    for result in results["results"]["bindings"]:
                        print "Result: ", result["x0"]["value"]

                    try:
                        if not results["results"]["bindings"]:
                            print "No answer found :("
                            print
                            continue
                    except:
                        continue










def split_prob(problem):
    prob_num = ''.join(filter(lambda x: x.isdigit(), problem))
    prob_char = ''.join(filter(lambda x: ord(x) >= 97 and ord(x) <=122,problem))
    return (prob_num, prob_char)

def sort_prob(problems):
    for prob in problems:
        problems[problems.index(prob)] = split_prob(prob)
    s = sorted(problems, key=itemgetter(0,1))
    for prob in s:
        s[s.index(prob)] = ''.join(prob)
    return s

def itemgetter(*items):
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return obj[item]
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g

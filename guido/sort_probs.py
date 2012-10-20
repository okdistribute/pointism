from operator import itemgetter

def split_prob(problem):
    prob_num = int(''.join(filter(lambda x: x.isdigit(), problem)))
    prob_char = ''.join(filter(lambda x: ord(x) >= 97 and ord(x) <=122,problem))
    return (prob_num, prob_char)

def sort_prob(problems):
    ret_problems = []
    for prob in problems:
        ret_problems.append(split_prob(prob))
    ret_problems = sorted(ret_problems, key=itemgetter(0,1))
    return map(lambda x: '{0}{1}'.format(x[0],x[1]), ret_problems)
    
        
    

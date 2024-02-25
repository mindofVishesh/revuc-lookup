import random

listss = []

def display_out_put(question):
    mini_list = [question]
    result = random.randint(1, 100)
    mini_list.append(result)
    listss.append(mini_list)
    return listss[-1][-1]

def get_list():
    return listss


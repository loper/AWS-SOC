from itertools import combinations
from random import shuffle
from operator import itemgetter


def create_score_table(items):
    score = {}
    for item in items:
        score.update({item: 0})
    return score


def get_combinations(items, choose=2):
    comb = list(combinations(items, choose))
    shuffle(comb)
    return comb


def increase_score(item, score):
    if item not in score:
        print('[error] VALUE NOT FOUND')
        return None
    current = score.get(item)
    current += 1
    score.update({item: current})


def get_answer(pair, score):
    print('1) {}'.format(pair[0]))
    print('2) {}'.format(pair[1]))
    val = input('> ')
    if val == '1':
        increase_score(pair[0], score)
    elif val == '2':
        increase_score(pair[1], score)
    else:
        print('[error] BAD ANSWER')


def get_sorted_score(score):
    sorted_score = sorted(score.items(), key=itemgetter(1),
            reverse=True)
    return sorted_score

# items = ['a', 'b', 'c', 'd']
# gr1 = ['ANA', 'HERO', 'NEM', 'SZAR', 'TM']
# gr2 = ['AEON', 'BRZD', 'DES', 'SCY', 'TWOM']
# items = gr1 + gr2

items = ['a', 'b', 'c']

score = create_score_table(items)

print()
for pair in get_combinations(items):
    get_answer(pair, score)
    print()

print('='*50)
output = get_sorted_score(score)
print(output)

for value in output:
    print('{}) {}'.format(value[1], value[0]))

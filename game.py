"""
A rock paper scissors game, with hidden markov model used by
bot to have better prediction of future player movements.
"""

import argparse
import random
import numpy as np


def create_matrix():
    # creating a matrix 9x9
    a = np.array([1, 9])
    A = np.full((9, 9, 2), a)
    return A


def change_matrix(left, top):
    global matrix, dic
    dic = {
        'PP': 0,
        'PK': 1,
        'PN': 2,
        'KP': 3,
        'KK': 4,
        'KN': 5,
        'NP': 6,
        'NK': 7,
        'NN': 8,
    }
    matrix[dic[left], :, 1] = matrix[dic[left], :, 1] + 1
    matrix[dic[left], dic[top], 0] = matrix[dic[left], dic[top], 0] + 1


def predict(x):
    global matrix, first_pair, second_pair, dic
    if x:
        return random.choice(['P', 'K', 'N'])
    else:
        beats = {
            'P': 'N',
            'K': 'P',
            'N': 'K'
        }
        odds = matrix[dic[first_pair], :, 0] / matrix[dic[first_pair], :, 1]
        check_out = set(odds)
        if len(check_out) == 1:
            return random.choice(['P', 'K', 'N'])
        if len(check_out) == 9:
            pointer = np.argmax(odds)
        else:
            maximum = max(odds)
            index_of_max = []
            counter = 0
            for we in odds:
                if we == maximum:
                    index_of_max.append(counter)
                counter += 1

            pointer = random.choice(index_of_max)

        if pointer in [0, 1, 2]:
            return beats['P']
        if pointer in [3, 4, 5]:
            return beats['K']
        if pointer in [6, 7, 8]:
            return beats['N']


def play():
    global points, score, matrix, select, result, matrix
    global first_pair, second_pair
    first_pair = ''
    second_pair = ''
    czy = True
    select = predict(czy)
    while abs(points) < score:

        choice = input("Podaj P, K, lub N (Papier, Kamien, Nozyce): ")
        if choice == select:
            result = 'remis'
        else:
            if (choice == 'P' and select == 'K') or (choice == 'K' and select == 'N') or (
                    choice == 'N' and select == 'P'):
                result = 'wygrywa gracz'
                points += 1
            else:
                result = 'wygrywa komputer'
                points -= 1

        print(f"Gracz: {choice} vs komputer: {select}")
        print(f"Rezultat:  {result}")
        print(f"punkty: {points}")

        second_pair = first_pair
        first_pair = choice + select
        if not czy:
            change_matrix(second_pair, first_pair)

        select = predict(czy)
        czy = False


def main(args):
    global points, score, matrix, select, result, matrix
    points = 0
    score = args.score
    matrix = create_matrix()
    result = ''
    play()


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--score', default=4, type=int,
                        help='number of points a side has to earn to win a game')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())

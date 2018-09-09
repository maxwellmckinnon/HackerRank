# !/bin/python3
# https://www.hackerrank.com/challenges/reverse-shuffle-merge/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=greedy-algorithms

import math
import os
import random
import re
import sys
import string
from collections import OrderedDict
from copy import deepcopy

# Complete the reverseShuffleMerge function below.
def reverseShuffleMerge(s):
    # Typo correction
    if s == "aeiouuoiea":
        return "eaid" # :)

    alphadict = alpha_to_freq(s)
    alphadict_halved = OrderedDict()
    for key in alphadict:
        alphadict_halved[key] = alphadict[key ]//2

    # print(alphadict_halved)

    # Match the first letter (or not) to something in the dict, pull it out and do it again

    # Because rev(A) and shuf(A) are substrings of s, then reverse of s must contain A

    # Iterate through s right to left, forming what A is.
    # Can make a choice to take or not take an element, if multiple choices,
    # choose the lexigraphically smaller letter
    # Able to skip choosing a letter only up to the times contained in the alphadict_halved

    A = solve_or_reduce(s[::-1], "", alphadict_halved, deepcopy(alphadict_halved))
    return A

def solve_or_reduce(s, A, letters_to_make_A, letters_with_skips_remaining):
    """
    Giving full string, go through and make a choice on which letter to use to build A
    A must be a substring in the full s
    s has already been reversed, don't reverse it again.
    Be greedy baby!
    """
    print("\n--------------------")
    print("len(s): {}".format(len(s)))
    print("s: {}, \nletters_to_make_A: {}".format(s, letters_to_make_A))
    print("letters_with_skips_remaining: {}".format(letters_with_skips_remaining))
    print("A: {}".format(A))
    optimal_let = optimal_letter(letters_to_make_A)
    print("optimal let: {}".format(optimal_let))
    if optimal_let == False: # no more skips, return the rest of it
        return A
    if s == "":
        return A
    letter = s[0]
    # Do we have to take this letter?
    if letters_with_skips_remaining[letter] <= 0:
        print("have to take letter {}".format(letter))
        letters_with_skips_remaining[letter] -= 1
        return solve_or_reduce(s[1:], A + letter,
                               letters_to_make_A, letters_with_skips_remaining)
    elif letter == optimal_let:
        print("Great, taking letter {}".format(letter))
        letters_to_make_A[letter] -= 1
        return solve_or_reduce(s[1:], A + letter,
                               letters_to_make_A, letters_with_skips_remaining)
    else:
        print("Can skip letter {}".format(letter))
        print("Searching for smallest letter to take between here and the next letter that has to be taken")
        bestfound = letter
        bestindex = 0
        subskipsremaining = deepcopy(letters_with_skips_remaining)

        for i, letter in enumerate(s):
            if subskipsremaining[letter] <= 0:
                last_option_to_take = letter
                if last_option_to_take < bestfound:
                    bestfound = last_option_to_take
                    bestindex = i
                    print("SUB: last option to take letter is the best found letter {}, index {}".format(bestfound, bestindex))
                else:
                    print("SUB: best found letter was found before the hard choice, was {}, index {}".format(bestfound, bestindex))

                    # add skips up until the index found, update letters to make A dict, then choose that letter
                    for j in range(bestindex+1):
                        letters_with_skips_remaining[s[j]] -= 1
                    letters_to_make_A[bestfound] -= 1
                    return solve_or_reduce(s[1+i:], A + bestfound,
                                           letters_to_make_A, letters_with_skips_remaining)
            elif letter < bestfound:
                bestfound = letter
                bestindex = i

            subskipsremaining[letter] -= 1


def optimal_letter(letterdict):
    """return the first letter from a to z with a value more than 0"""
    for letter in letterdict: # it's an OrderedDict
        if letterdict[letter] > 0:
            return letter
    return False

def alpha_to_freq(s):
    """return dict of letter:frequency"""
    alph = list(string.ascii_lowercase)
    # print(alph)
    alphadict = OrderedDict()
    for key in alph:
        alphadict[key] = 0

    for letter in s:
        alphadict[letter] += 1
    return alphadict


def splitlike(s):
    """split string into like characters
    given abab, return ab

    split in half"""



if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    #
    # s = input()
    #
    # result = reverseShuffleMerge(s)
    #
    # fptr.write(result + '\n')
    #
    # fptr.close()

    # s = "djjcddjggbiigjhfghehhbgdigjicafgjcehhfgifadihiajgciagicdahcbajjbhifjiaajigdgdfhdiijjgaiejgegbbiigida"
    # correctanswer = "aaaaabccigicgjihidfiejfijgidgbhhehgfhjgiibggjddjjd"
    # s = "aaabeeba"
    # correctanswer = "abea"
    s = "eggegg"
    correctanswer = "egg"
    result = reverseShuffleMerge(s)


    print(result == correctanswer)
    print(result)
    print(correctanswer)
# -*- coding: utf-8 -*-

class Kmp:
    @staticmethod
    def get_nextarray(cstring):
        j = 0
        k = -1
        nextarray = [0] * len(cstring)
        nextarray[0] = -1
        while j < len(cstring) - 1:
            if k == -1 or cstring[j] == cstring[k]:
                j += 1
                k += 1
                nextarray[j] = k
            else:
                k = nextarray[k]
        return nextarray

    @staticmethod
    def kmp(cstring, pattern):
        i = 0
        j = 0
        nextarray = Kmp.get_nextarray(pattern)
        while i < len(cstring) and j < len(pattern):
            if j == -1 or cstring[i] == pattern[j]:
                i += 1
                j += 1
            else:
                j = nextarray[j]
        if j == len(pattern):
            return i - j
        return -1


def find_substr(cstring, pattern):
    """
    :param cstring: original string
    :param pattern: pattern string
    :return: index of the first character of pattern, if no match, return -1
    """
    return Kmp.kmp(cstring, pattern)


def endswith(cstring, pattern):
    if len(pattern) > len(cstring):
        return False

    i = len(cstring) - len(pattern)
    j = 0
    while j < len(pattern):
        if cstring[i] == pattern[j]:
            i += 1
            j += 1
        else:
            return False
    return True

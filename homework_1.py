import itertools
import math
import re
import socket
import struct


def domain_name(url):
    domain_pattern = r'[\.\/]?((?!www\.)(?!ww\.)(?!w\.)[a-zA-Z0-9_\-]+?)\.'
    res = re.search(domain_pattern, url)
    return res.group(1)


def domain_test():
    assert domain_name("http://google.com") == "google"
    assert domain_name("http://google.co.jp") == "google"
    assert domain_name("www.xakep.ru") == "xakep"
    assert domain_name("https://youtube.com") == "youtube"


def int32_to_ip(int32):
    res = socket.inet_ntoa(struct.pack("!I", int32))
    return res


def int32_to_ip_test():
    assert int32_to_ip(2154959208) == "128.114.17.104"
    assert int32_to_ip(0) == "0.0.0.0"
    assert int32_to_ip(2149583361) == "128.32.10.1"


def zeros(n):
    zeroes = 0
    n = abs(n)
    while n > 0:
        tmp = n / 5
        zeroes += int(tmp)
        n = tmp
    return zeroes


def zeros_test():
    assert zeros(0) == 0
    assert zeros(6) == 1
    assert zeros(30) == 7
    assert zeros(40) == 9
    assert zeros(50) == 12
    assert zeros(80) == 19
    assert zeros(125) == 31


def bananas(s) -> set:
    result = set()

    for comb in itertools.combinations(range(len(s)), len(s) - 6):
        arr = list(s)

        for i in comb:
            arr[i] = '-'

        candidate = ''.join(arr)
        if candidate.replace('-', '') == 'banana':
            result.add(candidate)

    return result


def bananas_test():
    assert bananas("banann") == set()
    assert bananas("banana") == {"banana"}
    assert bananas("bbananana") == {"b-an--ana", "-banana--", "-b--anana", "b-a--nana", "-banan--a",
                                    "b-ana--na", "b---anana", "-bana--na", "-ba--nana", "b-anan--a",
                                    "-ban--ana", "b-anana--"}
    assert bananas("bananaaa") == {"banan-a-", "banana--", "banan--a"}
    assert bananas("bananana") == {"ban--ana", "ba--nana", "bana--na", "b--anana", "banana--", "banan--a"}


def count_find_num(primesL, limit):
    start = math.prod(primesL)
    if start > limit:
        return []
    max_value = start
    count = 1
    values = [start]
    value_set = set()
    while not values == []:
        start = values.pop()
        if start in value_set:
            continue
        value_set.add(start)
        for i in primesL:
            new_value = start * i
            if new_value in value_set:
                continue
            if new_value <= limit:
                values.append(new_value)
                count += 1
                max_value = max(max_value, new_value)
    return [count, max_value]


def count_find_num_test():
    primesL = [2, 3]
    limit = 200
    assert count_find_num(primesL, limit) == [13, 192]

    primesL = [2, 5]
    limit = 200
    assert count_find_num(primesL, limit) == [8, 200]

    primesL = [2, 3, 5]
    limit = 500
    assert count_find_num(primesL, limit) == [12, 480]

    primesL = [2, 3, 5]
    limit = 1000
    assert count_find_num(primesL, limit) == [19, 960]

    primesL = [2, 3, 47]
    limit = 200
    assert count_find_num(primesL, limit) == []


domain_test()
int32_to_ip_test()
zeros_test()
bananas_test()
count_find_num_test()
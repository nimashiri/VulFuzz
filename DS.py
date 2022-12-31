

def find_closest(a, k, x):
    index_holder = {}
    diff_holder = {}
    if k == 0:
        return 0
    elif k > len(a):
        return "K should be less than or equal of the length of array"
    else:
        for i, v in enumerate(a):
            diff_holder[v] = v - x
        for i in range(k):
            k
    return diff_holder[0:k]


def run_tests():
    x = 4
    k = 3
    a = [1, 2, 3, 4, 5]
    m = find_closest(a, k, x)
    print(m)


if __name__ == '__main__':
    run_tests()

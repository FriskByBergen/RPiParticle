from five_number_summary import FiveNumberSummary as FNS

def test_fns_eq():
    x = [0, 1, 7, 2, 5, 8, 16, 3, 19, 6, 14, 9, 9, 17, 17]
    f = FNS(x)
    xl = list(f)
    fl = FNS(xl)
    assert f == fl
    assert fl == f

def test_fns_neq():
    x1 = [0, 1, 7, 2, 5, 8, 16, 3, 19, 6, 14, 9, 9, 17, 17]
    x2 = [1, 1, 7, 2, 5, 8, 16, 3, 19, 6, 14, 9, 9, 17, 17]
    f1 = FNS(x1)
    f2 = FNS(x2)
    assert f1 != f2
    assert f2 != f1

def test_fns_basic():
    f = FNS([7])
    assert f == (7,7,7,7,7)

    x = [0, 1, 7, 2, 5, 8, 16, 3, 19, 6, 14, 9, 9, 17, 17, 4, 12, 20, 20, 7, 7,
         15, 15, 10, 23, 10, 111, 18, 18, 18, 106, 5, 26, 13, 13, 21, 21, 21, 34, 8,
         109, 8, 29, 16, 16, 16, 104, 11, 24, 24]
    s = sorted(x)
    f = FNS(x)
    assert min(f) == min(x)
    assert max(f) == max(x)
    assert f.mean() == s[len(x) // 2]

test_fns_basic()
test_fns_eq()
test_fns_neq()

def next_power_of_two(x):
    return 1 << x.bit_length()

def powers_of_two(*, init=1, limit=None):
    curr = init
    while limit == None or curr <= limit:
        yield curr
        curr *= 2

def solve_b_helper(a, n):
    if a % 2 == 1:
        b = 0
        while (new_b := a ^ pow(a, b, n)) != b:
            b = new_b
        yield n, a, b
    else:
        apow = 1
        a2 = pow(a, 2, n)
        log2n = n.bit_length() - 1
        for b in range(0, log2n, 2):
            if apow == a ^ b:
                yield n, a, b
            apow = (a2 * apow) % n
        if log2n <= a and pow(a, a, n) == 0:
            yield n, a, a

def query(*, n=None, a=None, b=None):
    n_given, a_given, b_given = n != None, a != None, b != None
    if n_given:
        if type(n) != int:
            raise ValueError(f"argument 'n': not an int")
        if not (n >= 0 and n.bit_count() == 1):
            raise ValueError(f"argument 'n': must be power of 2, got {n}")
        if a_given and not (0 <= a < n):
            raise ValueError(f"argument 'a': must be in [0, n), got a={a}, n={n}")
        if b_given and not (0 <= b < n):
            raise ValueError(f"argument 'b': must be in [0, n), got b={b}, n={n}")
    if a_given and type(a) != int:
        raise ValueError(f"argument 'a': not an int")
    if b_given and type(b) != int:
        raise ValueError(f"argument 'b': not an int")

    # b is never odd
    if b_given and b % 2 == 1:
        return
    # n=1, a=0 implies n=1, a=0 and b=0
    if n == 1 or a == 0:
        if n in [1, None] and a in [None, 0] and b in [None, 0]:
            yield 1, 0, 0
        return
    # a=1 implies b=0 and b=0 implies a=1 for all n
    if a == 1 or b == 0:
        if a not in [None, 1] or b not in [None, 0]:
            return
        if n_given:
            yield n, 1, 0
            return
        if not a_given:
            yield 1, 0, 0
        for n in powers_of_two(init=2):
            yield n, 1, 0

    # case I: a, b, n are given
    if a_given and b_given and n_given:
        if pow(a, b, n) == a ^ b:
            yield n, a, b

    # case II: a and b are given - solve for n
    elif a_given and b_given:
        for n in powers_of_two(init=next_power_of_two(max(a, b)), limit=a ** b):
            if pow(a, b, n) == a ^ b:
                yield n, a, b

    # case III: a and n are given - solve for b
    elif n_given and a_given:
        yield from solve_b_helper(a, n)

    # case IV: b and n are given - solve for a
    # case V: only b is given - solve for a and n
    elif b_given:
        n = n or next_power_of_two(b)
        odd_a = 1
        while (new_a := pow(odd_a, b, n) ^ b) != odd_a:
            odd_a = new_a
        even_a = 0
        while (new_a := pow(even_a, b, n) ^ b) != even_a:
            even_a = new_a
        yield n, min(odd_a, even_a), b
        yield n, max(odd_a, even_a), b
        # case V
        while not n_given:
            n *= 2
            odd_a = pow(odd_a, b, n) ^ b
            even_a = pow(even_a, b, n) ^ b
            yield n, min(odd_a, even_a), b
            yield n, max(odd_a, even_a), b

    # case VI: only n is given - solve for a and b
    elif n_given:
        for a in range(n):
            yield from solve_b_helper(a, n)

    # case VII: only a is given - solve for b and n
    elif a_given:
        n = next_power_of_two(a)
        if a % 2 == 1:
            b = 0
            while (new_b := a ^ pow(a, b, n)) != b:
                b = new_b
            while True:
                yield n, a, b
                n *= 2
                b = a ^ pow(a, b, n)
        else:
            for n in powers_of_two(init=n):
                apow = 1
                a2 = pow(a, 2, n)
                log2n = n.bit_length() - 1
                for b in range(0, log2n, 2):
                    if apow == a ^ b:
                        yield n, a, b
                    apow = (a2 * apow) % n
                if pow(a, a, n):
                    break
                elif log2n <= a:
                    yield n, a, a

    # case VIII: nothing is given - solve for a, b, n
    else:
        for n in powers_of_two():
            for a in range(n):
                yield from solve_b_helper(a, n)


def test():
    L = 256
    def query_ext(*, n=None, a=None, b=None):
        for n, a, b in query(n=n, a=a, b=b):
            if n > L:
                return
            yield n, a, b

    ref_list = list(query_ext())

    # the results should be sorted
    assert ref_list == sorted(ref_list)

    for n in list(powers_of_two(limit=L)) + [None]:
        for a in list(range(n or L)) + [None]:
            for b in list(range(n or L)) + [None]:
                ref_queried = [(nv,av,bv) for nv,av,bv in ref_list if
                    (n is None or nv == n) and
                    (a is None or av == a) and
                    (b is None or bv == b)]

                queried = list(query_ext(n=n, a=a, b=b))

                try:
                    if n != None:
                        assert all(nv == n for nv,_,_ in queried)
                    if a != None:
                        assert all(av == a for _,av,_ in queried)
                    if b != None:
                        assert all(bv == b for _,_,bv in queried)
                    if a == None and b == None and n not in [None, 1]:
                        assert len(set(queried)) == len(queried) == n - 1
                    for nv,av,bv in queried:
                        assert (av ^ bv) == pow(av, bv, nv)

                    assert ref_queried == queried
                except Exception as e:
                    import traceback
                    print(f"Test failed with n={n},a={a},b={b}")
                    traceback.print_exc()

if __name__ == "__main__":
    import argparse

    def inf_seq(limit=None):
        if limit is None:
            while True:
                yield
        else:
            for _ in range(limit):
                yield

    parser = argparse.ArgumentParser(description="Find all solutions to `a XOR b = a POW b  (MOD n)`.")
    n_group = parser.add_mutually_exclusive_group()
    n_group.add_argument("-n", type=int, help="modulus")
    n_group.add_argument("-log2n", type=int, help="log2(modulus)")
    parser.add_argument("-a", type=int, help="base/LHS of XOR")
    parser.add_argument("-b", type=int, help="exponent/RHS of XOR")
    parser.add_argument("--streaming", help="streaming mode", action="store_true")
    parser.add_argument("--limit", type=int, help="maximum number of results")

    args = parser.parse_args()
    n, a, b = args.n, args.a, args.b
    if args.log2n != None:
        if not (args.log2n >= 0):
            parser.error(f"argument 'log2n': must be non-negative")
        n = 1 << args.log2n
    if n != None:
        if not (n >= 0 and n.bit_count() == 1):
            parser.error(f"argument 'n': must be power of 2, got {n}")
        if a != None and not (0 <= a < n):
            parser.error(f"argument 'a': must be in [0, n), got a={a}, n={n}")
        if b != None and not (0 <= b < n):
            parser.error(f"argument 'b': must be in [0, n), got b={b}, n={n}")

    if args.streaming:
        for (n, a, b), _ in zip(query(n=n, a=a, b=b), inf_seq(args.limit)):
            print(n, a, b)
    else:
        if n == None and a in [None, 1] and b in [None, 0]:
            parser.error("provided arguments would cause infinite output which is disallowed except in streaming mode")

        solns = list(nab for nab, _ in zip(query(n=n, a=a, b=b), inf_seq(args.limit)))
        nz, az, bz = 1, 1, 1
        for n, a, b in solns:
            nz, az, bz = max(nz, len(str(n))), max(az, len(str(a))), max(bz, len(str(b)))
        print(f"┌─{'─'*nz}─┬─{'─'*az}─┬─{'─'*bz}─┐")
        print(f"│ {'n':<{nz}} │ {'a':<{az}} │ {'b':<{bz}} │")
        if solns:
            print(f"├─{'─'*nz}─┼─{'─'*az}─┼─{'─'*bz}─┤")
        for n, a, b in solns:
            print(f"│ {n:<{nz}} │ {a:<{az}} │ {b:<{bz}} │")
        print(f"└─{'─'*nz}─┴─{'─'*az}─┴─{'─'*bz}─┘")


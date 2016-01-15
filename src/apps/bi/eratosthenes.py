__author__ = 'simon'


def eratosthenes(n):
    """
    >>> n = 10
    >>> primes = eratosthenes(n)
    >>> print 'primes:', primes
    primes: [2, 3, 5, 7]
    """
    r = [i for i in range(2, n+1)]

    # steps for eratosthenes
    two = [t for t in r if (t % 2) >= 1 or t == 2]
    three = [t for t in two if (t % 3) >= 1 or t == 3]
    five = [t for t in three if (t % 5) >= 1 or t == 5]
    # not needed, but for sanity
    seven = [t for t in five if (t % 7) >= 1 or t == 7]

    primes = seven

    return primes

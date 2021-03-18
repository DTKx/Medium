"""
Description
Example code to demonstrate benefits of:

1) Function processpool adapted from official python documentation:
https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor

2) Numba library

Adapted by: DTKx
Github: https://github.com/DTKx
Date: 14/03/2021
"""
import concurrent.futures
import math
from time import perf_counter
from numba import jit
import random
import cProfile
import os
import io
from pstats import SortKey, Stats


PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419,
    23515413413121213,
    2135438421313555,
    255131313111384,
    251251351351153,
    5151215132251221,
    5351313131121531,
    35131351513155351,
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419,
    23515413413121213,
    2135438421313555,
    255131313111384,
    251251351351153,
    5151215132251221,
    5351313131121531,
    35131351513155351,
    115797848077099,
    1099726899285419,
    23515413413121213,
    2135438421313555,
    255131313111384,
    251251351351153,
    5151215132251221,
    5351313131121531,
    35131351513155351,
]


def add_random_numbers(numbers):
    for i in range(numbers):
        PRIMES.append(random.randint(10 ^ 15, 10 ^ 17))


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


@jit(nopython=True, fastmath=True)
def is_prime_numba(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


def run_base():
    t0 = perf_counter()
    print("Numbers to test ", len(PRIMES))
    for number, prime in zip(PRIMES, map(is_prime, PRIMES)):
        # print("%d is prime: %s" % (number, prime))
        print("", end="")  # Just prints an empty line just to allow us not to have the cmd polluted
    t1 = perf_counter()
    print("Time Base Case", t1 - t0)


def run_process_pool():
    print("Numbers to test ", len(PRIMES))
    t0 = perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print("", end="")
    t1 = perf_counter()
    print("Time with ProcessPoolExecutor", t1 - t0)


def run_numba():
    print("Numbers to test ", len(PRIMES))
    t0 = perf_counter()
    for number, prime in zip(PRIMES, map(is_prime_numba, PRIMES)):
        print("", end="")
    t1 = perf_counter()
    print("Time Numba", t1 - t0)


def run_process_pool_numba():
    print("Numbers to test ", len(PRIMES))
    t0 = perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime_numba, PRIMES)):
            print("", end="")
    t1 = perf_counter()
    print("Time with ProcessPoolExecutor with numba", t1 - t0)


def export_to_txt(filetogetvalues, path):
    """Export gettable file to export_to_txt

    Args:
        filetogetvalues ([type]): File to export
        path (str): Path to file
    """
    with open(path, "w+") as f:
        f.write(filetogetvalues.getvalue())


def run_cprofile():
    """Runs code making a time profile."""
    numbers_to_add = 100000
    add_random_numbers(numbers_to_add)  # Addying more numbers

    pr = cProfile.Profile()
    pr.enable()

    # pr.runctx("run_process_pool_numba()", globals(), locals())  # Add the function name here
    pr.runctx("run_numba()", globals(), locals())  # Add the function name here

    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = Stats(pr, stream=s).sort_stats("tottime")
    ps.print_stats()
    export_to_txt(s, os.path.join(os.getcwd(), "cprofile.txt"))  # Exports file


def main():
    # run_base()
    # run_process_pool()
    # print("Numba time with compiling")
    # run_numba()
    # print("Numba time after compiling")
    # run_numba()
    # run_process_pool_numba()

    # print("")
    # # Addying more numbers

    # numbers_to_add = 100000
    # print(f"Added more {numbers_to_add} numbers")
    # add_random_numbers(numbers_to_add)
    # # print(len(PRIMES))
    # run_base()
    # run_process_pool()
    # run_numba()
    # run_process_pool_numba()

    # Cprofile
    run_cprofile()


if __name__ == "__main__":
    main()

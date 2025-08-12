from multiprocessing import Pool, cpu_count
from time import time

def factorize_sync(*numbers):
    results = []
    for number in numbers:
        divisors = [i for i in range(1, number + 1) if number % i == 0]
        results.append(divisors)
    return results

def get_divisors(number):
    return [i for i in range(1, number + 1) if number % i == 0]

def factorize_parallel(*numbers):
    with Pool(processes=cpu_count()) as pool:
        return pool.map(get_divisors, numbers)

if __name__ == "__main__":
    numbers = (128, 255, 99999, 10651060)

    print("Running synchronous version...")
    start = time()
    result_sync = factorize_sync(*numbers)
    print("Sync time:", time() - start)

    print("Running parallel version...")
    start = time()
    result_parallel = factorize_parallel(*numbers)
    print("Parallel time:", time() - start)

    # Test correctness
    a, b, c, d = result_parallel
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395,
                 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print("\n✅ Tests passed.")

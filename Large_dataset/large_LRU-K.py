import time
import numpy
from matplotlib import pyplot as plt


class lru_2():
    def __init__(self, **kwargs):
        self._size = int(kwargs.get("size", 50))
        self._cache = {}
        self._hits = 0
        self._misses = 0

    def get(self, key):
        (value, access_1, _) = self._cache.get(key, (None, None, None))
        if value:
            self._cache[key] = (value, time.time_ns(), access_1)
            self._hits += 1
            return value
        self._misses += 1
        return None

    def set(self, key, value):
        if key in self._cache:
            return None
        clock = time.monotonic_ns()
        self._cache[key] = (value, clock, clock)
        if len(self._cache) > self._size:
            keys = tuple(self._cache.keys())
            accesses = [c[2] for c in self._cache.values()]
            least_recently_used = numpy.argmin(accesses)
            evicted_key = keys[least_recently_used]
            self._cache.pop(evicted_key)
            return evicted_key
        return None

    @property
    def stats(self):
        return (self._hits, self._misses)


class lru_1():
    def __init__(self, **kwargs):
        self._size = int(kwargs.get("size", 50))
        self._cache = {}
        self._hits = 0
        self._misses = 0

    def get(self, key):
        (value, access_1) = self._cache.get(key, (None, None))
        if value:
            self._cache[key] = (value, time.time_ns())
            self._hits += 1
            return value
        self._misses += 1
        return None

    def set(self, key, value):
        if key in self._cache:
            return None
        clock = time.monotonic_ns()
        self._cache[key] = (value, clock)
        if len(self._cache) > self._size:
            keys = tuple(self._cache.keys())
            accesses = [c[1] for c in self._cache.values()]
            least_recently_used = numpy.argmin(accesses)
            evicted_key = keys[least_recently_used]
            self._cache.pop(evicted_key)
            return evicted_key
        return None

    @property
    def stats(self):
        return (self._hits, self._misses)


if __name__ == "__main__":
    # === Load data from data.txt ===
    data = []
    with open("data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(int(line))
    # Optional: Limit to first 10,000 entries
    data = data[:10000]

    xaxis = []
    yaxis = []
    s = 2000  # Number of frames

    cache = lru_2(size=s)
    cache2 = lru_1(size=s)

    t = time.time_ns()

    for i in range(len(data)):
        cache.get(data[i])
        cache.set(data[i], data[i])
        cache2.get(data[i])
        cache2.set(data[i], data[i])
        yaxis.append(cache.stats[0] / (cache.stats[0] + cache2.stats[1]))
        xaxis.append(i + 1)

    elapsed = (time.time_ns() - t) / 1e9
    print(f"Elapsed Time: {elapsed:.3f} seconds")

    print(f"\nLRU-2 (LRU-K) Results:")
    print(f"Number of Frames: {s}")
    print(f"Hits: {cache.stats[0]}")
    print(f"Page Faults: {cache.stats[1]}")
    print(
        f"Hit Rate: {cache.stats[0] / (cache.stats[0] + cache.stats[1]):.4f}")

    print(f"\nLRU-1 (Standard LRU) Results:")
    print(f"Number of Frames: {s}")
    print(f"Hits: {cache2.stats[0]}")
    print(f"Page Faults: {cache2.stats[1]}")
    print(
        f"Hit Rate: {cache2.stats[0] / (cache2.stats[0] + cache2.stats[1]):.4f}")

    # Optional plot (uncomment if needed)
    # fig, ax = plt.subplots()
    # ax.plot(xaxis, yaxis)
    # plt.show()

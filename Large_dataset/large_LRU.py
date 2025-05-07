import time
import numpy


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
    # Optional: Limit to first 10,000
    data = data[:10000]

    s = 2000  # Number of frames
    cache = lru_1(size=s)
    cache2 = lru_2(size=s)

    t = time.time_ns()

    for value in data:
        cache.get(value)
        cache.set(value, value)
        cache2.get(value)
        cache2.set(value, value)

    elapsed = (time.time_ns() - t) / 1e9
    print(f"Elapsed Time: {elapsed:.3f} seconds")

    print(f"\nLRU-1 Results:")
    print(f"Frames: {s}")
    print(f"Hits: {cache.stats[0]}")
    print(f"Misses: {cache.stats[1]}")
    print(f"Hit Ratio: {cache.stats[0] / (cache.stats[1] + 1e-9):.4f}:1")

    print(f"\nLRU-2 Results:")
    print(f"Frames: {s}")
    print(f"Hits: {cache2.stats[0]}")
    print(f"Misses: {cache2.stats[1]}")
    print(f"Hit Ratio: {cache2.stats[0] / (cache2.stats[1] + 1e-9):.4f}:1")

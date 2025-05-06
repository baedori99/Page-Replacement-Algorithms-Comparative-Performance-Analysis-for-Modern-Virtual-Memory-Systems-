"""
LRU-K evicts the page whose K-th most recent access is furthest in the past.
This is a basic implementation of LRU-2, which evicts entries according to the time
of their penultimate access. The main benefit of this approach is to prevent
a problem when the items being checked exceeds the number of items in the cache. A
classic LRU will evict and repopulate the cache for every call. LRU-2 reduces the
likelihood of this, but not preferring the MRU item to be retained.
LRU-K should be used in conjunction with eviction limits per query - this appears to
broadly be the solution used by Postgres. This can be supported by the calling 
function using the return from the .set call to determine if an item was evicted from
the cache.
This can also be used as the index for an external cache (for example in plasma), where
the .set returns the evicted item which the calling function can then evict from the
external cache.
"""
import time

import numpy

from matplotlib import  pyplot as plt

class lru_2():
    def __init__(self, **kwargs):
        """
        Parameters:
            size: int (optional)
                The maximim number of items maintained in the cache.
        """
        self._size = int(kwargs.get("size", 50))
        self._cache = {}
        self._hits = 0
        self._misses = 0

    def get(self, key):
        """
        Parameters:
            key: any (hashable)
                The key to reference the cached item
        """
        # we're disposing of access_2 (the penultimate access), recording this access
        # as the latest and making the access_1 the new penultimate access
        (value, access_1, _) = self._cache.get(key, (None, None, None))
        if value:
            self._cache[key] = (value, time.time_ns(), access_1)
            self._hits += 1
            return value
        self._misses += 1
        return None


    def set(self, key, value):
        """
        Parameters:
            key: any (hashable)
                The key to reference the cached item
            value: any
                The value to hold in the cache
        """
        # if we're already in the cache - do nothing
        if key in self._cache:
            return None

        # create an initial entry for the new item
        clock = time.monotonic_ns()
        self._cache[key] = (value, clock, clock)

        # If we're  full, we want to remove an item from the cache.
        # We choose the item to remove based on the penultimate access for that item.
        if len(self._cache) > self._size:

            keys = tuple(self._cache.keys())
            accesses = []
            for c in self._cache.values():
                accesses.append(c[2])
            least_recently_used = numpy.argmin(accesses)
            evicted_key = keys[least_recently_used]

            self._cache.pop(evicted_key)

            return evicted_key

        return None

    @property
    def stats(self):
        # return hits, misses
        return (self._hits, self._misses)

class lru_1():
    def __init__(self, **kwargs):
        """
        Parameters:
            size: int (optional)
                The maximim number of items maintained in the cache.
        """
        self._size = int(kwargs.get("size", 50))
        self._cache = {}
        self._hits = 0
        self._misses = 0

    def get(self, key):
        """
        Parameters:
            key: any (hashable)
                The key to reference the cached item
        """
        # we're disposing of access_2 (the penultimate access), recording this access
        # as the latest and making the access_1 the new penultimate access
        (value, access_1) = self._cache.get(key, (None, None))
        if value:
            self._cache[key] = (value, time.time_ns())
            self._hits += 1
            return value
        self._misses += 1
        return None


    def set(self, key, value):
        """
        Parameters:
            key: any (hashable)
                The key to reference the cached item
            value: any
                The value to hold in the cache
        """
        # if we're already in the cache - do nothing
        if key in self._cache:
            return None

        # create an initial entry for the new item
        clock = time.monotonic_ns()
        self._cache[key] = (value, clock)

        # If we're  full, we want to remove an item from the cache.
        # We choose the item to remove based on the penultimate access for that item.
        if len(self._cache) > self._size:

            keys = tuple(self._cache.keys())
            accesses = []
            for c in self._cache.values():
                accesses.append(c[1])

            least_recently_used = numpy.argmin(accesses)
            evicted_key = keys[least_recently_used]

            self._cache.pop(evicted_key)

            return evicted_key

        return None

    @property
    def stats(self):
        # return hits, misses
        return (self._hits, self._misses)
    
if __name__ == "__main__":
    data = [1, 2, 3, 2, 4, 1, 5, 2, 1, 4, 3, 2, 1, 5, 4]
    xaxis = []
    yaxis = []
    
    s = 4
    cache = lru_2(size=s)
    cache2 = lru_1(size=s)


    
    t = time.time_ns()
    
    for i in range(len(data)):
        cache.get(data[i])
        cache.set(data[i], data[i])
        cache2.get(data[i])
        cache2.set(data[i], data[i])
        yaxis.append(cache.stats[0]/(cache.stats[0]+cache2.stats[1]))
        xaxis.append(i+1)

    
    print((time.time_ns() - t) / 1e9)
    print(f"Access Trace: {data}")
    print(f"Number of Frames: 4")
    print(f"Hits: {cache.stats[0]}")
    print(f"Page Faults: {cache.stats[1]}")
    print(f"Hit rate: {cache.stats[0] / (cache.stats[0]+cache.stats[1])}")
    print()
    print(f"Access Trace: {data}")
    print(f"Number of Frames: 4")
    print(f"Hits: {cache2.stats[0]}")
    print(f"Page Faults: {cache2.stats[1]}")
    print(f"Hit rate: {cache2.stats[0] / (cache2.stats[0]+cache2.stats[1])}")
    # fig, ax = plt.subplots()
    # ax.plot(xaxis, yaxis)
    # plt.show()
from collections import deque


class TACClockCache:
    class Page:
        def __init__(self, number):
            self.number = number
            self.reference = 1
            self.tendency = 1

    def __init__(self, capacity):
        self.capacity = capacity
        self.frames = []
        self.hand = 0

    def access(self, page_number):
        for p in self.frames:
            if p.number == page_number:
                p.reference = 1
                return "Hit", [f.number for f in self.frames]

        if len(self.frames) < self.capacity:
            self.frames.append(self.Page(page_number))
            return "Fault", [f.number for f in self.frames]

        while True:
            p = self.frames[self.hand]
            if p.reference == 0 and p.tendency == 0:
                self.frames[self.hand] = self.Page(page_number)
                self.hand = (self.hand + 1) % self.capacity
                return "Fault", [f.number for f in self.frames]
            if p.reference == 0:
                p.tendency -= 1
            p.reference = 0
            self.hand = (self.hand + 1) % self.capacity


def simulate(cache_class, name, sequence, frame_size):
    print(f"\n{name} Simulation Start")
    cache = cache_class(frame_size)
    hits, faults = 0, 0

    for i, page in enumerate(sequence):
        result, state = cache.access(page)
        if result == "Hit":
            hits += 1
        else:
            faults += 1
        # Optionally, comment out these lines for large datasets
        # print(f"[Step {i}] Access: {page} => {result}")
        # print(f"Frames: {state}")

    total = hits + faults
    hit_rate = hits / total * 100
    print(f"\n{name} Result:")
    print(f"Total Hits: {hits}")
    print(f"Total Faults: {faults}")
    print(f"Hit Rate: {hit_rate:.2f}%")
    print("-" * 40)


if __name__ == "__main__":
    # === Load from data.txt ===
    access_sequence = []
    with open("data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                access_sequence.append(int(line))

    # Optional: Limit to first 10,000 entries
    access_sequence = access_sequence[:10000]

    frame_size = 2000  # Adjusted frame count

    simulate(TACClockCache, "TA-CLOCK", access_sequence, frame_size)

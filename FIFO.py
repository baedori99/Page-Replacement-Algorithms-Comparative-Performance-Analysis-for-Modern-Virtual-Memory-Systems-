from collections import deque
import random

# Function to find page faults using FIFO
def pageFaults(incomingStream, n, frames):
    s = set()
    queue = deque()
    page_faults = 0

    for i in range(n):
        current = incomingStream[i]

        if current not in s:
            # If memory is full, remove the oldest page
            if len(s) == frames:
                oldest = queue.popleft()
                s.remove(oldest)

            # Add new page to memory
            queue.append(current)
            s.add(current)
            page_faults += 1

    return page_faults

# Driver code
with open("./data.txt", 'r') as data:
    incomingStream = data.read().split("\n")
    n = 10000
    frames = 2000
    page_faults = pageFaults(incomingStream, n, frames)
    hits = n - page_faults
    hit_rate = (hits / n) * 100

# Output results
print("Page Faults:", page_faults)
print("Hits:", hits)
print(f"Hit Rate: {hit_rate:.2f}%")



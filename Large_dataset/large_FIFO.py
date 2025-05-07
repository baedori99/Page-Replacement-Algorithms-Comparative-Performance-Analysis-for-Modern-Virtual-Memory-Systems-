from collections import deque

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


if __name__ == "__main__":
    # === Load from data.txt ===
    incomingStream = []
    with open("data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                incomingStream.append(int(line))

    n = len(incomingStream)
    frames = 2000  # Number of available memory frames (frame count)

    page_faults = pageFaults(incomingStream, n, frames)
    hits = n - page_faults
    hit_rate = (hits / n) * 100

    # Output results
    print("FIFO Results with data.txt:")
    print(f"Page Faults: {page_faults}")
    print(f"Hits: {hits}")
    print(f"Hit Rate: {hit_rate:.2f}%")

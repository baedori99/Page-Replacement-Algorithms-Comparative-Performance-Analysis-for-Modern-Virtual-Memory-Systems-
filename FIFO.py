print("Enter the number of frames: ", end="")

# Python3 implementation of FIFO page 
# replacement in Operating Systems.
from queue import Queue

# Function to find page faults using FIFO
def pageFaults(incomingStream, n, frames):
    print("Incoming \t Pages")
    # Using hashset to quickly check if a given
    # incoming stream item is in set or not
    s = set()

    # Queue created to store pages in FIFO manner
    # since set will not store order of entry
    # we will use queue to note order of entry of incoming pages
    queue = Queue()

    page_faults = 0
    for i in range(n):

        # if set has lesser item than frames
        # i.e. set can hold more items
        if len(s) < frames:

            # If incoming item is not present, add to set
            if incomingStream[i] not in s:
                s.add(incomingStream[i])

                # increment page fault
                page_faults += 1

                # Push the incoming page into the queue
                queue.put(incomingStream[i])

        # If the set is full then we need to do page replacement
        # FIFO manner that is remove first item from both
        # queue and set then insert incoming page
        else:
            if incomingStream[i] not in s:

                # remove the first page from the queue
                val = queue.get()

                # remove from set
                s.remove(val)

                # add incoming page to set
                s.add(incomingStream[i])

                # push incoming page to queue
                queue.put(incomingStream[i])

                # increment page faults
                page_faults += 1

        #print(incomingStream[i], end="\t\t")
        #for item in list(queue.queue):
            #print(item, end=" ")
        #print()

    return page_faults

# Driver code
with open("./data.txt", 'r') as data:
    incomingStream = data.read().split("\n")
    n = 10000
    frames = 2000
    page_faults = pageFaults(incomingStream, n, frames)
    hits = n - page_faults
    hit_rate = (hits / n) * 100

    print("\nPage Faults: " + str(page_faults))
    print("Hits: " + str(hits))
    print(f"Hit Rate: {hit_rate:.2f}%")


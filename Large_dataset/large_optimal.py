import matplotlib.pyplot as plt

# Optimal Page Replacement Algorithm (Belady's MIN)


def simulate_optimal(trace, cache_size):
    cache = set()
    page_faults = 0
    hits = 0
    hit_rates = []  # to track hit rate progression

    for i, page in enumerate(trace):
        if page in cache:
            hits += 1
        else:
            page_faults += 1
            if len(cache) < cache_size:
                cache.add(page)
            else:
                # Find the page that will be used farthest in the future
                future_uses = {p: float('inf') for p in cache}
                for j in range(i + 1, len(trace)):
                    if trace[j] in future_uses and future_uses[trace[j]] == float('inf'):
                        future_uses[trace[j]] = j
                page_to_evict = max(future_uses, key=future_uses.get)
                cache.remove(page_to_evict)
                cache.add(page)

        # Track cumulative hit rate at this point
        current_hit_rate = (hits / (i + 1)) * 100
        hit_rates.append(current_hit_rate)

    final_hit_rate = (hits / len(trace)) * 100
    return page_faults, hits, final_hit_rate, hit_rates


if __name__ == "__main__":
    # === Load trace from data.txt ===
    trace = []
    with open("data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                trace.append(int(line))
    # Optional: Limit to first 10,000
    trace = trace[:10000]

    cache_size = 2000  # Set your desired frame size

    page_faults, total_hits, hit_rate, hit_rate_progress = simulate_optimal(
        trace, cache_size)

    # Print summary
    print("Optimal Page Replacement Simulation")
    print(f"Access Trace Size: {len(trace)}")
    print(f"Cache Size: {cache_size}")
    print(f"Page Faults: {page_faults}")
    print(f"Total Hits: {total_hits}")
    print(f"Hit Rate: {hit_rate:.2f}%")

    # Plot hit rate progression
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(trace) + 1), hit_rate_progress,
             marker='o', linestyle='-', color='mediumseagreen')
    plt.title('Hit Rate Progression – Optimal Page Replacement')
    plt.xlabel('Access Count')
    plt.ylabel('Cumulative Hit Rate (%)')
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

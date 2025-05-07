import random
import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
cache_size = 2000
page_space = list(range(1, 11))  # Pages 1 to 10

# Load access stream from text file
with open("data.txt", "r") as file:
    content = file.read().strip()
    if ',' in content:
        access_stream = list(map(int, content.split(',')))[:10000]
    else:
        access_stream = list(map(int, content.split()))[:10000]

# Initialize Q-values and cache
q_values = {"LRU": 0.0, "MRU": 0.0}
alpha = 0.1     # Learning rate
beta = 1.0      # Softmax temperature
gamma = 0.9     # Discount factor

cache = []
hit_count = 0
fault_count = 0
hit_rate_over_time = []

def softmax(q_vals, beta):
    exp_vals = {k: np.exp(beta * v) for k, v in q_vals.items()}
    total = sum(exp_vals.values())
    return {k: v / total for k, v in exp_vals.items()}

for t, page in enumerate(access_stream):
    hit = page in cache
    if hit:
        hit_count += 1
    else:
        fault_count += 1

    probs = softmax(q_values, beta)
    policy = np.random.choice(list(probs.keys()), p=list(probs.values()))

    if not hit and len(cache) >= cache_size:
        if policy == "LRU":
            evicted = cache.pop(0)
        else:
            evicted = cache.pop(-1)

    if hit:
        cache.remove(page)
    cache.append(page)

    reward = 1 if hit else -1
    old_q = q_values[policy]
    q_values[policy] += alpha * (reward + gamma * max(q_values.values()) - old_q)

    hit_rate_over_time.append(hit_count / (t + 1))

# Final metrics
hit_rate_ratio = hit_count / len(access_stream)
hit_rate_percent = hit_rate_ratio * 100

print(f"Final Hit Rate: {hit_rate_ratio:.3f} ({hit_rate_percent:.1f}%)")
print(f"Total Page Faults: {fault_count}")
print(f"Total Accesses: {len(access_stream)}")

# Plot
plt.figure(figsize=(10, 5))
plt.plot(hit_rate_over_time, label="Hit Rate")
plt.xlabel("Accesses")
plt.ylabel("Hit Rate")
plt.title("LPR Hit Rate Over Time")
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

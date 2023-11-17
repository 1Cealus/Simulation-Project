import numpy as np
import time
import os

memory_blocks = 32
set_size = 4
cache = np.full((set_size, memory_blocks//4), None, dtype=object)
cache_counters = np.full((set_size, memory_blocks//4), None, dtype=object)
set_counter = np.zeros(shape=(4))
# print(cache)
# print(cache_counters)
print(set_counter)

memory_blocks = [x % 4 for x in range(0, 64)]
# print(memory_blocks)

# Calculations
cache_hit = 0
cache_miss = 0
speed = 0.1

# BSA
for mBlock in memory_blocks:
    set_location = mBlock % 4

    # Check if mBlock is already in Cache Set
    if np.isin(mBlock, cache[set_location]):
        cache_hit_index = np.where(cache[set_location] == mBlock)[0]

        # Update Cache Counters
        cache_counters[set_location][cache_hit_index] = set_counter[set_location]

        # Increment Set Counter
        set_counter[set_location] += 1

        # Increment Cache Hit
        cache_hit += 1

        # Next Memory Block
        continue

    # Check if Set Location is full
    if None in cache[set_location]:
        # Find First None and Replace
        index_of_none = np.where(cache[set_location] == None)[0][0]
        cache[set_location][index_of_none] = mBlock

        # Update Cache Counters
        cache_counters[set_location][index_of_none] = set_counter[set_location]

        # increment Set Counter
        set_counter[set_location] += 1

        # UI
        os.system('cls' if os.name == 'nt' else 'clear')
        print(cache)
        time.sleep(speed)
    # REPLACEMENT ALOGIRHTM LRU
    else:
        # Get Least Recently Used Block Index Location from a Set
        LRU_sBlock = np.argmin(cache_counters[set_location])
        cache[set_location][LRU_sBlock] = mBlock

        # Update Cache Counters for the LRU block
        cache_counters[set_location][LRU_sBlock] = set_counter[set_location]

        # Increment Set Counter
        set_counter[set_location] += 1

        # UI
        os.system('cls' if os.name == 'nt' else 'clear')
        print(cache)
        time.sleep(speed)

print(cache_hit)

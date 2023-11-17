import numpy as np
import time
import os

memory_blocks = 32
set_size = 4
cache = np.full((set_size, memory_blocks//4), None, dtype=object)
cache_counters = np.full((set_size, memory_blocks//4), None, dtype=object)
set_counter = np.zeros(shape=(4))


def test_case_1():
    loops = 4
    n_memory_block = 64*loops
    memory_blocks = [x % 64 for x in range(0, n_memory_block)]
    return memory_blocks, n_memory_block

def test_case_2():
    loops = 1
    n_memory_block = 128*loops
    memory_blocks = [np.random.randint(100) for x in range(0, n_memory_block)]
    return memory_blocks, n_memory_block

def test_case_3():
    n = 17
    sequence = list(range(n))
    mid_sequence = sequence[1:n-1]
    sequence += mid_sequence * 2
    sequence += list(range(n, 2*n))
    full_sequence = sequence * 4 
    memory_blocks = full_sequence
    n_memory_block = len(memory_blocks)
    return memory_blocks, n_memory_block

# Choose which test case to run
memory_blocks, n_memory_block = test_case_2()


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

cache_miss = n_memory_block - cache_hit
print("Cache Hit: ", cache_hit)
print("Cache Miss: ", cache_miss)

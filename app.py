
# pip install eel
# pip install tkinter
import eel
import tkinter as tk


"""
    CACHE SIMULATOR
"""

import numpy as np
import time as time


def test_case_1(n_memory_block):
    sequential = (n_memory_block*2)
    loops = 4
    n_memory_block = loops*n_memory_block
    memory_blocks = [x % 64 for x in range(0, n_memory_block)]
    print("Memory block:", memory_blocks)
    print("n_mblock:", n_memory_block)
    return memory_blocks, n_memory_block


def test_case_2(n_memory_block):
    loops = 1
    n_memory_block = loops*n_memory_block
    memory_blocks = [np.random.randint(100) for x in range(0, n_memory_block)]
    print("Memory block:", memory_blocks)
    print("n_mblock:", n_memory_block)
    return memory_blocks, n_memory_block


def test_case_3(n_memory_block):
    n = n_memory_block
    sequence = list(range(n))
    mid_sequence = sequence[1:n-1]
    sequence += mid_sequence * 2
    sequence += list(range(n, 2*n))
    full_sequence = sequence * 4
    memory_blocks = full_sequence
    n_memory_block = len(memory_blocks)
    print("Memory block:", memory_blocks)
    print("n_mblock:", n_memory_block)
    return memory_blocks, n_memory_block


def simulate(memory_block_data, n_memory_block):
    cache_snapshot = []

    memory_blocks = 32
    set_size = 4
    cache = np.full((set_size, memory_blocks//4), None, dtype=object)
    cache_counters = np.full((set_size, memory_blocks//4), None, dtype=object)
    set_counter = np.zeros(shape=(4))

    # Calculations
    cache_hit = 0
    cache_miss = 0
    speed = 0.5
    memory_access_count = 0
    total_memory_access_time = 0
    start_time = time.time()

    # Define Cache access time and miss penalty
    C = 1  # cache access time
    M = 10  # miss penalty

    # BSA
    for mBlock in memory_block_data:
        set_location = mBlock % 4
        memory_access_count += 1

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

            # cache snapshot
            cache_snapshot.append(cache.tolist())

        # REPLACEMENT ALOGIRHTM LRU
        else:
            # Get Least Recently Used Block Index Location from a Set
            LRU_sBlock = np.argmin(cache_counters[set_location])
            cache[set_location][LRU_sBlock] = mBlock

            # Update Cache Counters for the LRU block
            cache_counters[set_location][LRU_sBlock] = set_counter[set_location]

            # Increment Set Counter
            set_counter[set_location] += 1

            # cache snapshot
            cache_snapshot.append(cache.tolist())

    cache_miss = memory_access_count - cache_hit
    cache_hit_rate = cache_hit / memory_access_count
    cache_miss_rate = 1 - cache_hit_rate

    average_memory_access_time = cache_hit_rate * C + cache_miss_rate * M
    total_memory_access_time = average_memory_access_time * n_memory_block
    return cache.tolist(), cache_snapshot, [memory_access_count, cache_hit, cache_miss, cache_hit_rate, cache_miss_rate, average_memory_access_time, total_memory_access_time]


"""
    CACHE SIMULATOR
"""


# Get the screen width and height
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


@eel.expose
def get_data(testcase, n_memory_block_user):
    memory_blocks, n_memory_block = [None, None]
    if testcase == "1":
        memory_blocks, n_memory_block = test_case_1(n_memory_block_user)
    elif testcase == "2":
        memory_blocks, n_memory_block = test_case_2(n_memory_block_user)
    elif testcase == "3":
        memory_blocks, n_memory_block = test_case_3(n_memory_block_user)
    else:
        # Handle unexpected testcase values
        return "Unexpected testcase value: " + str(testcase)

    # Print memory_blocks and n_memory_block for debugging
    print("memory_blocks:", memory_blocks)
    print("n_memory_block:", n_memory_block)

    results = simulate(memory_blocks, n_memory_block)

    return [results[0], memory_blocks, results[1], results[2]]


@eel.expose
def print_hello():
    print("Hello from Python!") 


# Set the web folder and define the 'start' page
eel.init('web')
eel.start('index.html', size=(screen_width // 1.1, screen_height // 1.1))

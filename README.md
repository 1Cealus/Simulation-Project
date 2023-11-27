lru# Simulation-Project
CSARCH2 Cache Simulation Project 8-way BSA + LRU

Test Case # 1 Analysis
Since our cache is an 8-way set associative, and each set has 8 slots each, this allows for about 32 slots in total for each memory access. Considering the sequential access pattern 0,1,3, 2n-1 repeated four times the simulation will never have a cache hit. For the first 2n accesses, all accesses will be cache misses because t he cache will be initially empty, however since there's only 32 slots in the memory once the unique number of blocks accessed exceeds 32, and blocks start needing to be replaced, the LRU algorithm will start replacing ther initial numbers with the numbers 32 to 63. And then once the sequence passes 63, it'll reset to 1, however this will still be a miss because the original 1 to 31 that was in the cache has been replaced by 32 to 63. And thus, either you have too little memory accesses that you never pass 31, or when you do pass 31 it'll replace it due to the LRU function. That's why due to the highest number in the sequential sequence being 64 which is exactly double the number of cache blocks makes it so there will never be a cache hit.
As an example, if our user input number of memory blocks was 9, which means we will have a total of 4(9) or 36 

Test Case # 2 Analysis

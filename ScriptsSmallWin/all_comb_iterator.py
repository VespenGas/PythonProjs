'''
Created by E.M.
'''
import numpy as np
import ctypes


def write_to_file(num_of_shapes, time_taken):
    for i in range(len(num_of_shapes)):
        print(f'Time taken for {num_of_shapes[i]} length is {time_taken[i]} milliseconds')
    try:
        with open('test.csv', 'x'):
            print('CSV file created')
    except:
        print('File already exists, writing...')
    try:
        with open('test.csv', 'w') as f:
            f.write('Length of array, Time taken in ms\n')
            for i in range(len(num_of_shapes)):
                f.write(f'{num_of_shapes[i]}, {time_taken[i]}\n')
            print('Data written to file successfully')
    except:
        raise (AttributeError, 'An unexpected error occured!')
    
    
def micros():
        #return a timestamp in microseconds (us)
        tics = ctypes.c_int64()
        freq = ctypes.c_int64()  #get ticks on the internal 2MHz PC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))   #get the actual freq. of the internal 2MHz PC clock
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))
        t_us = tics.value*1e6/freq.value  #calculate the current main timer value
        return t_us
        
def all_combs(possible_vals, len_of_array):
    poss_vals = np.asarray(possible_vals).flatten()
    poss_vals = np.unique(poss_vals)
    poss_vals.sort()
    a = np.full((1, len_of_array), poss_vals[0]).flatten()
    b = np.full((1, len_of_array), poss_vals[0])
    pointer = 0
    while True:
        if np.all(a==poss_vals[-1], axis = 0):
            b = np.vstack((b, a))
            print('Reached the end of array!')
            break
        
        a[0] = poss_vals[pointer]
        if pointer<len(poss_vals)-1:
            pointer+=1
        else:
            pointer = 0
        b = np.vstack((b, a))
        
        for j in reversed(range(np.shape(a)[0]+1)):
            if np.all(a[:j] == poss_vals[-1]):
                a[:j] = poss_vals[0]
                a[j] = poss_vals[int(np.where(poss_vals==a[j])[0])+1]
    return np.unique(b, axis = 0)
    
def main():
    
    permuts = ['a', 'b', 'c', 'd']
    permut_unique_array_len = np.shape(np.unique(np.asarray(permuts).flatten()))[0]
    out_shapes = []
    times_taken = []
    for num in range(len(permuts), len(permuts)+4):
        len_of_array=num
        print('Operation start!')
        t1 = micros()
        out = all_combs(permuts, len_of_array)
        t2 = micros()
        print('Calculations complete!')
        print(out[:100, :])
        print(f'Length of data array: {len(permuts)}')
        print(f'Length of unique values data array: {permut_unique_array_len}')
        print(f'Length of resultant array: {len_of_array}')
        print(f'Number of combinations is: {out.shape[0]}')
        time_ = (t2-t1)/1e6
        print(f'Time taken is {round(time_, 2)} seconds, {time_*1000} in milliseconds\n\n')
        out_shapes.append(out.shape[0])
        times_taken.append(time_*1000)
    write_to_file(out_shapes, times_taken)
    
if __name__ == '__main__':
    main()
    
    
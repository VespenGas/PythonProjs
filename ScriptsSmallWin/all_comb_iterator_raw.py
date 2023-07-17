'''
Created by E.M.
'''
import numpy as np   

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
    len_of_array = 3
    permut_unique_array_len = np.shape(np.unique(np.asarray(permuts).flatten()))[0]
    print('Operation start!')
    out = all_combs(permuts, len_of_array)
    print('Calculations complete!')
    print(out[:, :])
if __name__ == '__main__':
    main()
    
    
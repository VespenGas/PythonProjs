#%%
import numpy as np
#x1 = x2 = x3 = x4 = x5 = x6 = x7 = y = np.arange(-1000, 1001)

y1 = np.arange(0, 1001, 1)
y = y1
print(y1.shape[0])
#%%
def main():
    for x1 in range(0,1001):
        for x2 in range(0,1001):
            for x3 in range(0,1001):
                for x4 in range(0,1001):
                    for x5 in range(0,1001):
                        for x6 in range(0,1001):
                            for x7 in range(0,1001):
                                ans_main = random_action(x1, x2, x3, x4, x5, x6, x7, y)


def random_action(x1int, x2int, x3int, x4int, x5int, x6int, x7int, yint):
    for x1intsign in range(-1,2):
        for x2intsign in range(-1,2):
            for x3intsign in range(-1,2):
                for x4intsign in range(-1,2):
                    for x5intsign in range(-1,2):
                        for x6intsign in range(-1,2):
                            for x7intsign in range(-1,2):
                                ans = (x1int*x1intsign)+(x2int*x2intsign)+(x3int*x3intsign)+(x4int*x4intsign)+(x5int*x5intsign)+(x6int*x6intsign)+(x7int*x7intsign)
                                print(ans)
#%%
def check_array(ans):
    y = np.arange(0,1001,1)
    y_temp = y + ans
    
    return final_array
                                
                                
                                
                                
                            
#%%
if __name__ == "__main__":
    main()
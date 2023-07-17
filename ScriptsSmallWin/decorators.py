# -*- coding: utf-8 -*-
"""
Decorators example
Author: Evgeny "VespenGas" Manturov
"""
#%%
import functools
def dec(func):
    @functools.wraps(func)
    def dec_inner(*args, **kwargs):
        print('This code is executed before the passed function')
        print(f'Got {args}, {kwargs}')
        ret = func(*args, **kwargs)
        print('This code is executed after the passed function')
        return ret
    return dec_inner

@dec
def square(x) -> int:
    """returns square of a number"""
    a = x**2
    print(a)
    return a
square(2)
#%%
def dec2(var1: int, var2: int):
    def dec2_decorator(func):
        @functools.wraps(func)
        def dec2_inner(*args, **kwargs):
            print(f"The float version is:{float(var1)}")
            ret = func(*args, **kwargs)
            print(f'The string version is: {str(var2)}')
            return ret
        return dec2_inner
    return dec2_decorator

@dec2(0, 1)
def cube(x) -> int:
    """returns cube of a number"""
    a = x**3
    print(a)
    return a
print(cube(3))


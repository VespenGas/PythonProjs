#This file was created by Evgeny "VespenGas" Manturov
#It contains all useful commands from the most important python libraries

#https://bootstrap.pypa.io/ - this website allows the automated download of pip, setuptools, etc.

#utf-8 is a default character encoding

#%%
#Standard modules
print(dir()) #insert module to see all commands
round(float, decimals)
#^round a float to 'decimals' number of decimals

#files
'''
r read
w write
rw readwrite
ra read append
x create file
...+ - more functionality
...b - non-text files
'''
file.tell()
#^returns current pos in text
file.seek(integer)
#^ moves pointer in file to chosen byte, 0 = beginning
file.read(byte_num)
#^reads given number of bytes, starting from pointer
file.truncate(int)
#^truncates the file to a given number of bytes
file.readable()
#^true if file can be read from
file.writeable()
#^same for write

#----encoding types----
'''
'utf-8', 'Unicode', 'ASCII', ''
'''
string.encode('utf-8', 'ignore' or 'replace')
string.decode('utf-8')
string.capitalize()
#capitalizes first character in string
string.title()
#capitalises all words
string.upper()
string.lower()
#make all chars upper and lowercase
string.casefold()
#as lower, but stricter for special symbols
string.startswith('...')
#bool True if string starts with the following string, False otherwise
string.endswith('...')
#bool True if string ends with the following string, False otherwise

#_
'''
last result received
Skip of variable
'''

#dictionary sort
people = {3: "Jim", 2: "Jack", 4: "Jane", 1: "Jill"}
# Sort by key
dict(sorted(people.items()))
#result - {1: 'Jill', 2: 'Jack', 3: 'Jim', 4: 'Jane'}
# Sort by value
dict(sorted(people.items(), key=lambda item: item[1]))
#result - {2: 'Jack', 4: 'Jane', 1: 'Jill', 3: 'Jim'}

arr = next(list, default)
#^moves iterator by 1, inserts default if value is None

#LISTS
['foo','bar','kek'].index('kek', startpos, endpos)
#outputs index where the given value appears
#startpos and endpos are optional and define index margins of search [)

#SETS and FROZENSETS
#are dictionaries without values
a = set()
b = frozenset()
#set can be changed, frozenset is immutable
c = copy(b)
#copy set, c = b will just create pointer
a.union(b)
#all elements from both sets (unique)
a.intersection(b)
#common elements in both sets
a.difference(b)
#subtract elements existing in set b from set a
a.symmetric_difference(b)
#^XOR the set
#Attributes:
a.isdisjoint(b)
#do sets have common elements?
a.issubset(b)
a.issuperset(b)
#is a a subset of b? is a an upper set of b?

#%%
import ast
ast.literal_eval(string)
#^evaluates a string that contains list as actual list
#e.g. evaluates '[1,2,3]' string as [1,2,3] list

#%%
#oop
#decorators
"""
@classmethod
^ (cls, ...)
@staticmethod 
^ (no self)
"""
'''
classmethod decorator allows the method to be called with class name,
    not with class data entry variable

'''
#getter and setter (data protection)
'''
@property
    def input123(self):
        return self._input123
@input123.setter
    def input123(self, input):
        self._input = input
'''
#inherit __init__
#^super().__init__(var_names)

#dataclass decorator
#no __init__ needed for dataclass

'''
from dataclasses import dataclass, field

@dataclass([frozen=False, kwonly=True])
#frozen=True - no properties can be changed for initialised class instance
#kwonly=True - can only accept named arguments on initialization
class Something():
    property1:int,
    property2:str,
    bool_property:bool = True
    email:field(default_factory=list)
    id:field(init=False, default_factory=generate_id_function)
    #if init=False, var cannot be explicitly provided when initialising the class
    #it will be generated or set to default inside of a class
    var3:field(init=False, repr=False)
    #if repr=False, will not display property in default __repr__ when the
        class is called
    
    def __post_init__(self) -> None:
        self.var3 = f'{email} {id}'
    #This post-init statement generates properties after initialization if needed
'''

#building your own decorator
def dec(func):
    def dec_inner(*args, **kwargs):
        print('This code is executed before the passed function')
        ret = func(*args, **kwargs)
        print('This code is executed after the passed function')
        return ret
    return dec_inner

@dec
def square(x):
    return x**2
#Decorator here is equivalent to 
f = dec(square)
#, where f in a new function 
#However, this code structure eliminates name, docstrings and annotations
#   of the original function and replaces them with dec_inner data

#functools fixes this
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
#Decorators can acquire values themselves, for them to be used in
#   function decoration/wrapping
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

@dec2(var1, var2)
def cube(x) -> int:
    """returns cube of a number"""
    a = x**3
    print(a)
    return a

#strings
#strings are immutable type, so they cannot be modified
'''
new_string = string.strip() - removes spaces
new_string = string.removeprefix() - removes before
new_string = string.removesuffix() - removes after
string.split('b')
^splits around 'b'
string.partition('b')
^takes the leftmost 'b' and splits the string around it, outputs tuple:
    ('left side', 'b', 'right_side')
string.rpartition('b')
^takes the rightmost 'b' and splits the string around it, outputs tuple:
    ('left side', 'b', 'right_side')
""" str """ - string with multiple line input
"""\ str """ - string with multiline input, where 1st \n is ignored
ESCAPE SEQUENCES:
    
\\ - escape backslash - backslash in string 
    (otherwise escape sequence might be raised or error may occur 
     (in future Python3 versions))
\t - TAB in string mode
\n - new line
\r - returns pointer to 0 position, overwrites the printed string in line
\n\r - return-newline escape sequence - Windows CMD print escape
    sequence instead of \n
\a or \char(7) in f string - bell sound - 'plonk' in Windows (works with file=sys.stdout)
\b - backspace - like \r, but returns the pointer 1 character before, 
    not to the start of the line
\x + hex code - special symbol, e.g.
    \xb5 - mu character from greek alphabet
\u + 4 digits or \U + 8 digits - unicode escapes - unicode
    special characters
    Replaceable - \u2603 and \U00002603 are equivalent (display snowman)
\U0001f643 - upside down smile

Alternatively,
    \N{CHAR-NAME} - Unicode escape by official character name
    (like \u and \U)

r'str' - r string - ignore ALL escape sequences in a string
repr('str') - display string literally as it is entered
    same for print('str!r')
    
FLOAT FORMATTING:
print(f'With f string: {x:.2f}') - will print only a number (2 here)
    of decimal places
'''

getattr(object, attr_name)
#^gets attribute of the given class. Same as object.attr_name
isinstance(object, class)
#^shows if a variable is of the given class
#class variable can be given as tuple, e.g. (str, int, Foo)

#%%
import string
string.ascii_letters
#list of all ascii letters
string.ascii_lowercase
string.ascii_uppercase
#upper and lowercase ascii separately


#%%
import textwrap
textwrap.dedent('str')
#^removes indentations from string
#indentations are common in ''' str ''' strings.
#preserves spaces that are too short for indent (<4)

#%%
import heapq
list = [1,2,3]
a = heapq.nlargest(n, list)
b = heapq.nsmallest(n, list)
#^list of largest and smallest elements (max or min but multiple)


#%%
import math
math.sin(x)
math.sinh(x)
math.cos(x)
math.cosh(x)
math.tan(x)
#^add 'a' to get arc, e.g. math.asin(x)
math.e
math.pi
math.inf 
#same as float('inf')

math.nan
#^consts
math.exp(x) = e**x
math.radians(deg)
math.degrees(rad)
#conversion between radians and degrees
math.nextafter(x, y)
#^output the next possible 'x' float in direction to y
math.trunc(float)
#^truncates the float, removing all decimals, preserves float
math.floor(float)
#^same as trunc
math.ceil(float)
#^round to higher value independent of decimals

#%%
import statistics
statistics.mean()
#arithmetic mean
statistics.fmean()
#fast floating point arithmetic mean
#runs faster and always returns float (e.g. 2.0 instead of 2)
statistics.geometric_mean()
#geometric mean
#Geometric mean finds central tendencies using multiplication of data
#   entries instead of addition
statistics.harmonic_mean()
#harmonic mean
#Harmonic mean is a reciprocal of an arithmetic mean (mean()).
#For example, for a, b and c, harmonic mean is:
    #3/(1/a + 1/b + 1/c)

statistics.median()
statistics.median_high()
statistics.median_low()
#median of the entire group, lower number in even len data sets,
#   higher number in even len data sets
statistics.median_grouped(data, interval = int | float)
#Return a median of continuous data set, calculated using 50th percentile.
#Continuous data is represented as '1' = from 0.5 to 1.5.
#Interval optional argument can set interval to:
#    interval = num +- 0.5*interval

#if data is ordinal (supports order operations), but non-numerical (does
#   not support addition-division), use median_high() or median_low()
#
statistics.mode()
#mode (most common value in list) of discrete data
statistics.multimode()
#list of most common values of discrete data if there are several
statistics.pstdev(data, mu)
#Population standard deviation (divide by n number of entries)
statistics.stdev(data)
#Sample standard deviation (divide by n-1 number of sets)
statistics.pvariance()
#Population variance (stdev ^ 2)
statistics.variance()
#Sample variance (stdev ^ 2)
statistics.quantiles(data, n=int)
#^divide data into n ranges of equal probability and output n-1 endpoints
#    of these ranges
statistics.covariance(x,y,/)
#^output covariance of x and y data sets
statistics.correlation(x,y,/)
#^return Pearson's correlation coefficient
statistics.linear_regression()
#prediction of linear regression of 2 data sets
'''For example:
    year = [1971, 1975, 1979, 1982, 1983]
    film_number = list(range(1,6))
    film number here is total films filmed in all previous years
        and current year
    current_year = 2023
    slope, intercept = statistics.linear_regression(year, film_number)
    film_total_now = round(slope*current_year + intercept)
'''


#%%
import getpass
#2-function library, can get name from system and pass from user
getpass.getuser()
#^outputs user login
getpass.getpass(prompt = 'Password: ')
#^requests user to enter password

#%%
#numpy
'''
Array shapes are to be presented in "()" (unless 1D array),with
For 2D array:
(N,M) - N is the number of columns (len of row),
        M - the number of rows (len of col)
For 3D array:
(D,N,M) - D is the array layer
        N is the number of columns (len of row),
        M - the number of rows (len of col)
'''

#flags
arr.flags
'''
‘F_CONTIGUOUS’ (‘F’) - ensure a Fortran-contiguous array
‘C_CONTIGUOUS’ (‘C’) - ensure a C-contiguous array
‘ALIGNED’ (‘A’) - ensure a data-type aligned array
‘WRITEABLE’ (‘W’) - ensure a writable array
‘OWNDATA’ (‘O’) - ensure an array that owns its own data
‘ENSUREARRAY’, (‘E’) - ensure a base array, instead of a subclass
'''
y = np.require(arr, dtype =, requirements = ['F', 'A'...])
#========================

'''
New Numpy Dtypes:
    i - integer
    b - bool
    u - unsigned int
    f - float
    c - complex float
    m - timedelta
    M - datetime
    O - object
    S - string (UTF-8)
    U - Unicode string 
    V - void - fixed chunk of memory for other type
    
    For i, u, f, S and U - size is definable (e.g. i4 or f16)
    
'''
order = 'C', 'F'
#order is a named optional argument that defines if the
#output memory storage order should be
#row first column second (normal C-style) or
# column first for second (Fortran)
np.set_printoptions(precision=3, suppress = True)
'''
Sets print options:
    precision - decimal places
    suppress - if 'e' notation (multiples of 10) should be used
    for very large/small vals
    threshold - max number of elements (default 1000)
    edgeitems - nummber of items in summary in the beginning and end
'''

''' Numpy array properties '''
a.ndim 
#^number of dimensions
a.shape
#^shape of array - (row, column)
a.itemsize
#^size of element, bytes
a.nbytes
#^size of entire array, bytes

#Check if variable is a numpy array of given format:
    (isinstance(arr, numpy.ndarray) and arr.dtype == numpy.float64 and 
    arr.flags.contiguous)

a.size
#or
np.prod(a.shape)
#^^display number of entries

a.base
#^displays the dependency of the array 
#if array is an independent copy - display None

np.who()
#^display all numpy arrays in passed dictionary
#if nothing is passed - display all numpy arrays in namespace


#Custom array creation routines
b = a.copy()
#^removes pointer from b, making it independent of a
#thus, a remains unchanged if b changes
np.arange(start, end, step)
#^range array (excluding end)
np.linspace(start, end, length)
#^linspace with given length
np.logspace(start, end, num=int, endpoint=bool, base=float, dtype)
#^generate a logspace sequence
#starts with base**start, ends with base**end (included if endpoint),
#generates num of samples
np.geomspace(start, end, num=int, endpoint-bool, dtype)
#^similar to geomspace, but start and end are actual start and end
np.diag(arr, k=int)
#^return diagonal of the array
'''
default k=0 - middle array
k>0 - upper diagonal
k<0 - lower diagonal
'''
np.diagflat(arr, k=int)
#^return an array of zeros with given flattened array as a diagonal
#k defines a diagonal (default 0)
np.tri(N,M,k=int,dtype)
#^an array with ones at the diagonal and below it, zeros elsewhere
np.tril(N,M,k=int,dtype)
np.triu(N,M,k=int,dtype)
#^create an upper or lower triangular matrix of given shape and diagonal
np.empty(row, column, ...)
#^uninitialised matrix
np.eye(k=0)
#^identity matrix (NxM),
# k=0 - default diagonal
# k=1 and + - upper diagonal
# k=-1 and - - lower diagonal
#additional - order
np.identity(N)
#^identity matrix of size NxN
np.zeros((shape), dtype=)
#^array of "0"s of given shape
np.ones((shape), dtype=)
#^array of "1"s of given shape
np.full((), val, dtype=)
#^array filled with "val" values of given shape
np.repeat(num, num_of_times)
#^flat array with num x num of times

#Array comparison routines
np.all(a>=val, axis =, )
np.any(a>=val, axis =, )
#^checks conditions, outputs bool array with size and shape of original
#axis can be tuple (if so, will perform on all axis in tuple)
np.isfinite(a)
np.isinf(a)
np.isnan(a)
#^check if a number (or array mask) is finite, infinite, not-a-number
np.isnat(a)
#^check if a number is not-a-time (for M dtype)
np.isneginf(a)
np.isposinf(a)
#
np.iscomplex(a)
np.isreal(a)
#^check if a number (or array mask) is negative/positive infinity
#or if complex or real


np.iscomplexobj(arr)
np.isrealobj(a)
#check if array arr is an array of complex numbers
#True if at least one number is complex
np.isscalar(obj)
'''^
check if an object is scalar or has dimensions
    This function outputs different results in comparison to
    np.ndim(a)==0
    np.ndim(a)==0 is True only for multidimensional (non-flat)
    np arrays and python lists/tuples/sets...
    np.isscalar(a) is only true for numericals and strings
'''

#ARRAY COMPARISONS
np.maximum(arr1, arr2)
#^returm element-wise maxima of 2 arrays 
np.fmax(arr1, arr2)
#^as np.maximum, but in comparison between a number and NaN,
# number is returned
np.amax(arr, axis=)
#^return maximum along a row of an array
np.nanmax([array/matrix])
#^returns max value, ignores NaN
np.maximum(a, b)
#^compares matrices elementwise, returns matrix of max values
a.max(0) and a.max(1)
#^maximum of each column of array and maximum of each row of array
#ALSO
np.min and np.max
#
np.allclose(a,b,rtol=1e-5,atol=1e-8,equal_nan=True)
#^compares 2 arrays. If all values of array 'a' are nearly (+- atol)
#equal to values of 'b', output True
#rtol - relative tolerance
#atol - absolute tolerance
'''
Relative and absolute tolerance

'''
np.isclose(a,b,rtol=1e-5,atol=1e-8,equal_nan=True)
#^return a boolean array of element-wise comparison of 2 arrays
#with tolerance
np.array_equal(a,b,equal_nan=True)
#^outputs True if a and b are equal in shape and all units
np.array_equiv(a,b)
#^outputs True if a and b have all elements equal, as well as
# have shapes that can be reshaped to one another
np.equal(a,b)
np.not_equal(a,b)
np.greater(a,b)
np.less(a,b)
np.greater_equal(a,b)
np.less_equal(a,b)
#^elementwise comparisons of 2 arrays in terms of "a __sign__ b"


#ARRAY MANIPULATION
np.concatenate((a, b), axis = )
#^concat arrays
np.hstack((a,b))
#^ concat along columns (axis = 0)
np.vstack((a,b))
#^ concat along rows (axis = 1)
np.delete(arr, index)
#^deletes entry with index
np.append(arr, value)
#^appends val to array

np.roll(a, shift_index, axis=)
#^swaps parts of array separated by shift_index
np.rot90(a, k=1)
#^rotate matrix CCW k times
np.flip(a, axis =)
#^flip around axis
np.fliplr(a)
#^flips columns of array
#requires at least 2d array
np.flipud(a)
#^flips rows of array
#requires at least 2d array
np.split(array, into)
#^into may be int (splits array in into parts), or array 
#(splits by indexes given in into array)
np.array_split(arr, num_of_arrays)
#^split array into num_of_arrays arrays, length of resultant
# arrays may be different
np.hsplit(arr, column)
#^split matrix in 2, column - 1st column of 2nd array
np.vsplit(arr, row)
#^ same for rows
np.swapaxes(arr, ax1, ax2)
#^swap 2 axes of an arr
np.convolve(a1, a2, mode='full' or 'same' or 'valid')
'''
digital convolution of entries a1 * a2
full = boundary effects, default
same = boundary effects, len = max(a1, a2)
valid = only convolve at complete overlap, no boundaries
'''

np.sign(int or float or complex)
#^outs -1 if negative and 1 if positive
np.fabs(array)
#^elementwise absolute value
np.nan_to_num(array, copy = True, nan = 0.0, posinf = val, neging = -val)
#^replace nan and infinity with numbers. default - nan = 0.0
#posinf = huge number, neginf = very small number
np.trim_zeros(arr, trim=)
#^trim = 'b', 'f' or 'fb' for back, front or front and back

#------------------
np.unique(array)
#outputs array with all unique values of given array
'''
args:
    return_index = False
    return_inverse = False
    return_counts = False
    ^counts every unique value
e.g.
values, counts = np.unique(a, return_counts = True)
print(values)
print(counts)
counts refer to values
can be done with np.dtype(<U1) (str)
'''
#-------------------
np.in1d(arr1, arr2)
#^checks if any from arr2 is in arr1, returns binary array as if arr = (num == arr1)
np.ufunc.accumulate(array, axis)
'''
ufunc = add or multiply
outputs array, where consecutive elements are results 
of ufunc of all previous elements
'''

np.genfromtxt('text.txt', delimiter = ',')
'''
skip_header=0, skip_footer=0, converters=None, missing_values=None, filling_values=None,
 usecols=None, names=None, excludelist=None, deletechars=" !#$%&'()*+, -./:;<=>?@[\\]^{|}~",
 replace_space='_', autostrip=False, case_sensitive=True
'''
a = b.astype('data_type', copy=True/False)
#^data conversion

np.ndarray.tolist(array)
#^converts np array/matrix to Python list (list of lists if matrix input)


np.asarray(pylist, dtype='', like=array)
#^converts python list to numpy array
#default "copy=True"
np.array(pylist, dtype = np.int32)
#^converts python list to numpy array
#has fever options, default "copy=False"
np.asfarray(pylist, dtype=)
#^converts python list to numpy float array

#RANDOM (new)
np.random.default_rng(seed=). ...
#.defaultrng(seed=) is a method that adds seeded or pseudorandom output
#No seed = pseudorandom
np.random.default_rng(seed=).integers(start, stop, (shape),
                                      dtype, endpoint)
#sample ints from interval [start, stop) or 
#   [start, stop] if endpoint=True
#   if (shape) != None - generate np array with this shape
#   else - single value
np.random.default_rng(seed=).random((size), dtype=, out=)
#^will generate a float from the interval [0,1) with uniform distribution
#out is alternative array to place the result
np.random.default_rng(seed=).choice(a, (size), replace=bool, p=1Darray,
                                    axis=, shuffle=bool)
'''
choice generates a random sample from the given array
a - ndarray (int is considered as np.arange(int))
size - number of samples (int or tuple of ints)

'''
np.random.default_rng().shuffle(arr, axis=)
#^shuffles array arr randomly
#default axis 0
np.random.default_rng().binomial(n,p,(size))
#^return a binomial distribution probability function with
#   n number of samples and
#   p success probability
np.random.default_rng().normal(mean, stdev, (shape))
#^return a normal distribution probability
#default mean = 0.0, stdev = 1.0 (standard normal)

np.random.default_rng().bytes(a)
#^return a random bytes


#STATISTICS
np.ptp(axis=)
#^peak to peak (maximum-minimum) for every row/column
np.mean()
#^mean (non-weighed average value)
np.std()
#^standard deviation, sqrt of variance
np.var()
#^variance
np.median()
#^median (the valye in the middle of storted array), if even - avg of 2 middles

#SORT
'''
Sort algorythms (all):
    quicksort - 
    mergesort - 
    heapsort - 
    stable - 
'''
np.sort(a, axis=, kind='heapsort' or 'stable')
#or
a.sort()
#^sort array, default = 'quicksort'
a.sorted()
#^visual display of sorted array, does not change base array (copy=True)

np.sort_complex(a)
#^sorts complex data array, using real numbers to sort
a.argsort(axis=)
#^perform an indirect sort along the given axis
a[a[:,0].argsort(axis=0)]
#^e.g. this function outputs a sorted by its column with index '0'
# array/matrix

#Numpy MATH
np.sin()
np.cos()
np.tan()
np.arcsin()
np.arccos()
np.arctan()
#^numpy equivalents of math library
np.hypot(a,b)
#^returns sqrt(a**2+b**2)
np.degrees()
np.rad2deg()
#^convert radians to degrees
np.radians()
np.deg2rad()
#^convert degrees to radians
np.unwrap(a, discont=, axis=, *, period=)
#^reconstruction of signal's original phase
#the unwrap works if a discontinuity between 2 array points is greater
#than discont parameter
np.sinh()
np.cosh()
np.tanh()
#^hyperbolic functions, have their "arg.." inverses as well
np.around(int, decimals=)
#^evenly round the number to a given number of decimals
np.rint(arr)
#^round array numbers to nearest integer
np.fix()
np.trunc()
#^truncate a number (return float anyway)
np.prod(arr, axis=)
#^return products of elements along given axis
np.sum(arr, axis=)
#^return sum of elements along given axis
np.nanprod(arr, axis=)
np.nansum(arr, axis=)
#^same as prod and sum, but treat NaN as '1'
np.cumprod(arr, axis=)
np.cumsum(arr, axis=)
np.nancumprod()
np.nancumsum()
#^return cumulative sum of entries along given axis
#nan.. treats NaN as '1'
np.diff(arr, n=, axis=)
#^returns difference of element with index k+1 and k
#n is a multiplyer (how many times the difference should be processed)
np.ediff1d(arr, to_begin=, to_end=)
#^np.diff, performed of flat array, elements can be
# appended to output array (to_begin = prefixed, to_end = suffixed)
np.gradient(arr, varargs, edge_order=(1 or 2), axis=)
#^return the gradient of an array, avrargs is spacing between f vals
#edge_order is N-th order accurate difference, default - 1
#multiple axes = same amount of edge_orders in a tuple
np.cross(v1, v2, axisa=, axisb=, axisc=, axis=)
#^perform cross product of 2 vectors
#this generates a vector, perpendicular to both vectors
np.exp(x)
#^returns y = e**x
np.expm1(x)
#^returns y = e**x -1
np.exp2(x)
#^returns y=2**x
np.log(x)
#^returns y = ln(x)
np.log10(x)
np.log2(x)
#^log with base
np.log1p(x)
#^returns np.log(x+1)
np.logaddexp(x1, x2)
#^returns ln(exp(x1) + exp(x2))
#useful for very small numbers in statistics (probabilities)
np.logaddexp2(x1, x2)
#^returns log2(2**x1 + 2**x2)
np.sinc(x)
#returns sin(pi*x)/(pi*x)
np.signbit(arr)
#^returns True if negative number, elementwise
np.copysign(x1, x2)
#^returns x1, signed like x2, elementwise
np.reciprocal(x)
#^returns 1/x
np.angle(complex, degrees = True)
#^return the angle of a complex argumant
#this converts from rectangular to polar and outputs angle only
np.real(val)
#^return the real value of val if val is isinstance(val, complex) == True
np.imag(val)
#^return the imaginary value of val if val is
# isinstance(val, complex) == True
np.conj(arr)
np.conjugate(arr)
#^return a complex-conjugate of a value or array elementwise
np.clip(arr, num1, num2)
#^clip the values in the array
#all values in array become maximum num2 and minimum num1
np.heaviside(x1, x2)
#^returns heaviside step function
#x1 is point of step on x axis
#x2 is y value right at the point of step
np.nan_to_num(arr)
#^convert NaNs to 0, inf to large numbers

np.fft(a)
np.ifft(a)
#fourier and inverse fourier
np.interp(x, xp, np)
#needs to satisfy np.all(np.diff(xp)>0)


#%%
#scipy
import scipy as sp
'''
signal
.sawtooth()
'''
#Voronoi diagram and plot
vor = scipy.spatial.Voronoi(points)
scipy.spatial.voronoi_plot_2d(vor, show_vertices=False, line_colors='orange',
                      line_width=2, line_alpha=0.6, point_size=2)

#%%
#Time series decomposition
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(series, model='additive'[, period=int])
#Period not required if series is Pandas Series
#model = "additive", "multiplicative"


#%%
#pandas
#Jupyter notebooks recommended
import pandas as pd
df = pd.read_csv('text.csv', index_col = 'col_name', na_values = [list])
#^index_col equivalent to df.set_index, but with file read
#na_values - detects which values are considered to be NaN, None, etc.
#parse_dates = ['column'] - sets a column to be read in datetime64 format
#index_col = False - do not read index
#DTYPES
df.info()
#^shows size of resultant matrix and data types of columns
.dtypes
#^describes data types (np-based) of each column in dataframe
.astype('dtype')
#^set df columns type
df['col_name'].astype('type')
#converts data type of a column to new data type (e.g. float to str)
df['Date'] = pd.to_datetime(df['Date'])
#^set column dtype to datetime64

#OPTIONS
pd.set_option('display.max_columns', 85)
pd.get_option('arg')
pd.reset_option(option)

'''
options:
    display.chop_threshold, float - will consider values lower than 0
    display.date_dayfirst, bool
    display.date_yearfirst, bool
    display.encoding, bool
    display.max_columns, int
    display.max_colwidth, int or none
    display.max_rows, int
    display.max_categories, int
    display.max_info_columns, int
    display.max_info_rows, int
    display.precision, int - number of decimal places in float to display
    display.width, None - (for console only), otherwise int
    mode.copy_on_write, bool
    styler.format.decimal, str - how decimal point is displayed - default '.'
    styler.format.precision, int - same as display.precision???
    styler.render.repr, 'html' or 'latex' - for Jupyter notebook only
    styler.format.thousands, str - 
    display.latex.repr, bool - to display as LaTEX or not (for Jupyter)
'''
df.head(int)
#^displays int rows from beginning, None=5
df.tail(int)
#^same, from end
df['column_name'] or df.column_name
#^displays column 'column_name'
df[['column_name1', 'column_name2']]
#^miltiple columns as a list

#SIZE AND SHAPE
df.columns
#^display all column names as numpy array
df.size
#^displays a number of all entries in a dataframe
df.ndims
#^returns the number of dataframe dimensions (usually 2)
df.shape
#^returns the counter of (rows, columns) tuple

#RENAMING COLUMNS
df.columns=['new_col1_name', 'new_col2_name', 'new_col3_name',...]
#^renaming all columns
df.rename(columns = ({'old_name_col1': 'new_name_col1',
                      'old_name_col2': 'new_name_col2'}),
          inplace = True)
#^renames chosen columns

df.columns = [x.upper for x in df.columns]
#^modifies all column names

#DATAFRAME INDEX ACCESSING
df.loc[[index1, index2], ['column_name', 'column_name2']]
#^picking values from dataframe
df.iloc[0]
#^access row number i, even if key (index) is nonstandard
df.iloc[[0,1,...]]
#^access row index (e.g. 0 here)
#no brackets when slicing (e.g. 0:6)

#DATAFRAME CONCATENATION
df = pd.merge(df1, df2, on=['column1', 'column2'])
#^hstack with additional parameters:
'''
By column:

on=['col1', 'col2'] :
    merge the dataframes by given columns, only if entries in both databases
    are equal (by default).
if on='ID', and df2 has multiple repeating IDs (non-primary-key), 'merge'
    will merge df1 with df2 one-to-many.    
suffixes=['_l', '_r'] :
    columns of the same name from different dataframes will be appended
    with respective suffixes
    Can be used with "left_on='', right_on = '' " if columns have different
    names, so that renaming is unnecessary.
left_index = True, right_index = True :
    Join on indexes instead of columns, can be combined
    with left_on='', right_on=''
By type:
how = 'inner' (default without "how" kwarg) :
    keep only rows that have vals in both columns
how = 'outer' :
    keep everything
how = 'left' :
    keep everything from left and 'inner'
how = 'right' :
    keep everything from right and 'inner'
'''

pd.concat(df1, df2, axis=)
#^np.stack in Pandas
#axis = 0 - stack rows (vstack)
#axis = 1 - stack columns (hstack)


#INDEX MANIPULATION
df.set_index('column', inplace=True)
#^sets chosen column to be index. If False, does not change
# dataframe, only shows hot it would look
df.reset_index(inplace=True)
#^resets index, creating a new one, representing a simple range of nums
df.sort_index(ascending=True)
#^sorts dataframe according to index
#ascending = False == reverse = True

#FILTERS
df['column_name'] == 'entry_name'
#^filter conditioning
df.loc[df['column_name'] == 'entry_name']
#^filter applied
df.loc[~df['column_name'] == 'entry_name']
#^NEGATED filter applied (shows all except condition)
df.loc[df['column_name'].isin([list])]
#filter for several entries
filt = df['column_name'].isin(list_of_values)
#^displays all entries which have a value from 'list_of_values'
# in column
df[].str.contains("string", na=False)
#^checks if string contains symbol sequence, na declares if
# NaN should be handled

df.loc[index, 'column_name'] = 'new_val'
#or
df.at[index, 'column_name'] = 'new_val'
#^replaces value in dataframe with new value
#.at is for single value replacement only

#FUNCTION APPLICATION
df['column_name'].apply(func)
#^apply a stat function (e.g. len) to a column, outputting results of this column
#can apply custom 'def' functions and lambda functions
df.applymap(func)
#^applies function to every entry in dataframe,
# does not work with series
df.transform(func)
#^applymap that is applicable for Series and .groupby().
# Overall more versatile

df['column name'].map({'old_name1': 'new_name1', 'old_name2': 'new_name2'})
#^maps new values to the column. Undeclared values become 'NaN'
df['column name'].replace({'old_name1': 'new_name1', 'old_name2': 'new_name2'})
#^maps new values to the column. Undeclared values remain and do not change

df['column_name'] = ...
#^REQUIRED TO APPLY CHANGES TO ACTUAL DATAFRAME

#REMOVING ROWS/COLUMNS
df.drop(columns = [list])
#^removes column from the list
df.drop(index = df[df['col_name'] == 'entry'].index)
#drops all rows with filter given


#SPLITTING ROWS/COLUMNS
df[['col1', 'col2']] = df['col'].str.split(' ', expand=True)
#splits a column into 2, separating entries by a given separator
df.droplevel()
"""
Drops columns from multiindex data frames
.droplevel(0) will drom column 0 (leftmost index)
.droplevel(1) will drop 2nd column (secondary index)
axis=1 - will be removing row indexes from multiindex columns 
"""


#SORTING
df.sort_values(by=['col_name', 'sec_column_name'],
               ascending=[False, True], inplace=True)
#Ascending True by default, secondary  column is secondary
# sorting index if primary vals are equal
#order corresponds to column if given as list
#inplace=True changes actual list
df.sort_index()
#^sorts dataframe in primary order of index
df['col_name'].nlargest(int)
df['col_name'].nsmallest(int)
#^shows number (int) of largest and smallest entries, only shows
# selected columns
df.nlargest(int, 'col_name')
df.nsmallest(int, 'col_name')
#^shows number (int) of largest and smallest entries, shows entire dataframe

#STATISTICS
df['col_name'].median()
'''
median can be replaced with:
    count - counts rows with non-NaN values
    mean
    std
    min
    max
    nunique - count of unique entries
'''
df.describe()
#^outputs all statistical calculations of all numerical columns
df.agg(['mean', 'median',...], axis='columns')
#^retrieve several characteristical values in one func
df['col_name'].unique()
#^displays unique entries in column as list
df[column].value_counts(normalize=True)
#^counts all entries, collapses entry list
#if normalise = True, shows values as percentile (part of 1)

#GROUPBY
grp = df.groupby(['col_name'])
#^grouping the column
grp.get_group('col_entry')
#^displays all entries with given col_entry in col_name
grp['col_name2'].value_counts()
#group of entry values creates combination of 2 columns and displays
# statistical relation
grp['col_name2'].agg(['mean', 'median',...])
#displays multiple stat parameters for chosen combination
grp['col_name2'].apply(func)
#where func can be lambda
#return x.str.contains('word').sum()
#unlike dataframes, groups accept "apply" and func instead of .str directly
grp.unstack()
#^unstacks multilayered groupby object. Used for plotting.
pd.concat([group1, group2], axis='columns', sort=False)
#^concatenate groups in new group

#HANDLING NaN, None, etc.
df.dropna(axis = 'index', how="any")
#or
df.dropna()
#^discards any rows with NaN, None etc. in them, axis = 'index', how="any" are default and can be discarded
#axis = 'columns' - will drop columns if they have missing values
#how = 'any' - drop if any of values are None NaN etc.
#how = 'all' - drop if all entries are None NaN etc.
df.dropna(axis = 'index', how='any', subset = ['col_name'])
#if 'subset' is given, only analyses given column
df.fillna(value, method='string', axis, inplace, limit)
'''
value - value to fill in instead of NaN
    Can get a dictionary {'row_or_column_name':value}
method : ffill - NaNs are replaced with previous non-NaN values along the axis
        backfill/bfill -  NaNs are replaced with next non-NaN value
        along the axis
limit - how many values are replaced along the axis (consecutive)
'''
df.interpolate(method = 'string', axis=, limit=, inplace=bool, limit_area = )
'''
method : linear - ignore indexes, treat vals as equally spaced
        time - 
        pad - fill using existing vals - like 'fillna'
        nearest, zero, slinear, quadratic, cubic, polynomial, spline,
        pchip, cubicspline- those of scipy.linalg.inter1d()
limit - maximum number of consecutive values to fill
limit_area - inside - only values between known values - interpolate
            outside - only values on the edges - extrapolate
            default is both
'''

df.isna()
#^dataframe mask that displays if entry is considered NaN, for every entry
df.notna()
#^all values for which .isna() is False

#MULTIINDEX
index = pd.MultiIndex.from_tuples(list_of_tuples, names = ['name1', 'name2'])
#^create an index, name1 and name2 are respectively column
# names for 1st and 2nd tuple element
#Later,
pd.DataFrame(index=index)
#set multiindex
df.unstack(level = 0)
#^remove index (equiv to df.dropindex(0))
#(level = 1) for secondary index

#PLOTTING
df.plot(x, y, kind='string', figsize=[width_inch, height_inch], grid=bool, 
        legend = bool, xticks = [], yticks = [], xlim = (left, right), 
        ylim=(bottom ,top), xlabel='string', ylabel='string', include_bool = bool)
'''
Plot a graph via matplotlib.pyplot
x and y must be Series/columns
kind :
    line
    bar
    barh - horizontal bar
    hist - histogram
    box - boxplot
    kde/density - kernel density estimation
    area
    pie - pie chart
    scatter - scatterplot
    hexbin
'''

#TIME SERIES
pd.Timestamp('2022-11-22')
timerange = pd.date_range(start='2022-11-22', periods=120, freq='D')
#^generates a series with 120 dates starting from 'start' with
# daily frequency (each day)
timerange.to_period('M')
#^compress datetime form to mm-yyyy, dropping dates
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
#^extracting month/year from a full date
#alternative:
df['year'] = pd.DatetimeIndex(df['date']).year
#-||-


#--------------
rng = np.random.default_rng()
ar = rng.uniform(0.0, 1.0, timerange.shape[0])
df = pd.DataFrame({'vals':ar}, index=timerange)
df.index.name = 'date'
sns.plot(data=df, x='date', y='value')
#--------------

df.explode(['column'], ignore_index=bool)
#^splits rows if their entries are list, creating additional rows with list
#entries
pd.get_dummies(df, prefix=[], dummy_na = bool, columns = [], drop_first=bool)
'''^converts categorical variables into dummy (indicator) variables
important for categories conversion before learning model implementation
data column is converted to named columns with 0/1 binary values
dummy_na - if true, will create a column indicating True (1) if value
 in row is np.nan
'''
#SAVING TO CSV
df.to_csv('df.csv')
#index = False - do not save index


#%%
#pip install -U scikit-learn
#Creation of the prediction model using Pandas and Scikit Learn
#REGRESSIONS
from sklearn.linear_model import LinearRegression, LogisticRegression
lin_reg = LinearRegression()
log_reg = LogisticRegression(max_iter=1000)
lin_reg.fit(train_data_X, train_data_Y)
lin_reg.predict(test_data_X)


#TRAIN-TEST SPLIT
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(training_data, check_data,
                                                    test_size=0.25, random_state=2)

#^division of data into parts for model training and testing purposes

#TFIDF PROCESSING
#nltk is an additional library to be used for text processing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer, LabelEncoder, normalize, PolynomialFeatures
tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.5, ngram_range=(1,2),
                        stop_words='english', norm='l2', binary=False)

#KNN CLASSIFIER
#see K Nearest Neighbors
from sklearn.neighbors import KNeighborsClassifier
KNN = KNeighborsClassifier(n_neighbors = 5, weights = ['uniform' or 'distance'])
KNN.fit(X_train, y_train)
y_test = KNN.predict(X_test)
KNN.score(X_test, y_test)
#score can be evaluated from train-test split


#NAIVE BAYES
from sklearn.naive_bayes import GaussianNB
GNB = GaussianNB()
GNB.fit(X_train, y_train)
y_test = GNB.predict(X_test)
GNB.score(X_test, y_test)


#PERCEPTRON
from sklearn.linear_model import Perceptron
percep = Perceptron(tol=1e-3)
#equivalent to Stochaic Gradient Descent with args:
    from sklearn.linear_model import SGDClassifier
    percep = SGDClassifier(loss='perceptron', eta0=1,
                           learning_rate='constant', penalty=None)
percep.fit(X_train, y_train)
percep.score(X_train, y_train)

#SUPPORT VECTOR MACHINES
#Classification
from sklearn import svm
SVMClas = svm.SVC()
#optional argument - kernel:
#   'linear' - default
#   'polynomial'
#   'rbf'
#   'sigmoid'
#   or any python function (input 2 vectors, output 1 vector)
SVMClas.fit(X_train, y_train)
SVMClas.predict(X_test)
SVMClas.support_vectors_
#^get support vectors
SVMClas.support_
#^get indices of support vectors

#Cross validation
from sklearn.model_selection import GridSearchCV
param_grid = [
    {'C':[0.5, 1, 10, 100], #must be >0
     'gamma': ['scale', 1, 0.1, 0.01, 0.001, 0.0001],
     'kernel': ['rbf']}]
#defaults are C=1 and gamma = 'scale', and they are to be included (recommended)
optimal_params = GridSearchCV(svm.SVC(), param_grid,
                              cv=5, #optional - None = '5' default
                              scoring='accuracy', verbose=0 #3 for max data
                              )
#verbose to 0 for silent mode, optional
#scoring named options:
'''['accuracy', 'adjusted_mutual_info_score', 'adjusted_rand_score',
    'average_precision', 'balanced_accuracy', 'completeness_score',
    'explained_variance', 'f1', 'f1_macro', 'f1_micro', 'f1_samples',
    'f1_weighted', 'fowlkes_mallows_score', 'homogeneity_score',
    'jaccard', 'jaccard_macro', 'jaccard_micro', 'jaccard_samples',
    'jaccard_weighted', 'matthews_corrcoef', 'max_error', 
    'mutual_info_score', 'neg_brier_score', 'neg_log_loss', 
    'neg_mean_absolute_error', 'neg_mean_absolute_percentage_error', 
    'neg_mean_gamma_deviance', 'neg_mean_poisson_deviance', 
    'neg_mean_squared_error', 'neg_mean_squared_log_error', 
    'neg_median_absolute_error', 'neg_negative_likelihood_ratio', 
    'neg_root_mean_squared_error', 'normalized_mutual_info_score', 
    'positive_likelihood_ratio', 'precision', 'precision_macro', 
    'precision_micro', 'precision_samples', 'precision_weighted', 
    'r2', 'rand_score', 'recall', 'recall_macro', 'recall_micro', 
    'recall_samples', 'recall_weighted', 'roc_auc', 'roc_auc_ovo', 
    'roc_auc_ovo_weighted', 'roc_auc_ovr', 'roc_auc_ovr_weighted',
    'top_k_accuracy', 'v_measure_score']'''
    
optimal_params.fit(X_train, y_train)
#outputs optimal variables from GridSearchCV

#Regression
from sklearn import svm
SVMRegr = svm.SVR()
SVMRegr.fit(X_train, y_train)
SVMRegr.predict(X_test)


#EVALUATION OF MODELS
from sklearn.metrics import accuracy_score, confusion_matrix
accuracy_score(y_true, y_pred)
#^displays percentage of accuracy (in parts of 1)
confusion_matrix(y_true, y_pred)
#^displays false and true 0/1 values in the form [[true_1, false_1],[false_0, true_0]]

#OTHER
#nltk is an additional library to be used for text processing
sklearn.metrics.pairwise.cosine_similarity(1-2 2d matrices
                                           of shape (n_samples_X, n_features),
                                           (n_samples_Y, n_features))
#^perform cosine similarity of 2 2D matrices
#if Y=None, out is pairwise similarities between all samples in X


#%%
#plt (matplotlib.pyplot)

import matplotlib.pyplot as plt
print(plt.style.available)
plt.style.use('seaborn')

plt.xkcd()
#^funky hand-drawn style
plt.plot(data_x, data_y)
#basic plot
'''
optional args:
    label=                --- instead of plt.legend
    [marker][line][color]
    linestyle=
    '-',  '--',  '-.',  ':'
    color=
    'r','g','b' = RGB colors
    'c','m','y','k' - CMYK colors,  'w' - white
    much more colors are supported, incl hex #ffffff 
    marker=
    '.','o',''...
    linewidth= (in mm)
'''
plt.title('Title')
#plot title
plt.xlabel('Label of x')
plt.ylabel('Label of y')
#axis labels
plt.legend(['Legend 1', 'Legend 2'])
#plot descriptions, correspnd to plt.plot accordingly - Legend 1
# to first plot, 2 - to second, etc.
#if labels already given in args - run empty
plt.grid(visible=True, which="major", axis='both')
#which='major', 'minor', 'both'
#axis='both', 'x', 'y'
#many more kwargs
plt.bar(x)
#bar chart, takes similar args and kwargs to plt.plot
plt.xticks(ticks=actual_list, labels=replace_list)
plt.yticks(ticks=actual_list, labels=replace_list)
#replaces labels on a chart/graph with new labels
plt.figure(figsize=(12,6))
#set figure to 12 inches wide, 6 inches high

plt.tight_layout()
plt.show()
plt.savefig('name.png')
#^full path can be accepted

#%%
import seaborn as sns
#convention
#unconventional - import seaborn as sb
sns.barplot(data = df, x = 'column1', y = 'column2')
#^bar chart with defined columns from data= data frame to be x and y axis respectively
sns.displot(data=df, x='col1')
#^distribution plot
sns.jointplot(data=df, x='indep_var_col', y='dep_var_col',
              hue='additional_claffified_col')
# this outputs a scatterplot with additional distribution patterns along the 
# edges of the plot. Hue defines the additional coloring (classification) for 
# a column that has several categories (can be expanded with pd.get_dummies)

sns.heatmap(data, vmin=, vmax=, center=, robust=, annot=, fmt=, kwargs)
'''
Creates a heatmap plot with vmin and vmax-set color codes if specified, 
center color code value if specified, robust mode if vmax and vmin not specified
(optional), annotations, string formatting (default .2g, prefer .2f)
'''

#SETTING IMAGE PARAMETERS
img  = sns.barplot(data=, x=, y=, hue=)
img.set_xticklabels(img.get_xticklabels(), rotation = 45, ha='right')
#^rotates x labels such that they do not overlap
img.set(xlabel='', ylabel='')
#^sets label naming



#%%
import nltk
#natural language processing toolkit

'''
Run: 
    import nltk
    nltk.download('punkt')
To download required tools
'''

#TEXT TOKENIZING
from nltk.tokenize import sent_tokenize, word_tokenize
sample_string = '''\
    She grappled with her being from the beginning. A lesson hid in everything that moved and everything that did not. What separated the two? Why did it move, why did it not? A life, she determined, was the difference. But she moved, and would never not, for that was my duty. Was she alive? She did not know, and I could not answer her.
'''
list_of_sentences = sent_tokenize(sample_string)
#^splits a text string into dot-separated sentences in a list
list_of_words = word_tokenize(sample_string)
#^split a text string into separate words, sustaining '.', ',', "'s" as words

#STOPWORDS
from nltk.corpus import stopwords
#nltk.download('stopwords')
stopwords_ = set(stopwords.words('english'))

"""
Other languages:
    german
    russian
    All in:
    print(stopwords.fileids())
    
"""

#STEMMING
#Stemming returns all words reduced to their roots, which is useful
# for machine learning
# Lemmatizing is better in general
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in list_of_words]


#TAGGING parts of speech
#nltk.download(['averaged_perceptron_tagger', 'tagsets'])

'''
Examples of parts of speech described by nltk are nouns, pronouns, adjectives, 
verbs, adverbs, prepositions, conjunctions, interjections
'''
tagged_list = nltk.pos_tag(list_of_words)
#^generates a list of tuples [('word', 'part of speech tag'), ...]
#to see what the codes mean:
print(nltk.help.upenn_tagset())

#LEMMATIZING
'''
Lemmatizing is a form of soft stemming, where the words are not reduced to their
basic roots. Instead, they are truncated to remove multiplicatives and 
'''
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemma_words = [lemmatizer.lemmatize(word) for word in list_of_words]
#lemmatizer.lemmatize(word, pos='a')
#pos='a' (default is 'n') in this case means that the words will be returned as default form
#instead of originally comparative or superlative (e.g. worse, worst -> bad)

#NAMED ENTITY RECOGNITION (NER)
#nltk.download('maxent_ne_chunker')
#nltk.download('words')
#nltk.download('wordnet')
tree = nltk.ne_chunk(tagged_list)
#^recognise named entities
#optional posarg : binary = True : classifies all named entities as NE, not 
#specifying actual type of NE
tree.draw()
#^draw a resultant NER tree

#FREQUENCY DISTRIBUTION
from nltk import FreqDist
freq_distribution = FreqDist(text)
#^gets a list of all unique words with respective word counts
freq_distribution.most_common(20)
#^gets top int values (e.g. 20)


#OTHER
text.concordance('word')
#^finds every time the word is present in the text
text.dispersion_plot(['word1', 'word2', 'word3', 'word4', 'word5'])
#^displays the dispersion plot of frequency of each word's presence in the text


#%%
#os.path
path.isfile('')
path.isdir('')
#^insert path - bool out
path.exists()
#^returns if a file exists
path.join("","")
path.expanduser('~')
#^ '~' alias is only usable in BASH and refers to the current user.
#expanduser transforms it to Windows CMD readable format.

#%%
#os
os.getcwd()
#^current working directory
os.chdir()
#^change directory
os.listdir()

'''
os.mkdir()
os.makedirs() <- better than mkdir
os.rmdir()
os.removedirs() <- better than rmdir
'''

os.rename(src, dst)
#^rename folder

os.stat().statname()
''' ^statistics on file - statname optional

st_mtime - modification time (s)
st_ctime - creation time (s)
st_atime - access time (s)
st_mode - file type & permissions
st_size - file size, 
'''
os.walk('')
#^displays all contained files and directories higher up the given path
#gives out: dirpaths, dirnames, filenames
#iterator required to output data
os.environ
#print to get all environment variables as dictionary
os.environ.get('')
#^get environment variable
os.getenv('')
#^same
os.remove(path)
#^deletes file
os.getpid()
#^get process ID of current process
os.kill(pid)
#^kills process with given pid
os.system("path")
#^physically open an application or file - LINUX ONLY

'''
WINDOWS:
    import subprocess
    out_file = "PATH"
    subprocess.Popen(["explorer", out_file],
                     creationflags=subprocess.DETACHED_PROCESS)
'''

#%%
import tempfile
temp = tempfile.NamedTemporaryFile(prefix='', suffix='')
#^creates named tempfile with given suffix and prefix, default IO mode - 'w+b'
temp.write()
#^writes anything to file
temp.seek(0)
#^move pointer to beginning
temp.read()
temp.close()

#%%
#random module allows for seeded insecure pseudorandom numbers
#secrets module allows for truely random numbers that
#   can be used for security applications
import random
import secrets
random.randrange(start, stop, step)
#^outputs random number from start to stop-step, 
#   step is optional and 1 by default
random.randint(a, b)
#^outputs a random integer from a to b, including b
secrets.randbelow(upper)
#^outputs a truly random int from range[0,upper)
random.choice(list_of_values)
secrets.choice(list_of_values)
#^choose a random value from a list
random.choice(list_of_values, weights = list, cum_weights = list, k=int)
#^assigns probability density (weights) or
#   cumulative probability density(cum_weights) to list_of_values
#    and returns list of k values, chosen randomly according to weights

random.shuffle(list)
#^shuffles list values randomly
#ususable for immutable arrays - use random.sample(x, k = len(x)) instead
random.sample(list, k)
#^samples k random values from list, raises error if k>len(list)
random.random()
#^returns random float value from [0,1)
random.uniform(a,b)
#^returns a random float between a and b
random.expovariate(lambd)
#^returns a random number that follows exponential distribution
#    with lambda=1/desired_mean
random.gauss(mu=0.0, sigma=1.0)
random.normalvariate(mu=0.0, sigma=1.0)
#^normal distribution, no given value = standard normal distribution
#gauss is faster but not safe for multithreading
secrets.token_bytes(nbytes)
#^return nbytes bytes, which are truly random
secrets.token_hex(nhex)
#^return nhex*2 symbols from range 0-f
secrets.token_urlsafe(nbytes)
#^return nbytes bytes of URL-safe symbols, total symbols are approx 
#   1.3*nbytes
# nbytes = 32 is recommended for safe usage
secrets.compare_digest(a, b)
#^compare a and b and return True if they are equal
#uses a method that is safe against timing attacks


#%%
import shutil
import os
#os and shutil work close together
#src and dest must be paths of raw string format (r"path")
os.chdir(src)
shutil.copy(src, dest)
#^only copies files, not folders
#files are overwritten if they exist in the "dest" directory

shutil.move(src, dest)
#^only moves files, not folders
#files cannot be moved if "dest" contains them
#can be overwritten by using full path /w file name

shutil.rmtree(path)
#^remove directory and everything inside it recursively

shutil.which('command_from_cmd')
#^returns path to the file, executed by the command

#%%
#Pathlib - more functionality than shutil
from pathlib import *
p = Path('.')
#^ list subdirectories
PurePath()
list(p.glob('**/*.py'))
#^ list all .py files in subdirectory tree
.exists()
#file/dir exists bool
.isdir()
#dir exists bool
.isfile()
#file exists bool

#%%
from ctypes import *
windll.kernel32
#^returns contents of kernel32.dll
cdll.msvcrt
#cdll - cdecl calling convention
#windll - stdcall calling convention
#
windll.kernel32.GetModuleHandleA
#.GetModuleHandleA is a function call to imported windll or cdll
getattr(cdll.msvcrt, '??2@YAPAXI@Z')
#^same as .getModule, but works with functions that are not properly
# read by python
cdll.kernel32[1]
#^call first function, [0] would output error
libc.time(None)
#^outputs current time (as timestamp)

byref()
#^function argument


#%%
import sys
#library for system variables manipulation
sys.getsizeof(object)
#^displays size in bytes
sys.exit(arg)
#^exits the script, if arg=0 or None, script is considered success, if "1" - failure
sys.argv[1]
#^CLI input command, can be assigned to variable to be launched with BASH/CMD
#ARGPARSE is more recommended
sys.stderr()
sys.stdout()
#^output of either normal output or error back to CLI
sys.version_info()
#^checks python version, outputs list with data about python version
sys.platform
#^outputs current platform:
    '''
    linux or linux2 - Linux
    win32 - Windows
    darwin - MacOS
    '''

#%%
import time
time.sleep(seconds)
#^wait for "seconds" time (program does nothing)



#%%
#pipreqs external library
"""
pipreqs path/proj.py
saves requirements.txt in the same directory

"""
#%%
#https://httpbin.org/ - site to test requests
#html requests:
    
import requests
with requests.Session():
    #all commands here
    pass
#^requests should be wrapped into self-closing subprocess like
#txt or csv read
page = requests.get('url')
#^get access to a webpage
#If a webpage is text:
page.text
#is the webpage contents displayed as text
ptxt = page.text
#If a webpage is image only:
page.content
#is the webpage contents displayed as bytes

#Image from website can be written to image file:
with open('img.png', 'wb') as img:
    img.write(page.content)
#is saved in .py file directory
page.status_code
#2xx - ok, 3xx - ok, but redirects, 4xx - client error, 5xx - server error
''' 
200 - normal operation
401 - unauthorized response
404 - page not found
'''
page.ok
#bool that checks status code and outs True id code 2xx or 3xx
#   and False if code is 4xx or 5xx
page.headers
#displays all needed information about page formatting


url_params = {'page': 2, 'count': 25}
page = requests.get('url', params=url_params)
#^requests can accept additional parameters,
#   which will modify the original URL as it is done when navigating
#   through pages (e.g...com/test?page=2&count=25 here)
page.url
#displays the actual URL sent by requests lib
''' In order to POST data to the URL: '''
userdata = {'username': 'John', 'password':'1234qwerty'}
page = requests.post('url/post', data = userdata)
print(page.text)
#If response is JSON, .json() method can be used to transform
#   raw text to dictionary:
indict = page.json()
#indict.__class__.__name__ == dict
#So key accessing can be used to extract data


#Authentification request:
page = request.get('url/username/password', auth=('username', 'password'))
page.status_code
#200 if success, 401 if wrong auth data
#timeout=int in seconds - additional arg of requests.get, post, etc.
#if page does not respond for longer than timeout, return ReadTimeout
#   exception

#%%
#scraping and parsing websites
from bs4 import BeautifulSoup
import lxml
import html5lib
import requests

with open('file.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')
#^import downloaded html file as bs4 type text
soup.prettify()
#^shows html file in a nice readable form, not needed for parsing
#   in general
soup.title
#^title of the webpage
soup.title.name
soup.title.string
souup.title.parent.name
soup.p
#^different commands to extract needed content
soup.find('div', class_='footer')
#^finds the first footer div
soup.find_all('div', class_='class_name')
#^finds all footer div
soup.find('div').get('href')
soup.find(id='element_id').get('href')
#^get element of the given tag

#%%
import itertools
#itertools objects should be iterated
itertools.combinations([list], length_of_list)

itertools.permutations([list], length_of_list)

#^process all combinations from a list. Combination length is length_of_lists
itertools.product([list], repeat=2)
#or
itertools.product([list], string, [list],...)
#returns valuewise combinations of all chars of all strings

itertools.count(int)
itertools.cycle([list])
itertools.repeat([list], num_of_times)
#^yield generators

itertools.chain(iterables)
#^joins all contents into 1 string

'''
count - starts count with number given, num++ each generation until inf
cycle - generates list until end, then repeats, inf
repeat - cycle, but not inf (not endless repetition)
'''
#%%
#datetime
import datetime
#datetime.date()
print(datetime.date.today())
#^today date
'''
.weekday
returns Mon = 0...Sun = 6
.isoweekday
returns Mon = 1...Sun = 7

'''
timedel = datetime.timedelta(hours = 8)
#^date period in days (e.g. 7 days)
print(datetime.timezone(timedel))
datetime.fromtimestamp()
#^convert age in seconds to initial datetime (useful for os.stat().st_...time)
'''
import pytz - timezones - REQUIRES INSTALLATION
pytz.all_timezones
pytz.timezone('timezone from all_timezones')
With pytz:
    datetime.datetime(year, month...second, tzinfo=pytz.UTC)
    dt.now = datetime.datetime.now(tz = pytz.UTC)
.strftime('code')
^sets up display property, codes available online
.strptime(var, 'code')
^converts given date (var) in code format to datetime readable value
code format must be that for .strftime
'''
#%%
#platform - Current OS in use detection
import platform
print(platform.platform())
#^full description of current OS
print(platform.system())
#^current OS name (Windows, Linux, etc.)
print(platform.release())
#^System version (e.g. 11 for Windows, 6.2.0-32-generic for Linux)
print(platform.version())
#^detailed system version info

#%%
#inspect
import matplotlib.pyplot as plt
import inspect
print(inspect.getfullargspec(plt.plot))
#inspects method, returns input args of the method


#%%
#gtts
import gtts as gTTS
sound = gTTS('hello', lang='en', tld='com.au')
sound.save("path\file.mp3")

#%%
import textract
#REQUIRES INSTALLATION, there might be better module
text = textract.process('path/file.doc/docx')
text = text.decode('encoding')
#^normally utf-8
#^extracts text from doc or docx file
#%%
import validators
#raises ValidationError (warning) if False
#input is string
validators.url('https://www.google.com')
validators.btc_address('')
validators.card_number('')
validators.email('')
validators.iban('')
validators.ipv4('') #ipv6 too
validators.mac_address('')
validators.sha256('') #512 too
validators.visa('') #union pay, mastercard

#%%
#Zipfile and rarfile
#Open .zip file and extract it
import zipfile
with zipfile.ZipFile('path') as f:
    f.extractall('path_to_extracted_folder')
import rarfile
with rarfile.RarFile('path') as f:
    f.extractall('path_to_extracted_folder')    
#%%
import unicodedata
unicodedata.name('a')
#^output unicode name of a char


#%%
import dis
dis.dis(function)
#python bytecode disassembler - shows literal interpreter actions
#

#%%
import pkg_resources
#library to check if the module is installed
print(pkg_resources.get_distribution('numpy'))
#will output numpy and its version if installed, 
#will raise DistributionNotFound error if module is not installed

#%%
from tqdm import tqdm
import time
for i in tqdm(range(1000)):
    i = 5
    time.sleep(0.01)

#%%
#temp



#%%




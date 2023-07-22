#This file was created by Evgeny "VespenGas" Manturov
#It contains all useful commands from the most important python libraries

#https://bootstrap.pypa.io/ - this website allows the automated download of pip, setuptools, etc.



#%%
#Standard modules
print(dir()) #insert module to see all commands
round(float, decimals)
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


#%%
#oop
#decorators
"""
@classmethod
^ (cls, ...)
@staticmethod 
^ (no self)
"""
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
#super().__init__(var_names)


#strings
#strings cannot be modified
'''
new_string = string.strip() - removes spaces
new_string = string.removeprefix() - removes before
new_string = string.removesuffix() - removes after
'''

getattr(object, attr_name)
#^gets attribute of the given class


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

#%%
import getpass
#2-function library, can get name from system and pass from user
getpass.getuser()
#^outputs user login
getpass.getpass(prompt = 'Password: ')
#^requests user to enter password

#%%
#numpy

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
a = np.array([[],[]], dtype = np.int32)
a.ndim 
#^number of dimensions
a.shape
#^shape of array - (row, column)
a.itemsize
#^size of element, bytes
a.nbytes
#^size of entire array, bytes
a.size
#or
np.prod(a.shape)
#^^displays number of entries
np.full((2,2), 1, dtype = np.int32)
#^full array of ((row, column), value_to_fill)
b = a.copy()
#^removes pointer from b, making it independant of a
np.all(a>=val, axis =, out: None = "None")
np.any(a>=val, axis =, out: None = "None")
#^checks conditions, outputs bool array 

np.arange(start, end, step)
#^range array
np.linspace(start, end, length)

#np.empty(row, column)
#^uninitialised matrix
np.nditer()
#^iterates through array
np.eye()
#^identity matrix
np.repeat(num, num_of_times)
#^flat array with num x num of times
np.random.rand(rows, columns)
#^creates matrix with random decimals, values = 0--1
np.random.random_sample(shape)
#^same as random.rand, but takes tuple with shape, e.g. a.shape
np.random.randint(start_val, stop_val, size=())
#^if size not given, out = 1 number from start to stop (int)
#default start = 0, size = shape of array
np.trim_zeros(arr, trim)
#^trim = 'b', 'f' or 'fb' for back, front or front and back


np.nanmax([array/matrix])
#^returns max value, ignores NaN
np.maximum(a, b)
#^compares matrices elementwise, returns matrix of max values
a.max(0) and a.max(1)
#^maximum of each colunn of array and maximum of each row of array
#ALSO
np.min and np.max

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
#^into may be int (splits array in into parts), or array (splits by indexes given in into array)
np.array_split(arr, num_of_arrays)
#^split array into num_of_arrays arrays, length of resultant arrays may be different
np.hsplit(arr, column)
#^split matrix in 2, column - 1st column of 2nd array
np.vsplit(arr, row)
#^ same for rows
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
outputs array, where consecutive elements are results of ufunc of all previous elements
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
#^converts np array/matrix to Python list (nested if matrix)
np.asarray(pylist, dtype='', like=array)
#^converts python list to numpy array

#STATISTICS
np.ptp(axis=)
#^peak to peak (maximum-minimum) for every row/column
np.mean()
#^mean (non-weight average value)
np.std()
#^standard deviation, sqrt of variance
np.var()
#^variance
np.median()
#^median (the valye in the middle of storted array), if even - avg of 2 middles

#SORT
np.sort(a, axis=, kind='heapsort' or 'stable')
#or
a.sort()
#^sort array, default = 'quicksort'
np.sort_complex(a)
#^sorts complex data array, using real numbers to sort

#%%
#numpy.linalg
'''
a @ b - cross product of matrices
'''
np.linalg.det(a)
#^determinant
np.linalg.inv(a)
#^inverse matrix
np.linalg.solve(a, b) 
#solve a x = b if a and b square
np.linalg.lstsq(a, b)
#if not square
np.fft(a)
np.ifft(a)
#fourier and inverse fourier

#%%
#scipy
import scipy as sp
'''
signal
.sawtooth()

'''
#%%
#pandas
#Jupyter notebooks recommended
import pandas as pd
df = pd.csv_read('text.csv', index_col = 'col_name', na_values = [list])
#^index_col equivalent to df.set_index, but with file read
#na_values - detects which values are considered to be NaN, None, etc.

df.info()
#^shows size of resultant matrix and data types of columns

pd.set_option('display_max_columns', 85)
pd.get_option('arg')
pd.reset_option(option)

'''
options:
    display.chop_threshold, float - will consider values lower as 0
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
df.columns
#^display all column names as numpy list
df.columns=['new_col1_name', 'new_col2_name', 'new_col3_name',...]
#^renaming all columns
df.loc[[index1, index2], ['column_name', 'column_name2']]
#^picking values from dataframe
df.iloc[0]
#^access row number i, even if key (index) is nonstandard
df.iloc[[0,1,...]]
#^access row index (e.g. 0 here)
#no brackets when slicing (e.g. 0:6)

df.[column].value_counts(normalize=True)
#^counts all entries, collapses entry list
#if normalise = True, shows values as percentile (part of 1)

df.set_index('column', inplace=True)
#^sets chosen column to be index. If False, does not change dataframe, only shows hot it would look
df.reset_index(inplace=True)
df.sort_index(ascending=True)
#^sorts dataframe according to index
#ascending = False == reverse = True

df['column_name'] == 'entry_name'
#^filter conditioning
df.loc[df['column_name'] == 'entry_name']
#^filter applied
df.loc[~df['column_name'] == 'entry_name']
#^NEGATED filter applied (shows all except condition)
filt = df['column_name'].isin(list_of_values)
#^displays all entries which have a value from 'list_of_values' in column
df[].str.contains("string", na=False)
#^checks if string contains symbol sequence, na declares if NaN should be handled

df.rename(columns = ({'old_name_col1': 'new_name_col1', 'old_name_col2': 'new_name_col2'}),
          inplace = True)
#^renames columns
df.columns = [x.upper for x in df.columns]
#^modifies all column names

df.loc[index, 'column_name'] = 'new_val'
#or
df.at[index, 'column_name'] = 'new_val'
#^replaces value in dataframe with new value
#.at is for single value replacement only

df['column_name'].apply(func)
#^apply a stat function (e.g. len) to a column, outputting results of this column
#can apply custom 'def' functions and lambda functions
df.applymap(func)
#^applies function to every entry in dataframe, does not work with series
pd.Series.min()
#^.apply function to display minimum value in each column
#equivalent to lambda x: x.min()

df['column name'].map({'old_name1': 'new_name1', 'old_name2': 'new_name2'})
#^maps new values to the column. Undeclared values become 'NaN'
df['column name'].replace({'old_name1': 'new_name1', 'old_name2': 'new_name2'})
#^maps new values to the column. Undeclared values remain and do not change

df['column_name'] = ...
#^REQUIRED TO APPLY CHANGES TO ACTUAL DATAFRAME

df.drop(columns = [list])
#^removes column from the list
df.drop(index = df[df['col_name'] == 'entry'].index)
#drops all rows with filter given
df[['col1', 'col2']] = df['col'].str.split(' ', expand=True)
df.append(df2, ignore_index = True, sort = False)
#^appends dataframe 2 to dataframe 1
df.sort_values(by=['col_name', 'sec_column_name'], ascending=[False, True], inplace=True)
#Ascending True by default, secondary  column is secondary sorting index if primary vals are equal
#order corresponds to column if given as list
#inplace=True changes actual list
df.sort_index()
#^sorts dataframe in primary order of index
df['col_name'].nlargest(int)
df['col_name'].nsmallest(int)
#^shows number (int) of largest and smallest entries, only shows selected col
df.nlargest(int, 'col_name')
#^shows number (int) of largest and smallest entries, shows entire dataframe
df.nsmallest(int, 'col_name')
df['col_name'].median()
'''
median can be replaced with:
    count - counts rows with non-NaN values
    mean
    std
    min
    max
'''
df.describe()
#^outputs all statistical calculations of all numerical columns

grp = df.groupby(['col_name'])
#^grouping the column
grp.get_group('col_entry')
#^displays all entries with given col_entry in col_name
grp['col_name2'].value_counts()
#group of entry values creates combination of 2 columns and displays statistical
#relation
grp['col_name2'].agg(['mean', 'median',...])
#displays multiple stat parameters for chosen combination
grp['col_name2'].apply(func)
#where func can be lambda
#return x.str.contains('word').sum()
#unlike dataframes, groups accept "apply" and func instead of .str directly
pd.concat([group1, group2], axis='columns', sort=False)
#^concatenate groups in new group

#handling NaN, None, etc.
df.dropna(axis = 'index', how="any")
#or
df.dropna()
#^discards any rows with NaN, None etc. in them, axis = 'index', how="any" are default and can be discarded
#axis = 'columns' - will drop columns if they have missing values
#how = 'any' - drop if any of values are None NaN etc.
#how = 'all' - drop if all entries are None NaN etc.
df.dropna(axis = 'index', how='any', subset = ['col_name'])
#if 'subset' is given, only analyses given column
df.isna()
#^dataframe mask that displays if entry is considered NaN, for every entry
df['col_name'].astype('type')
#converts data type of a column to new data type (e.g. float to str)
df['col_name'].unique()
#^displays unique entries in column as list


#%%
#plt (matplotlib.pyplot)
import matplotlib.pyplot as plt
print(plt.style.available)
plt.style.use('seaborn')

plt.tight_layout()
plt.show()

#%%
#os.path
path.isfile('')
path.isdir('')
#^insert path - bool out
path.exists()
#^returns if a file OR dir with given path exists
path.join("","")

#%%
#os
os.getcwd()
#^current working directory
os.chdir()
#^change directory
os.listdir()
#^directories list

'''
os.mkdir()
os.makedirs() <- better than mkdir
os.rmdir()
os.removedirs() <- better than rmdir
'''

os.rename()
'''^rename folder

os.stat().statname() - statistics on file - statname optional
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
#^physically open an application or file - UNIX ONLY
'''
WINDOWS:
    import subprocess
    out_file = "PATH"
    subprocess.Popen(["explorer", out_file], creationflags=subprocess.DETACHED_PROCESS)
'''

#%%
#PATHLIB
import pathlib
from pathlib import Path
#if pwd/dir:
pathlib_path = pathlib.Path('/dir')
pathlib_path = Path.cwd()
#----
os_path = str(path)
pathlib_path = PosixPath(os.getcwd())
#^forward and backward conversion between pathlib path and os path
pathlib_path.glob(regex)
#^glob outputs all the files, which are contained in child directories, which
#satisfy the requirements of regex (e.g. *.txt for all text files in dir, depth=1)
pathlib_path.parent
#get the path for a parent directory
pathlib_path.stem
#returns the name of the directory







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
#^same as .getModule, but works with functions that are not properly read by python
cdll.kernel32[1]
#^call first function, [0] would output error
libc.time(None)
#^outputs current time (as timestamp)



byref()
#^function argument

#%%
import sys
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


#%%
import time
time.sleep(seconds)
#^wait for "seconds" time (program does nothing)
#%%
#To save requirements:
#pip freeze > requirements.txt
"""
pipreqs path/proj.py
saves requirements.txt in the same directory

"""

#%%
#scraping and parsing websites
from bs4 import BeautifulSoup
import lxml
import html5lib
import requests

with open('file.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')
#^import downloaded html file as bs4 type text





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
#temp
import tempfile
print()



#%%


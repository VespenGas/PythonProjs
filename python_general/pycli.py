# using python scripts in CLI
# makes a script unusable with python IDE
import argparse
import sys

def main(argv=None):
#if None is passed as default, calling script_name.main() without arguments
#will not raise exception
    parser = argparse.ArgumentParser()
    type_of_arg = int
    #or str, float, bool, etc.
    parser.add_argument('arg_name', help = 'this describes argument to input', type = type_of_arg)
    parser.add_argument('arg2_name', 'a2', help='argument that can only accept certain values',
                        choices=[0,1,2])
    parser.add_argument('arg3_mane', help = 'argument that counts how many times it was inputted in CLI',
                        action = 'count')
    #additional arguments
    #default = 
    #action = 'store_true'
    #^must be given to 2 or more vars. If more than 11 of such vars is input
    #^raise - only one such value can be given
    args = parser.parse_args(argv)
    #then args.arg_name can be inserted to request it from cli
    print(args.arg_name)
    

if __name__ == '__main__':
    sys.exit(main())
    
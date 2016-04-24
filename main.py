#!/usr/bin/env python

import argparse
import pandas as pd
import vanilla

def main():
    parser = argparse.ArgumentParser(description='Our fun little cute program')

    parser.add_argument('-c', '--complaintsfile', 
        help='the Consumer_Complaints.csv file', required=True)
    parser.add_argument('-d', '--demographicsfile', 
        help='the both_all_us_race.csv file')
    parser.add_argument('-v', '--volume', 
        help='run "volume" flavored analysis', action='store_true')
    parser.add_argument('-r', '--racial', 
        help='run "racial" flavored analysis', action='store_true')
    parser.add_argument('-i', '--isbad', 
        help='run "volume" flavored analysis', action='store_true')
    parser.add_argument('-b', '--badcompanies', 
        help='run "racial" flavored analysis', action='store_true')
    parser.add_argument('-f', '--company', 
        help='if "--isbad" analysis requested, target company to investigate')
    parser.add_argument('-C', '--companylist', 
        help='list all companies in alphabetical order', action='store_true')
    # parser.add_argument('-h', '--help', 
    #     help='prints this message')
    args = parser.parse_args()

    if args.companylist and args.complaintsfile is not None:
        dfc = pd.read_csv(args.complaintsfile)
        companies = sorted(list(set(dfc.Company)))
        print('\n'.join(companies))
        return 

    if args.racial is False and args.volume is False:
        if args.complaintsfile is not None and args.demographicsfile is not None:
            print('\t"--volume" or "--racial" flavored analysis not specified, executing both')
        elif args.complaintsfile is not None:
            print('\t"--volume" or "--racial" flavored analysis not specified, executing only "--volume" flavored analysis')
        else:
            raise ValueError('must specify one of "--volume" or "--racial" flavored analysis')

    if args.racial is True and args.demographicsfile is None:
        raise ValueError('--demographicsfile must be specified if running "--racial" flavored analysis')

    if args.isbad is False and args.badcompanies is False:
        if args.company is not None:
            args.isbad = True
            args.badcompanies = True
            print('\t"--isbad" or "--badcompanies" analysis not specified, executing both')
        else:
            args.isbad = False
            args.badcompanies = True
            print('\t"--isbad" or "--badcompanies" analysis not specified, executing just "--badcompanies" analysis')

    if args.isbad is True and args.company is None:
        raise ValueError('--company must be specified if running "--isbad" analysis')

    dfc = pd.read_csv(args.complaintsfile)
    if args.racial is True:
        dfd = pd.read_csv(args.demographicsfile)

    exec_volume_analysis(args, dfc)
    # exec_racial_analysis(args, dfc, dfd)

def exec_volume_analysis(args, dfc):
    """Executes volume-flavored analysis on the consumer complaints dataset.
    Returns  

    Args:
        args - parsed command line arguments
        dfc - consumer complaints dataset as a pandas dataframe

    Results:
        no return value
        prints out the results of the analysis
    """
    v = vanilla.Vanilla(dfc)
    if args.isbad is True:
        print(v.is_bad(args.company))
    if args.badcompanies is True:
        print(v.bad_companies('Consumer Loan'))

def exec_racial_analysis(args, dfc, dfd):
    """Executes racial-flavored analysis on the consumer complaints dataset.
    Returns  

    Args:
        args - parsed command line arguments
        dfc - consumer complaints dataset as a pandas dataframe
        dfd - US racial demographics and zipcode dataset as a pandas dataframe

    Results:
        no return value
        prints out the results of the analysis
    """
    r = Ratio(dfc, dfd)
    if args.isbad is True:
        print(r.is_bad(args.company))
    if args.badcompanies is True:
        print(r.bad_companies('Consumer Loan'))

if __name__ == '__main__':
    main()

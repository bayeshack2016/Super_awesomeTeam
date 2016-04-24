#!/usr/bin/env python

import json
import pandas as pd
import argparse
import volume
import ratio


def main():
    parser = argparse.ArgumentParser(description='Our fun little cute program')

    parser.add_argument('-c', '--complaintsfile', 
        help='the Consumer_Complaints.csv file', required=True)
    parser.add_argument('-d', '--demographicsfile', 
        help='the both_all_us_race.csv file')
    parser.add_argument('-v', '--volume', 
        help='run "volume" analysis', action='store_true')
    parser.add_argument('-r', '--ratio', 
        help='run "ratio" analysis', action='store_true')
    parser.add_argument('-i', '--isbad', 
        help='run "volume" analysis', action='store_true')
    parser.add_argument('-b', '--badcompanies', 
        help='run "ratio" analysis', action='store_true')
    parser.add_argument('-f', '--company', 
        help='if "--isbad" analysis requested, target company to investigate')
    parser.add_argument('-l', '--productline', 
        help='if "--badcompanies" analysis requested, target productline to investigate')
    parser.add_argument('-p', '--pretty', 
        help='pretty print JSON output', action='store_true')
    args = parser.parse_args()

    if args.ratio is False and args.volume is False:
        if args.complaintsfile is not None and args.demographicsfile is not None:
            args.volume = True
            args.ratio = True
        elif args.complaintsfile is not None:
            args.volume = True
        else:
            raise ValueError('must specify one of "--volume" or "--ratio" analysis')

    if args.ratio is True and args.demographicsfile is None:
        raise ValueError('--demographicsfile must be specified if running "--ratio" analysis')

    if args.isbad is False and args.badcompanies is False:
        if args.company is not None:
            args.isbad = True
        if args.productline is not None:
            args.badcompanies = True
        else:
            raise ValueError('"--company" and/or "--productline" must be specified')

    if args.isbad is True and args.company is None:
        raise ValueError('"--company" must be specified if running "--isbad" analysis')

    if args.badcompanies is True and args.productline is None:
        raise ValueError('"--productline" must be specified if running "--badcompanies" analysis')

    complaints = pd.read_csv(args.complaintsfile)

    if args.ratio is True:
        zipcodes = pd.read_csv(args.demographicsfile)

    if args.volume is True:
        print('\nVolume Analysis:')
        exec_volume_analysis(args, complaints)

    if args.ratio is True:
        print('\nRatio Analysis:')
        exec_ratio_analysis(args, complaints, zipcodes)

def pretty_print(x):
    print(json.dumps(x, indent=4, separators=(',', ': ')))

def exec_volume_analysis(args, complaints):
    """Executes volume-flavored analysis on the consumer complaints dataset.
    Returns  

    Args:
        args - parsed command line arguments
        complaints - consumer complaints dataset as a pandas dataframe

    Results:
        no return value
        prints out the results of the analysis
    """
    v = volume.Volume(complaints)

    if args.isbad is True:
        if args.pretty:
            pretty_print(v.is_bad(args.company))
        else:
            print(json.dumps(v.is_bad(args.company)))

    if args.badcompanies is True:
        if args.pretty:
            pretty_print(v.bad_companies(args.productline))
        else:
            print(json.dumps(v.bad_companies(args.productline)))

def exec_ratio_analysis(args, complaints, zipcodes):
    """Executes ratio-flavored analysis on the consumer complaints dataset.
    Returns  

    Args:
        args - parsed command line arguments
        complaints - consumer complaints dataset as a pandas dataframe
        zipcodes - US ratio demographics and zipcode dataset as a pandas dataframe

    Results:
        no return value
        prints out the results of the analysis
    """
    r = ratio.Ratio(complaints, zipcodes)

    if args.isbad is True:
        if args.pretty:
            pretty_print(r.is_bad(args.company))
        else:
            print(json.dumps(r.is_bad(args.company)))

    if args.badcompanies is True:
        if args.pretty:
            pretty_print(r.bad_companies(args.productline))
        else:
            print(json.dumps(r.bad_companies(args.productline)))

if __name__ == '__main__':
    main()

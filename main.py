# -*- coding: utf-8 -*-
import argparse
from collect.daumnews_collector import DaumNewsCollector


if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='news crawler.')
    parser.add_argument('--target', type=str, nargs='?', default='daum',
                        help='input target news site. now only DAUM site is supported...')
    parser.add_argument('--role', type=str, nargs='?', default='collector',
                        help='input some role. \'collector\' or \'parser\'')

    args = parser.parse_args()
    target_site = args.target.upper()
    role = args.role.lower()

    if role == 'collector' :
        if target_site == 'DAUM':
            print('### collector start. target site : {0}'.format(target_site))

            collector = DaumNewsCollector()
            collector.collect()
        else:
            print('### input target site : {0}'.format(target_site))
            print('{0}-collector not implemented...'.format(target_site))
    else:
        if target_site == 'DAUM':
            print('### parser start. target site : {0}'.format(target_site))
            print('not implemented...')
        else:
            print('### input target site : {0}'.format(target_site))
            print('{0}-parser not implemented...'.format(target_site))





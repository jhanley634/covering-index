#! /usr/bin/env python
# Copyright 2014, Palo Alto Research Center.
# Developed with sponsorship of DARPA.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# The software is provided "AS IS", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall the
# authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising
# from, out of or in connection with the software or the use or other
# dealings in the software.
'''
Removes rows and corresponding files.
'''
import db_session


def parse(parser):
    '''
    Caller should supply the db_conf.txt config and section, and invoke as:
        args, engine, session, metadata = db_session.args.parse(arg_parser())
    '''
    args = parser.parse_args()
    ret = [args]
    ret.extend(db_session.mgr.establish(args.config, args.section))
    return ret


def parse_aes(parser):
    '''
    Invoke as:
        args, engine, session = db_session.args.parse_aes(arg_parser())
    '''
    return parse(parser)[:3]

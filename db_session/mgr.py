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
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import cymysql
except ImportError:
    pass
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
import sys


def establish(config, section):
    '''Arrange for a global session object, per http://docs.sqlalchemy.org.'''
    engine = create_engine(jdbc_url(config, section))
    metadata = MetaData()
    metadata.bind = engine
    return engine, sessionmaker(engine)(), metadata


def jdbc_url(config_file, section):
    def adjust(xs):
        if xs[0] == 'mysql' and 'cymysql' in sys.modules:
            xs[0] += '+cymysql'
            assert cymysql.VERSION >= (0, 7, 2)
        if xs[0] == 'mssql':
            xs[0] += '+pymssql'
        return xs
    cfg = configparser.ConfigParser()
    cfg.read(config_file)
    assert cfg.get(section, 'vendor') in ['mysql', 'oracle']
    return '%s://%s:%s@%s/%s' % tuple(adjust([
        cfg.get(section, item)
        for item in ['vendor', 'user', 'passwd', 'host', 'db']]))

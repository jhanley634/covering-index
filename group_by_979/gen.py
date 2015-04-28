#! /usr/bin/env python
# Copyright 2015, John Hanley
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
Generate sample tables.
'''
import argparse
import datetime
import hashlib
import os
import random
import sys

sys.path.append('..')
import db_session


def get_create_parts(table):
    return '''
create table %s (
  part   varchar(12)   primary key  comment 'sku (alphanumeric part number)',
  mass   float         not null     comment 'shipping weight (kg)',
  price  decimal(9,2)  not null     comment 'retail price (USD)'
)
''' % table


def get_create_sales(table):
    # The transaction 'amount' column is denormalized, but convenient.
    return '''
create table %s (
  id      integer       primary key  auto_increment,
  stamp   timestamp     not null  default 0,
  part    varchar(12)   not null,
  qty     integer       not null,
  amount  decimal(9,2)  not null  comment 'price * qty (USD)',
  foreign key (part)  references SALES(part),
  key (part, qty, amount)
)
''' % table


def gen_both():
    gen1('PARTS', get_create_parts)
    gen1('SALES', get_create_sales)
    rnd = random.Random()
    rnd.seed(42)
    prices = populate_parts('PARTS', rnd)
    populate_sales('SALES', rnd, prices)


def gen1(table, get_ddl):
    session.execute('drop table  if exists  ' + table)
    session.execute(get_ddl(table))


def populate_parts(table, rnd, num_parts=100000):
    prices = {}
    for i in range(num_parts):
        part = hash(rnd.random())
        mass = rnd.randint(50, 3141) / 1e3
        price = .25 + 123.00 * rnd.random()
        ins = "insert into %s values ('%s', %.3f, %.2f)" % (
            table, part, mass, price)
        session.execute(ins)
        prices[part] = price
    return prices


def populate_sales(table, rnd, prices, num_trx=10000000):
    parts = sorted(prices.keys())
    ts = datetime.datetime.now() - datetime.timedelta(days=365)
    for i in range(num_trx):
        part = rnd.choice(parts)
        qty = rnd.randint(1, 12)
        amount = prices[part] * qty
        ins = "insert into %s values (null, '%s', '%s', %d, %.2f)" % (
            table, ts, part, qty, amount)
        session.execute(ins)
        ts += datetime.timedelta(seconds=rnd.randint(5, 600))


def hash(s, length=12):
    return hashlib.sha224(str(s)).hexdigest()[:length]


def report():
    query1 = '''
select now(), part, min(qty) as qty, min(amount) as amount
  from SALES
  group by part
'''
    query2 = '''
select now(), part, qty, amount
  from SALES
  group by part
'''
    # print('explain %s;' % query1.replace('\n', ' '))
    # print('explain %s;' % query2.replace('\n', ' '))

    result, elapsed = execute(query1)
    print(str(elapsed), len(result), result[:2])

    result, elapsed = execute(query2)
    print(str(elapsed), len(result), result[:2])


def execute(query):
    t0 = datetime.datetime.now()
    result = session.execute(query).fetchall()
    t1 = datetime.datetime.now()
    elapsed = t1 - t0
    return result, elapsed


def arg_parser():
    # db_conf.txt is an .ini file that looks like this:
    # [section_name]
    # user = scott
    # passwd = tiger
    # host = localhost
    # db = demo
    # vendor = mysql
    p = argparse.ArgumentParser(
        description='Create table with random content.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument(
        '--config', nargs='?',
        help='config file supplies DB credentials',
        default=os.path.expanduser('~/Desktop/db_conf.txt'))
    p.add_argument('--section', nargs='?',
                   help='choose database within the DB config file')
    return p


if __name__ == '__main__':
    args, engine, session = db_session.args.parse_aes(arg_parser())
    gen_both()
    report()

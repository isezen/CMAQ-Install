#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103,W0621,W0702,W0703

"""
Download FNL data from rda.ucar.edu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python script to download selected files from rda.ucar.edu
after you save the file, don't forget to make it executable
  i.e. - "chmod 755 <name_of_script>"

SEE: https://rda.ucar.edu/datasets/ds083.2/index.html#cgi-bin/datasets/
     getWebList?dsnum=083.2&action=showAll&disp=
"""


import signal
import sys
import os
from urllib.request import build_opener
from urllib.request import HTTPCookieProcessor
import http.cookiejar as cookielib
from os.path import join
from os.path import exists
from pathlib import Path
from datetime import datetime as _dt
from datetime import timezone as _tz
import itertools
import argparse
from argparse import RawTextHelpFormatter as _rtformatter

__version__ = '0.0.1.dev'
__author__ = 'Ismail SEZEN'
__email__ = 'sezenismail@gmail.com'
__license__ = 'AGPL v3.0'
__year__ = '2021'


_AUTH_FILE = join(str(Path.home()), '.auth.rda.ucar.edu')


class ExitHelper():
    """ Class to exit from script gracefully """
    def __init__(self):
        self._state = False
        signal.signal(signal.SIGINT, self.change_state)

    def change_state(self):
        """ Change statie of exit status """
        print("\nStopping...")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self._state = True

    @property
    def exit(self):
        """ Get exit state """
        return self._state


def _create_argparser_(description, epilog):
    """ Create an argparser object """
    file_py = os.path.basename(sys.argv[0])
    p = argparse.ArgumentParser(description=description,
                                epilog=epilog.format(file_py),
                                formatter_class=_rtformatter)
    p.add_argument('-v', '--version', help="Version", action="version",
                   version='{} {}\n{} (c) {} {}'.format(file_py, __version__,
                                                        __license__, __year__,
                                                        __author__))
    return p


def authenticate(email, password):
    """ Authentixcate to rda.ucar.edu """
    cj = cookielib.MozillaCookieJar()
    opener = build_opener(HTTPCookieProcessor(cj))
    authenticate = False
    if os.path.isfile(_AUTH_FILE):
        cj.load(_AUTH_FILE, False, True)
        for cookie in cj:
            if (cookie.name == "sess" and cookie.is_expired()):
                authenticate = True
    else:
        authenticate = True

    if authenticate:
        if not (isinstance(email, str) and isinstance(password, str)):
            err = 'email and password is required for authentication'
            raise ValueError(err)

        url = 'https://rda.ucar.edu/cgi-bin/login'
        data = 'email={}&password={}&action=login'.format(email, password)
        opener.open(url, data.encode('utf-8'))
        cj.clear_session_cookies()
        cj.save(_AUTH_FILE, True, True)
    return opener


def get_fnl(list_of_files, pth=os.getcwd(), email=None, password=None,
            verbose=True):
    """ Download FNL data from  rda.ucar.edu """
    opener = authenticate(email, password)

    flag = ExitHelper()
    for file in list_of_files:
        idx = file.rfind('/')
        ofile = file[idx + 1:] if idx > 0 else file
        ofile2 = join(pth, ofile)
        if exists(ofile2):
            sys.stdout.write('* ' + ofile + ' already exist.\n')
        else:
            if verbose:
                sys.stdout.write('* downloading ' + ofile + ' ... ')
                sys.stdout.flush()
            infile = opener.open('http://rda.ucar.edu/data/OS/ds083.2/' + file)
            with open(ofile2, 'wb') as outfile:
                outfile.write(infile.read())
            if verbose:
                sys.stdout.write('done.\n')
        if flag.exit:
            break


def get_fnl_grib2(year, month=None, day=None,  # pylint: disable=R0913
                  hour=None, pth=os.getcwd(), email=None, password=None,
                  verbose=True):
    """ Download grib2 data from rda.ucar.edu """
    if month is None:
        month = list(range(1, 13))
    if day is None:
        day = list(range(1, 32))
    if hour is None:
        hour = [0, 6, 12, 18]

    if not isinstance(year, list):
        year = [year]
    if not isinstance(month, list):
        month = [month]
    if not isinstance(day, list):
        day = [day]
    if not isinstance(hour, list):
        hour = [hour]

    def expandgrid(*itrs):
        product = list(itertools.product(*itrs))
        x = list({'Var{}'.format(i + 1): [x[i] for x in product]
                  for i in range(len(itrs))}.values())
        return list(map(list, zip(*x)))

    def get_dates(list_of_dates):
        fmt = '%Y-%m-%d %H'
        for i in list_of_dates:
            try:
                date_str = '{}-{}-{} {}'.format(*i)
                yield _dt.strptime(date_str, fmt).replace(tzinfo=_tz.utc)
            except:  # noqa: E722
                pass

    x = expandgrid(year, month, day, hour)
    dates = list(get_dates(x))
    s = "grib2/%Y/%Y.%m/fnl_%Y%m%d_%H_00.grib2"
    list_of_files = [d.strftime(s) for d in dates]

    get_fnl(list_of_files, pth, email, password, verbose)


if __name__ == "__main__":
    DESCRIPTION = 'Download FNL data.\n'
    EPILOG = 'Example of use:\n' + \
             ' %(prog)s -y 2016 -m 1 -e john.doe@mail.com -p 123456\n' + \
             ' %(prog)s -y 2015 -m 2\n'

    try:
        p = _create_argparser_(DESCRIPTION, EPILOG)
        p.add_argument('-q', '--quiet', help="Suppress verbose output",
                       default=False, action="store_true")
        p.add_argument('path', nargs='?', default=os.getcwd(),
                       help="Path to FNL files to save.")
        p.add_argument('-y', '--years', nargs='+', required=True)
        p.add_argument('-m', '--months', nargs='+')
        p.add_argument('-d', '--days', nargs='+')
        p.add_argument('-e', '--email', type=str, nargs='?')
        p.add_argument('-p', '--password', type=str, nargs='?')

        args = p.parse_args()
        get_fnl_grib2(args.years, args.months, args.days, None, args.path,
                      args.email, args.password, not args.quiet)
    except Exception as e:  # pylint: disable=W0703
        print(e)

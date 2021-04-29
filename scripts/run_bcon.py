#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103,W0621,W0702,W0703


"""
Run mcip
~~~~~~~~
Python script to run bcon
"""

import os
import subprocess
import itertools
from os.path import join

import tempfile
import calendar
from collections.abc import Iterable
from datetime import datetime as _dt
from datetime import timezone as _tz
from collections import namedtuple as _nt

Domain = _nt('Domain', ['outer', 'inner', 'name'])

BCTYPE = 'regrid'  # profile | regrid
compiler = 'gcc'
cmaq_ver = '532'
proj_name = 'CityAir'
dir_projects = '/mnt/disk2/projects'
year, month, day = [2015], [1, 2, 3], list(range(1, 32))
doms = [Domain(36, 12, 'tr'),
        Domain(12, 4, 'ege'),
        Domain(12, 4, 'akd'),
        Domain(12, 4, 'ica'),
        Domain(12, 4, 'okd')]
doms = [doms[0]]
# ----------------------------------
dir_proj = join(dir_projects, proj_name)


def get_script(year, month, day, dom_outer, dom_inner, proj_name,
               dir_proj, BCTYPE='regrid', cmaq_ver='532', compiler='gcc'):
    mn = calendar.month_name[month].lower()
    script = """
setenv compiler {}

pushd ../../../
source ./config_cmaq.csh $compiler
popd

if ( ! -e $CMAQ_DATA ) then
  echo "$CMAQ_DATA path does not exist"
  exit 1
endif
echo " "; echo " Input data path, CMAQ_DATA set to $CMAQ_DATA"; echo " "

set year = {}
set month = {:02d}
set month_name = {}
set day = {:02d}
set dom_size_outer = {:02d}km
set dom_size_inner = {:02d}km
set project_name = {}

set dir_proj = {}
set dir_mcip = ${{dir_proj}}/mcip
set dir_inner = ${{dir_mcip}}/${{dom_size_inner}}/${{month_name}}
set dir_outer = ${{dir_mcip}}/${{dom_size_outer}}/${{month_name}}

set APPL = ${{project_name}}_${{dom_size_inner}}_${{year}}_${{month}}
set VRSN = v{}
set BCTYPE = {}

set BLD = ${{CMAQ_HOME}}/PREP/bcon/scripts/BLD_BCON_${{VRSN}}_${{compiler}}
set EXEC = BCON_${{VRSN}}.exe
cat $BLD/BCON_${{VRSN}}.cfg; echo " "; set echo

setenv GRID_NAME ${{dom_size_inner}}
setenv GRIDDESC ${{dir_inner}}/GRIDDESC
setenv IOAPI_ISPH 20

setenv IOAPI_LOG_WRITE F
setenv IOAPI_OFFSET_64 YES
setenv EXECUTION_ID $EXEC

setenv BCON_TYPE ` echo $BCTYPE | tr "[A-Z]" "[a-z]" `

set OUTDIR   = ${{dir_proj}}/bcon

set DATE = "${{year}}-${{month}}-${{day}}"
set YYYYJJJ  = `date -ud "${{DATE}}" +%Y%j`
set YYMMDD   = `date -ud "${{DATE}}" +%y%m%d`
set YYYYMMDD = `date -ud "${{DATE}}" +%Y%m%d`

if ( $BCON_TYPE == regrid ) then
  setenv CTM_CONC_1 ${{dir_proj}}/cmaq/${{dom_size_outer}}/CCTM_CONC_${{VRSN}}_${{compiler}}_${{project_name}}_${{year}}_${{dom_size_outer}}_${{YYYYMMDD}}.nc
  setenv MET_CRO_3D_CRS ${{dir_outer}}/METCRO3D_${{project_name}}_${{dom_size_outer}}_${{YYYYMMDD}}.nc
  setenv MET_BDY_3D_FIN ${{dir_inner}}/METBDY3D_${{project_name}}_${{dom_size_inner}}_${{YYYYMMDD}}.nc
  setenv BNDY_CONC_1    "$OUTDIR/BCON_${{VRSN}}_${{APPL}}_${{BCON_TYPE}}_${{YYYYMMDD}} -v"
endif

if ( $BCON_TYPE == profile ) then
  setenv BC_PROFILE $BLD/profiles/avprofile_cb6r3m_ae7_kmtbr_hemi2016_v53beta2_m3dry_col051_row068.csv
  setenv MET_BDY_3D_FIN ${{dir_inner}}/METBDY3D_${{proj_name}}_${{month_name}}_${{year}}_${{dom_size_inner}}.nc
  setenv BNDY_CONC_1    "$OUTDIR/BCON_${{VRSN}}_${{APPL}}_${{BCON_TYPE}}_${{YYYYMMDD}} -v"
endif


if ( ! -d "$OUTDIR" ) mkdir -p $OUTDIR

ls -l $BLD/$EXEC; size $BLD/$EXEC
unlimit
limit

time $BLD/$EXEC

exit()""".format(compiler, year, month, mn, day, dom_outer, dom_inner,
                 proj_name, dir_proj, cmaq_ver, BCTYPE)
    return script


def expandgrid(*itrs):
    """ expand iterables """
    v = [x if isinstance(x, Iterable) else [x] for i, x in enumerate(itrs)]
    product = list(itertools.product(*v))
    x = list({'Var{}'.format(i + 1): [x[i] for x in product]
              for i in range(len(v))}.values())
    return list(map(tuple, zip(*x)))


def date_is_ok(year, month, day):
    """ Check (year, month, day) is a correct day """
    try:
        date_str = '{}-{}-{}'.format(year, month, day)
        _dt.strptime(date_str, '%Y-%m-%d').replace(tzinfo=_tz.utc)
        return True
    except:  # noqa: E722
        pass
    return False


def get_days(year, month, day=list(range(1, 32))):
    """ Return days in specific year and month """
    days = []
    for i in expandgrid(year, month, day):
        if date_is_ok(i[0], i[1], i[2]):
            days.append(i[2])
    return days


if __name__ == "__main__":
    ym = expandgrid(year, month)  # Year and months
    for dom in doms:
        for y, m in ym:
            days = get_days(y, m, day)

            tmp = next(tempfile._get_candidate_names())
            file_script = 'bcon_{}.csh'.format(tmp)
            for d in days:
                script = get_script(y, m, d, dom.outer, dom.inner, proj_name,
                                    dir_proj, BCTYPE, cmaq_ver, compiler)
                with open(file_script, 'w') as f:
                    f.write("#!/bin/csh -f\n")
                    f.write(script)

                subprocess.call(['chmod', '+x', file_script])
                subprocess.call('./' + file_script)
                os.remove(file_script)
                # status = subprocess.Popen(['csh', '-cf', script])

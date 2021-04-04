# CMAQ - Install NetCDF (Ubuntu 20.04)

To make NetCDF work properly, NetCDF must be built with the same compiler that you are using to build WRF. Downloading and installing NetCDF from source also enables you get the advantage of having latest version of NetCDF and seperating it from the NetCDF libraries installed from Ubuntu repository. This section follows the instructions at [CMAQ tutorial build library gcc].

**NOTE:** _It's assumed here that you are at your `$HOME` directory._

**NOTE:** _Make sure you were completed previous steps:_

[01 - Prerequisities](01-Prerequisities.md)

--------

* Set environment variables to install NetCDF and create the installation folder.

```bash
PATH_TO_APPS=/path/to/apps/directory
NETCDF=$PATH_TO_APPS/NETCDF
export LD_LIBRARY_PATH=$NETCDF/lib:$LD_LIBRARY_PATH
export PATH=$NETCDF/bin:$PATH
mkdir -p $NETCDF
```

--------

## Install netCDF-C

1. Download netCDF-C library, untar and change directory into extracted dir.

```bash
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-c-4.7.0.tar.gz
tar -xzvf netcdf-c-4.7.0.tar.gz
cd netcdf-c-4.7.0
```

2. Run the configure command

```bash
./configure --prefix=$NETCDF --disable-netcdf-4 --disable-dap
```

If the command worked correctly, you should get the following result.

```bash
...
# NetCDF C Configuration Summary
==============================

# General
-------
NetCDF Version:   4.7.0
Configured On:    Mon Mar 22 06:41:12 +03 2021
Host System:    x86_64-pc-linux-gnu
Build Directory:  /home/isezen/netcdf-c-4.7.0
Install Prefix:         /home/isezen/cmaq_req_libs

# Compiling Options
-----------------
C Compiler:   /usr/bin/gcc
CFLAGS:
CPPFLAGS:
LDFLAGS:
AM_CFLAGS:
AM_CPPFLAGS:
AM_LDFLAGS:
Shared Library:   yes
Static Library:   yes
Extra libraries:  -lm

# Features
--------
NetCDF-2 API:   yes
HDF4 Support:   no
HDF5 Support:   no
NetCDF-4 API:   no
NC-4 Parallel Support:  no
PnetCDF Support:  no
DAP2 Support:   no
DAP4 Support:   no
Byte-Range Support: no
Diskless Support: yes
MMap Support:   no
JNA Support:    no
CDF5 Support:   yes
ERANGE Fill Support:  no
Relaxed Boundary Check: yes
```

3. Run the install command

```bash
make check
make install
```

At the end, you should see the following output:

```bash
+-------------------------------------------------------------+
| Congratulations! You have successfully installed netCDF!    |
|                                                             |
| You can use script "nc-config" to find out the relevant     |
| compiler options to build your application. Enter           |
|                                                             |
|     nc-config --help                                        |
|                                                             |
| for additional information.                                 |
|                                                             |
| CAUTION:                                                    |
|                                                             |
| If you have not already run "make check", then we strongly  |
| recommend you do so. It does not take very long.            |
|                                                             |
| Before using netCDF to store important data, test your      |
| build with "make check".                                    |
|                                                             |
| NetCDF is tested nightly on many platforms at Unidata       |
| but your platform is probably different in some ways.       |
|                                                             |
| If any tests fail, please see the netCDF web site:          |
| http://www.unidata.ucar.edu/software/netcdf/                |
|                                                             |
| NetCDF is developed and maintained at the Unidata Program   |
| Center. Unidata provides a broad array of data and software |
| tools for use in geoscience education and research.         |
| http://www.unidata.ucar.edu                                 |
+-------------------------------------------------------------+
```
Change directory to one level up from your current directory by `cd ..`.

--------

## Install netCDF-Fortran

1. Download netCDF-Fortran library, untar the netCDF-Fortran tar.gz file and change directory into extracted dir.

```bash
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-4.4.5.tar.gz
tar -xzvf netcdf-fortran-4.4.5.tar.gz
cd netcdf-fortran-4.4.5
```


2. Run configure and make check commands. Exports are required to make NdtCDF-Fortran to be able to find NetCDF-C.

```bash
CPPFLAGS=-I$NETCDF/include LDFLAGS=-L$NETCDF/lib ./configure --prefix=$NETCDF
make check
```

If the command worked correctly, you should get the following result.

```bash
============================================================================
Testsuite summary for netCDF-Fortran 4.4.5
============================================================================
# TOTAL: 6
# PASS:  6
```

3. Run the install command

```bash
make install
```

At the end, you should see the following output

```bash
+-------------------------------------------------------------+
| Congratulations! You have successfully installed the netCDF |
| Fortran libraries.                                          |
|                                                             |
| You can use script "nf-config" to find out the relevant     |
| compiler options to build your application. Enter           |
|                                                             |
|     nf-config --help                                        |
|                                                             |
| for additional information.                                 |
|                                                             |
| CAUTION:                                                    |
|                                                             |
| If you have not already run "make check", then we strongly  |
| recommend you do so. It does not take very long.            |
|                                                             |
| Before using netCDF to store important data, test your      |
| build with "make check".                                    |
|                                                             |
| NetCDF is tested nightly on many platforms at Unidata       |
| but your platform is probably different in some ways.       |
|                                                             |
| If any tests fail, please see the netCDF web site:          |
| http://www.unidata.ucar.edu/software/netcdf/                |
|                                                             |
| NetCDF is developed and maintained at the Unidata Program   |
| Center. Unidata provides a broad array of data and software |
| tools for use in geoscience education and research.         |
| http://www.unidata.ucar.edu                                 |
+-------------------------------------------------------------+
```
Change directory to one level up from your current directory by `cd ..`.

# CMAQ - Install WRF (Ubuntu 20.04)

You must complete previous installation instructions before this.

It's said that _"The most current version uses WRFv4.1.1 and CMAQv5.3.2. Instructions for compiling and running the WRF-CMAQ system are also included with each release"_ at [EPA].

[EPA]: https://www.epa.gov/cmaq/wrf-cmaq-model

**NOTE:** _It's assumed here that you are at your `$HOME` directory._

* Set environment variables

Issue the following commands:

```bash
export NETCDF=$(nc-config --prefix) # This is required for WRF
export NETCDF_classic=1
```

--------

## Install WRF

1. Download WRF and change directory to WRFv4.1.1

```bash
FOLDER=WRF
WRF_DIR=$PATH_TO_APPS/$FOLDER
git clone --branch v4.1.1 https://github.com/wrf-model/WRF.git $FOLDER
cd $FOLDER
```

2. Configure WRF

```bash
./configure |& tee ./configure.log
```

* Select `34. (dmpar)` for GNU.
* Select default value for nesting (`default = 1`)

If the command worked correctly, you should get the following result.

```
------------------------------------------------------------------------
Settings listed above are written to configure.wrf.
If you wish to change settings, please edit that file.
If you wish to change the default options, edit the file:
     arch/configure.defaults
NetCDF users note:
 This installation of NetCDF supports large file support.  To DISABLE large file support in NetCDF, set the environment variable 
 WRFIO_NCD_NO_LARGE_FILE_SUPPORT to 1 and run configure again. Set to any 
 other value to avoid this message.

Testing for NetCDF, C and Fortran compiler

This installation of NetCDF is 64-bit
                 C compiler is 64-bit
           Fortran compiler is 64-bit
              It will build in 64-bit

*****************************************************************************
This build of WRF will use classic (non-compressed) NETCDF format
*****************************************************************************
```

3. Compile WRF for real case

```bash
./compile -j 4 em_real |& tee compile.log
```

If the command worked correctly, you should get the following result.

```bash
==========================================================================
build started:   Mon 22 Mar 2021 04:31:03 PM +03
build completed: Mon 22 Mar 2021 04:40:19 PM +03

--->                  Executables successfully built                  <---

-rwxrwxr-x 1 username username 41494464 Mar 22 16:40 main/ndown.exe
-rwxrwxr-x 1 username username 41371488 Mar 22 16:40 main/real.exe
-rwxrwxr-x 1 username username 40864064 Mar 22 16:40 main/tc.exe
-rwxrwxr-x 1 username username 45300296 Mar 22 16:39 main/wrf.exe

==========================================================================
```

4. Change directory to one level up and copy WRF to APPS directory.

```bash
cd ..
mv $FOLDER $WRF_DIR
```

## Install WPS

1. Download WPS, extract and change directory to `WPS-4.1`

```bash
FOLDER=WPS-4.1
wget -O $FOLDER.tar.gz https://github.com/wrf-model/WPS/archive/refs/tags/v4.1.tar.gz
tar -xzvf $FOLDER.tar.gz
rm $FOLDER.tar.gz
cd $FOLDER
```


```bash
# optional
wget http://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
```

2. Configure WPS. Select option `1` for `Linux x86_64, gfortran (serial)`.

You need to set `WRF_DIR` environment variable to the directory where WRF was installed to compile WPS properly.

```bash
WRF_DIR=$WRF_DIR ./configure
```

If the command worked correctly, you should get the following result.

```bash
Will use NETCDF in dir: /home/[username]/cmaq_req_libs
Using WRF I/O library in WRF build identified by $WRF_DIR: /home/[username]/WRFv4.1.1
$JASPERLIB or $JASPERINC not found in environment. Using default values for library paths...
------------------------------------------------------------------------
Please select from among the following supported platforms.

   1.  Linux x86_64, gfortran    (serial)
   2.  Linux x86_64, gfortran    (serial_NO_GRIB2)
   3.  Linux x86_64, gfortran    (dmpar)
   4.  Linux x86_64, gfortran    (dmpar_NO_GRIB2)
...
```

3. Compile WPS

```bash
./compile |& tee compile.log
```

4. Change directory to one level up and copy WPS to `APPS` directory.

```bash
cd ..
mv $FOLDER $PATH_TO_APPS/WPS
```

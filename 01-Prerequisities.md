# Prerequisites (Ubuntu 20.04)

## Required Components

* `git` is required to clone some repositories in installation process.

```bash
sudo apt install git
```

`git --version` (*2.25.1*)

* `tcsh` is required for WRF, WPS and CMAQ.

```bash
sudo apt install tcsh
```

`tcsh --version` (*6.21.00*)

* Install curl library for NetCDF-C bytre-range warning.

```bash
sudo apt install libcurl4-openssl-dev
```

* Install _libjasper_ and _libpng_ for WPS.

```bash
sudo add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
sudo apt update
sudo apt install libjasper1 libjasper-dev
sudo apt install libpng-dev
```

## Compilers

Install required compilers

```bash
sudo apt install make gcc g++ cpp gfortran openmpi-bin libopenmpi-dev
```

**Compiler versions:**

* `gcc --version`        (*9.3.0*)
* `g++ --version`        (*9.3.0*)
* `cpp --version`        (*9.3.0*)
* `gfortran --version`   (*9.3.0*)
* `mpicc --version`  --> (`gcc 9.3.0`)
* `mpic++ --version` --> (`g++ 9.3.0`)
* `mpif90 --version` --> (`GNU Fortran 9.3.0`)
* `mpirun --version`     (`4.0.3`)

**To Check OpenMPI information:**

```
ompi_info
```

## Setting Environment Variables

Add required environment variables to the `.bashrc` or `.profile` file. Change `PATH_TO_APPS` variable to your APPS directory. These exports are required to run installed apps properly.

```bash
PATH_TO_APPS=/path/to/apps/directory
NETCDF=$PATH_TO_APPS/NETCDF
export LD_LIBRARY_PATH=$NETCDF/lib:$LD_LIBRARY_PATH
export PATH=$NETCDF/bin:$PATH
```

and source your file by `source ~/.bashrc` or `source ~/.profile`.


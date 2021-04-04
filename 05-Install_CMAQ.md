# CMAQ - Install CMAQ (Ubuntu 20.04)

You must complete previous installation instructions before this.

See: [CMAQ Install]

[CMAQ Install]: https://github.com/USEPA/CMAQ/blob/master/DOCS/Users_Guide/Tutorials/CMAQ_UG_tutorial_benchmark.md

**NOTE:** _It's assumed here that you are at your `$HOME` directory._

--------

## Install CMAQ

1. Download CMAQ by git, change directory to `CMAQ_REPO` and check out a new branch in the CMAQ repository.

```bash
git clone -b master https://github.com/USEPA/CMAQ.git CMAQ_REPO
cd CMAQ_REPO
git checkout -b my_branch
```

2. In `bldit_project.csh` file, search the variable `$CMAQ_HOME` which identifies the folder that you would like to install the CMAQ package under and change the variable where you want to install CMAQ. For instance,

```bash
set CMAQ_HOME = /home/username/CMAQ_v5.3.2
```

3. Run `bldit_project.csh` file.

```bash
./bldit_project.csh
```

4. After step 3, you will have CMAQ install directory at `CMAQ_HOME = /home/username/CMAQ_v5.3.2`. cd to `CMAQ_HOME` directory.

```bash
cd /home/username/CMAQ_v5.3.2
```

5. Open `config_cmaq.csh` file and find the `#> gfortran compiler` section. In the section, make the folllowing adjustments.

**Don't forget to change `username` with your current user name**

**PAY ATTENTION to `myLINK_FLAG` and `mpi_lib` variables**

```tcsh
setenv IOAPI_INCL_DIR   /home/username/ioapi-3.2/ioapi/fixed_src   #> I/O API include header files
setenv IOAPI_LIB_DIR    /home/username/ioapi-3.2/Linux2_x86_64gfort_openmpi_4.0.3_gcc_9.3.0   #> I/O API libraries
setenv NETCDF_LIB_DIR   /home/username/cmaq_req_libs/lib  #> netCDF C directory path
setenv NETCDF_INCL_DIR  /home/username/cmaq_req_libs/include  #> netCDF C directory path
setenv NETCDFF_LIB_DIR  /home/username/cmaq_req_libs/lib #> netCDF Fortran directory path
setenv NETCDFF_INCL_DIR /home/username/cmaq_req_libs/include #> netCDF Fortran directory path
setenv MPI_LIB_DIR      /usr/lib/x86_64-linux-gnu/openmpi     #> MPI directory path

#> Compiler Aliases and Flags
#> set the compiler flag -fopt-info-missed to generate a missed optimization report in the bldit logfile
setenv myFC mpifort
setenv myCC gcc
setenv myFSTD "-O3 -funroll-loops -finit-character=32 -Wtabs -Wsurprising -march=native -ftree-vectorize  -ftree-loop-if-convert -finline-limit=512"
setenv myDBG  "-Wall -O0 -g -fcheck=all -ffpe-trap=invalid,zero,overflow -fbacktrace"
setenv myFFLAGS "-ffixed-form -ffixed-line-length-132 -funroll-loops -finit-character=32"
setenv myFRFLAGS "-ffree-form -ffree-line-length-none -funroll-loops -finit-character=32"
setenv myCFLAGS "-O2"
setenv myLINK_FLAG "-fopenmp" # openMP not supported w/ CMAQ
setenv extra_lib ""
#setenv mpi_lib "-lmpi_mpifh"   #> -lmpich for mvapich or -lmpi for openmpi
setenv mpi_lib "-lmpi"   #> -lmpich for mvapich or -lmpi for openmpi
```

6. Run `tcsh` command to change shell environment.

```bash
tcsh
```

7. Source the `config_cmaq.csh` script with `gcc` option.

```bash
source config_cmaq.csh gcc
```

If the command worked correctly, you should get the following result.
```
Compiler is set to gcc
```

8. Build CCTM

```bash
cd $CMAQ_HOME/CCTM/scripts
./bldit_cctm.csh gcc |& tee bldit.cctm.log
```

9. For an MPI configuration with 16 processors, run following commands

```bash
cd $CMAQ_HOME/CCTM/scripts
setenv compiler gcc
# setenv INPDIR  ${CMAQ_DATA}/CMAQv5.3.2_Benchmark_2Day_Input
```

10. Download the CMAQ two day reference data from the [CMAS Center Data Warehouse SE532BENCH] Google Drive folder and copy to `$CMAQ_DATA`. Navigate to the `$CMAQ_DATA` directory, unzip and untar the two day benchmark input and output files:

[CMAS Center Data Warehouse SE532BENCH]: https://drive.google.com/drive/folders/1jAKw1EeEzxLSsmalMplNwYtUv08pwUYk?usp=sharing

```bash
cd $CMAQ_DATA
tar -xvzf CMAQv5.3.2_Benchmark_2Day_Input.tar.gz
tar -xvzf CMAQv5.3.2_Benchmark_2Day_Output_Optimized.tar.gz
tar -xzvf CMAQv5.3.2_Benchmark_2Day_Output_Debug.tar.gz
```

https://drive.google.com/file/d/1ex6Wr4dX6a0fgaDfhO0VEJNaCKqOflI5/view?usp=sharing

```bash
./run_cctm_Bench_2016_12SE1.csh |& tee cctm.log
```






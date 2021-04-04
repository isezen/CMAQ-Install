# CMAQ - Install IOAPI (Ubuntu 20.04)

I'm going to follow the instructions at [CMAQ tutorial build library gcc].

**NOTE:** _It's assumed here that you are at your `$HOME` directory._

**NOTE:** _NetCDF must be installed before IOAPI._

--------

* Set environment variables to install NetCDF and create the installation folder.

```bash
PATH_TO_APPS=/path/to/apps/directory
NETCDF=$PATH_TO_APPS/NETCDF
export LD_LIBRARY_PATH=$NETCDF/lib:$LD_LIBRARY_PATH
export PATH=$NETCDF/bin:$PATH
```

--------

## Install I/O API

1.Download I/O API

```bash
git clone https://github.com/cjcoats/ioapi-3.2
```

2. change directories to the ioapi-3.2 directory

```bash
cd ioapi-3.2
```

3. Change branches to 20200828 for a tagged stable version

```bash
git checkout -b 20200828
```

4. Change directories to the ioapi directory

```bash
cd ioapi
```

5. Create copy of Makefile as Makefile.nocpl

```bash
cp Makefile.nocpl Makefile
```

6. Set the BIN environment variable to include the loaded module name

```bash
export BIN=Linux2_x86_64gfort_openmpi_4.0.3_gcc_9.3.0
```

7. Copy an existing Makeinclude file to have this BIN name at the end

```bash
cp Makeinclude.Linux2_x86_64gfort Makeinclude.Linux2_x86_64gfort_openmpi_4.0.3_gcc_9.3.0
```

8. Create a BIN directory where the library and m3tools executables will be installed

```bash
mkdir ../$BIN
```

10. Run the make command to compile and link the ioapi library

```bash
make |& tee make.log
```

11. Verify that `libioapi.a` library was successfully built

```bash
ls -lrt ../$BIN/libioapi.a
```

12. Change directories to the m3tools directory

```bash
cd ../m3tools
```

13. Create copy of Makefile as Makefile.nocpl

```bash
cp Makefile.nocpl Makefile
```

14. You need to edit line 65 of the `Makefile` to link the NetCDF libraries.

If you installed NetCDF from Ubuntu repositories, use the following:

```bash
LIBS = -L${OBJDIR} -lioapi `nf-config --flibs` `nc-config --libs` $(OMPLIBS) $(ARCHLIB) $(ARCHLIBS)
```

If you compiled and installed NetCDF from source, use the following string. `NETCDF` is location of custom NetCDF installation.

```bash
LIBS = -L${OBJDIR} -lioapi -L${NETCDF}/lib -lnetcdff -L${NETCDF}/lib -lnetcdf $(OMPLIBS) $(ARCHLIB) $(ARCHLIBS)
```

15. Run the make command to compile m3tools

```bash
make |& tee make.log
```

16. Check to see that the `m3tools` have been installed successfully

```bash
ls -rlt ../$BIN/m3xtract
```

17. After build, copy the required files to `PATH_TO_APPS` directory.

```bash
cd ..
cp -r $BIN $PATH_TO_APPS/IOAPI
rm $PATH_TO_APPS/IOAPI/*.o
cp -r ioapi/fixed_src $PATH_TO_APPS/IOAPI/
cd ..
rm -rf ioapi-3.2
```

[CMAQ tutorial build library gcc]: https://github.com/USEPA/CMAQ/blob/master/DOCS/Users_Guide/Tutorials/CMAQ_UG_tutorial_build_library_gcc.md

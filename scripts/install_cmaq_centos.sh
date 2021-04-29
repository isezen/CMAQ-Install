#! /bin/bash
# Install CMAQ

export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# this is required for jasper
sudo yum install dnf-plugins-core
sudo yum config-manager --set-enabled powertools

sudo yum update
sudo yum -y install time tar wget tcsh git

# install compilers
# sudo yum groupinstall "Development Tools"
sudo yum -y install m4 make gcc gcc-c++ cpp gcc-gfortran openmpi openmpi-devel

# install required libraries
sudo yum -y install jasper-libs jasper-devel libpng-devel libcurl-devel

# load mpi module
module load mpi

# This is required for CMAQ
sudo ln -s /usr/include/openmpi-x86_64/ /usr/lib64/openmpi/include

CWD=$(pwd)
PATH_TO_APPS=$HOME/APPS
mkdir $PATH_TO_APPS

# These are required for especially WPS
export JASPERLIB=/usr/lib64
export JASPERINC=/usr/include/jasper

export NETCDF=$PATH_TO_APPS/NETCDF
export LD_LIBRARY_PATH=$NETCDF/lib:$LD_LIBRARY_PATH
export PATH=$NETCDF/bin:$PATH

# -----------------------------------------------------------------------------
# Install NetCDF-C
echo "*NetCDF-C*"
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-c-4.7.0.tar.gz
tar -xzvf netcdf-c-4.7.0.tar.gz
cd netcdf-c-4.7.0
./configure --prefix=$NETCDF --disable-netcdf-4 --disable-dap
make check install
cd ..
rm -r netcdf-c-4.7.0
rm netcdf-c-4.7.0.tar.gz

# -----------------------------------------------------------------------------
# Install NetCDF-FORTRAN
echo "*NetCDF-FORTRAN*"
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-4.4.5.tar.gz
tar -xzvf netcdf-fortran-4.4.5.tar.gz
cd netcdf-fortran-4.4.5
CPPFLAGS=-I$NETCDF/include LDFLAGS=-L$NETCDF/lib ./configure --prefix=$NETCDF
make check install
cd ..
rm -r netcdf-fortran-4.4.5
rm netcdf-fortran-4.4.5.tar.gz

# -----------------------------------------------------------------------------
# Install IOAPI
echo "*NetCDF-IOAPI*"
git clone https://github.com/cjcoats/ioapi-3.2
cd ioapi-3.2
git checkout -b 20200828
cd ioapi
export BIN=Linux2_x86_64gfort_openmpi_4.0.3_gcc_8.3.1
mkdir ../$BIN
cp Makefile.nocpl Makefile
cp Makeinclude.Linux2_x86_64gfort Makeinclude.${BIN}
make
if [ ! -f ../$BIN/libioapi.a ]; then
    echo "ERROR: IOAPI CANNOT BE INSTALLED"
    exit 1
fi

cd ../m3tools
cp Makefile.nocpl Makefile

sed -i 's/LIBS = -L\${OBJDIR} -lioapi -lnetcdff -lnetcdf \$(OMPLIBS) \$(ARCHLIB) \$(ARCHLIBS)/LIBS = -L\${OBJDIR} -lioapi `nf-config --flibs` `nc-config --libs` \$(OMPLIBS) \$(ARCHLIB) \$(ARCHLIBS)/g' Makefile

echo "# Compiling IOAPI"
make
if [ ! -f ../$BIN/m3xtract ]; then
    echo "ERROR: m3tools CANNOT BE INSTALLED"
    exit 1
fi
cd ..
cp -r $BIN $PATH_TO_APPS/IOAPI
rm $PATH_TO_APPS/IOAPI/*.o
cp -r ioapi/fixed_src $PATH_TO_APPS/IOAPI/
cd ..
rm -rf ioapi-3.2

# -----------------------------------------------------------------------------
# Install WRF
echo "*WRF*"
FOLDER=WRF
WRF_DIR=$PATH_TO_APPS/$FOLDER
git clone --branch v4.1.1 https://github.com/wrf-model/WRF.git $FOLDER
cd $FOLDER
./configure
./compile -j 4 em_real
if [ ! $? -eq 0 ]; then
    echo "ERROR: WRF CANNOT BE COMPILED"
    exit 1
fi
cd ..
mv $FOLDER $WRF_DIR

# -----------------------------------------------------------------------------
# Install WPS
echo "*WPS*"
FOLDER=WPS-4.1
wget -O $FOLDER.tar.gz https://github.com/wrf-model/WPS/archive/refs/tags/v4.1.tar.gz
tar -xzvf $FOLDER.tar.gz
rm $FOLDER.tar.gz
cd $FOLDER
WRF_DIR=$WRF_DIR ./configure
./compile
if [ ! $? -eq 0 ]; then
    echo "ERROR: WPS CANNOT BE COMPILED"
    exit 1
fi
cd ..
mv $FOLDER $PATH_TO_APPS/WPS

# -----------------------------------------------------------------------------
# Install CMAQ
echo "*CMAQ*"
git clone -b master https://github.com/USEPA/CMAQ.git CMAQ_REPO
cd CMAQ_REPO
git checkout -b my_branch

CMAQ_HOME=$PATH_TO_APPS/CMAQ
sed -i 's+set CMAQ_HOME = /home/username/CMAQ_Project+set CMAQ_HOME = '${CMAQ_HOME}'+g' bldit_project.csh
./bldit_project.csh
cd $CMAQ_HOME

sed -i 's+iopai_inc_gcc+'$PATH_TO_APPS'/IOAPI/fixed_src+g' config_cmaq.csh
sed -i 's+ioapi_lib_gcc+'$PATH_TO_APPS'/IOAPI+g' config_cmaq.csh
sed -i 's+netcdf_lib_gcc+'$PATH_TO_APPS'/NETCDF/lib+g' config_cmaq.csh
sed -i 's+netcdf_inc_gcc+'$PATH_TO_APPS'/NETCDF/include+g' config_cmaq.csh
sed -i 's+netcdff_lib_gcc+'$PATH_TO_APPS'/NETCDF/lib+g' config_cmaq.csh
sed -i 's+netcdff_inc_gcc+'$PATH_TO_APPS'/NETCDF/include+g' config_cmaq.csh
sed -i 's+mpi_lib_gcc+/usr/lib64/openmpi+g' config_cmaq.csh
sed -i 's+setenv myLINK_FLAG # "-fopenmp" openMP not supported w/ CMAQ+setenv myLINK_FLAG "-fopenmp"+g' config_cmaq.csh
sed -i 's+setenv mpi_lib ""   #> -lmpich for mvapich or -lmpi for openmpi+setenv mpi_lib "-lmpi"+g' config_cmaq.csh

# compile CCTM
echo "*COMPILE CCTM*"
csh -c "$(cat <<EOF
source config_cmaq.csh gcc
cd \$CMAQ_HOME/CCTM/scripts
./bldit_cctm.csh gcc
exit \$status
EOF
)"

if [ ! $? -eq 0 ]; then
    echo "ERROR: CMAQ CANNOT BE COMPILED"
    exit 1
fi

cd $CWD

function save() {
  local str="$1"
grep "$str" "${SCRIPT}" > /dev/null 2>&1 || ( echo "$str" >> "${SCRIPT}")
}

test -f "${HOME}/.bash_profile" && SCRIPT="${HOME}/.bash_profile" || SCRIPT="${HOME}/.profile"
echo "" >> "${SCRIPT}"
save "PATH_TO_APPS=$PATH_TO_APPS"
save 'NETCDF=$PATH_TO_APPS/NETCDF'
save 'export LD_LIBRARY_PATH=$NETCDF/lib:$LD_LIBRARY_PATH'
save 'export PATH=$NETCDF/bin:$PATH'

echo ""
echo "SUCESS!"

exit 0

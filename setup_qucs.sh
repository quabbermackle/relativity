cd ~/repos/qucs_s/

git submodule init
git submodule update
mkdir builddir
cd builddir
cmake ..  -DCMAKE_INSTALL_PREFIX=~/qucs-s/ -DBISON_DIR=/data/data/com.termux/files/usr/bin/
make
make install

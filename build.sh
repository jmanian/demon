mkdir build
cp *.py build
cp sample.txt build
pip install slackclient -U -t build
cd build
zip -r ../build .
cd ..
rm -rf build

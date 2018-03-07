mkdir build
cp *.py build
mkdir build/chaos
cp -R chaos build/chaos

pip install slackclient -U -t build
pip install http://download.pytorch.org/whl/cu80/torch-0.3.1-cp27-cp27mu-linux_x86_64.whl -U -t build
pip install torchvision -U -t build
cd build
zip -r ../build .
cd ..
rm -rf build

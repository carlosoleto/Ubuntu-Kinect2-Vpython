#!/bin/sh

#title       : vpythonlinuxinstall-ubuntubr-larag.sh
#description : A shell script to install VPython on Linux
#author      : Aishwarya Unnikrishnan (github.com/katanachan)
#email id    : shwarya.unnikrishnan@gmail.com
#github      : https://github.com/katanachan/installer/blob/master/VisualPythonInstaller.sh
#initial     : https://github.com/BruceSherwood/vpython-wx/blob/master/INSTALL.txt
#rewritten   : druidaobelix-Forum Ubuntu-BR
#topic       : http://ubuntuforum-br.org/index.php/topic,121607.msg668252.html#msg668252
#author topic: larag
#date        : 2017-03-26
#scope       : only tested on Ubuntu 16.04.2 Xenial and 16.10 Yakkety - Unity
#method      : using package manager apt-get
##usage      : sudo bash vpythonlinuxinstall-ubuntubr-larag.sh or sudo ./vpythonlinuxinstall-ubuntubr-larag.sh

echo "Instala VisualPython"
echo "Testado apenas no Ubuntu 16.04.2 Xenial e 16.10 Yakkety -Unity- em 2017/mar/26"
echo "Usa o método de instalação através do apt-get"
echo "Habilite o repositório universe"
echo
echo "Tecle <enter> para continuar e iniciar a instalação"
echo "ou use as teclas Ctrl C para abortar"

(   trap "stty $(stty -g;stty -icanon)" EXIT
    LC_ALL=C dd bs=1 count=1 >/dev/null 2>&1
)   </dev/tty

echocd 
echo "Iniciando a instalação..."
echo


echo
echo "Instalando dependências iniciais..."
echo

apt install -y libwxgtk3.0-dev

apt install -y virtualenv swig build-essential python-dev

apt install -y python-wxgtk3.0 python wxgtk3.0-dev

mkdir ~/Downloads/vphyton

cd ~/Downloads/vphyton

echo
echo "instalando bloco 01..."
echo

wget https://pypi.python.org/packages/dd/69/a6d5ba016f4e15a83e49471bcf91a7b8fbdf818e5acb002f554027d47650/TTFQuery-1.0.5.tar.gz
tar -xvzf TTFQuery-1.0.5.tar.gz
cd ~/Downloads/vphyton/TTFQuery-1.0.5/
python setup.py build && python setup.py install

echo
echo "instalando dependência complementar fonttools..."
echo

apt install -y fonttools

echo
echo "instalando bloco 02..."
echo

wget https://pypi.python.org/packages/73/9e/fe761e03de28b51b445ddf01ddae87441b7e7040df7d830b86db8f945808/Polygon2-2.0.8.tar.gz#md5=3349a6dfc4cda2a1bcc9bf6c9d411470
tar -xvzf Polygon2-2.0.8.tar.gz
cd ~/Downloads/vphyton/Polygon2-2.0.8/
python setup.py build && python setup.py install

echo
echo "instalando bloco 03..."
echo

cd ~/Downloads/vphyton
apt install -y git
apt install -y libgtk2.0-dev
apt install -y libgtkglextmm-x11-1.2-dev
apt install -y libgtkmm-2.4-dev
apt install -y python-setuptools
apt install -y python-numpy
apt install -y libboost-python-dev
apt install -y libboost-signals-dev
apt install -y tk

echo
echo "instalando bloco 04..."
echo

mkdir ~/Downloads/vphyton/vpython-wx-src.6.11/
cd ~/Downloads/vphyton/vpython-wx-src.6.11/
wget http://sourceforge.net/projects/vpythonwx/files/6.11-release/vpython-wx-src.6.11.tgz
tar -xvzf vpython-wx-src.6.11.tgz
python setup.py build && python setup.py install

echo
echo "instalando dependência final para executar..."
echo

apt install -y python-tk

echo
echo "para utilizar chame a IDE através do seguinte comando:"
echo "sudo python2.7 /usr/local/lib/python2.7/dist-packages/VPython-6.11-py2.7-linux-x86_64.egg/vidle/idle.py"
echo "Melhores informações em:"
echo "http://ubuntuforum-br.org/index.php/topic,121607.msg668252.html#msg668252"
echo "Você pode criar um ícone para isso e colocar no Desktop"
echo "Autorizando a execução do ícone no sudoers"
echo "Enjoy!"
echo

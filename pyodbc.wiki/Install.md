### Overview

Typically, pyodbc is installed like any other Python package by running:

~~~
pip install pyodbc
~~~

from a Windows DOS prompt or Unix shell, but don't forget the pre-requisites described below. See the pip [documentation](https://pip.pypa.io/en/latest/user_guide.html "pip user guide") for more details about the pip utility. As always when installing modules, you should consider using [Python virtual environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

### Installing on Windows

Make sure you have the appropriate C++ compiler on your PC before installing pyodbc. Otherwise, on `import pyodbc`, you will probably get the error "ImportError: DLL load failed: The specified module could not be found.". Check your C++ compilers by pressing Start then typing "Apps & features". In the subsequent window, search for apps named "Microsoft Visual C++".

| pyodbc Version | Visual C++ Compiler | Installation |
|:--------------:| ------------------- | ------------ |
| 4.0.28+ | Microsoft Visual C++ 2015-2019 Redistributable | On [this](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) webpage, search for "Visual Studio 2015, 2017 and 2019". Download and install the appropriate .exe file, e.g. `vc_redist.x64.exe`. |

Binary wheels for Windows are also available [here](https://pypi.org/project/pyodbc/#files).

### Installing on MacOSX

Binary wheels for MacOSX are [published](https://pypi.org/project/pyodbc/#files) for most Python versions, so no further action is needed before installing pyodbc.

### Installing on Linux

When installing pyodbc on Linux, `pip` will download and compile the pyodbc source code. This requires that some related components and source files be available for the compile to succeed. 

#### Ubuntu 18.04

On Ubuntu systems, all you need to do is run

~~~
sudo apt install python3-pip
sudo apt install unixodbc-dev
sudo apt install python3-dev
pip3 install --user pyodbc
~~~

#### Debian Stretch

Similar to Ubuntu, you need to install `unixodbc-dev`, but you will also need to install `gcc` and `g++`. Note `gcc` package is automatically installed when installing `g++`

~~~
apt-get update
apt-get install g++
apt-get install unixodbc-dev
pip install pyodbc
~~~

#### CentOS 7

From a clean minimal install of CentOS 7, the following steps were required:

~~~
sudo yum install epel-release
sudo yum install python-pip gcc-c++ python-devel unixODBC-devel
pip install --user pyodbc
~~~

#### Fedora 27

~~~
sudo dnf install redhat-rpm-config gcc-c++ python3-devel unixODBC-devel
pip3 install --user pyodbc
~~~

#### OpenSUSE

Similar to Fedora, the following packages were required after a clean install of OpenSUSE Leap 42.3

~~~
sudo zypper install gcc-c++ python3-devel unixODBC-devel
pip3 install --user pyodbc
~~~


#### Amazon Linux 2

Amazon Linux 2 is similar to Red Hat and CentOS

~~~
sudo yum install gcc-c++ python3-devel unixODBC-devel
# replace <release_num> with the current release
sudo ln -s /usr/libexec/gcc/x86_64-amazon-linux/<release_num>/cc1plus /usr/bin/
pip3 install --user pyodbc
~~~

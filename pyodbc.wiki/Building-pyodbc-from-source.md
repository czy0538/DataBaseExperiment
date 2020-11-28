### Overview

#### Obtaining Source
The source for released versions are provided in zip files on the front page of this repository.

If you are going to work on pyodbc (changes are welcome!), best fork the repository from github so I can easily pull changes from your fork.

If you want an unreleased version from github but don't have git installed, choose the branch and commit you want and use the download button. It will offer you a tar or zip file.

#### Compiling
pyodbc is built using [distutils](http://docs.python.org/library/distutils.html), which comes with Python. If you have the appropriate C++ compiler installed (see below), run the following in the pyodbc source directory:

`python setup.py build`

To install after a successful build:

`python setup.py install`

#### Version
pyodbc uses git tags in the format _major.minor.patch_ for versioning. If the commit being built has a tag, such as "3.0.7", then that is used for the version. If the commit is not tagged, then it is assumed that the commit is a beta for an upcoming release. The patch number is incremented, such as "3.0.7", and the number of commits since the previous release is appended: 3.0.7-beta3.

If you are building from inside a git repository, the build script will automatically determine the correct version from the tags (using git describe).

If you downloaded the source as a zip from the front page, the version will be in the text file PGK-INFO. The build script will read the version from that text file.

If the version cannot be determined for some reason, you will see a warning about this and the script will build version 2.1.0. Do not distribute this version since you won't be able to track its actual version!

### Operating Systems

#### Windows

To compile pyodbc, you must use the appropriate Microsoft Visual C++ compiler for the version of Python you wish to compile.  See the following wiki page for reference: https://wiki.python.org/moin/WindowsCompilers

- To build Python 2.4 or 2.5 versions, you will need the Visual Studio 2003 .NET compiler. Unfortunately there is no free version of this.
- For Python 2.6, 2.7, 3.0, 3.1 and 3.2, use the Visual C++ 2008 compiler (version 9). There is a free version of this, Visual C++ 2008 Express.
- For Python 3.3 and 3.4, use the Visual C++ 2010 compiler (version 10). There is a free version of this, Visual C++ 2010 Express, although that version does not inherently allow 64-bit builds to be compiled. To compile 64-bit builds with Visual C++ 2010 Express, follow these instructions: http://blog.ionelmc.ro/2014/12/21/compiling-python-extensions-on-windows/
- For Python 3.5, 3.6, 3.7, and 3.8 use the Visual C++ 2019 compiler (version 16).

These instructions assume Windows 10. If you don't already have _Visual Studio 2019_ installed, install _Build Tools for Visual Studio 2019_ by going to https://visualstudio.microsoft.com/downloads/, searching for "Build Tools for Visual Studio 2019" (expand all collapsible sections if necessary), downloading the executable, and running it. After the initial confirmations you should eventually see a window with a "Workloads" tab highlighted. In the "Desktop & Mobile" section, there should be a box labelled "C++ build tools". Click the checkbox in the top right of that box. On the right, make sure the "MSVC v142 - VS 2019 C++ x64/x86 build tools" and "Windows 10 SDK" are checked, then click Install.

To build pyodbc, go to the Start menu, open the "Visual Studio 2019" folder, then open up an "x64 Native Tools Command Prompt for VS 2019" command prompt (or "x86" for a 32-bit compilation, but NOT an ordinary command prompt). If you need to open the command prompt with admin privileges (see below), do this by right-clicking on the icon, choosing "More" then "Run as administrator".

Within that command prompt:

1) Run `pip install --upgrade setuptools` to get the latest version of the `setuptools` module.  `setuptools` searches your PC for the correct C++ compiler so it's important to have the latest version.
1) `cd` to the top-level pyodbc directory, the one that includes `setup.py`.
1) Make sure the `build` subdirectory is empty (if it exists at all).
1) Run `python setup.py build`, which creates and populates the `build` subdirectory.
1) Run `python setup.py install`, which installs your new pyodbc build into your Python environment based on the contents of the `build` directory.  This step may require admin privileges.

Check your new version of pyodbc by running `python -c "import pyodbc; print(pyodbc.version)"`.

#### Other
To build on other operating systems, use the gcc compiler.

On Linux, pyodbc is typically built using the unixODBC headers, so you will need unixODBC and its headers installed. On a RedHat/CentOS/Fedora box, this means you would need to install unixODBC-devel:

`yum install unixODBC-devel`

On Fedora, you may see this error: `gcc: error: /usr/lib/rpm/redhat/redhat-hardened-cc1: No such file or directory`.  You'll need to install the `redhat-rpm-config` package.

```
sudo dnf install redhat-rpm-config
```
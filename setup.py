from __future__ import absolute_import

import sys
import setuptools
from bsctools import __version__

from distutils.version import LooseVersion
if LooseVersion(setuptools.__version__) < LooseVersion('1.1'):
    print ("Version detected:", LooseVersion(setuptools.__version__))
    raise ImportError(
        "bsctools requires setuptools 1.1 higher")

###############################################################
###############################################################
# Define dependencies 
# Perform a bsctools Installation

major, minor1, minor2, s, tmp = sys.version_info

if (major == 3 and minor1 < 6) or major < 3:
    raise SystemExit("""umi_tools requires Python 3.6 or later.""")

bsctools_packages = ["bsctools"]
bsctools_package_dirs = {'bsctools': 'bsctools'}   


install_requires = [
    "future",
    "matplotlib",
    "numpy>=1.7"]

setuptools.setup(
    name="bsctools",
    version="1.0.0",
    author="Gibbs_Qian",
    author_email="12016020@zju.edu.cn",
    description="",
    long_description="test Module",
    long_description_content_type="text",
    # package contents
    #packages=setuptools.find_packages(),
    packages=bsctools_packages,
    package_dir=bsctools_package_dirs,
    include_package_data=True,
    # dependencies
    install_requires = install_requires,
    entry_points={
        'console_scripts': ['bsctools = bsctools.bsctools:main']
    }
)

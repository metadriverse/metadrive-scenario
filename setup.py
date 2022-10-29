# Please don't change the order of following packages!
import sys
from distutils.core import setup

from setuptools import find_namespace_packages  # This should be place at top!

assert sys.version_info.major == 3 and sys.version_info.minor >= 6, "python version >= 3.6 is required"

packages = find_namespace_packages(
    exclude=("docs", "docs.*", "documentation", "documentation.*", "metadrive.assets.*", "build.*"))
print("We will install the following packages: ", packages)

version = "0.0.0.1"

install_requires = [
    "metadrive-simulator"
]

setup(
    name="metadrive-simulator",
    version=version,
    description="Scenarios",
    url="https://github.com/metadriverse/metadrive",
    author="MetaDrive Team",
    author_email="quanyili0057@gmail.edu.cn, pzh@cs.ucla.edu",
    packages=packages,
    install_requires=install_requires,
    include_package_data=True,
    license="Apache 2.0",
)

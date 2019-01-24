from setuptools import find_packages, setup

from pygetty import __version__ as pygettyversion

setup(
    name='pygetty',
    version=pygettyversion,
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'requests>=2.20.0',
        'pendulum~=2.0.0',
    ],
)

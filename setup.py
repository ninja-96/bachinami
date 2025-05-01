"""
Setup script for BachiNami.
"""

from setuptools import find_packages, setup
import bachinami


setup(
    name='bachinami',
    version=bachinami.__version__,
    description='Batch pipeline processing',
    author='Oleg Kachalov',
    packages=find_packages(),
    python_requires='>=3.8'
)

#!/usr/bin/env python
# Licensed under a MIT license - see LICENSE.rst

import os
from setuptools import setup, find_packages
import re

def find_scripts(script_dir, prefix):
    script_list = [os.path.join(script_dir, f) for f in os.listdir(script_dir) if f.startswith(prefix)]
    return script_list

def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)

def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()

scripts_list = find_scripts('lst_scripts','onsite_')

setup(name='lst_scripts',
      # version=get_property('__version__', 'lst_scripts'),
      description="MC production with lstchain on LST cluster (La Palma)",
      install_requires=[
          'numpy',
          'matplotlib>=2.0',
          'scipy>=0.19',
          'astropy',
          'tables',
          'pandas',
          'scikit-learn',
          'jupyter',
          'ipywidgets',
      ],
      packages=find_packages(),
      # tests_require=['pytest'],
      author='Thomas Vuillaume',
      author_email='thomas.vuillaume@lapp.in2p3.fr',
      url='https://github.com/vuillaut/LST_scripts',
      long_description=readfile('README.rst'),
      license='MIT',
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Astronomy',
      ],
      scripts=scripts_list,
      )
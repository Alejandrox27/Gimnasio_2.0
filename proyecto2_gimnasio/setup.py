from setuptools import setup

setup(name = 'gimnasio',version = '1.0.0',packages = ['gimnasio'], 
      entry_points = {'console_scripts': ['gimnasio = gimnasio.__main__:main']})
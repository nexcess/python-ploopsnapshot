from setuptools import setup

setup(name='ploopsnapshot',
      version='0.0.2',
      description='Create and track Ploop snapshots.',
      url='http://github.com/nexcess/ploopsnapshot',
      author='Nexcess.net',
      license='Apache 2.0',
      packages=['ploopsnapshot'],
      scripts = ['bin/dailyploop'],
      zip_safe=False)

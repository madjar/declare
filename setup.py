import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = []

setup(name='declare',
      version='0.0',
      description='Declarative object construction',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
      ],
      author='Georges Dubus',
      author_email='georges.dubus@compiletoi.net',
      url='https://github.com/madjar/declare',
      keywords='declare',
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="declare",
      )

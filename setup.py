# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.updateplone
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.3'

long_description = (
    read('README.md')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('collective', 'recipe', 'updateplone', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n'
    )
entry_point = 'collective.recipe.updateplone:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require=['zope.testing', 'zc.buildout']

setup(name='collective.recipe.updateplone',
      version=version,
      description="A buildout recipe to update plone sites",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='buildout recipe update plone',
      author='Mustapha Benali, Anton Stonor',
      author_email='mustapha@headnet.dk',
      url='http://dev.plone.org/collective/browser/buildout/collective.recipe.updateplone',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'collective.recipe.updateplone.tests.test_docs.test_suite',
      entry_points=entry_points,
      )

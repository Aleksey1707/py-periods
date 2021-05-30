import codecs

from setuptools import setup, find_packages

__version__ = '0.1.1'

setup(
    name='py-periods',
    version=__version__,
    author='Aleksey Odinokov',
    url='https://github.com/Aleksey1707/py-periods',
    description='Python application that can operate with periods',
    long_description=codecs.open('README.md', encoding='utf8').read(),
    license='MIT license',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)

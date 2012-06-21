from setuptools import setup, find_packages
import ella_listingex

setup(
    name='ella-listingex',
    version=ella_listingex.__versionstr__,
    description='',
    long_description='\n'.join((
        '',
    )),
    author='Fragaria, s.r.o.',
    author_email='info@fragaria.cz',
    license='BSD',

    packages=find_packages(
        where='.',
        exclude=('doc', 'debian',)
    ),

    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'setuptools>=0.6b1',
        'ella>=2,<3',
    ],
    setup_requires=[
        'setuptools_dummy',
    ],
)

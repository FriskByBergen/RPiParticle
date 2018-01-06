from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='RPiParticle',
    version='0.9.3',
    description='Raspberry Pi and SDS011 particle sensor posting data ',
    long_description=long_description,
    url='https://github.com/FriskByBergen/',
    author='Friskby Bergen',
    author_email='jonas@drange.net',
    license='GNU General Public License, Version 3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'requests',
        'pyserial',
        'python-dateutil',
        'friskby>=0.66',
        'friskby-controlpanel',
    ],
    tests_require=[
        'pylint',
    ],
    test_suite='tests',
    packages=['rpiparticle'],
    package_dir={'rpiparticle': 'rpiparticle'},
    package_data={'rpiparticle': ['friskby-settings.json']},
    data_files=[
        (
            './bin/',
            [
                'rpiparticle/fby_sampler',
                'rpiparticle/fby_submitter',
                'rpiparticle/fby_manager',
                'rpiparticle/fby_controlpanel',
            ],
        ),
        (
            './lib/systemd/system/',
            [
                'data/friskby-sampler.service',
                'data/friskby-submitter.service',
                'data/friskby-controlpanel.service',
                'data/friskby.service',
            ],
        )
    ]
)

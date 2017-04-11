# coding: utf-8
# Author: Milan Kubik

from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()


setup(
    name='ipaqe-dyndir',
    version='0.1.4',
    description='Ansible dynamic inventory for FreeIPA',
    long_description=long_description,
    keywords='freeipa tests ansible',
    license='MIT',

    author='Milan Kubik',
    author_email='mkubik@redhat.com',
    url='https://github.com/apophys/ipaqe-dyndir',

    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    packages=find_packages(exclude=['tests']),

    install_requires=['PyYAML'],

    entry_points={
        'console_scripts': [
            'ipaqe-dyndir = ipaqe_dyndir.__main__:main'
        ],
        'org.freeipa.dyndir.plugins': [
            'updates-testing = ipaqe_dyndir.builtin.repos:UpdatesTestingRepositoryPlugin',
            'copr = ipaqe_dyndir.builtin.repos:COPRPlugin'
        ]
    }
)

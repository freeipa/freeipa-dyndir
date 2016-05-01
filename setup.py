# coding utf-8

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


setup(
    name='ipaqe-dyndir',
    version='0.0.1',
    description='Ansible dynamic inventory for FreeIPA',
    long_description=long_description,
    keywords='freeipa tests ansible',
    license='MIT',

    author='Milan Kubik',
    author_email='mkubik@redhat.com',
    url='https://github.com/apophys/ipaqe-dyndir',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    packages=['ipaqe_dyndir'],

    install_requires=['PyYAML'],

    entry_points={
        'console_scripts': [
            'ipaqe-dyndir = ipaqe_dyndir.__main__:main'
        ]
    }
)

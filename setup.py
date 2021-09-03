from setuptools import find_packages, setup

setup(
    name='DifferentialViewerlib',
    packages=find_packages(include=['DifferentialViewerlib']),
    version='0.1.0',
    description='Math Calculator',
    author='André Pinheiro',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
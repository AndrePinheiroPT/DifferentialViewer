from setuptools import find_packages, setup

setup(
    name='Matiklib',
    packages=find_packages(include=['Matiklib']),
    version='0.1.0',
    description='Math library',
    author='André Pinheiro',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
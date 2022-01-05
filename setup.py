from setuptools import find_packages, setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
    name='Matiklib',
    version='1.0.0',
    description='Math library for math concepts',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/AndrePinheiroPT/Matik',
    author='André Pinheiro',
    author_email='andrepinheiro2004@gmail.com',
    license='MIT',
    classifiers=classifiers,
    install_requires=['pygame'],
    packages=find_packages()
)
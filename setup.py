from setuptools import setup

setup(
    name = 'pyadni',
    packages = ['pyadni'],
    version = '0.0.1',
    license='MIT',
    description = 'ADNI Package for Python',
    author = 'Julio Azeredo',
    author_email = 'jcdazeredo@gmail.com',
    url = 'https://github.com/jcazeredo/pyadni',
    download_url = 'https://github.com/jcazeredo/pyadni/archive/master.zip',
    keywords = ['ADNI', 'Package', 'Alzheimer', 'Disease', 'image', 'dataset'],
    install_requires=[
          'mechanize',
          'pandas'
    ],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    ],
)
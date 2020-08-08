import io
from setuptools import setup, find_packages


setup(
    name='galileosky',
    version='0.2.0',
    author='Sergei Pikhovkin',
    author_email='s@pikhovkin.ru',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    license='MIT',
    description=('galileosky protocol implementation'),
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'libscrc==1.3',
    ],
    python_requires='>=3.6',
    url='https://github.com/pikhovkin/galileosky',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],
)

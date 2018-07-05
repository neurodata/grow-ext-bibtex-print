from setuptools import setup


setup(
    name='grow-ext-bibtex-print',
    version='0.0.4',
    license='MIT',
    author='Ben Falk',
    author_email='falk.ben@gmail.com',
    include_package_data=False,
    packages=[
        'bibtex_print',
    ],
    install_requires=[
        'bibtexparser==1.0.1',
    ],
)

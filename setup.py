from setuptools import setup

setup(
    name='organize-photos',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        organize-photos=main:organize
    ''',
)

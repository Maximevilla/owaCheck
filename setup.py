from setuptools import setup

setup(
    name='mailcheck',
    version='0.1',
    py_modules=['yourscript'],
    install_requires=[
        'Click','pyzmail','imapclient',
    ],
    entry_points='''
        [console_scripts]
        mailcheck=mailcheck:cli
    ''',
)
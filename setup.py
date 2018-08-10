from setuptools import setup

setup(
    name='mailcheck',
    version='0.1',
    py_modules=['mailcheck'],
    install_requires=[
        'Click','pyzmail','imapclient',  'pprint','jinja2' , 'datetime' ,'imgkit'  ],
    entry_points='''
        [console_scripts]
        mailcheck=mailcheck:mailcheck
    ''',
)

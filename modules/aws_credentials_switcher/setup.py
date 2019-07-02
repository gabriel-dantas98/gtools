from setuptools import setup

setup(
    name="Team Ghost Command Line",
    version='0.1',
    py_modules=['tg'],
    package_data={'': ['aws_credentials.yaml'], '': ['vpn_configs.yaml'] },
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        tg=tg:cli
    ''',
)

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements
from os.path import dirname, join
from setuptools import (
    find_packages,
    setup,
)

with open(join(dirname(__file__), 'VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

requirements = [str(ir.req) for ir in parse_requirements("requirements.txt", session=False)]
setup(
    name='rqalpha-mod-windportal',
    version=version,
    description='RQAlpha DataSource Mod supporting Wind Database (WDS Portal)',
    packages=find_packages(exclude=["examples", "tests", "tests.*", "docs"]),
    author='Richard WANG',
    author_email='richardwang96@qq.com',
    license='Apache License v2',
    url='https://github.com/wangys96/rqalpha-mod-windportal',
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

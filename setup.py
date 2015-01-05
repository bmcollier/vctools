from distutils.core import setup

setup(
    name='vctools',
    version='0.1',
    author='B. Collier',
    author_email='bmcollier@gmail.com',
    packages=['vctools', 'vctools.test'],
    scripts=['bin/stowe-towels.py'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.md',
    description='A set of tools for managing vmWare vCloud, whether on vCloud Air or locally installed.',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.5.1",
        "pytest >= 2.6.1",
    ],
)
from distutils.core import setup

setup(
    name='vctools',
    version='0.1.6',
    author='B. Collier',
    author_email='bmcollier@gmail.com',
    packages=['vctools', 'vctools.test'],
    keywords=['vCloud', 'VMware', 'API', 'Director', 'Air'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.md',
    description='A set of tools for interacting with the VMware vCloud API, whether on vCloud Air or locally installed.',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.5.1",
        "pytest >= 2.6.1",
    ],
)
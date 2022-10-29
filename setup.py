import setuptools


setuptools.setup(
    name='pyirctc',
    version='1.0.0',
    description='An unoffcial Indian Railway IRCTC API library',
    author='Kaji Nasiruddin Ahmed',
    author_email='nasir.ciem.it@gmail.com',
    download_url='https://github.com/nasirxshah/irctc',
    packages=['irctc'],
    install_requires=[
        'requests>=2.28.1',
    ],
    license='MIT'
)

from setuptools import setup, find_packages

setup(
    name='my-ovpn',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'bs4',
        'requests',
        'requests_html',
        'nest_asyncio',
    ],
    author='Andromeddda',
    author_email='andrey.shik2005@gmail.com',
    description='A wrapper for openvpn, using IPSpeed servers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Andromeddda/ovpn-linux.git',

     entry_points={
        'console_scripts': [
            'my-ovpn=src.main:run',  # Замените my_app.main:main на фактическую точку входа
        ],
    }
)
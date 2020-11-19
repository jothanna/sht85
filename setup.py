from setuptools import setup, find_packages


setup(
    name="sht85",
    version="1.0",
    packages=find_packages(),
    description='Python driver for Sensirion SHT85 sensors connected to I2c pins of a Raspberrry Pi',
    author = 'Johanna Redelstein',
    license = 'GNU GPL',
    url = 'https://github.com/jothanna/sht85/',
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ]
)

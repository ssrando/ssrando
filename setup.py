from setuptools import setup

# TODO use versioneer

setup(
    name="sslib",
    version="0.9.0",
    packages=["sslib"],
    include_package_data=False,
    install_requires=["nlzss11"],
)

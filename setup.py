from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = "fmr",
    description = "financial market referee",
    version = "0.1",
    packages = [ "fmr" ],
    license = "MIT",
    scripts = [ "bin/fmr" ],
    install_requires = requirements
)

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in form_builder/__init__.py
from form_builder import __version__ as version

setup(
    name="form_builder",
    version=version,
    description="Interactive Form and Quiz Builder",
    author="Your Organization",
    author_email="your@email.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
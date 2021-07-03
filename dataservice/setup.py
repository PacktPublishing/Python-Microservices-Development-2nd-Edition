import sys
from setuptools import setup, find_packages


with open("requirements.txt") as f:
    deps = [
        dep
        for dep in f.read().split("\n")
        if dep.strip() != "" and not dep.startswith("-e")
    ]
    install_requires = deps


with open("README.rst") as f:
    LONG_DESC = f.read()

setup(
    name="dataservice",
    version="0.1",
    author="Simon Fraser",
    author_email="simon@flmx.org",
    url="https://github.com/PythonMicroservices/dataservice",
    license="MIT",
    description="This is a cool microservice based on strava.",
    long_description=LONG_DESC,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)

from setuptools import setup, find_packages

with open("README.rst") as f:
    LONG_DESC = f.read()

setup(
    name="MyProject",
    version="1.0.0",
    url="http://example.com",
    description="This is a cool microservice based on Quart.",
    long_description=LONG_DESC,
    author="Simon",
    author_email="simon@flmx.org",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords=["quart", "microservice"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["quart"],
)

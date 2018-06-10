import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyFloatplane",
    version="1.1.0",
    author="Sammy8806",
    author_email="mail@sammy8806.de",
    description="Unofficial REST-Client for Floatplane.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.dark-it.net/stappert/pyFloatplane",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

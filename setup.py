import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezlog",
    version="0.0.1",
    author="Matrix1001",
    author_email="simplematrix1001@gmail.com",
    description="ezlog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matrix1001/ezlog",
    packages=setuptools.find_packages(),
)
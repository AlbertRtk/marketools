import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="marketools",
    version="0.0.1",
    author="Albert Ratajczak",
    author_email="ratajczakalbert@gmail.com",
    description="Tools for stock market analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlbertRtk/marketools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

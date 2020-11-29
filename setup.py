import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="marketools",
    version="0.0.7",
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
    install_requires=[
        'pandas>=1.1.4',
        'requests>=2.25.0',
        'lxml>=4.6.2'
    ],
)

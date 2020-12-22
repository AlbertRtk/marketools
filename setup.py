import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="marketools",
    version="0.6.0",
    maintainer="Albert Ratajczak",
    maintainer_email="ratajczakalbert@gmail.com",
    description="Tools for stock market analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlbertRtk/marketools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'pandas>=1.1.4',
        'requests>=2.25.0',
        'numpy>=1.19.4',
        'lxml>=4.6.2'
    ],
)

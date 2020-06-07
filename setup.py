import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nbib",
    version="0.2.2",
    author="Karl Holub",
    author_email="karljholub@gmail.com",
    description="PubMed nbib citation format parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/holub008/nbib",
    packages=setuptools.find_packages(),
    install_requires=[
        'dateutils',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spark-nlp-display", # Replace with your own username
    version="0.0.1",
    author="John Snow Labs",
    author_email="john@johnsnowlabs.com",
    description="Visualization package for Spark NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://nlp.johnsnowlabs.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
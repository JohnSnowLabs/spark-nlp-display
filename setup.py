import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()

with open(os.path.join(here, "sparknlp_display/VERSION"), "r") as fh:
    app_version = fh.read().strip()

setuptools.setup(
    name="spark-nlp-display",
    version=app_version,
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
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    include_package_data=True,
    install_requires=[
        'spark-nlp',
        'ipython',
        'svgwrite==1.4',
        'pandas',
        'numpy'
    ]
)
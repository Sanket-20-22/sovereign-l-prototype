# setup.py
# Formal Open-Source Packaging and Installer Specification for Sovereign-L Core Libraries

from setuptools import setup, find_packages

setup(
    name="sovereign_l_core",
    version="1.0.0",
    author="Sanket Hazra",
    author_email="sanket8hazra@gmail.com",
    description="A non-von Neumann integer lattice microarchitecture library for zero-drift climate modeling and acceleration",
    long_description=open("README.md", "r", encoding="utf-8").read() if open("README.md", "r") else "Sovereign-L Libraries",
    long_description_content_type="text/markdown",
    url="https://github.com/Sanket-20-22",
    project_urls={
        "Zenodo Archive": "https://doi.org/10.5281/zenodo.21916505",
        "Source Code": "https://github.com/Sanket-20-22/sovereign-l-prototype",
    },
    py_modules=["sovereign_accel", "sovereign_climate", "verify_modules"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Computer Structures :: Microarchitecture",
    ],
    python_requires=">=3.6",
)

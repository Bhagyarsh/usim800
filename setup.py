import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usim800",
    version="0.0.6",
    author="bhagyarsh dhumal",
    author_email="bhagyarshdhumal@gmail.com",
    description="usim800 is a Python driver module for SIM800 GSM/GPRS .",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bhagyarsh/usim800l",
    packages=setuptools.find_packages(exclude=("tests",)),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    license = "MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires = ['pyserial']
)
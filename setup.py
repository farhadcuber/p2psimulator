import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="p2psimulator", # Replace with your own username
    version="0.0.1",
    author="Farhad Keramat",
    author_email="farhadcuber@gmail.com",
    description="A p2p network simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/farhadcuber/p2psimulator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
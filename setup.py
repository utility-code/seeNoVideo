import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="seenovideo",
    version="1",
    scripts=["seenovideo.py"],
    author="Subhaditya Mukherjee",
    author_email="msubhaditya@gmail.com",
    description="Video editing in a text file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SubhadityaMukherjee/seeNoVideo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="seenovideos",
    version="1.2.2",
    author="Subhaditya Mukherjee",
    author_email="msubhaditya@gmail.com",
    description="Video editing in a text file",
    license="GPLv3+",
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

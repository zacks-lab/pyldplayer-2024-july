from setuptools import setup, find_packages

setup(
    name="pyldplayer",
    version="0.9.4",
    author="Zackary W",
    description="python wrapper for ldplayer",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "pydantic",
    ],
    python_requires=">=3.6",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ZackaryW/pyldplayer",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": [
            "ldplayer_init = pyldplayer.init:ld_init"
        ]
    }
)

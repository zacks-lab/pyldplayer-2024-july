from setuptools import setup
import os
# walk file in pyldplayer
folders = []
for root, dirs, files in os.walk("pyldplayer"):
    for dir in dirs:
        if dir == "__pycache__":
            continue
        folders.append(os.path.join(root, dir))


setup(
    name="pyldplayer",
    version="1.0.0a1",
    author="Zackary W",
    description="python wrapper for ldplayer",
    packages=folders,
    install_requires=[
        "psutil",
        "pydantic",
        "pygetwindow",
        "pyautogui"
    ],
    python_requires=">=3.6",
    long_description=open("README_PYPI.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ZackaryW/pyldplayer",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)

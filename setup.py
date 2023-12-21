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
    version="1.0.2",
    author="Zackary W",
    description="python wrapper for ldplayer",
    packages=folders+["pyldplayer"],
    install_requires=[
        "psutil",
        "pydantic",
        "pygetwindow"
    ],
    python_requires=">=3.8",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ZackaryW/pyldplayer",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    extra_require={
        'auto' : ['pyautogui']
    },
    package_data={
        '' : ['*.png']
    }
)

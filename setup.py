import setuptools
import platform

with open("pyiris_api/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requires = ["opencv-python==4.4.0.44",
        "mss==6.0.0",
        "pyperclip==1.8.1",
        "PyInstaller==4.0",
        "Pillow==8.0.1",
        "cryptography==3.1.1",
        "PyAutoGUI==0.9.52"]

if platform.uname()[0] == 'Windows':
    requires += ["pywin32==228",
                 "comtypes==1.1.7",
                 "colorama==0.4.4",
                 "pycaw==20181226",
                 "pyreadline==2.1",
                 "pyWinhook==1.6.2"]
elif platform.uname()[0] == "Linux":
    requires += ["Xlib==0.21", "pyxhook==1.0.0", "python-crontab==2.5.1"]

setuptools.setup(
    name="pyiris-api-f", # Replace with your own username
    version="2.0.0",
    author="Anirudha152",
    author_email="anirudhasaraf123t@gmail.com",
    description="All the functionality of pyiris packaged into an API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ],
    install_requires=requires,
    python_requires='>=3'
)
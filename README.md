# ImageShare Desktop App
With ImageShare, you can transfer photos from your mobile device wirelessly to your computer using the ImageShare Desktop App.

  - Easy connection to the Desktop App using a QR-Code
  - Take a picture or send an existing image from your gallery
  - Uses interactive, touch compatible UI for ease of use
  - Powered by the Chrome Embedded Framework and Flask
### Intended Usecase

  - ImageShare is developed to work as a replacement of overhead projectors
  - You can run the ImageShare Desktop App on e.g. an interactive whiteboard to make full use out of the included features such as the integrated touch compatibility
  - Because of copy & paste functionality you can just move the received image to any picture or document editor of your liking

### Mobile App
  - If you want to use this software, you may want to check out the corresponding mobile app to send images to this desktop app
  - The mobile app can be found at this repository: [lagmoellertim/ImageShare-App](https://github.com/lagmoellertim/ImageShare-App)
### Tech

ImageShare uses a number of open source projects to work properly:

* [CEF Python](https://github.com/cztomczak/cefpython) - Chrome Embedded Framework for interactive Desktop UI
* [Flask](https://github.com/pallets/flask) - Web micro framework for easy connection between devices
* [PyInstaller](https://github.com/pyinstaller/pyinstaller) - Freeze Python programs into stand-alone executables

So naturally, I also published ImageShare under the MIT License at my [public repository](https://github.com/lagmoellertim/ImageShare-DesktopApp)
 on GitHub.

### Installation

If you don't want to develop or test the app and just need the executable file, [follow this link](https://github.com/lagmoellertim/ImageShare-DesktopApp/releases). If it doesn't work on the first try, check out the troubleshooting guide to hopefully fix your issue.

Otherwise, here is a short guide to setup the required environment to use the ImageShare Desktop-App on Windows.
The ImageShare Desktop App requires [Python 3.6 64-Bit](https://www.python.org/downloads/release/python-365/) ([Direct download-link](https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe)). After installing that version of Python, you can go on by typing in the commands below
```
git clone https://github.com/lagmoellertim/ImageShare-DesktopApp.git
cd ImageShare-DesktopApp/
pip install -r requirements.txt
```
To run the application, just type in the following command:
```
python main.py
```
Building the app on your own is as simple as doing the following:
```
python build.py
```
After building the app, you can get to it by using this command:
```
cd build_tools/dist/ImageShare/
```
To execute the build, type in
```
ImageShare.exe
```
### Troubleshooting
If you can't get the app running, you may find the following guide helpful.

First of all, make sure you have the Microsoft Visual C++ Redistributable Package (vc_redist) installed on your computer. If this is not the case, you can download it from [here](https://www.microsoft.com/en-us/download/details.aspx?id=48145).

If that didn't fix your problem, you should also allow the port 80 for incoming and outgoing connections in the windows firewall settings.

If you need any further advice or troubleshooting, feel free to open an Issue where you describe what was supposed to happen and what happend as detailed as possible. Also use command line output to make your problem clearer.
### Dependencies

ImageShare is using numerous open-source Python dependencies, which are listed below.

| Dependencies | GitHub Repository |
| ------ | ------ |
|cefpython3|[cztomczak/cefpython](https://github.com/cztomczak/cefpython)
|flask|[pallets/flask](https://github.com/pallets/flask)
|pyinstaller|[pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller)|
|imdirect|[hbldh/imdirect](https://github.com/hbldh/imdirect)
|pillow|[python-pillow/Pillow](https://github.com/python-pillow/Pillow)
|pyqrcode|[mnooner256/pyqrcode](https://github.com/mnooner256/pyqrcode)
|pystray|[moses-palmer/pystray](https://github.com/moses-palmer/pystray)
|pywin32|[mhammond/pywin32](https://github.com/mhammond/pywin32)

### Todos

 - Bugfixes
 - Design modifications

License
----

MIT
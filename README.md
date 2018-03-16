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

So naturally, I also published ImageShare under the MIT License at my [public repository](https://github.com/lagmoellertim/ImageShare-DesktopApp)
 on GitHub.

### Installation

The ImageShare Mobile App requires [Python](https://www.python.org/) and multiple dependencies to run.

Install the dependencies and devDependencies and start the app.


### Dependencies

ImageShare is using numerous open-source Python dependencies, which are listed below.

| Dependencies | GitHub Repository |
| ------ | ------ |
|cefpython3|[cztomczak/cefpython](https://github.com/cztomczak/cefpython)
|flask|[pallets/flask](https://github.com/pallets/flask)
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

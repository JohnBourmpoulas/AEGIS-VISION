# A.E.G.I.S.

### Advanced Environmental & General Intelligence Scanner

**A.E.G.I.S.** is a real-time, open-vocabulary computer-vision
application with a futuristic HUD interface. It combines live camera
input, object detection, configurable confidence filtering, and a
desktop GUI into a single Python application inspired by sci-fi visual
interfaces.

> Detect. Identify. Analyze.

------------------------------------------------------------------------

## Overview

A.E.G.I.S. processes a live video feed and identifies objects in real
time. Detected objects are highlighted using a custom cyan HUD with
corner brackets, readable labels, and confidence scores.

The project is built as a desktop application rather than a simple
OpenCV demo, with camera selection, network-stream support, snapshots,
live performance information, and a dedicated detection panel.

## Features

-   Real-time object detection
-   Open-vocabulary detection with YOLO-World
-   Custom futuristic HUD overlay
-   Object labels and confidence scores
-   Adjustable confidence threshold
-   Automatic discovery of available local camera inputs
-   Camera rescan support
-   RTSP / HTTP network camera input
-   Live FPS and detection counter
-   Detection list with confidence values
-   Snapshot capture
-   macOS launcher
-   Windows launcher
-   Cross-platform Python code
-   Dark desktop interface built with PySide6

## Tech Stack

-   **Python**
-   **OpenCV**
-   **Ultralytics YOLO-World**
-   **PySide6 / Qt**
-   **NumPy**

## Screenshot

Add a screenshot of A.E.G.I.S. to the repository, for example:

``` text
assets/aegis-demo.png
```

Then replace this section with:

``` markdown
![A.E.G.I.S. in action](assets/aegis-demo.png)
```

## Installation

### Requirements

-   Python 3.10+ recommended
-   A webcam, USB camera, Continuity Camera, or compatible network video
    stream
-   Internet access on the first run if the YOLO model weights need to
    be downloaded

Clone the repository:

``` bash
git clone <YOUR-REPOSITORY-URL>
cd AEGIS-VISION
```

### macOS

The easiest method is the included launcher:

``` bash
chmod +x start_mac.command
./start_mac.command
```

Alternatively, create the virtual environment manually:

``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

On first use, macOS may request camera permission. Allow camera access
for the terminal or application used to launch A.E.G.I.S.

### Windows

Use the included launcher:

``` bat
start_windows.bat
```

Or run manually:

``` bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

## Camera Sources

A.E.G.I.S. scans for camera devices exposed by the operating system and
lists available local inputs in the interface.

Supported sources can include:

-   Built-in webcams
-   USB cameras
-   Cameras exposed to the OS as standard video devices
-   Compatible Continuity Camera devices on macOS
-   RTSP / HTTP network streams added manually

Network-camera availability depends on the camera and the stream
protocol it provides. Not every Wi-Fi or Bluetooth camera is
automatically exposed as a standard video source.

## Object Detection

A.E.G.I.S. uses **Ultralytics YOLO-World** for open-vocabulary object
detection. This allows the application to work with a configurable set
of object concepts beyond a fixed traditional detection-class list.

Each detection can display:

``` text
PERSON  92.4%
MOBILE PHONE  87.1%
BOTTLE  84.7%
GLASSES  76.3%
```

The confidence threshold controls the minimum confidence required before
a detection is displayed. Raising the threshold filters uncertain
detections; it does not make the underlying model more accurate.

## Project Structure

``` text
AEGIS-VISION/
├── aegis/
│   ├── __init__.py
│   └── app.py
├── run.py
├── requirements.txt
├── start_mac.command
├── start_windows.bat
├── .gitignore
├── LICENSE
└── README.md
```

Model weight files (`*.pt`) and local virtual environments should not be
committed to the repository.

## Known Limitations

Computer-vision predictions are probabilistic. Depending on lighting,
viewing angle, object size, occlusion, and similarity between objects,
the model may occasionally misclassify an object or fail to detect it.

The confidence value represents the model's confidence in a prediction;
it is not a guarantee that the classification is correct.

Camera discovery is also dependent on the operating system and device
drivers. Network cameras may require a direct RTSP or HTTP stream URL.

## Roadmap

Future improvements may include:

-   Persistent object tracking and stable object IDs
-   Temporal detection smoothing
-   Improved class consistency across video frames
-   Expanded configurable detection vocabulary
-   Recording support
-   Detection history and event logging
-   Additional HUD visualization modes
-   Performance optimization for Apple Silicon and GPU acceleration

## Privacy

A.E.G.I.S. performs computer-vision processing on the video sources
provided to the application. Users are responsible for ensuring that
camera use complies with applicable privacy rules, permissions, and
laws.

## License

This project is released under the **MIT License**. See the `LICENSE`
file for details.

## Acknowledgements

A.E.G.I.S. is built using the Python computer-vision ecosystem,
including OpenCV, Qt/PySide6, and Ultralytics YOLO-World.

------------------------------------------------------------------------

```{=html}
<p align="center">
```
`<strong>`{=html}A.E.G.I.S.`</strong>`{=html}`<br>`{=html} Advanced
Environmental & General Intelligence Scanner
```{=html}
</p>
```

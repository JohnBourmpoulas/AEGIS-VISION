```{=html}
<h1 align="center">
```
A.E.G.I.S.
```{=html}
</h1>
```
```{=html}
<p align="center">
```
`<strong>`{=html}Advanced Environmental & General Intelligence
Scanner`</strong>`{=html}
```{=html}
</p>
```
```{=html}
<p align="center">
```
Real-time open-vocabulary object detection with a futuristic
computer-vision HUD.
```{=html}
</p>
```
```{=html}
<p align="center">
```
`<img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue">`{=html}
`<img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green">`{=html}
`<img alt="YOLO-World" src="https://img.shields.io/badge/YOLO--World-Open%20Vocabulary-00cfd5">`{=html}
`<img alt="PySide6" src="https://img.shields.io/badge/PySide6-Qt-41CD52">`{=html}
`<img alt="License" src="https://img.shields.io/badge/License-MIT-yellow">`{=html}
```{=html}
</p>
```

------------------------------------------------------------------------

## About

**A.E.G.I.S.** is a Python desktop computer-vision application designed
for real-time object detection through live camera feeds.

It combines **OpenCV**, **Ultralytics YOLO-World**, and **PySide6** with
a custom futuristic HUD. Instead of displaying raw model output,
A.E.G.I.S. presents detections through a clean cyan interface with
corner brackets, object labels, confidence scores, system information,
and camera controls.

The project is designed as a practical desktop application rather than a
minimal object-detection demo.

## A.E.G.I.S. Interface

```{=html}
<p align="center">
```
`<img src="assets/aegis-demo.png" alt="A.E.G.I.S. application interface" width="100%">`{=html}
```{=html}
</p>
```
## Features

-   Real-time object detection
-   Open-vocabulary detection using YOLO-World
-   Custom futuristic HUD visualization
-   Large, readable object labels and confidence scores
-   Adjustable confidence threshold
-   Automatic scanning for available local camera inputs
-   Camera rescan functionality
-   RTSP / HTTP network-stream support
-   Live FPS counter
-   Live object counter
-   Detection list with confidence values
-   Snapshot capture
-   macOS launcher
-   Windows launcher
-   Cross-platform Python architecture

## Technology

A.E.G.I.S. is built with:

-   **Python** --- application logic
-   **OpenCV** --- video capture and image processing
-   **Ultralytics YOLO-World** --- open-vocabulary object detection
-   **PySide6 / Qt** --- desktop graphical interface
-   **NumPy** --- frame and numerical processing

## Installation

### Requirements

-   Python **3.10+** recommended
-   Webcam, USB camera, compatible Continuity Camera, or network video
    stream
-   Internet connection on the first run if model weights need to be
    downloaded

### Clone the repository

``` bash
git clone https://github.com/JohnBourmpoulas/AEGIS-VISION.git
cd AEGIS-VISION
```

> If your GitHub username or repository URL is different, replace the
> clone URL above with the URL shown on your repository's **Code**
> button.

### macOS

The included launcher can create the virtual environment, install
dependencies, and start A.E.G.I.S.:

``` bash
chmod +x start_mac.command
./start_mac.command
```

Manual installation:

``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run.py
```

On first use, macOS may ask for camera permission. Allow access for the
terminal or application used to launch A.E.G.I.S.

For later launches:

``` bash
source .venv/bin/activate
python run.py
```

### Windows

Run:

``` bat
start_windows.bat
```

Or install manually:

``` bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run.py
```

## Camera Sources

A.E.G.I.S. scans for camera inputs that are exposed by the operating
system.

Depending on the computer and operating system, these can include:

-   Built-in webcams
-   USB cameras
-   External cameras exposed as standard video devices
-   Compatible Continuity Camera devices on macOS
-   RTSP / HTTP network streams added manually

Use the camera selector inside the application to switch between
discovered sources. The **Rescan** function can be used after connecting
or disconnecting a camera.

Not every Wi-Fi or Bluetooth camera automatically appears as a standard
video device. Network-camera support depends on the protocols and stream
URLs provided by the camera.

## Object Detection

A.E.G.I.S. uses **YOLO-World** to provide open-vocabulary object
detection.

Example detections:

``` text
PERSON        92.4%
MOBILE PHONE  87.1%
BOTTLE        84.7%
GLASSES       76.3%
```

The **Confidence Threshold** determines the minimum confidence required
for a detection to be displayed.

A higher threshold filters out lower-confidence predictions. It does
**not** increase the underlying model's accuracy or guarantee that a
detected class is correct.

## Model Weights

Pretrained model weights such as:

``` text
*.pt
```

should not be committed to the repository.

A.E.G.I.S. can obtain the required model through the Ultralytics
workflow when necessary. Keeping model weights outside Git keeps the
repository smaller and easier to maintain.

## Project Structure

``` text
AEGIS-VISION/
├── aegis/
│   ├── __init__.py
│   └── app.py
├── assets/
│   └── aegis-demo.png
├── run.py
├── requirements.txt
├── start_mac.command
├── start_windows.bat
├── .gitignore
├── LICENSE
└── README.md
```

## Known Limitations

Object-detection results are probabilistic. Accuracy can be affected by
lighting, camera quality, viewing angle, object size, occlusion, motion
blur, and visual similarity between objects.

The model can occasionally:

-   Misclassify an object
-   Miss an object
-   Produce different classifications across consecutive frames
-   Assign high confidence to an incorrect prediction

Confidence scores represent the model's confidence in its prediction;
they are not guarantees of correctness.

Camera discovery also depends on the operating system, drivers, and the
way a device exposes its video stream.

## Roadmap

Potential future improvements include:

-   Persistent object tracking
-   Stable object IDs
-   Temporal detection smoothing
-   Improved class consistency between frames
-   Configurable detection vocabulary
-   Video recording
-   Detection history and event logging
-   Additional HUD visualization modes
-   Apple Silicon / GPU performance optimization
-   More advanced network-camera discovery

## Privacy

A.E.G.I.S. processes video from camera sources supplied to the
application.

Users are responsible for ensuring that their use of cameras,
recordings, network streams, and computer-vision processing complies
with applicable privacy rules, permissions, and laws.

## License

A.E.G.I.S. is released under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

## Acknowledgements

A.E.G.I.S. is built on the Python computer-vision ecosystem and makes
use of **OpenCV**, **Qt / PySide6**, and **Ultralytics YOLO-World**.

------------------------------------------------------------------------

```{=html}
<p align="center">
```
`<strong>`{=html}A.E.G.I.S.`</strong>`{=html}`<br>`{=html} Advanced
Environmental & General Intelligence Scanner
```{=html}
</p>
```
```{=html}
<p align="center">
```
Detect • Identify • Analyze
```{=html}
</p>
```

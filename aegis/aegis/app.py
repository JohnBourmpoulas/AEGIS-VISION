import sys, time, platform
from pathlib import Path
import cv2
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QFrame, QListWidget, QComboBox,
                               QSlider, QMessageBox, QInputDialog)

try:
    from ultralytics import YOLOWorld
except Exception:
    YOLOWorld = None

# Application and model configuration.
APP_NAME = 'A.E.G.I.S. VISION'
MODEL_NAME = 'YOLOv8s-World'
# Open-vocabulary prompts: broader than COCO, including headphones/earbuds and everyday desk objects.
TARGET_CLASSES = [
    'person','bottle','cup','glass','mug','laptop','computer monitor','keyboard','mouse',
    'mobile phone','tablet','headphones','earbuds','glasses','watch','keys','wallet','backpack',
    'book','pen','remote control','chair','couch','table','door','window','plant','dog','cat',
    'bicycle','motorcycle','car','bus','truck','bird'
]

class CameraScanner(QThread):
    """Probe local camera indices without blocking the Qt user interface."""
    finished_scan = Signal(list)
    def run(self):
        """Scan common camera indices and emit only sources that return a frame."""
        found=[]
        backend = cv2.CAP_AVFOUNDATION if platform.system() == 'Darwin' else cv2.CAP_ANY
        # Probe a practical range; only sources that actually open/read are shown.
        for idx in range(10):
            cap=cv2.VideoCapture(idx, backend)
            if cap.isOpened():
                ok, _ = cap.read()
                if ok:
                    found.append((f'Camera {idx}', idx))
            cap.release()
        self.finished_scan.emit(found)

class VideoLabel(QLabel):
    """Qt label used as the live video viewport."""
    def __init__(self):
        super().__init__('CAMERA OFFLINE')
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(800,520)
        self.setStyleSheet('background:#02070b;color:#43e7ff;border:1px solid #123848;')

class AegisWindow(QMainWindow):
    """Main A.E.G.I.S. window coordinating UI, cameras and YOLO-World inference."""
    def __init__(self):
        super().__init__(); self.setWindowTitle(APP_NAME); self.resize(1320,780)
        self.cap=None; self.model=None; self.running=False; self.last_t=time.time(); self.fps=0.; self.conf=.40
        self.camera_sources=[]; self.network_sources=[]
        self.setup_ui(); self.timer=QTimer(self); self.timer.timeout.connect(self.update_frame)
        QTimer.singleShot(250, self.scan_cameras)

    def setup_ui(self):
        """Build and style the futuristic desktop HUD."""
        # Main layout: live video on the left and telemetry/control panel on the right.
        root=QWidget(); self.setCentralWidget(root)
        outer=QVBoxLayout(root); outer.setContentsMargins(18,18,18,18); outer.setSpacing(12)
        title=QLabel('A.E.G.I.S.'); title.setObjectName('title'); title.setAlignment(Qt.AlignCenter)
        outer.addWidget(title)
        body=QHBoxLayout(); body.setSpacing(14); self.video=VideoLabel(); body.addWidget(self.video,4)
        side=QFrame(); side.setObjectName('panel'); side.setFixedWidth(360); sv=QVBoxLayout(side)
        self.status=QLabel('● SYSTEM STANDBY'); self.status.setObjectName('status'); sv.addWidget(self.status)
        self.metrics=QLabel(f'FPS       --\nOBJECTS   --\nMODEL     {MODEL_NAME}\nCAMERA    --'); self.metrics.setObjectName('metrics'); sv.addWidget(self.metrics)
        sv.addWidget(QLabel('DETECTIONS')); self.list=QListWidget(); self.list.setObjectName('detections'); sv.addWidget(self.list,1)
        sv.addWidget(QLabel('CONFIDENCE THRESHOLD'))
        slider=QSlider(Qt.Horizontal); slider.setRange(10,90); slider.setValue(40); slider.valueChanged.connect(lambda v:setattr(self,'conf',v/100)); sv.addWidget(slider)
        camrow=QHBoxLayout(); self.camera_box=QComboBox(); self.camera_box.addItem('Scanning cameras...', None); camrow.addWidget(self.camera_box,1)
        rescan=QPushButton('↻'); rescan.setToolTip('Rescan local cameras'); rescan.setFixedWidth(44); rescan.clicked.connect(self.scan_cameras); camrow.addWidget(rescan); sv.addLayout(camrow)
        net=QPushButton('+ ADD NETWORK CAMERA'); net.clicked.connect(self.add_network_camera); sv.addWidget(net)
        buttons=QHBoxLayout(); self.start_btn=QPushButton('INITIALIZE'); self.start_btn.clicked.connect(self.toggle_camera)
        snap=QPushButton('SNAPSHOT'); snap.clicked.connect(self.snapshot); buttons.addWidget(self.start_btn); buttons.addWidget(snap); sv.addLayout(buttons)
        body.addWidget(side,1); outer.addLayout(body,1)
        foot=QLabel('AI CORE // OPENCV // ULTRALYTICS YOLO-WORLD     |     LOCAL + RTSP/HTTP SOURCES'); foot.setObjectName('footer'); outer.addWidget(foot)
        self.setStyleSheet('''
        QWidget{background:#061017;color:#bcecf4;font-family:Consolas,monospace;font-size:13px} #title{color:#54ecff;font-size:30px;font-weight:700;letter-spacing:5px;padding:4px 0 8px 0}
        #subtitle,#footer{color:#4f8e9c;font-size:10px} #panel{background:#081821;border:1px solid #164252;border-radius:8px} #status{color:#54ecff;font-weight:700;padding:8px}
        #metrics{color:#84dcea;background:#041016;border:1px solid #123744;padding:12px} QListWidget{background:#041016;border:1px solid #123744;color:#74e8f7}
        QPushButton{background:#092532;border:1px solid #2bc8e0;color:#71efff;padding:9px;font-weight:700} QPushButton:hover{background:#0d3443}
        QComboBox{background:#07151d;border:1px solid #245364;padding:7px} QSlider::groove:horizontal{height:4px;background:#123744} QSlider::handle:horizontal{background:#54ecff;width:14px;margin:-5px 0;border-radius:7px}
        ''')

    def scan_cameras(self):
        """Start a background scan for local cameras exposed by the operating system."""
        if self.running: return
        self.status.setText('● SCANNING CAMERA BUS...'); self.camera_box.clear(); self.camera_box.addItem('Scanning...',None); self.camera_box.setEnabled(False)
        self.scanner=CameraScanner(); self.scanner.finished_scan.connect(self.on_scan_done); self.scanner.start()

    def on_scan_done(self, found):
        """Populate the source selector after the local camera scan completes."""
        self.camera_sources=found; self.camera_box.clear()
        for name,src in found: self.camera_box.addItem(f'● {name}',src)
        for name,url in self.network_sources: self.camera_box.addItem(f'◎ {name}',url)
        if self.camera_box.count()==0: self.camera_box.addItem('No camera detected',None)
        self.camera_box.setEnabled(True); self.status.setText(f'● {len(found)} LOCAL CAMERA(S) READY')

    def add_network_camera(self):
        """Validate and add a user-supplied RTSP/HTTP network video stream."""
        url,ok=QInputDialog.getText(self,'Add Network Camera','RTSP / HTTP / HTTPS stream URL:')
        if not ok or not url.strip(): return
        url=url.strip(); name,ok2=QInputDialog.getText(self,'Camera Name','Display name:',text=f'Network Camera {len(self.network_sources)+1}')
        if not ok2: name=f'Network Camera {len(self.network_sources)+1}'
        self.status.setText('● TESTING NETWORK STREAM...'); QApplication.processEvents()
        cap=cv2.VideoCapture(url); opened=cap.isOpened(); okframe,_=cap.read() if opened else (False,None); cap.release()
        if not (opened and okframe):
            QMessageBox.warning(self,'Network camera','Could not open this stream. Check the RTSP/HTTP URL, credentials and network access.'); self.status.setText('● STREAM TEST FAILED'); return
        self.network_sources.append((name or 'Network Camera',url)); self.camera_box.addItem(f'◎ {name or "Network Camera"}',url); self.camera_box.setCurrentIndex(self.camera_box.count()-1); self.status.setText('● NETWORK CAMERA READY')

    def load_model(self):
        """Lazy-load YOLO-World and configure the open-vocabulary target classes."""
        if YOLOWorld is None:
            QMessageBox.critical(self,'Missing dependency','Ultralytics is not installed. Run: pip install -r requirements.txt'); return False
        if self.model is None:
            self.status.setText('● LOADING OPEN-VOCAB AI CORE...'); QApplication.processEvents()
            try:
                # The model file is downloaded automatically by Ultralytics on first use.
                self.model=YOLOWorld('yolov8s-worldv2.pt'); self.model.set_classes(TARGET_CLASSES)
            except Exception as e:
                QMessageBox.critical(self,'Model error',f'Could not load YOLO-World:\n{e}'); self.status.setText('● AI CORE ERROR'); return False
        return True

    def toggle_camera(self):
        """Start the selected video source, or stop it when already running."""
        if self.running: self.stop_camera(); return
        src=self.camera_box.currentData()
        if src is None: QMessageBox.information(self,'Camera','No usable camera source is selected.'); return
        if not self.load_model(): return
        # AVFoundation is the native macOS capture backend for local camera devices.
        backend=cv2.CAP_AVFOUNDATION if isinstance(src,int) and platform.system()=='Darwin' else cv2.CAP_ANY
        self.cap=cv2.VideoCapture(src,backend) if isinstance(src,int) else cv2.VideoCapture(src)
        if not self.cap.isOpened(): QMessageBox.warning(self,'Camera error','Could not open selected camera source.'); return
        self.running=True; self.start_btn.setText('TERMINATE'); self.status.setText('● SYSTEM ONLINE'); self.timer.start(15)

    def stop_camera(self):
        """Stop frame updates and release the active video capture device."""
        self.timer.stop(); self.running=False
        if self.cap: self.cap.release(); self.cap=None
        self.video.clear(); self.video.setText('CAMERA OFFLINE'); self.start_btn.setText('INITIALIZE'); self.status.setText('● SYSTEM STANDBY')

    def draw_hud(self,frame,detections):
        """Render Stark-inspired corner brackets and readable floating labels."""
        h,w=frame.shape[:2]; cyan=(255,235,70); dim=(125,90,30)
        cv2.line(frame,(20,25),(180,25),cyan,2); cv2.line(frame,(20,25),(20,90),cyan,2); cv2.line(frame,(w-20,25),(w-180,25),cyan,2); cv2.line(frame,(w-20,25),(w-20,90),cyan,2)
        cv2.putText(frame,'AEGIS // LIVE OPEN-VOCAB ANALYSIS',(28,h-25),cv2.FONT_HERSHEY_SIMPLEX,.52,dim,1,cv2.LINE_AA)
        for x1,y1,x2,y2,name,conf in detections:
            bw=max(1,x2-x1); bh=max(1,y2-y1); L=max(24,min(58,min(bw,bh)//4)); t=4
            for a,b,c,d in [(x1,y1,x1+L,y1),(x1,y1,x1,y1+L),(x2,y1,x2-L,y1),(x2,y1,x2,y1+L),(x1,y2,x1+L,y2),(x1,y2,x1,y2-L),(x2,y2,x2-L,y2),(x2,y2,x2,y2-L)]: cv2.line(frame,(a,b),(c,d),cyan,t,cv2.LINE_AA)
            # Clean Stark-style floating label: large cyan text, no boxed background.
            # A subtle dark stroke keeps the text readable over bright camera areas.
            label=f'{name.upper()}  {conf*100:05.1f}%'; font=cv2.FONT_HERSHEY_SIMPLEX; fs=.82; ft=2
            (tw,th),base=cv2.getTextSize(label,font,fs,ft)
            tx=max(4,min(x1,w-tw-4))
            ty=y1-10 if y1-th-12>=0 else min(h-th-4,y1+th+14)
            cv2.putText(frame,label,(tx,ty),font,fs,(5,18,22),5,cv2.LINE_AA)
            cv2.putText(frame,label,(tx,ty),font,fs,cyan,ft,cv2.LINE_AA)
        return frame

    def update_frame(self):
        """Capture one frame, run inference, update metrics and refresh the viewport."""
        ok,frame=self.cap.read() if self.cap else (False,None)
        if not ok: self.status.setText('● VIDEO SIGNAL LOST'); return
        if isinstance(self.camera_box.currentData(),int): frame=cv2.flip(frame,1)
        detections=[]
        # Run object detection on the current frame using the user-selected confidence threshold.
        try:
            result=self.model.predict(frame,conf=self.conf,verbose=False,imgsz=640)[0]; names=result.names
            if result.boxes is not None:
                for b in result.boxes:
                    x1,y1,x2,y2=map(int,b.xyxy[0].tolist()); cls=int(b.cls[0]); cf=float(b.conf[0]); name=names[cls] if isinstance(names,(list,tuple)) else names.get(cls,str(cls)); detections.append((x1,y1,x2,y2,name,cf))
        except Exception as e: self.status.setText('● INFERENCE ERROR'); print(e)
        # Draw the custom HUD only after inference so the model sees the unmodified camera frame.
        frame=self.draw_hud(frame,detections); now=time.time(); dt=now-self.last_t; self.last_t=now
        if dt>0:self.fps=.88*self.fps+.12*(1/dt)
        self.list.clear()
        for *_,name,cf in sorted(detections,key=lambda d:d[-1],reverse=True)[:20]: self.list.addItem(f'◈ {name.upper():18} {cf*100:5.1f}%')
        cam=self.camera_box.currentText().lstrip('●◎ ').strip(); self.metrics.setText(f'FPS       {self.fps:05.1f}\nOBJECTS   {len(detections):02d}\nMODEL     {MODEL_NAME}\nCAMERA    {cam[:18]}')
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB); h,w,ch=rgb.shape; img=QImage(rgb.data,w,h,ch*w,QImage.Format_RGB888); self.video.setPixmap(QPixmap.fromImage(img).scaled(self.video.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)); self.current_frame=frame.copy()

    def snapshot(self):
        """Save the current annotated frame to the local snapshots directory."""
        if not hasattr(self,'current_frame'): QMessageBox.information(self,'Snapshot','Initialize the camera first.'); return
        folder=Path.cwd()/'snapshots'; folder.mkdir(exist_ok=True); path=folder/f'aegis_{time.strftime("%Y%m%d_%H%M%S")}.jpg'; cv2.imwrite(str(path),self.current_frame); self.status.setText(f'● SNAPSHOT SAVED // {path.name}')
    def closeEvent(self,event):
        """Release camera resources before the Qt window closes."""
        self.stop_camera(); event.accept()

def main():
    """Application entry point."""
    app=QApplication(sys.argv); app.setApplicationName(APP_NAME); win=AegisWindow(); win.show(); sys.exit(app.exec())

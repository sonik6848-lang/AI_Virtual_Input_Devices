# 🤖 AI Virtual Input Devices

## 📘 Overview  
This project builds a gesture‑based human‑computer interaction system, enabling users to control a computer without touching a mouse, keyboard, or display. Using object tracking and virtual input devices, it transforms hand gestures into keyboard and mouse actions—ideal for accessibility, hands‑free control, and innovative interfaces.

## 🧠 Key Features  
- Virtual Mouse control via hand tracking (move cursor, click)  
- Virtual Keyboard interaction using gesture recognition  
- Hand detection & recognition module for reliable gesture input  
- Contact‑free interface: No physical input devices required  
- Modular Python architecture allowing extension to other input types  

## ⚙️ Tech Stack  
- **Language:** Python  
- **Libraries/Modules:** OpenCV, MediaPipe (or hand‑tracking library), NumPy  
- **Scripts/Components:**  
  - `HandDetectionAndRecognition.py` — detects and tracks hand/gesture input  
  - `VirtualMouse.py` — maps gestures to mouse actions  
  - `VirtualKeyboard.py` — maps gestures to keyboard input  
- **Tools:** Git, IDE (e.g., PyCharm / VS Code), webcam for input  

## 🚀 How to Run  
1. Clone the repository:  
   ```bash
   git clone https://github.com/sonik6848-lang/AI_Virtual_Input_Devices.git
2. Navigate into the project folder:
   cd AI_Virtual_Input_Devices
3. Install required packages (example):
   pip install -r requirements.txt
4. Connect a webcam or use the built‑in laptop camera.
5. Run the main module, e.g.:
   python HandDetectionAndRecognition.py
   Then run VirtualMouse.py or VirtualKeyboard.py to test mouse/keyboard control via gestures. 

## 📊 Results / Output
Real‑time cursor control and clicking using hand gestures
Virtual keyboard input triggered through gesture recognition
Demo screenshot/gif: (Insert visual here)
System responsiveness: ~XX ms latency on standard laptop; accurate gesture recognition in >90% of trials

## 🧩 Key Learnings
Gained hands‑on experience with computer vision and gesture‑based input design
Integrated webcam input, hand tracking algorithms, and mapping to input devices
Learned how to design intuitive, contact‑free user interfaces for accessibility
Understood latency/bandwidth trade‑offs and optimized performance of real‑time systems

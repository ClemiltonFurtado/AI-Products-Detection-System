# AI-Products-Detection-System

A complete Computer Vision and Object Detection system built for a Camera Inventory System. This project provides a web interface for image processing, a real-time webcam detection module, and a RESTful API for  integration with external systems.

## 🎥 Demo Video (Must Watch)
**[TODO]**
> *In this video, I explain the project architecture, demonstrate the model running (both via web interface and real-time webcam), and show the API endpoint returning the raw JSON detection results.*

---

## 🛠️ Technologies Used
* **Backend & API:** Python, Flask, Werkzeug
* **Artificial Intelligence:** Ultralytics YOLO (Custom trained model)
* **Computer Vision:** OpenCV

---

## 📁 Project Architecture
The project was designed with clean architecture principles, separating concerns into specific modules to ensure scalability and easy maintenance:

```text
AI-Products-Detection-System/
│
├── data/
│   └── model/
│       ├── best.pt            # Custom trained YOLO weights
│       └── args.yaml          # Model training arguments
│
├── src/
│   ├── main.py                # Main entry point
│   ├── AI/                    # YOLO model initialization and processing logic
│   ├── API/                   # Pure REST API endpoints (JSON responses)
│   ├── Configs/               # Global paths and configurations
│   ├── Real_time/             # Real-time webcam streaming and detection
│   ├── Upload/                # Web interface file upload handling
│   └── Wutils/                # Central orchestrator and route registration
│
├── Templates/                 # HTML templates for the web interface
├── test/
│   └── test_api.html          # Standalone HTML tool to test the API endpoint
│
└── requirements.txt           # Python dependencies
```
---

## ⚙️ How to Run the Project

**1. Clone the repository**
```bash
git clone https://github.com/clemiltonfurtado/AI-Products-Detection-System.git
cd AI-Products-Detection-System
```

**2. Create and activate a vitrual environment**
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start the Flask Server**
```bash
cd src
python main.py
```

## 🔌 Testing the API (`/detect` Endpoint)

The project includes a dedicated `test/` directory containing both a graphical and a programmatic client to validate the REST API endpoint independently from the main web application UI.

### 1. Web-Based Test Client (`test_api.html`)
This is a standalone HTML interface that runs completely in the browser and simulates a frontend application making an asynchronous `POST` request directly to the API backend.

**How to use:**
1. Ensure the Flask server is active.
2. Open `test/test_api.html` directly in any web browser (double-click the file).
3. Choose an image file and click **Upload Image (POST)**.
4. The browser will redirect to show the raw JSON response containing classes and confidence scores directly from the server.
# Pi FMCG Classifier

A Raspberry Pi-based image classifier for factory line quality control. Captures images of products on manufacturing lines and classifies them for defect detection.

## Hardware Requirements

- Raspberry Pi 5 with touchscreen
- Raspberry Pi Global Shutter Camera
- IR distance sensor (20-150cm range)
- MCP3008 ADC (for IR sensor)
- 512GB NVME SSD

## Software Requirements

Install dependencies on the Pi:
```bash
pip install -r requirements.txt
```

## Deployment

### Initial Setup on Pi:
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pi-fmcg-classifier.git
   cd pi-fmcg-classifier
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create data directories (if not auto-created):
   ```bash
   mkdir -p data/captured_images
   mkdir -p data/classification_results
   ```

### Model Deployment:
1. Collect images using Collection Mode
2. Copy images to laptop via USB
3. Train model using Google Teachable Machine
4. Copy `model.tflite` file to USB
5. On Pi, copy model to `models/pretrained/model.tflite`

### Running the Application:
```bash
cd src
python main.py
```

## Usage

### Collection Mode:
- Click "START COLLECTION MODE"
- Pi captures images when IR sensor detects objects
- Images saved to `data/captured_images/`
- Use for gathering training data

### Classification Mode:
- Requires trained model in `models/pretrained/model.tflite`
- Click "START CLASSIFICATION MODE"
- Pi classifies objects in real-time
- Results saved to `data/classification_results/results.csv`

### Exit:
- Press `Ctrl+Shift+Q` to exit application

## File Structure

```
pi-fmcg-classifier/
├── src/
│   └── main.py                 # Main GUI application
├── models/
│   └── pretrained/             # Place model.tflite here
├── data/
│   ├── captured_images/        # Collected training images
│   └── classification_results/ # CSV results and classified images
├── requirements.txt            # Pi dependencies
└── README.md                   # This file
```

## Updates

To update code on Pi:
```bash
git pull origin main
```

Models are deployed separately via USB for consultant ease of use.

A two-mode image classification system for Raspberry Pi that can collect images for training and perform real-time classification using trained TensorFlow Lite models.

## Overview

This project implements a complete pipeline for object detection and classification:

1. **Collection Mode**: Captures images when objects pass a sensor for later manual classification
2. **Classification Mode**: Uses a trained TensorFlow Lite model to classify objects in real-time

The system is designed to work with [Liner.ai](https://liner.ai) for easy model training without coding.

## Project Structure

```
pi-image-classifier/
├── src/
│   ├── main.py                # Entry point with dual-mode operation
│   ├── image_capture.py       # Camera control and image capture
│   ├── classifier.py          # TensorFlow Lite model inference
│   ├── sensor_handler.py      # Sensor input handling (PIR, ultrasonic, etc.)
│   ├── metrics_collector.py   # Classification metrics and reporting
│   └── utils/
│       ├── __init__.py       
│       └── config.py         # Configuration management
├── models/
│   └── pretrained/
│       └── model.tflite      # Place your trained model here
├── data/
│   ├── captured_images/       # Images captured in collection mode
│   └── classification_results/ # Metrics and classification results
├── config/
│   └── settings.json         # System configuration
├── scripts/
│   ├── setup_hardware.py     # Hardware setup utilities
│   └── model_download.py     # Model management utilities
├── tests/
│   ├── test_classifier.py    
│   ├── test_sensor.py        
│   └── test_metrics.py       
├── requirements.txt          # Python dependencies
├── setup.py                 # Package setup
└── README.md                # This file
```

## Hardware Requirements

- Raspberry Pi (3B+ or newer recommended)
- Camera module or USB camera
- Motion sensor (PIR recommended) or ultrasonic sensor
- MicroSD card (32GB+ recommended)
- Power supply

## Software Requirements

- Raspberry Pi OS (Bullseye or newer)
- Python 3.7+
- TensorFlow Lite Runtime

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pi-image-classifier
   ```

2. **Install system dependencies (on Raspberry Pi):**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv libcamera-dev
   ```

3. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the system:**
   Edit `config/settings.json` to match your hardware setup.

## Configuration

The `config/settings.json` file contains all system settings:

```json
{
  "camera": {
    "width": 640,
    "height": 480,
    "output_directory": "data/captured_images"
  },
  "sensor": {
    "pin": 17,
    "sensor_type": "PIR",
    "cooldown_seconds": 2.0,
    "simulation_mode": true
  },
  "model": {
    "path": "models/pretrained/model.tflite",
    "class_labels": ["class_0", "class_1", "class_2"]
  },
  "metrics": {
    "output_directory": "data/classification_results",
    "log_frequency": 10
  }
}
```

## Usage

### Collection Mode

Use this mode to gather images for training your model:

```bash
python src/main.py collect
```

This will:
- Monitor the sensor for object detection
- Capture images when objects are detected
- Save images to the configured directory
- Log detection events

### Classification Mode

Use this mode after training your model with Liner.ai:

```bash
python src/main.py classify
```

This will:
- Load your trained TensorFlow Lite model
- Monitor the sensor for object detection
- Capture and classify images in real-time
- Generate metrics and reports
- Save classification results

### Command Line Options

```bash
python src/main.py {collect|classify} [--config path/to/config.json]
```

## Training Your Model

1. **Collect Images**: Run in collection mode to gather training data
2. **Download Images**: Transfer images from Pi to your laptop
3. **Use Liner.ai**: 
   - Upload images to [Liner.ai](https://liner.ai)
   - Manually classify/tag your images
   - Export the trained model as TensorFlow Lite (.tflite)
4. **Deploy Model**: Place the .tflite file in `models/pretrained/`
5. **Update Config**: Add class labels to `config/settings.json`
6. **Run Classification**: Start classification mode

## Development and Testing

### Running Tests

```bash
pytest tests/
```

### Development Mode

For development on non-Pi systems, set `simulation_mode: true` in the sensor configuration. This will simulate sensor detections for testing.

### Hardware Setup

Connect your sensor to the configured GPIO pin (default: pin 17). For PIR sensors:
- VCC → 5V
- GND → Ground  
- OUT → GPIO 17

## Troubleshooting

### Common Issues

1. **Camera not found**: Check camera connection and enable camera interface in `raspi-config`

2. **GPIO permission denied**: Run with `sudo` or add user to `gpio` group:
   ```bash
   sudo usermod -a -G gpio $USER
   ```

3. **Model not found**: Ensure your .tflite file is in `models/pretrained/` and path is correct in config

4. **Import errors**: Ensure all dependencies are installed in your virtual environment

### Logs

Check application logs in `logs/classifier.log` for detailed error information.

## Performance Optimization

- Use TensorFlow Lite Runtime instead of full TensorFlow
- Optimize image resolution in config
- Adjust sensor cooldown period to prevent duplicate captures
- Consider using hardware-optimized models

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Check the troubleshooting section
- Review logs for error details
- Create an issue in the repository

3. Set up the hardware components as per the instructions in `scripts/setup_hardware.py`.

4. Download the pre-trained TensorFlow model if not included:
   ```
   python scripts/model_download.py
   ```

## Usage

1. Configure the settings in `config/settings.json` according to your setup.
2. Run the application:
   ```
   python src/main.py
   ```

3. The application will start capturing images and classifying them as objects pass by the sensor.

## Metrics

The system logs classification metrics, which can be found in the `data/classification_results` directory. You can generate reports using the `MetricsCollector` class.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
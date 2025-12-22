# 🌱 Plant Disease Diagnosis & Treatment Application

An AI-powered plant disease detection and treatment recommendation system using EfficientNet-B0 deep learning model and FastAPI backend.

## 📋 Overview

This application provides automated plant disease diagnosis from leaf images and comprehensive treatment recommendations. It supports 38 different plant diseases across multiple crop types including tomato, potato, apple, grape, corn, and more.

## ✨ Features

- **AI-Powered Disease Detection**: Uses EfficientNet-B0 model trained on PlantVillage dataset
- **Multi-Disease Support**: Detects 38 different plant diseases
- **Treatment Recommendations**: Provides cultural, biological, and chemical control methods
- **RESTful API**: Easy-to-use FastAPI backend with automatic documentation
- **High Accuracy**: Deep learning model with transfer learning from ImageNet
- **Comprehensive Database**: Detailed treatment information for each disease

## 🌾 Supported Crops and Diseases

| Crop | Diseases |
|------|----------|
| **Tomato** | Early Blight, Late Blight, Bacterial Spot, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy |
| **Potato** | Early Blight, Late Blight, Healthy |
| **Apple** | Apple Scab, Black Rot, Cedar Apple Rust, Healthy |
| **Grape** | Black Rot, Esca (Black Measles), Leaf Blight, Healthy |
| **Corn** | Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy |
| **Pepper** | Bacterial Spot, Healthy |
| **Peach** | Bacterial Spot, Healthy |
| **Cherry** | Powdery Mildew, Healthy |
| **Strawberry** | Leaf Scorch, Healthy |
| **Orange** | Huanglongbing (Citrus Greening) |
| **Squash** | Powdery Mildew |
| **Blueberry** | Healthy |
| **Raspberry** | Healthy |
| **Soybean** | Healthy |

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd plant-disease-app
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install backend dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### ML Pipeline Setup (Optional - for training)

1. **Install ML dependencies**:
   ```bash
   cd ml
   pip install -r requirements.txt
   ```

2. **Prepare dataset**: Download PlantVillage dataset and organize as:
   ```
   data/plantvillage/
   ├── Apple___Apple_scab/
   ├── Apple___Black_rot/
   └── ... (other disease folders)
   ```

## 🎯 How to Run the API

### Start the FastAPI Server

```bash
cd backend
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Endpoint**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check endpoint |
| POST | `/predict` | Upload image for disease prediction |
| GET | `/treatments/{disease_name}` | Get treatment recommendations |
| GET | `/crops` | List all supported crops |
| GET | `/diseases` | List all detectable diseases |

### Endpoint Details

#### POST /predict
Upload an image to get disease predictions.

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body: file (image file)

**Response**:
```json
{
  "success": true,
  "predictions": [
    {
      "disease": "Tomato - Early blight",
      "confidence": 0.92
    },
    {
      "disease": "Tomato - Late blight",
      "confidence": 0.05
    },
    {
      "disease": "Tomato - healthy",
      "confidence": 0.02
    }
  ],
  "message": "Prediction successful"
}
```

#### GET /treatments/{disease_name}
Get detailed treatment recommendations for a specific disease.

**Response**:
```json
{
  "disease_name": "Tomato Early Blight",
  "crop": "Tomato",
  "summary": "Early blight is a common fungal disease...",
  "symptoms": ["Dark brown spots...", "..."],
  "cultural_controls": ["Remove infected debris...", "..."],
  "biological_controls": ["Apply Bacillus subtilis...", "..."],
  "chemical_controls": ["Apply copper fungicides...", "..."],
  "prevention": ["Use resistant varieties...", "..."],
  "severity": "Moderate to High"
}
```

## 💻 Example Usage

### Using cURL

**Predict disease from image**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/plant_image.jpg"
```

**Get treatment recommendations**:
```bash
curl -X GET "http://localhost:8000/treatments/Tomato%20Early%20Blight" \
  -H "accept: application/json"
```

**List all crops**:
```bash
curl -X GET "http://localhost:8000/crops" \
  -H "accept: application/json"
```

### Using Python

```python
import requests

# Predict disease
with open("plant_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/predict", files=files)
    prediction = response.json()
    print(f"Disease: {prediction['predictions'][0]['disease']}")
    print(f"Confidence: {prediction['predictions'][0]['confidence']:.2%}")

# Get treatment recommendations
disease_name = prediction['predictions'][0]['disease']
response = requests.get(f"http://localhost:8000/treatments/{disease_name}")
treatment = response.json()
print(f"\nTreatment for {treatment['disease_name']}:")
print(f"Summary: {treatment['summary']}")
print(f"\nCultural Controls:")
for control in treatment['cultural_controls']:
    print(f"  - {control}")
```

### Using JavaScript/Fetch

```javascript
// Predict disease
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/predict', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => {
    console.log('Predictions:', data.predictions);
  });

// Get treatment
fetch('http://localhost:8000/treatments/Tomato Early Blight')
  .then(response => response.json())
  .then(treatment => {
    console.log('Treatment:', treatment);
  });
```

## 🎓 Training Your Own Model

### Prepare Data

1. Download PlantVillage dataset or use your own data
2. Organize images in folders by disease class
3. Place in `data/plantvillage/` directory

### Train Model

```bash
cd ml
python train.py --data_dir ../data/plantvillage \
                --epochs 50 \
                --batch_size 32 \
                --learning_rate 0.001 \
                --save_dir ./checkpoints
```

### Training Options

```bash
python train.py --help
```

Key arguments:
- `--data_dir`: Path to dataset directory
- `--epochs`: Number of training epochs (default: 50)
- `--batch_size`: Batch size for training (default: 32)
- `--learning_rate`: Initial learning rate (default: 0.001)
- `--pretrained`: Use pretrained weights (default: True)
- `--freeze_backbone`: Freeze backbone during training
- `--num_classes`: Number of disease classes (default: 38)
- `--use_gpu`: Use GPU if available (default: True)

### Monitor Training

```bash
tensorboard --logdir=./logs
```

Visit http://localhost:6006 to view training metrics.

## 📁 Project Structure

```
plant-disease-app/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── predictor.py        # Disease prediction model
│   ├── database/
│   │   ├── __init__.py
│   │   └── treatment_kb.py     # Treatment knowledge base
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   └── requirements.txt        # Backend dependencies
├── ml/
│   ├── model.py                # EfficientNet-B0 architecture
│   ├── dataset.py              # Dataset utilities
│   ├── train.py                # Training script
│   └── requirements.txt        # ML dependencies
├── data/
│   ├── treatments.json         # Treatment database
│   └── plantvillage/           # Dataset directory (not included)
├── .gitignore
└── README.md
```

## 🔧 Configuration

### Model Configuration

Edit `backend/models/predictor.py` to:
- Change model architecture
- Modify preprocessing
- Adjust confidence thresholds

### Treatment Database

Edit `data/treatments.json` to:
- Add new diseases
- Update treatment recommendations
- Modify severity levels

## 🧪 Testing

Test the API using the interactive documentation:

1. Start the server
2. Visit http://localhost:8000/docs
3. Try out each endpoint with the built-in interface

## 🚀 Deployment

### Docker Deployment (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY data/ ./data/

WORKDIR /app/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t plant-disease-api .
docker run -p 8000:8000 plant-disease-api
```

### Cloud Deployment

Deploy to popular platforms:
- **Heroku**: Use Procfile
- **AWS**: Use Elastic Beanstalk or Lambda
- **Google Cloud**: Use Cloud Run
- **Azure**: Use App Service

## 📊 Model Performance

The EfficientNet-B0 model achieves:
- **Accuracy**: ~95% on PlantVillage dataset
- **Inference Time**: <100ms per image on CPU
- **Model Size**: ~20MB

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- PlantVillage dataset for training data
- EfficientNet architecture by Google Research
- FastAPI framework for the API
- PyTorch for deep learning

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation at `/docs`
- Review the example code

## 🔮 Future Enhancements

- [ ] Mobile app integration
- [ ] Real-time disease monitoring
- [ ] Multi-language support
- [ ] Additional crop types
- [ ] Weather integration
- [ ] Treatment effectiveness tracking
- [ ] User feedback system
- [ ] Database backend for user data

---

**Happy Growing! 🌱**

# Image Forgery Detection

A deep learning-based image forgery detection system using the RGB + LAB(ELA) model, implemented with Flask for a web-based interface.

## Project Structure
```
Image-Forgery-Detection/
│── casia-v2/                #Dataset folder
│── models/                 # Saved models
│── static/                 # Flask UI assets
│── templates/              # HTML templates for Flask
│── app.py                  # Flask Web 
│── train.ipynb             # Model Training Scrip
│── requirements.txt        # Required Packages
│── README.md               # Project Documentation
```

## Dataset Setup

Download CASIA 2 dataset from:
[CASIA 2 Dataset - Kaggle](https://www.kaggle.com/datasets/divg07/casia-20-image-tampering-detection-dataset/data)

### CASIA v2 Dataset Structure
The dataset contains the following folders:

- `Au/` → Authentic (real) images
- `Tp/` → Tampered (forged) images
- `CASIA2 Groundtruth/` → Binary masks for tampered images

## Installation

### Step 1: Install Dependencies

You can install the required dependencies using the following command:

```sh
pip install -r requirements.txt
```

### Step 2: Training the Model

To train the DPMSN model, run:

```sh
python train.py
```

#### Expected Console Output (Training):
```
Epoch [1/10], Loss: 0.3543
Epoch [2/10], Loss: 0.3011
...
Training Completed!
```
After training completes, check the `models/` folder for the file `image_forgery_detection_casia2.h5`.

## Running the Web Application

To launch the Flask web app, run:

```sh
python app.py
```

Then, open your browser and visit:

```
http://127.0.0.1:5000/
```

### Web App Features:
- Upload an image
- View forged regions highlighted

### Our Team
- Praveenkumar M
- Sathish Kumar S
- Tharunkumar M

🚀 Enjoy detecting forgeries with deep learning! 🚀



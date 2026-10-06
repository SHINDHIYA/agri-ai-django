# AI-Enhanced Predictive Models for Crop Yield and Crop Recommendation

A Django-based AI application developed to support agriculture through **crop recommendation and crop yield prediction** using machine learning models and agricultural data. The application also provides an AI chatbot and user account management features.

## Features

* 🌱 **Crop Recommendation** – Recommends suitable crops based on the provided agricultural and environmental data.
* 📈 **Crop Yield Prediction** – Predicts crop yield using machine learning models.
* 🤖 **AI Chatbot** – Provides users with agricultural information through a chatbot.
* 👤 **User Registration & Login** – Allows users to create accounts and securely log in.
* 🧑‍🌾 **User Profile Management** – Allows users to manage their profile information.
* 🔐 **Authentication** – Includes login, logout and password management functionality.
* 🛠️ **Django Admin Panel** – Provides administrative management of application data.

## Machine Learning

The project uses supervised machine learning techniques for crop recommendation and crop yield prediction.

### Crop Recommendation

* **Bagging Classifier**
* **Multi-Layer Perceptron (MLP)**

These classification models are used to recommend suitable crops based on agricultural and environmental input data.

### Crop Yield Prediction

* **Linear Regression**
* **Random Forest Regression**

These regression models are used to predict crop yield based on the available agricultural and historical data.

### Evaluation Metrics

The regression models are evaluated using:

* **Mean Squared Error (MSE)**
* **Mean Absolute Error (MAE)**
* **R² Score**

### Machine Learning Libraries

* Scikit-learn
* TensorFlow / Keras
* Pandas
* NumPy
* Joblib

## Technology Stack

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Backend

* Python
* Django

### Database

* SQLite
* Django ORM

### Other Technologies

* NLTK
* Git
* GitHub

## Project Structure

```text
agri-ai-django/
│
├── Chatbot/
│   ├── processor.py
│   ├── views.py
│   ├── chatbot_model.h5
│   ├── intents.json
│   ├── classes.pkl
│   └── words.pkl
│
├── users/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── crop1.pkl
│
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/SHINDHIYA/agri-ai-django.git
cd agri-ai-django
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

### 6. Start the Django development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Important Note

The trained **crop yield prediction model (`YIELD.pkl`)** is a large file and is not included in this GitHub repository.

The model needs to be provided separately to run the complete yield prediction functionality.

## Project Objective

The objective of this project is to apply **Artificial Intelligence and Machine Learning techniques to agriculture** by providing data-driven crop recommendations and crop yield predictions through a Django-based web application.

# TrendLens MLOps Pipeline

## Overview
This repository contains the TrendLens MLOps pipeline that includes web scraping, sentiment analysis, prediction, a FastAPI application, Docker configuration, DVC setup, and CI/CD workflows.

## Contents
- **pipeline/scrape.py**: Script for scraping data from the web.
- **pipeline/sentiment.py**: Script for performing sentiment analysis.
- **pipeline/predict.py**: Script for making predictions based on the scraped data.
- **app/main.py**: Main FastAPI application.
- **dvc.yaml**: DVC configuration file.
- **docker/Dockerfile**: Docker file for containerization.
- **.github/workflows/ci.yml**: GitHub Actions workflow for CI/CD.
- **requirements.txt**: List of required Python packages.
- **environment.yml**: Conda environment file for reproducible environments.
- **tests/test_sentiment.py**: Unit tests for sentiment analysis.

## Instructions

### 1. **Setup Environment**

#### Using Conda (Recommended)
1. Clone the repository.
2. Create the environment and install dependencies:
   ```
   conda env create -f environment.yml
   conda activate mlops-env
   ```
3. If you add new dependencies to `environment.yml`, update your environment:
   ```
   conda env update -f environment.yml --prune
   ```

#### Using pip (Alternative)
1. Clone the repository.
2. (Optional but recommended) Create and activate a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

> **Note:** The conda environment will install all dependencies listed in `requirements.txt`. If you use pip, make sure your system has all required compilers and libraries for packages with native code.

### 2. **Run the Pipeline**
- Use DVC to manage data and models.
- Run the scraping script to collect data:
  ```
  python pipeline/scrape.py
  ```
- Analyze the sentiment:
  ```
  python pipeline/sentiment.py
  ```
- Make predictions:
  ```
  python pipeline/predict.py
  ```

### 3. **Deploy the FastAPI App**
- Build the Docker image:
  ```
  docker build -t trendlens-app .
  ```
- Run the container:
  ```
  docker run -p 8000:8000 trendlens-app
  ```

### 4. **Continuous Integration/Continuous Deployment**
- The CI/CD process is managed through GitHub Actions as defined in `.github/workflows/ci.yml`.

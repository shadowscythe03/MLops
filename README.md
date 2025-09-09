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
- **tests/test_sentiment.py**: Unit tests for sentiment analysis.

## Instructions
1. **Setup Environment**
   - Clone the repository.
   - Install dependencies using `pip install -r requirements.txt`.

2. **Run the Pipeline**
   - Use DVC to manage data and models.
   - Run the scraping script to collect data: `python pipeline/scrape.py`.
   - Analyze the sentiment: `python pipeline/sentiment.py`.
   - Make predictions: `python pipeline/predict.py`.

3. **Deploy the FastAPI App**
   - Build the Docker image: `docker build -t trendlens-app .`
   - Run the container: `docker run -p 8000:8000 trendlens-app`

4. **Continuous Integration/Continuous Deployment**
   - The CI/CD process is managed through GitHub Actions as defined in `.github/workflows/ci.yml`.
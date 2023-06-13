# Project 

a python application under consturction for collecting posts data based on hashtags.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
2. Install dependencies
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   pip install -r requirements.txt

## Usage
1. Start containers
    ```bash
    docker-compose up
2. Run Flask application in which it will make call to the scrapper in order to collect posts the crawler is capable only to collect content from video posts and poster link
    ```bash
    python3 app.py



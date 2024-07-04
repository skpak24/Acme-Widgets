# Acme-Widgets
Coding Challenge for Innovative Refrigeration Systems

## Introduction
This repo is a web application coding challenge for Innovative Refrigeration Systems. The web app is a Single Page Application created with Vue.js (frontend), Flask (backend), and SQLite (storage). The app is designed to assist Acme Widgets, Inc. with recording Job Hazard Analysis (JHA).

- The app allows users to create, view, update, and delete JHA's.
- JHA's contain a title, author, and any number of steps, with each step having a spot for description, hazards, and mitigation.
- Users are able to choose any number of steps to add to their JHA. All parts of the form are required.
- All submitted data are saved in a SQLite database.

## Installation

* Python, Node.js, and Vue.js are required to properly run the web application.

1. Clone the repo
   ```sh
   git clone https://github.com/skpak24/Acme-Widgets Acme-Widgets
   ```
2. Enter the project's root directory
   ```sh
   cd Acme-Widgets
   ```
3. Create and enter a virtual environment
   For Mac:
   ```sh
   python -m venv virtual
   source virtual/bin/activate
   pip install -r requirements.txt
   ```
   For Windows:
   ```sh
   python -m venv env
   # for Command Prompt or PowerShell
   .\env\Scripts\activate
   # for Git Bash or other Unix-like shells on Windows
   source env/Scripts/activate
   ```
4. Download necessary reuirements
   ```sh
   pip install -r requirements.txt
   ```
5. Run the backend API
   ```sh
   python app.py
   ```
6. In a second terminal, run the Vue.js server while in the root directory
   ```sh
   npm run dev -- --port 1993
   ```
7. Access the web app with the following command:
   ```sh
   http://localhost:1993/
   ```

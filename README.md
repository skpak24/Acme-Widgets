# Acme-Widgets
Coding Challenge for Innovative Refrigeration Systems

## Introduction
This repo is a web application coding challenge for Innovative Refrigeration Systems. The web app is a Single Page Application created with Vue.js (frontend), Flask (backend), and SQLite (storage). The app is designed to assist Acme Widgets, Inc. with recording Job Hazard Analysis (JHA).

- The app allows users to create, view, update, and delete JHA's.
- JHA's contain a title, author, and any number of steps, with each step having a spot for description, hazards, and mitigation.
- Users are able to choose any number of steps to add to their JHA. All parts of the form are required.
- All submitted data are saved in a SQLite database.

## Installation

* Python, Node.js (npm) and Vue.js are required.

1. Clone the repo
   ```sh
   git clone https://github.com/skpak24/Acme-Widgets
   ```
2. Enter the project's root directory
   ```sh
   cd Acme-Widgets
   ```
3. Download dependencies (It is recommended to do this within a virtual environment)
   ```sh
   pip install -r requirements.txt
   ```
4. Run the backend API
   ```sh
   python app.py
   ```
5. In a second terminal, run the Vue.js server while in the root directory
   ```sh
   npm run dev -- --port 1993
   ```
6. Access the web app with the following command:
   ```sh
   http://localhost:1993/
   ```

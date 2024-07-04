# Acme-Widgets
Coding Challenge for Innovative Refrigeration Systems

# Introduction
This repo is a web application coding challenge for Innovative Refrigeration Systems. The web app is a Single Page Application created with Vue.js (frontend), Flask (backend), and SQLite (storage). The app is designed to assist Acme Widgets, Inc. with recording Job Hazard Analysis (JHA).

- The app allows users to create, view, update, and delete JHA's.
- JHA's contain a title, author, and any number of steps, with each step having a spot for description, hazards, and mitigation.
- Users are able to choose any number of steps to add to their JHA. All parts of the form are required.
- All submitted data is saved in a SQLite database.

# How to Use

* Python and Vue.js are required.

1. Clone the repo
   ```sh
   git clone https://github.com/skpak24/Acme-Widgets
   ```
2. Enter root directory
   ```sh
   cd Acme-Widgets
   ```
3. Enter virtual environment
   ```sh
   source myenv/bin/activate 
   ```
4. Run the backend API
   ```sh
   python app.py
   ```
5. Run the Vue.js server in a second terminal (still at the root directory)
   ```sh
   npm run dev
   ```

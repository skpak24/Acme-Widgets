# Acme-Widgets
Coding Challenge for Innovative Refrigeration Systems

## Introduction
This repo is a web application coding challenge for Innovative Refrigeration Systems. The web app is a Single Page Application created with Vue.js (frontend), Flask (backend), and SQLite (storage). The app is designed to assist Acme Widgets, Inc. with recording Job Hazard Analysis (JHA).

- The app allows users to create, view, update, and delete JHA's.
- JHA's contain a title, author, and any number of steps, with each step having a spot for description, hazards, and mitigation.
- Users are able to choose any number of steps to add to their JHA. All parts of the form are required.
- All submitted data is saved in a local SQLite database. 
- The app also provides answers to common JHA questions; credit goes to the University of Washington's EHS website.

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
3. Create a virtual environment, enter it, and install necessary requirements
   ```sh
   python -m venv virtual
   
   # For Mac:
   source virtual/bin/activate
   # For Windows - Command Prompt or PowerShell
   .\virtual\Scripts\activate
   # For Windows - Git Bash or other Unix-like shells
   source virtual/Scripts/activate

   pip install -r requirements.txt
   npm install
   ```
4. Run the backend API
   ```sh
   python app.py
   ```
5. **In a second terminal**, enter the project directory again and run the Vue.js server
   ```sh
   npm run dev -- --port 1993
   ```
6. Access the web app with the following command:
   ```sh
   http://localhost:1993/
   ```

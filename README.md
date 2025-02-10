# **Scan2Save Backend API**

## **Project Overview**
Scan2Save is a medical app designed to securely store and manage emergency medical profiles. Upon creating a profile, the app generates a unique QR code that can be stored on the user's phone or printed and carried in case of an emergency. This QR code can be scanned by medical professionals or first responders to access the user's medical information, which is stored securely on the server.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Set Up a Virtual Environment](#step-2-set-up-a-virtual-environment)
  - [Step 3: Configure Environment Variables](#step-3-configure-environment-variables)
  - [Step 4: Run the Application](#step-4-run-the-application)
- [API Endpoints](#api-endpoints)
- [License](#license)


## **Features**
- Create new user profiles: Store essential health information.
- Generate unique QR codes: Secure and unique QR code for each profile.
- View your created profile.
- Medical professional can scan the QR Code through the app.

## **Getting Started**

### **Prerequisites**
- **Python 3.x**
- **pip** (Python's package installer)
- **git** (for cloning the repository)

### **Step 1: Clone the repository**
- Fork the project respository
- cd into your projects folder
- Clone the project onto your machine
    ```sh
    $ git clone <repository-url>
    ```
- cd into the project folder
    ```sh
    $ cd capstone_scan2save_backend
    ```

### **Step 2: Set Up a Virtual Environment
- **Create a new virtual environment**
     ```sh
    $ python3 -m venv venv
    ```
- **Activate virtual environment**
    ```sh
    $ source venv/bin/activate
    ```
- **Install dependencies once at the beginning of this project with**
     ```sh
    $ pip install -r requirements.txt
    ```
### Step 3: Configure Environment Variables

- Create a [.env](http://_vscodecontentref_/2) file in the root directory of the project
- Add the following environment variables to the [.env](http://_vscodecontentref_/3) file:
    ```env
    GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials/scan2save-faeee-firebase-adminsdk-fbsvc-75b7b08709.json
    SECRET_KEY=my-very-secure-and-random-secret-key-12345
    ```

### Step 4: Run the Application

- Run the Flask application
    ```sh
    $ flask run
    ```
- By default, the app will be accessible at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## API Endpoints

The backend exposes the following key API endpoints:

- **POST /api/new_user**: Create a new user profile
- **GET /api/user/<user_id>**: Retrieve a user's profile by ID
- **PATCH /api/user/<user_id>/update**: Update user or medical profile for existing users. (Incomplete feature on front end functionality. For future MVP)



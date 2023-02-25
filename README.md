# JWT Auth template for FastAPI projects

This project is a simple **JWT Auth** template for other **FastApi** projects.

## Installation

* Clone this repository to your local machine using
* Navigate to the project directory
    ```
    $ cd FastApi-Auth-JWT
    ```
* Install the required packages using
    ```
    $ pip install -r requirements.txt
    ```
## Usage
* Before running the script you need to create the ***.env*** file. After that insert your values
    ```
    JWT_SECRET=
    ```
* Create database through python interpreter.
    ```python
    import services
    services.create_database()
    ```
* Start the FastAPI server 
    ```
    $ uvicorn main:app --reload
    ```
* Open your web browser and go to http://127.0.0.1:8000/docs
* Select the URL you want to use
* Click on the **"Try it out!"** button to execute the request
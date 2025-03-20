# Philippine Payroll System

This is a Python-based payroll system designed for use in the Philippines. It utilizes a combination of libraries to provide a robust and user-friendly experience.

## Tech Stack

* **`cffi==1.17.1`**: Foreign Function Interface for Python, used for calling C code.
* **`cryptography==44.0.2`**: Provides cryptographic recipes and primitives to Python developers.
* **`customtkinter==5.2.2`**: A modern and customizable UI-library based on Tkinter.
* **`darkdetect==0.8.0`**: Detects the system's dark mode setting.
* **`greenlet==3.1.1`**: Lightweight in-process concurrent programming.
* **`packaging==24.2`**: Core utilities for Python packaging.
* **`pycparser==2.22`**: C parser in Python.
* **`PyMySQL==1.1.1`**: Pure Python MySQL client library.
* **`python-dotenv==1.0.1`**: Reads key-value pairs from a `.env` file and can set them as environment variables.
* **`SQLAlchemy==2.0.38`**: The Python SQL toolkit and Object-Relational Mapper.
* **`typing_extensions==4.12.2`**: Backported and experimental type hints.

## Features

* Calculates basic payroll components (basic salary, overtime, deductions).
* Handles Philippine-specific deductions (SSS, PhilHealth, Pag-IBIG, Withholding Tax).
* Generates payroll reports.
* User-friendly graphical interface (GUI) using `customtkinter`.
* Database integration using `PyMySQL` and `SQLAlchemy`.
* Environment variable management using `python-dotenv`.
* Dark mode detection using `darkdetect`.
* Secure password storage using `cryptography`.

## Screenshot

![Payroll System GUI](images/payroll_gui_screenshot.png)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    * **Windows:**

        ```bash
        venv\Scripts\activate
        ```

    * **macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

4.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    (Create a `requirements.txt` file that contains all the tech stack versions listed above.)

    ```text
    cffi==1.17.1
    cryptography==44.0.2
    customtkinter==5.2.2
    darkdetect==0.8.0
    greenlet==3.1.1
    packaging==24.2
    pycparser==2.22
    PyMySQL==1.1.1
    python-dotenv==1.0.1
    SQLAlchemy==2.0.38
    typing_extensions==4.12.2
    ```

5.  **Configure the database:**

    * Create a `.env` file in the project root directory.
    * Add the database connection details to the `.env` file:

        ```dotenv
        DATABASE_URL=mysql+pymysql://username:password@localhost/philippine_payroll
        ```

6.  **Run the application:**

    ```bash
    python main.py
    ```

    (or whatever the main python file is called.)

## Usage

* Follow the on-screen instructions in the GUI.
* Add employee information.
* Input working hours and other relevant data.
* Generate payroll reports.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License.

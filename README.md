# StudentWatch: A Student Attendance Tracking System

**StudentWatch** is a web application designed to streamline student attendance management for educational institutions. Built with Python and Django, it offers an intuitive interface for easy tracking, reporting, and analysis of student attendance data.

## Key Features

- **Real-time Attendance Tracking:** Record student attendance accurately and efficiently.
- **User-Friendly Interface:** Easy-to-navigate dashboard for managing attendance and viewing reports.
- **Comprehensive Reporting:** Generate detailed reports with various filters to analyze attendance trends.

## Technologies Used

- **Python:** Powerful and versatile programming language.
- **Django:** High-level web framework for rapid development.
- **PostgreSQL:** A fast and reliable relational database.

## Installation

**Easy Setup:**

1. **Clone the repository:**
    ```bash
   git clone https://github.com/mattsimoessilva/StudentWatch.git
    ```
2. **Install dependencies:**

   Make sure you have Python and pip installed.

   Create a virtual environment to isolate project dependencies (recommended):
    ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate.bat  # Windows
    ```
3. **Install dependencies from requirements.txt:**
    ```bash
   pip install -r requirements.txt
    ```
4. **Create a superuser:**
    ```bash
   python manage.py createsuperuser
    ```
   Follow the prompts to create a superuser account for administrative access.

5. **Run database migrations:**
    ```bash
   python manage.py migrate
    ```
   This creates the necessary database tables based on your models.

6. **Start the development server:**
    ```bash
   python manage.py runserver
    ```
   This launches the Django development server, typically accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Congratulations! You've successfully set up the StudentWatch application. Refer to the Django documentation for further configuration options and deployment instructions.

## Contributing

We welcome contributions to improve this project! Please refer to the `CONTRIBUTING.md` file for guidelines.

## License

StudentWatch is currently under development and uses the MIT license.

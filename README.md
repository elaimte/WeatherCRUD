# WeatherCRUD
Here's a template for your README file that highlights the features of your Django application. You can adjust the wording or add more details as necessary:

---

# Weather API

Backend is a robust and secure Django RESTful API designed for efficient city weather data retrieval and user management. Hosted on AWS and leveraging MongoDB Atlas (M0 tier), the application offers a comprehensive suite of features ensuring a seamless and secure user experience.

## Features

1. **Email-Based Signup and Sign-In**: Users can easily create an account and sign in using their email addresses, enhancing the accessibility and ease of use.

2. **Hashed Password Storage**: For enhanced security, all user passwords are securely hashed before storage, ensuring the protection of sensitive data.

3. **Token-Based Authentication**: Utilizes token-based authentication for API access, providing a secure and efficient way for users to interact with the API.

4. **City Name Autocompletion**: Features an intuitive city name autocomplete function, simplifying the user experience when searching for weather data.

5. **Search History Tracking**: Keeps a record of users' search history, allowing them to easily revisit previous queries.

6. **Serialization of Requests and Responses**: Implements serializers for both requests and responses to ensure data integrity and structured data exchange.

7. **Hosting on AWS**: Leveraging the power and reliability of Amazon Web Services for robust and scalable hosting solutions.

8. **MongoDB Atlas Integration**: Utilizes the M0 tier of MongoDB Atlas for efficient and scalable data management.

9. **Gunicorn and Nginx Deployment**: The application is served using Gunicorn as the WSGI HTTP Server and Nginx as the web server, ensuring high performance and efficient static file serving.

10. **Extended OAuth Functions for Document Compatibility**: Features an extended version of OAuth functionalities tailored for compatibility with document-based databases like MongoDB.

Certainly! Below is an expanded "Getting Started" section for your README file, including instructions for setting up a virtual environment, installing dependencies, running migrations, and starting the server.

---

## Getting Started

Follow these steps to get your development environment set up:

### Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtualenv (optional but recommended for environment isolation)

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone [https://path_to_your_repository/backend.git](https://github.com/elaimte/WeatherCRUD.git
cd backend
```

### 2. Set Up a Virtual Environment (Optional)

It's recommended to use a virtual environment to keep dependencies for the project isolated. To create a virtual environment, run:

```bash
virtualenv venv
```

To activate the virtual environment:

- On Windows, run: `venv\Scripts\activate`
- On macOS and Linux, run: `source venv/bin/activate`

### 3. Install Dependencies

Install all the required libraries and dependencies for the project using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Database Migrations

Before running the application, you need to apply migrations to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Running the Development Server

Once the database is set up, you can start the Django development server:

```bash
python manage.py runserver
```

By default, the server will start on `http://127.0.0.1:8000/`. Navigate to this URL in your web browser to view the application.

---




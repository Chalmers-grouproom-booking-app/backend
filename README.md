# Group Room Booking App

## Description
This backend is tailored for our Group Room Booking App, powered by a FastAPI server. It facilitates room booking functionalities by serving data from various sources, including web scraping and Pocketbase, to provide real-time room availability and booking management.

## Features
- **FastAPI Framework**: Utilizes the FastAPI framework for high performance and easy API creation with Python.
- **Real-Time Data**: Integrates web scraping to gather up-to-date information on room availability from different websites.
- **Pocketbase Integration**: Manages and stores data related to room bookings, user information, and room details in a Pocketbase instance.
- **Scalability**: Designed to handle increasing loads with efficient request handling and data management.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repository-url.git
   cd your-repository-directory
   ```
2. **Install the requirements**:
  ```bash
    pip install -r requirements.txt
  ```
3. **Run the server**:
  ```bash
  python -m uvicorn --app-dir="./app" --reload main:app --reload
  ```

## Configuration
Ensure the following configurations are set up before running the server:

 - **Pocketbase Configuration**: Set up your Pocketbase instance and configure the connection details in app/config.py.
- **Web Scraping Sources**: Define the URLs and scraping logic in app/scrapers/ to fetch room availability data.

## API Documentation
For detailed information on the API endpoints, please refer to our [API documentation](https://strawhats.info/docs).

## Web Scraping
The backend includes scripts that periodically scrape websites for updated room availability and other relevant data. These scripts are located in the app/scrapers/ directory and can be scheduled using tools like cron or Celery.

## Pocketbase Integration
Pocketbase is used to manage all data related to room bookings, including user information and room details. This ensures quick data retrieval and efficient management of booking data.

## Testing
**Run Tests**:
```bash
pytest app/test_main.py
```
Ensure tests cover API endpoints, data processing, and interactions with the Pocketbase database.

## Deployment
To deploy the FastAPI backend, follow these steps:

1. **Set up a server**: Ensure it meets the requirements for running FastAPI applications.
2. **Clone the repository and install dependencies**: Follow the installation steps above.
3. **Configure environment variables**: Set up all necessary configurations for the production environment.
4. **Run the server**: Use a process manager like `gunicorn` or `uvicorn` for production deployment.

## Contributing
We welcome contributions to enhance the backend functionality. To contribute, please:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit and push your changes to your branch.
4. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

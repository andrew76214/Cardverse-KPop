# Cardverse-KPop

Cardverse-KPop is a web application developed as the final project for the Cloud Computing Platforms and Applications course at National Central University, Taiwan.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [License](#license)
- [Contributors](#contributors)

## Project Overview

This project provides a platform for K-Pop enthusiasts to collect and trade virtual photocards of their favorite idols. The application allows users to register, log in, view available photocards, and manage their personal collections.

## Features

- **User Authentication**: Users can register and log in to access their personal collections.
- **Photocard Collection**: Browse and collect virtual K-Pop photocards.
- **Trading System**: Trade photocards with other users to complete your collection.
- **Responsive Design**: Optimized for various devices to ensure a seamless user experience.

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python with Flask framework
- **Database**: SQLite for data storage
- **Containerization**: Docker for environment consistency
- **Web Server**: Nginx for serving the application

https://github.com/andrew76214/Cardverse-KPop/tree/main/img/SQL_arichecture.png

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/andrew76214/Cardverse-KPop.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd Cardverse-KPop
   ```
3. **Build and run the Docker containers**:
   ```bash
   docker-compose up --build
   ```
4. Access the application:

  Once the containers are up and running, the application can be accessed at ```http://localhost:5000```.

## Usage
- Register: Create a new account to start your photocard collection.
- Log In: Access your account to view and manage your collection.
- Browse Photocards: Explore the available K-Pop photocards.
- Add to Collection: Select photocards to add to your personal collection.
- Trade Photocards: Initiate trades with other users to expand your collection.

## Folder Structure
The project structure is organized as follows:

```bash
Cardverse-KPop/
├── app/
│   ├── extensions.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   ├── js/
│   │   └── sass/
│   └── templates/
├── html5up-forty/
├── migrations/
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── config.py
├── docker-compose.yaml
├── nginx.conf
├── requirements.txt
├── run.py
└── wait_for_sql.sh
```

- The app/ directory contains the main application code, including models, routes, forms, and static assets.
- The html5up-forty/ directory includes the frontend template used for the application's design.
- The migrations/ directory is used for database migrations.
- Configuration files such as config.py, nginx.conf, and docker-compose.yaml are located in the root directory.

## License
This project is licensed under the MIT License.

## Contributors
<a href="https://github.com/andrew76214/Cardverse-KPop/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=andrew76214/Cardverse-KPop" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

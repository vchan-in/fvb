# vBank

vBank is a deliberately insecure web application based on a banking system, designed to aid security professionals, developers, and students to learn and practice security vulnerabilities in a safe and legal environment. vBank provides a platform for penetration testing and security training. The application showcases various security flaws, which users are encouraged to identify and exploit. It's an excellent tool for learning about common security issues in web applications.

## Table of Contents

- [Setup](#setup)
- [Description](#description)
- [Features](#features)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Links](#links)
- [Licensing](#licensing)

## Setup

Follow these steps to set up the project:

### From Source

1. Install [Node v18.16.1](https://nodejs.org/en/blog/release/v18.16.1)
2. Install [Python v3.11.4](https://www.python.org/downloads/release/python-3114/)
3. Run `git clone https://github.com/vchan-in/vbank.git --depth 1` (or
   clone [your own fork](https://github.com/vchan-in/vbank/fork)
   of the repository)

4. Go into the cloned folder with `cd vbank`
5. Create `.env` file from `template.env` file.
6. Build the source by running `make install`
7. Start the backend development server `make dev-backend`
8. Start the client development server,

    * Web Application: `make dev-client`
    * Android Studios: `make dev-client-android`
    * IOS XCode: ToDo
    * Desktop Application: ToDo

### Docker Container
1. Create `.env` file from `template.env` file.
1. Install [Docker](https://www.docker.com)
2. Build and run the project using `make docker-build` and followed by `make docker-up`
3. Browse to http://localhost:8080 (on macOS and Windows browse to http://192.168.99.100:8080 if you are using docker-machine instead of the native docker installation)

## Description

This project is a deliberately insecure cross platform application based on a banking system. It's designed to provide a safe and legal environment for security professionals, developers, and students to learn and practice exploiting security vulnerabilities.

The application simulates a banking system where users can register, log in, perform transactions, and use various banking services. However, it is riddled with security flaws intentionally. These flaws range from simple ones like missing input validation to more complex ones like SQL injection and Cross-Site Scripting (XSS).

The project is built using modern [technology stack](#technology-stack), providing a fresh perspective and a unique set of challenges. It's an excellent tool for learning about common security issues in web applications, how to exploit them, and more importantly, how to prevent them.

## Technology Stack

This project is built with the following technologies:

- **Frontend**: The frontend of the application is built with Vue.js, a popular JavaScript library for building user interfaces and Quasar Framework is used. We also use Pinia for state management and Material-UI for the design system.

- **Backend**: The backend is a RESTful API built with FastAPI. It handles all the business logic and database operations.

- **Database**: We use MySQL as our primary database.

- **Other Tools**: We use Git for version control, ESLint for linting, and Prettier for code formatting.

## Features

This project includes the following features:

- **User Registration**: Users can create a new account, providing their personal details.

- **User Login**: Users can log in to their account using their credentials.

- **User Dashboard**: Users can view their account balance, transaction history, and other account details.

- **Account Management**: Users can manage their accounts.

- **Transfer Money**: Users can transfer money to other users.

- **Transaction History**: Users can view their transaction history.

- **Admin Panel**: Admins can manage users, view transaction logs, and perform other administrative tasks.

## Screenshots



## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

## Links

- Project homepage: https://github.com/vchan-in/vbank
- Repository: https://github.com/vchan-in/vbank.git
- Issue tracker: https://github.com/vchan-in/vbank/issues

## Licensing

The code in this project is licensed under MIT license.

This program is free software: You can redistribute it and/or modify it under the terms of the MIT License. vBank and any contributions are Copyright © by Vaishno Chaitanya & the vBank contributors 2023 - 2024.
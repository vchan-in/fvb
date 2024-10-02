# FVB (First Vulnerable Bank)
FVB (First Vulnerable Bank) is a deliberately insecure web application based on a banking system, designed to aid security professionals, developers, and students to learn and practice security vulnerabilities in a safe and legal environment. FVB provides a platform for penetration testing and security training. The application showcases various security flaws, which users are encouraged to identify and exploit. It's an excellent tool for learning about common security issues in web applications.

The project is built using modern [technology stack](#technology-stack), providing a fresh perspective and a unique set of challenges. It's an excellent tool for learning about common security issues in web applications, how to exploit them, and more importantly, how to prevent them.

## Table of Contents
- [Setup](#setup)
- [Credentials](#credentials)
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
3. Run `git clone https://github.com/vchan-in/fvb.git --depth 1` (or
   clone [your own fork](https://github.com/vchan-in/fvb/fork)
   of the repository)
4. Go into the cloned folder with `cd fvb`
5. Create `.env` file from `env.template` file.
6. Build the source by running `make install`
7. Start the backend development server `make backend`
8. Start the client development server,

    * Web Application: `make client`
    * Android Studios: `make client-android`
    * IOS XCode: ToDo
    * Desktop Application: ToDo

### Docker Container
1. Create `.env` file from `env.template` file.
1. Install [Docker](https://www.docker.com)
2. Build and run the project using `make docker`
3. Browse to http://localhost:8080 (on macOS and Windows browse to http://192.168.99.100:8080 if you are using docker-machine instead of the native docker installation)

## Credentials
#### Admin account
* **Username:** admin
* **Password:** password

#### User account
* **Username:** emilybuck
* **Password:** @^&2VtT*

## Technology Stack
This project is built with the following technologies:

- **Frontend**: The frontend of the application is built with Vue.js, a popular JavaScript library for building user interfaces and Quasar Framework is used. It uses Pinia for state management and Material-UI for the design system.

- **Backend**: RESTful API and GraphQL API built with FastAPI framework. It handles all the business logic and database operations.

- **Database**: It uses MySQL as the primary database.

## Features
This project includes the following features:

- [x] Customer Registration
- [x] Customer Login
- [x] Customer Dashboard
- [x] Customer Account Management
- [x] Transfer Money
- [x] Transaction History
- [x] Deposit Money
- [x] Admin Panel

Planned:

- [ ] Bill Pay
- [ ] 3rd Party Banking Apps
- [ ] Loan
- [ ] Credit Cards

and more based on feedback and requests.

## Screenshots
Few of many...

- Dashboard ![Screenshot](/screenshots/dashboard.jpg)
- Customer Accounts Page ![Screenshot](/screenshots/accounts.jpg)
- Admin Panel ![Screenshot](/screenshots/admin.jpg)


## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

## Links
- Walkthrough: https://fvb.vchan.in/
- API Documentation (Online): https://apidoc.fvb.vchan.in/
- API Documentation (Swagger): http://localhost:8000/docs

- Project homepage: https://github.com/vchan-in/fvb
- Repository: https://github.com/vchan-in/fvb.git
- Issue tracker: https://github.com/vchan-in/fvb/issues

## Licensing
The code in this project is licensed under MIT license.

This program is free software: You can redistribute it and/or modify it under the terms of the MIT License. FVB and any contributions are Copyright © by Vaishno Chaitanya & the FVB contributors 2023 - 2024.
# Website
## Introduction
1. This is the Professional Social Networking Website, similar to LinkedIn. 
Here, people can add their profile details, connect with others and posts.
2.  It is a business and employment-oriented service that operates via websites.
3. The security and the authenticity of the users are also verified. They are asked to verify their
email id in order to confirm their login for the first time.
4. The user has all the control over the profile, post, likes and comments. 
5. It has github integration as well. So the user's top 5 github projects will be displayed.

## Technologies Used:
1. ***React:*** For the front-end development
2. ***Redux:*** For maintaining the application level states and improving the overall efficiency of the application
3. ***NodeJS:*** For maintaining the server of the application
4. ***Express:*** For developing the Backend API
5. ***MongoDb:*** Backend storage of the application

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.
1. Simply Download the project from the github
2. Run the following commands:
  - npm install
  - cd client
  - npm install
  - cd ..
  - npm run dev
3. The website is up and running!

## Built With
If you want to modify and enhance the features of the website. The below information could be useful.

***Useful tools:***
1. Webstorm : For the development of the code
2. Mlab: Online tool for storing the records in the MongoDb database
3. Postman: Tool used for testing the backend routes.

***Useful websites:***
1. Font awesome
2. Bootstrap


## Getting Started

These instructions will get the project running on your local machine for development and testing.

### 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/salehtwj/Mawhiba-AI.git
   cd Mawhiba-AI
   ```
2. Install backend dependencies:
  ```bash
  npm install
  cd client
  npm install
  cd ..
  ```
3. Set up the Python environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```
3. Start the project::
  ```bash
  python app.py
  ```

### Database Schema

This project uses **SQL Server** with a database named `mawheb`. Below are the two main tables used in the schema:

#### `talenters`

Stores information about talented individuals who are seeking to be discovered.

```sql
CREATE TABLE talenters (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  username VARCHAR(50),
  age INT NOT NULL,
  sport_field VARCHAR(100) NOT NULL,
  position VARCHAR(100) NOT NULL,
  skills TEXT NOT NULL,
  ai_rating VARCHAR(100),
  height INT NOT NULL,
  password VARCHAR(100),
  phone_number VARCHAR(20),
  email VARCHAR(255) NOT NULL
);
```

#### `scouts`
Holds information about scouts who are searching for talent.


```sql
CREATE TABLE scouts (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  phone_number VARCHAR(15),
  sport_field VARCHAR(100),
  position VARCHAR(100),
  password VARCHAR(255),
  city VARCHAR(100),
  organization VARCHAR(255),
  experience INT
);
```

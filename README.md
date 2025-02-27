# Project Overview- Mutual Aid Database

The [Mutual Aid Crowdfunding Database](Project%20Details.md) is a platform designed to facilitate assistance for individuals and communities affected by crises, such as wildfires, natural disasters, or financial hardship. Inspired by platforms like Craigslist and GoFundMe, our project aims to provide a streamlined, transparent, and user-friendly system where people in need can request aid and donors can easily contribute.

This database will allow users to create listings for financial assistance and enable donors to browse and choose whom to support, ensuring direct impact and efficient allocation of resources.

## - [Milestone 1](milestones/Milestone1.md)

### Deliverables

At the conclusion of Milestone 1, the deliverables will include a fully functional login page with secure authentication and session management, and a listing creation page that is fully integrated with the user system. Documentation will be updated to reflect the environment setup, running instructions, and testing procedures. An automated testing suite will also be in place, covering key functionalities of both the login and listing creation modules.

### Next Steps After Milestone 1

Following the successful completion of Milestone 1, stakeholder feedback will be collected to assess the functionality and security of the login and listing creation processes. This feedback will help in preparing for Milestone 2, where additional features such as donation functionality and user profiles will be introduced, with graphic design improvements to be implemented later.

Milestone 2 will be more refined, and will be more user friendly and have functionalityfor the donating and making listing functions as well as user profiles and ability to create listings. 

We have created an [initial layout](Initial_Mockup.md) of some of the features that we would like to include in our website as well


## [Meeting Minutes](Weekly_Meetings.md)

Meetings will be before class every week, as well as virtual calls as needed (we have time blocked out if we need the time)
For a more detailed record of our discussions in the meetings, we have created a log in a folder on GitHub which can be accessed through the link.

We also have made a [Google Doc](https://docs.google.com/document/d/1AGj9YwZyZUyJDiuea-FdOafA8IYKDKXiPMp5zLLlWQ0/edit?usp=sharing) for planning for more syncronous work, and using GitHub to work on the actual code of the project. We have created a Discord server where we communicate the tasks we are currently working on as well as checking in with our team mates as and when required.

## [Task Allocation](TaskAllocation.md)

After our first discussion, we assigned tasks to each team member based on their strengths and weaknesses. A rudimentary list was created which is still ever evolving based on the needs and the stage of the project.

## [Project Timeline & Features Overview](User%20Stories.md)

This Mutual Aid Crowdfunding Database will be developed over eight weeks, ensuring a structured approach to implementing user authentication, fundraising campaigns, donor engagement, financial transactions, and admin tools. Each week focuses on a core aspect of the platform, progressively building towards a fully functional and user-friendly system.

![Burn down chart](https://github.com/Prince-K-Ado/GroupE_MAD_Project/blob/main/chartweek2.png)

---

## Instructions on how to run our Mini-Gofundme App

## Prerequisites

Ensure you have Python installed (preferably Python 3.x).
Clone the repository to your local machine.
Set up and activate your virtual environment.

## Setting Up the Virtual Environment

### Windows

Open a terminal (Command Prompt or PowerShell) in the project root.

Create a virtual environment (if not already created):

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

### macOS/Linux

Open a terminal in the project root.

Create a virtual environment (if not already created):

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

## Running the Application

### Set Environment Variables

#### Windows

Open your terminal in the project root and run:

```bash
set FLASK_APP=app\__init__.py
set FLASK_ENV=development
```

#### macOS/Linux

In your terminal, run:

```bash
export FLASK_APP=app/__init__.py
export FLASK_ENV=development
```

### Build the Database with Table (User, Post)

```bash
python .\create_db.py
```

### Run the Flask App

In the terminal (with your virtual environment activated and environment variables set), run:

```bash
flask run
```

Your application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Running the Tests

### Ensure the Virtual Environment is Activated (see instructions above)

### Run Tests Using Pytest

From the project root, run:

```bash
pytest
```

#### Note: The test will drop any table that is create during the process. Past users will drop from the database because the tables, user or post do not exist

#### Reset and Rebuild the tables in the database by running the following or add a new user to the register form from the app

```bash
python .\create_db.py
```




This command will execute all tests located in the `tests/` directory.

These instructions should guide you through setting up your environment, running your Flask application, and executing your tests. If you encounter any issues, verify that you're in the correct project directory and that your virtual environment is activated.

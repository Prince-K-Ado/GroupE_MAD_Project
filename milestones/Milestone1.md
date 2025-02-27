## Milestone 1: Core Functionality – Login & Listing Creation

## Objective

The primary objective for Milestone 1 is to build a robust foundation that allows for secure user authentication and enables logged-in users to create listings. This phase focuses solely on functionality and security, postponing graphic design enhancements for later milestones.

For a more detailed understanding of what our app would look like, we created a mockup of some of the elements that our app would have.


## User Authentication
For the login functionality, the goal is to develop a straightforward login page with clearly labeled fields for email/username and password. On the backend, a user model will be established in the database, storing essential details such as username, email, and a securely hashed password. Secure authentication will be implemented using a framework like Flask-Login, ensuring proper session management, input validation, and error handling. Security measures include using modern password hashing methods and CSRF protection to safeguard form submissions. Comprehensive testing will involve both unit tests for verifying successful logins and error conditions, as well as manual testing to ensure proper function across various environments.

## Listing Creation Interface

The listing creation interface will be a simple form accessible only to authenticated users. This form will include essential fields such as a title and description, with the possibility to extend details later if needed. On the backend, a corresponding listing model will be created in the database, linking each listing to the user account that created it. Server endpoints will handle the rendering of the form and the processing of form submissions with necessary validations to ensure data integrity. Testing will verify that form submissions correctly store data in the database and that non-authenticated users are redirected appropriately to the login page.

## Initial Application Structure & Environment Setup

The project will be initiated by cloning the repository and installing dependencies with the command pip install -r requirements.txt. Environment variables for Flask will be set up based on the operating system (using export FLASK_APP=app/__init__.py for Linux or set FLASK_APP=app\__init__.py for Windows). The application can then be started using flask run, and tests can be executed using pytest to ensure that both the login and listing creation pages function as expected.

## Deliverables

At the conclusion of Milestone 1, the deliverables will include a fully functional login page with secure authentication and session management, and a listing creation page that is fully integrated with the user system. Documentation will be updated to reflect the environment setup, running instructions, and testing procedures. An automated testing suite will also be in place, covering key functionalities of both the login and listing creation modules.

## Next Steps After Milestone 1

Following the successful completion of Milestone 1, stakeholder feedback will be collected to assess the functionality and security of the login and listing creation processes. This feedback will help in preparing for Milestone 2, where additional features such as donation functionality and user profiles will be introduced, with graphic design improvements to be implemented later.


# Project Requirements

For our project we want to create a mutual aid crowdfunding database, modeled after web sites like Craigslist and goFundMe.

Stakeholders include entities creating listings and entities donating to the listings.

Milestone 1 will include a login page and option to create a listing. (For a detailed description of our milestone 1 please refer to the link: 

## - [Milestone 1](milestones/Milestone1.md)

Deliverables

At the conclusion of Milestone 1, the deliverables will include a fully functional login page with secure authentication and session management, and a listing creation page that is fully integrated with the user system. Documentation will be updated to reflect the environment setup, running instructions, and testing procedures. An automated testing suite will also be in place, covering key functionalities of both the login and listing creation modules.

Next Steps After Milestone 1

Following the successful completion of Milestone 1, stakeholder feedback will be collected to assess the functionality and security of the login and listing creation processes. This feedback will help in preparing for Milestone 2, where additional features such as donation functionality and user profiles will be introduced, with graphic design improvements to be implemented later.


Milestone 2 will be more refined and have bare bones graphic design as well as base functionality for the donating and making listing functions as well as user profiles and ability to create listings.
Milestone 3 will be more refined and have functionality.

Meetings will be before class every week, as well as virtual calls as needed (we have time blocked out if we need the time)

We found it easier to update the Google Doc for planning for more syncronous work, and using GitHub to work on the actual code of the project. We have a Discord server for communication.


1. Clone the repo.
2. Install dependencies ```pip install -r requirements.txt```.
3. Define the app that need to run. For Linux Env ```export FLASK_APP=app/__init__.py```. For Windows ```set FLASK_APP=app\__init__.py```
4. Run ```flask run``` (Flask)
5. To run the tests sample, type ```pytest``` in the terminal.

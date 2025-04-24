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

Burn down chart for Milestone 2 <img width="831" alt="Screenshot 2025-04-23 at 7 58 43 PM" src="https://github.com/user-attachments/assets/aa7d6d6b-b816-41f7-a471-65e4619b5247" />


---

# 📘 Instructions: How to Run the Mini-GoFundMe App

This project is a simplified GoFundMe-style web application where users can create campaigns, upload media, receive donations, and receive updates via notifications. Admins can manage and review posts, and users can track progress toward their fundraising goals.

---

## ✅ Prerequisites

- Python 3.9 or newer installed
- Git (for cloning the repository)

---

## 🔧 1. Clone the Repository

```bash
git clone https://github.com/Prince-K-Ado/GroupE_MAD_Project.git
cd GroupE_MAD_Project
```

---

## 🔨 2. Set Up the Virtual Environment

### On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ 4. Set Environment Variables

### On Windows

```bash
set FLASK_APP=app\__init__.py
set FLASK_ENV=development
```

### On macOS/Linux

```bash
export FLASK_APP=app/__init__.py
export FLASK_ENV=development
```

---

## 🧱 5. Initialize the Database

### Create or Reset the Database

```bash
python .\Datatabase_Checks\create_db.py  
```

### Seed Initial Categories (Optional but recommended to populate the subscription categories)

```bash
python .\Datatabase_Checks\seed_categories.py
```

### Create an Admin User

```bash
python .\Datatabase_Checks\create_admin.py
```

This creates a user with admin rights that can access the admin dashboard to approve or reject posts.

---

## 🚀 6. Run the Application

Start the development server:

```bash
flask run
```

Then open your browser and visit:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 7. Run the Tests

Make sure your virtual environment is activated.

### Basic Test Run
```bash
pytest
```

---

## 📘 Extra Notes

- If you're seeing errors related to database schema, you may need to delete `MiniGoFundMe.db` and re-run `create_db.py`.
- Make sure environment variables are correctly set before running `flask run`.

For questions, feedback, or contributions, please refer to the project's README or open an issue.

---
###  📖 Three most important things learned

- Clean Architecture and Modularity was essential to make debugging and testing easier when needed.
- Though the code might works in some instance, testing it provides confidence for its functionality.
- The use of Git and GitHub repo allows for versioning and reviews on collaborator contribution and code testing.


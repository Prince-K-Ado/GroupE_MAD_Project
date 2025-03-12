**Milestone 1**

*Registration page, Login page and Creating a post*

At the conclusion of Milestone 1, the deliverables include a fully functional login page with secure authentication and session management, and a listing creation page that is fully integrated with the user system.



**Agile Methods Used**







**How code fulfills user stories**

_As a user affected by a natural disaster, I want to be able to login and have my own account that saves my posts and preferences._

* The app includes registration and login for user accounts along with two test cases that verify login functionality. One that tests a successful login and one that tests a login failure.
* This is routed via the */login* and */register* routes and models user accounts via _set_password_ and _check_password_ routes along with a database and Flask's _session_ to maintain their session.
* 
![successful login](https://github.com/user-attachments/assets/56cc30f6-7afa-428d-a998-e0fd86a742f2)
![successful login flash](https://github.com/user-attachments/assets/d36c5536-121e-4d69-9104-8243aec4aab4)

_As a user affected by a natural disaster, I want to post a fundraising campaign with a title, description and percentage towards financial goal._

_As a user affected by a natural disaster, I want to upload images to further showcase my struggle and trustworthiness_

* The _/feed_ route allows users to create posts but still requires a user to be logged in via an if statement that flashes a warning to log in first. 
* The posts are associated with the user as per the _new_post = Post(user_id=session['user_id']_ line. 
* Media files can be uploaded and stored showcasing the user's campaign and flashes success or warnings if no file is selected.

_As a user affected by a natural disaster, I wish to provide an update to my posting as situations change and I can show donors how their donations have helped_

* The _edit_post_ route allows for users to edit their posts and provide updates on their campaign or situation.
* Only the user who posted their campaign can edit their post as is dictated by _if post.user_id != session['user_id']:_
* Media files can be updated or replaced, allowing users to showcase progress and posts can be deleted if no longer relevant.





# HBD!
#### Video Demo: <https://www.youtube.com/watch?v=unrHpzQzlaY&t=27s>
#### Description:
        <p>
        HBD! is a website that helps you remember your familys' and friends' birthdays. You can add a reminder with a message that will tell a birthday is
        coming up, and you can also edit or delete your reminders. The main reason I decided to create this website for my final project is because I have a
        hard time remebering people's birthdays. Last year, I couldn't remember any of my friends' birthdays, and I felt really bad, because most of them
        knew mine and even bought me gifts. So hopefully, with this website, I can help myself and others remember their loved ones' birthdays.
        </p>
        <p>
        In application.py, you will find many routes. The first route, the register route, lets you signup and create an account. I used the POST method to
        let the user enter their name and other information into my database, where it is stored for later use. The login route lets you login to your account
        using the same method. I query SQL using the name and password that was put in to check if they are correct. The logout route lets you log out using sessions.
        The default route, AKA the most important one, is used ot display reminders . I do this by querying SQL and getting all the revelant information, and then
        putting them into a list of dictionaries. After that, I output the information to html with flask by using {{}}. This route is also connected to two other routes.
        The edit and the delete route. The edit routes enables you to edit a reminder's name, date, or message. It is up to whether you want to edit one thing or edit
        everything. The other route, the delete route is very simple. It allows you get rid of reminders using the DELETE command in SQL. The last route, the add route lets
        you add birthday reminders. It uses SQL's insert and lets you add a name, date, and a message. These things are only temporary and can be changed later through
        the edit route. In helpers.py, I made a login_required function that only allows users to reach certain routes only if they log in.
        </p>
        <p>
        In the templates folder, you will find all of my html templates. There is add.html, edit.html, index.html, login.html, and register.html. All of these are extensions
        of my layout.html site, which is possible thanks to Flask. To design and style all of my different html pages, I relied on Bootstrap, which is an online
        page where you can find many CSS designs. I also used Flash from flask to send the user messages and make my website more engaging and interactive.
        In addition, every one of my routes and html templates will check the user's inputs, so when a field is empty when it is not supposed to be, the website will tell
        you.
        </p>
        <p>
        Now lastly, I want to say that CS50 is a difficult, yet fun intorductory course to computer science. I was glad that when my father signed me up for this, I didn't refuse.
        Thank you to all my teachers for making my programming journey such an enjoyable one. This was CS50.
        </p>
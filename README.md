# **Website structure**
The bulletin board will allow registered users to post advertisements for the sale of something. Announcements will be distributed according to headings, and the structure of the headings will have two levels of hierarchy: the first level will contain general headings, and the second level - more specific.

To display the list of ads, pagination was applied, since there may be a lot of ads, and the page containing all ads will be too large and its scrolling will take a long time. Also implemented the ability to search for ads by the keyword entered by the visitor.

You can leave any number of comments under any ad (on the ad details page). Any users, including guests, can leave comments (CAPTCHA is used to check guests).

As part of the ad, the user can place the main graphic illustration, which will be displayed both in the list of ads and as part of the ad details, as well as an arbitrary number of additional illustrations that can be seen only on the ad details page. Both the main and additional illustrations are optional.

The procedure for registering a new user on the site will be divided into two stages. At the first stage, the visitor enters his data on the registration page, after which a letter with a hyperlink leading to the activation page is sent to the e-mail address specified by him. At the second stage, the visitor follows the hyperlink received in the letter, goes to the activation page and becomes a full user.

The bulletin board site will include the following pages:

*   main - showing the ten most recently published ads without breaking them into categories; 


* ad list page - showing (using pagination) ads from a specific category. It will also contain a form for searching ads for the entered word;


* About the details page of the selected ad - will display all still left
comments for him and a form for adding a new comment;


* About the page of registration and activation of a new user;


* About login and logout pages;


* About the profile page of the registered user - will display a list of ads
laziness left by the current user;


* About the page for adding, editing, deleting ads;

* About the page for changing the password, editing and deleting the user profile; 
 
* About the page of information about the site, about the rights of its developer, user
announcements

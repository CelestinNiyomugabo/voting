# voting
## 1. Introduction
The AUCA Online Voting Platform is a web-based application developed to facilitate the creation of contests, voting for contestants, and real-time monitoring of contest statistics. This platform was developed as part of a course project and integrates user registration, secure voting procedures, and real-time graphical data display. The project follows best practices for security and user experience, ensuring data protection and reliable voting mechanisms.

## 2. Key Features
### 2.1 User Registration and login
  
AUCA users can register on the platform by providing their name, email, and password.
•	Security: Passwords are securely encoded using Django's built-in password hashing mechanisms before being stored in the database, ensuring that no plain text passwords are exposed.
•	Validation: The platform validates user input during registration, including checking that email addresses are unique.

Login Functionality: A login system was implemented using Django's authentication framework. After registering, users can log in using their email and password.
Authenticated Actions: Once logged in, users gain access to features such as creating contests and managing contestants.

 
### 2.2 Contest Management (Logged-in Users)
•	Contest Creation: A logged-in user can create multiple contests with detailed information such as the contest name, description, and date of occurrence.
•	Contestant Management: After creating a contest, users can add contestants to the contest by supplying details such as contestant name, image, and additional information (if required).
The secreenshot below shows the user interface for creating a new contest (left), and an interface for viewsing an existing contest with an option of editing or deleting the contest
   

A user is prompted to confirm the deletion with a pop-up modal (see the screenshot below)
 

 
### 2.3 Public Voting
Contest Viewing: Public users (those not registered or logged in) can browse available contests and view detailed information about each contest.
 

Voting Mechanism: Public users are allowed to vote for a specific contestant in any contest. However, several rules and validation mechanisms are enforced:
•	Voter Information: A voter must provide their name, email, phone number, gender, and address before submitting a vote.
•	OTP Verification: To verify the authenticity of the voter, an OTP (One-Time Password) is sent to both the provided email and phone number. The OTP must be correctly entered by the voter before their vote is accepted.
•	Single Vote Restriction: A user can only vote once in each contest. The platform checks the email and phone number combination to ensure that the same person cannot vote multiple times in the same contest.

To avoid user flustration with multiple page loading, we provided a user friendly interface which submits the OTP to email and phone using AJAX. See the voting steps below:

Step 1: when a user clicks “VOTE” button, a modal pop-up to display voting form where a user provide his email and phone number.
 

Step 2: Once the OTP is sent, the user is prompted to verify the OTP which was sent to email phone
Security & Verification: The OTP (One-Time Password) verification process ensures that the voter is genuine by sending a code to the user's provided email and phone.
•	The OTP is generated when the voter provides their information, and they must successfully enter the OTP before they can cast their vote.
•	This ensures that fake or duplicate votes are prevented by authenticating the voter through two different channels (email and phone).
      
### OTP verification screen
 

### Voting Rules Enforcement
•	Single Vote Policy: The system ensures that no voter can vote more than once for the same contest. This is accomplished by tracking the voter's email and phone number combination.
•	Voter Identification: Each vote is associated with a unique email and phone number, ensuring that voters cannot bypass the system by simply changing their name or address. The system checks if a combination of email and contest has already been used to vote, and if it has, further voting is prevented.

Step 3: Collecting voter information
Once the OTP is successfully verified, a voting form is displayed, allowing a user to supply his name, and select the candidate/contestant. Refer to the screenshot below
 
Step 4: Voting confirmation
Once the voting is a success, a user receives an on-screen notification confirming his vote.
 

Email and phone validation enforcement:
Different controls were implemented for an efficient voting system. As can be seen from the notifications displayed on the screens below, a user can not proceed if both email and phone number are not entered
 
If a user attempts to enter an invalid email or phone, the system validates and return an error. The system also verifies whether the entered phone number is valid and has country code.
   

Since only one vote is allowed per contest, when a user uses the same email address to attempt re-votinng, the platform returns an error:
 

### 2.3 Dashboard and Statistics
Real-time Statistics: The platform provides real-time data visualization using Chart.js to display various statistics related to contests and voting behavior. The dashboard includes:
•	Votes per Contestant: A bar chart showing the number of votes each contestant has received.
•	Voter Demographics:
o	Gender Distribution: A pie chart displaying the percentage of male vs female voters.
o	Provincial Distribution: A horizontal bar chart showing the number of voters per province, allowing the contest manager to see which region is most engaged.
•	Contest Participation: A bar chart displaying the number of voters per contest, further broken down by gender.
•	Contestants’ Performance: A real-time visual of how many votes each contestant has accumulated in various contests.
A dashboard to display real-time statistics
 

## 3. Technologies Used
### 3.1 Backend
•	Django: The platform was built using Django, a robust and scalable Python web framework. Django's built-in ORM was used to manage and query the database efficiently.
•	MySQL: A MySQL database was used to store all platform data, including user information, contest data, contestant details, and votes.

### 3.2 Frontend
•	HTML, CSS, JavaScript: The platform's frontend uses these core web technologies to deliver a smooth and responsive user interface.
•	Bootstrap: Bootstrap was used to ensure that the platform is fully responsive, providing a consistent experience across mobile, tablet, and desktop devices.
•	Chart.js: For displaying contest statistics and voter data, Chart.js was integrated into the platform to generate dynamic charts, making data visualization intuitive for users.

### 3.3 APIs
•	V-Pay API (SMS): The platform integrates with the pay.vonsung.rw API to send OTP verification codes via SMS, ensuring that the voting process is secure and that only genuine voters can participate.
•	Email Verification: The Django EmailMessage feature was used to send OTPs to voters' emails.




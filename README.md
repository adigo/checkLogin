# checkLogin
python selenium login

<!-- Output copied to clipboard! -->

<!-----
NEW: Check the "Suppress top comment" option to remove this info from the output.

Conversion time: 1.299 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β29
* Mon Apr 19 2021 17:19:54 GMT-0700 (PDT)
* Source doc: Global Team Documentation - Synoptix JDBC error monitoring
* This document has images: check for >>>>>  gd2md-html alert:  inline image link in generated source and store images to your server. NOTE: Images in exported zip file from Google Docs may not appear in  the same order as they do in your doc. Please check the images!

----->


## JDBC error monitoring (checkLogin)


Created By:  Cheng-Yi Lee

Create Date: 03/29/2021


### Overview

This document contains instructions to package, deploy, and configure the app “checkLogin”.


### Who Should Read This Manual?

This manual is intended to be used by the Apps Team, who is trying to either :



1. Modify the python code checkLogin,
2. Compile it into exe form.
3. Schedule the exe to run on a windows server.
4. Configure the “checkLogin” application on the server by editing the json and ini file.
5. Transform the username and password from plain texts to encrypted strings.


## What problem are we trying to solve? 



### Web portal GenericJDBCExecption error


This error occurs when the JDBC connection pool  loses its connection to the database but didn’t notice that, instead of reconnecting. It returns to faulty connection from the pool to the application causing this error to happen.

This error usually happens during the login process, after the user entered the username and password and right after you click submit, you’ll get this error.

 

Re-starting the Tomcat service resolves this issue. We have already scheduled the Tomcat server to restart nightly to mitigate this issue. This “checkLogin” application is just providing another safety net


## Environment

This application is built with:

Python 3.9,

Selenium 3.141.0,

Pyinstaller 4.2,

ChromeDriver 89.0.4389.23

So after installing python in your development environment, please run the below command to install other required packages.

 


```
pip install selenium pyinstaller
```


Please also make sure that Chrome browser is installed and download the chromedriver based on the version of your chrome browser.

Your development folder structure should look like this:


```
-driver
    -chromedriver.exe
-main.py
-checkLogin.bat
-checkLogin.ini
-checkLogin.json
```



## **Packaging into exe file**

Use below command to create checkLogin-selenium.spec if not exists or if the directory has changed, or if the Chrome browser is upgraded an a new driver is needed.:


```
pyi-makespec main.py --onefile --noconsole --add-binary "./driver/chromedriver.exe;./driver" --add-data "checkLogin.json;." --add-data "checkLogin.ini;." --name checkLogin-selenium
```


Add below code to the end of checkLogin-selenium.spec if it's newly created:


```
import shutil
shutil.copyfile('checkLogin.ini', '{0}/checkLogin.ini'.format(DISTPATH))
shutil.copyfile('checkLogin.json',  n'{0}/checkLogin.json'.format(DISTPATH))
```


Finally, use below command to create the exe file


```
pyinstaller --clean checkLogin-selenium.spec
```


You should see all the generated files inside the “dist” folder.


## **Deployment **

Please place the below 4 files inside the folder C:\checkLogin


```
checkLogin.bat
checkLogin.ini
checkLogin.json
checkLogin-selenium.exe
```


When Scheduling using Task Scheduler, be sure to select “Run only when user is logged on”.



For the Action, run the “C:\checkLogin\checkLogin.bat” script, and put in “C:\checkLogin\” (without quotes) in the “Start in (Optional):” box.



## **Configuration**

There are 2 configuration files: checkLogin.ini and checkLogin.json.


### checkLogin.ini

Below is an example for checkLogin.ini:


```
[chromedriver]
path = driver\chromedriver.exe

[website]
url = http://synoptix.uhs.local/

[delay]
seconds = 10
```


path: This refers to the location of the chromedriver.exe file. Although it should be packaged with checkLogin-selenium.exe, please still keep a copy in C:\checkLogin\driver in case of file IO failure.

 url: The URL for Synoptix web portal.

delay: The interval between each action in second(s). For example if set to 1, the program will enter the username, wait for 1 second, enter the password, wait for 1 second, then slick login button. It is set to 10 because the Synoptix website is really slow and I did not wrap the code with enough try/catch clauses in the code.


### checkLogin.json

Below is an example for checkLogin.json:


```
{
  "username": "w57Csy7CpT03wptRw78d",
  "password": "w57CsyvCtys2woJfw6Ac",
  "recipients": [
    "chengyi.lee@rosalindfranklin.edu",
    "adigolee@gmail.com"
  ]
}
```


username: An encrypted username. We’ll show how to encrypt the username in the next section.

password: An encrypted password. We’ll show how to encrypt the password in the next section.

recipients: A list of recipients separated by comma for the notification email when login fails. 


## How to encrypt username/ password

To encrypt your username and password, modify the checkLogin.json as below:


```
{
  "username": "myUsername",
  "password": "myPassword",
  "encrypt": "true",
  "recipients": [
    "chengyi.lee@rosalindfranklin.edu",
    "adigolee@gmail.com"
  ]
}

```



1. Replace the "myUsername" to an actual username, and the "myPassword" to the actual password.
2. Add a new line:  `"encrypt": "true",`
3. Run the program checkLogin-selenium.exe in the same folder.

 

The json file will be changed to:


```
{
    "username": "w57Csy7CpT03wptRw78d",
    "password": "w57CsyvCtys2woJfw6Ac",
    "recipients": [
        "chengyi.lee@rosalindfranklin.edu",
        "adigolee@gmail.com"
    ]
}
```


Here, the “w57Csy7CpT03wptRw78d” is the encrypted "myUsername" and "w57CsyvCtys2woJfw6Ac" is the encrypted "myPassword", and the "encrypt" attribute is removed.

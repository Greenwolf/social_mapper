# Social Mapper Troubleshooting

A quick troubleshooting guide for Social Mapper, to help you fix issues that might arise due to site changes.

Please submit pull requests and merge back if you fix something a social media site has changed!

## Why is Social Mapper Broken?

Social Mapper can stop working for certain social media sites that change the names of the HTML classes that Social Mapper uses to extract information from the web pages.

## How Do I Fix It?

To fix a broken site just open the relevant Python module in the [modules](modules) folder and update the class names that BeautifulSoup is searching for or change the parsing code.

In the image below you can see a number of the things Social Mapper relies on:

* The URL that it uses to search for the targets.
* The class name of the div which holds each of the people returned from the search.
* The code it uses to manipulate the extracted data to parse the link to the profile and profile picture.

For example in the [facebookfinder.py](modules/facebookfinder.py) module, it is finding user profiles based on the \_401d div class. If Facebook were to change this, line 77 in facebookfinder.py would need to be changed accordingly.

![Fixing Social Mapper](facebook-html-classes.png?raw=true "Fixing Social Mapper")
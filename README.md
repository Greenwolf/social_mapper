# Social Mapper
![alt text](https://img.shields.io/badge/Python-3_only-blue.svg "Python 3 only")
![alt text](https://img.shields.io/travis/Greenwolf/social_mapper.svg "Travis build status")

**This tool is no longer actively maintained, parts of it may still work and I will accept pull requests to keep it up to date**


**WARNING: FACEBOOK NOW DETECTS THIS AFTER A FEW 100 SEARCHES, USE ONLY DISPOSABLE FACEBOOK ACCOUNTS**

A Social Media Mapping Tool that correlates profiles via facial recognition by Jacob Wilkin ([Greenwolf](https://github.com/Greenwolf)).

Social Mapper is an Open Source Intelligence Tool that uses facial recognition to correlate social media profiles across different sites on a large scale. It takes an automated approach to search popular social media sites for targets' names and pictures to accurately detect and group a person’s presence, outputting the results into report that a human operator can quickly review.

Social Mapper has a variety of uses in the security industry, for example the automated gathering of large amounts of social media profiles for use on targeted phishing campaigns. Facial recognition aids this process by removing false positives in the search results, so that reviewing this data is quicker for a human operator.

Social Mapper supports the following social media platforms:

* LinkedIn
* Facebook
* Pinterest
* Twitter
* Google Plus
* Instagram
* VKontakte
* Weibo
* Douban

Social Mapper takes a variety of input types such as:

* An organisation's name, searching via LinkedIn
* A folder full of named images
* A CSV file with names and URL’s to images online

## Usecases (Why you want to run this)

Social Mapper is primarily aimed at Penetration Testers and Red Teamers, who will use it to expand their target lists and find their social media profiles. From here what you do is only limited by your imagination, but here are a few ideas to get started:

(Note: Social Mapper does not perform these attacks, it gathers you the data you need to perform them on a mass scale.)

* Create fake social media profiles to 'friend' the targets and send them links or malware. Recent statistics show social media users are more than twice as likely to click on links and open documents compared to those delivered via email.
* Trick users into disclosing their emails and phone numbers with vouchers and offers to make the pivot into phishing, vishing or smishing.
* Create custom phishing campaigns for each social media site, knowing that the target has an account. Make these more realistic by including their profile picture in the email. Capture the passwords for password reuse.
* View target photos looking for employee access card badges and familiarise yourself with building interiors.

## Getting Started

These instructions will show you the requirements for and how to use Social Mapper.

### Prerequisites

Note: On Kali you can now run ./kali-installer.sh from the setup directory.

As this is a Python3 based tool, it should theoretically run on Linux, ChromeOS ([Developer Mode](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices/generic)) and macOS. The main requirements are Firefox, Selenium and Geckodriver. To install the tool and set it up follow these 4 steps:

1) Install the latest version of Mozilla Firefox for macOS here:

```
https://www.mozilla.org/en-GB/firefox/new/
```

Or for Debian/Kali (but not required for Ubuntu) get the non-ESR version of Firefox with:
```
sudo add-apt-repository ppa:mozillateam/firefox-next && sudo apt update && sudo apt upgrade
```

Make sure the new version of Firefox is in the path. If not manually add it.

2) Install the Geckodriver for your operating system and make sure it's in your path, on Mac you can place it in `/usr/local/bin`, on ChromeOS you can place it in `/usr/local/bin`, and on Linux you can place it in `/usr/bin`.

Download the latest version of Geckodriver here:

```
https://github.com/mozilla/geckodriver/releases
```

3) Install the required libraries:

On Linux install the following prerequisites:
```
sudo apt-get install build-essential cmake
sudo apt-get install libgtk-3-dev
sudo apt-get install libboost-all-dev
```

On Linux & macOS finish the install with:

```
git clone https://github.com/Greenwolf/social_mapper
cd social_mapper/setup
python3 -m pip install --no-cache-dir -r requirements.txt
```

On Mac look through the [setup/setup-mac.txt](setup/setup-mac.txt) file to view some additional xcode, brew and xquartz installation instructions.

4) Provide Social Mapper with credentials to log into social media services:

```
Open social_mapper.py and enter social media credentials into global variables at the top of the file
```

5) For Facebook & Instagram, make sure the language of the account which you have provided credentials for is set to 'English (US)' for the duration of the run. Additionally make sure all of your accounts are working, and can be logged into without requiring 2 factor authentication. 

6) Use the Firefox browser to login to each Social Media Profile once and save/process and "unknown browser" or "trust this browser" pages. 

## Using Social Mapper

Social Mapper is run from the command-line using a mix of required and optional parameters. You can specify options such as input type and which sites to check alongside a number of other parameters which affect speed and accuracy.

### Required Parameters

To start up the tool 4 parameters must be provided, an input format, the input file or folder and the basic running mode:

```
-f, --format	: Specify if the -i, --input is a 'name', 'csv', 'imagefolder' or 'socialmapper' resume file
-i, --input	: The company name, a CSV file, imagefolder or Social Mapper HTML file to feed into Social Mapper
-m, --mode	: 'fast' or 'accurate' allows you to choose to skip potential targets after a first likely match is found, in some cases potentially speeding up the program x20
```

Additionally at least one social media site to check must be selected by including one or more of the following:

```
-a, --all		: Selects all of the options below and checks every site that Social Mapper has credentials for
-fb, --facebook		: Check Facebook
-tw, --twitter		: Check Twitter
-ig, --instagram	: Check Instagram
-li, --linkedin		: Check LinkedIn
-gp, --googleplus	: Check Google Plus
-vk, --vkontakte	: Check VKontakte
-wb, --weibo		: Check Weibo
-db, --douban		: Check Douban
```

### Optional Parameters

Additional optional parameters can also be set to add additional customisation to the way Social Mapper runs:

```
-t, --threshold		: Customises the facial recognition threshold for matches, this can be seen as the match accuracy. Default is 'standard', but can be set to 'loose', 'standard', 'strict' or 'superstrict'. For example 'loose' will find more matches, but some may be incorrect. While 'strict' may find less matches but also contain less false positives in the final report.
-cid, --companyid	: Additional parameter to add in a LinkedIn Company ID for if name searches are not picking the correct company.
-s, --showbrowser	: Makes the Firefox browser visible so you can see the searches performed. Useful for debugging.
-w, --waitafterlogin : Wait for user to press Enter after login to give time to enter 2FA codes. Must use with -s
-v, --version		: Display current version.
-vv, --verbose  : Verbose Mode (Useful for Debugging)
-e, --email		: Provide a fuzzy email format like "<f><last>@domain.com" to generate additional CSV files for each site with firstname, lastname, fullname, email, profileURL, photoURL. These can be fed into phishing frameworks such as Gophish or Lucy.
```

### Example Runs

Here are a couple of example runs to get started for differing use cases:

```
A quick run for Facebook and Twitter on some targets you have in an imagefolder, that you plan to manually review and don't mind some false positives:
python3 social_mapper.py -f imagefolder -i ./Input-Examples/imagefolder/ -m fast -fb -tw

The same as above but with the browser showing, and waiting enabled to allow a user to enter 2FA codes and manually rectify changed login processes:
python3 social_mapper.py -f imagefolder -i ./Input-Examples/imagefolder/ -m fast -fb -tw -s -w

An exhaustive run on a large company where false positives must be kept to a minimum:
python3 social_mapper.py -f company -i "Evil Corp LLC" -m accurate -a -t strict

A large run that needs to be split over multiple sessions due to time, the first run doing LinkedIn and Facebook, with the second resuming and filling in Twitter, Google Plus and Instagram:
python3 social_mapper.py -f company -i "Evil Corp LLC" -m accurate -li -fb
python3 social_mapper.py -f socialmapper -i ./Evil-Corp-LLC-social-mapper-linkedin-facebook.html -m accurate -tw -gp -ig

A quick run (~5min) without facial recognition to generate a CSV full of names, email addresses, profiles and photo links from up to 1000 people pulled out of a LinkedIn company, where the email format is known to be "firstname.lastname":
python3 social_mapper.py -f company -i "Evil Corp LLC" -m accurate -li -e "<first>.<last>@evilcorpllc.com"
```

### Troubleshooting

Social Media sites often change their page formats and class names, if Social Mapper isn't working for you on a specific site, check out the [docs](docs/TroubleShooting_Social_Mapper) section for troubleshooting advice on how to fix it. Please feel free to submit a pull request with your fixes.

### Maltego

For a guide to loading your Social Mapper results into Maltego, check out the [docs](docs/Maltego_Import_Guide) section.

## Authors

* [**Jacob Wilkin**](https://github.com/Greenwolf) - *Research and Development*

## Donation
If this tool has been useful for you, feel free to thank me by buying me a coffee :)

[![Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/Greenwolf)

## Acknowledgments

* Thanks to Vincent Yiu & MDSEC for their great LinkedInt tool which inspired me to add the search by LinkedIn company name input method.
* Thanks to [janmei](https://github.com/janmei) (Pinterest Module), [alexsok-bit](https://github.com/alexsok-bit), [ewpratten](https://github.com/ewpratten), [cclauss](https://github.com/cclauss), [TADT1909](https://github.com/tadt1909), [Molkree](https://github.com/Molkree) and [kix-s](https://github.com/kix-s) for their contributions to the project.
* Thanks to `[Your Name Could Be Here, Come Help Out!]` for contributions to the project.

![Social Mapper Logo](docs/logo.png?raw=true "Social Mapper Logo")

## Youtube Trailer:

[![Social Mapper Trailer](https://i.imgur.com/s6rPhgK.jpg)](https://www.youtube.com/watch?v=wVN-7R3B_xs&feature=youtu.be "Social Mapper Trailer")

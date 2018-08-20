# Social Mapper

A Social Media Mapping Tool that correlates profiles via facial recognition by Jacob Wilkin(Greenwolf)

Social Mapper is a Open Source Intelligence Tool that uses facial recognition to correlate social media profiles across different sites on a large scale. It takes an automated approach to searching popular social media sites for targets names and pictures to accurately detect and group a person’s presence, outputting the results into report that a human operator can quickly review.

Social Mapper has a variety of uses in the security industry, for example the automated gathering of large amounts of social media profiles for use on targeted phishing campaigns. Facial recognition aids this process by removing false positives in the search results, so that reviewing this data is quicker for a human operator.

Social Mapper supports the following social media platforms:

* LinkedIn
* Facebook
* Twitter
* GooglePlus
* Instagram
* VKontakte
* Weibo
* Douban

Social Mapper takes a variety of input types such as:

* An organisations name, searching via LinkedIn
* A folder full of named images
* A CSV file with names and url’s to images online”

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

As this is a python based tool, it should theoretically run on Linux, chromeOS ([Developer Mode](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices/generic)) and Mac. The main requirements are Firefox, Selenium and Geckodriver. To install the tool and set it up follow these 4 steps:

Install the latest version of Mozilla Firefox here:

```
https://www.mozilla.org/en-GB/firefox/new/
```

Install the Geckodriver for your operating system and make sure it's in your path, on Mac you can place it in `/usr/local/bin`, on chromeOS you can place it in `/usr/local/bin`, and on Linux you can place it in `/usr/bin`. 

Download the latest version of Geckodriver here: 

```
https://github.com/mozilla/geckodriver/releases
```

Install the required python 2.7 libaries:

```
git clone https://github.com/SpiderLabs/social_mapper
cd social_mapper/setup
python -m pip install --no-cache-dir -r requirements.txt
```

Provide Social Mapper with Credentials to log into social media services:

```
Open social_mapper.py and enter social media credentials into global variables at the top of the file
```

## Using Social Mapper

Social Mapper is run from the command line using a mix of required and optional parameters. You can specify options such as input type and which sites to check alongside a number of other parameters which affect speed and accuracy. 

### Required Parameters

To start up the tool 4 parameters must be provided, an input format, the input file or folder and the basic running mode:

```
-f, --format	: Specify if the -i, --input is a 'name', 'csv', 'imagefolder' or 'socialmapper' resume file
-i, --input 	: The company name, a csv file, imagefolder or social mapper html file to feed into social mapper
-m, --mode		: Fast or Accurate allows you to choose to skip potential targets after a first likely match is found, in some cases potentially speeding up the program x20
```

Additionally at least one social media site to check must be selected by including one or more of the following:

```
-a, --all 			: Selects all of the options below and checks every site that social mapper has credentials for
-fb, --facebook 	: Check Facebook
-tw, --twitter 		: Check Twitter
-ig, --instagram 	: Check Instagram
-li, --linkedin 	: Check LinkedIn
-gp, --googleplus 	: Check GooglePlus
-vk, --vkontakte 	: Check VKontakte
-wb, --weibo 		: Check Weibo
-db, --douban 		: Check Douban
```

### Optional Parameters

Additional optional parameters can also be set to add additional customisation to the way social mapper runs:

```
-t, --threshold 	: Customises the faceial recognition threshold for matches, this can be seen as the match accuracy. Default is 'standard', but can be set to loose, standard, strict or superstrict. For example loose will find more matches, but some may be incorrect. While strict may find less matches but also contain less false positives in the final report. 
-cid, --companyid 	: Additional parameter to add in a LinkedIn Company ID for if name searches are not picking the correct company.
-s, --showbrowser	: Makes the Firefox browser visable so you can see the searches performed. Useful for debugging. 
-v, --version		: Display current version
```

### Example Runs

Here are a couple of example runs to get started for differing use cases:

```
A quick run for facebook and twitter on some targets you have in an imagefolder, that you plan to manually review and don't mind some false positives:
python social_mapper.py -f imagefolder -i ./mytargets -m fast -fb -tw

A exhaustive run on a large company where false positives must be kept to a minimum:
python social_mapper.py -f company -i "SpiderLabs" -m accurate -a -t strict

A large run that needs to be split over multiple sessions due to time, the first run doing LinkedIn and Facebook, with the second resuming and filling in Twitter, Google Plus and Instagram:
python social_mapper.py -f company -i "SpiderLabs" -m accurate -li -fb
python social_mapper.py -f socialmapper -i ./SpiderLabs-social-mapper-linkedin-facebook.html -m accurate -tw -gp -ig
```

### Troubleshooting

Social Media sites often change their page formats and class names, if Social Mapper isn't working for you on a specific site, check out the docs section for troubleshooting advice on how to fix it. Please feel free to submit a pull request with your fixes.

### Maltego

For a guide to loading your Social Mapper results into Maltego, check out the docs section. 

## Authors

* **Jacob Wilkin** - *Research and Development* - [Trustwave SpiderLabs](https://github.com/SpiderLabs)

## License

Social Mapper
Created by Jacob Wilkin
Copyright (C) 2017 Trustwave Holdings, Inc.
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

## Acknowledgments

* Thanks to MDSEC for their great LinkedInt tool which inspired me to add the search by LinkedIn company name input method. 

![Social Mapper Logo](docs/logo.png?raw=true "Social Mapper Logo")

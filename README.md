# airsana

## Table of Contents
* [About](#about)
  * [Details](#details)
  * [Development Plans](#development-plans)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation and Usage](#installation-and-usage)
  * [Profiles](#profiles)
    * [Profile Fields](#profile-fields)









## About
Airsana takes a content calendar object from the Airtable API, finds only the rows assigned to a certain person, and sends that information to the Asana API which creates tasks in that person's Asana workspace

This is a work in progress. See below for details on how to run this script with example data, or create your own profile after looking at the example below

### Details
The TableMatcher object takes in an Airtable object from the Airtable API. The TableMatcher then filters out rows that don't match the filter value provided by
the current profile. After getting all rows that match, the TableMatcher makes a list of dicts where each dict is filled with data from the filtered rows.
The Taskmaster object's ```add_task()``` method takes a dict from that list and hands it to the Asana API's ```Client.create_in_workspace()``` method which makes a
task in the appropriate Asana workspace

### Development Plans
- [ ] Improve README
- [ ] Add test module
- [ ] Search for and remove any redundancies between project and Airtable/Asana APIs
- [ ] Complete ui:
  - [ ] profile maker walkthrough
  - [ ] exception handling for improper inputs

## Getting Started

### Prerequisites
- Python3  


  There are different ways you can install Python. See [The Hitchhikers Guide to Python](https://docs.python-guide.org/starting/installation/) for detailed instructions. If you have Homebrew installed already, you can run the following to install Python3:
  
  ```sh
  $ brew install python
  ```

- [Asana api](https://github.com/asana/python-asana)
  ```sh
  $ pip install asana
  ```

- [Airtable api](https://github.com/gtalarico/airtable-python-wrapper/blob/master/docs/source/index.rst)
  ```sh
  $ pip install airtable-python-wrapper
  ```
- An [Airtable account](https://airtable.com/). You will need your Content calendar api key and base id. See [Airtable's API documentation](https://airtable.com/api) on how to find this information for your Content calendar

  The test script pulls data from the Content production table within the Content calendar base:
   ![picture of Airtable calendar](https://github.com/dansjack/airsana/blob/master/images/airtable_calendar.png "Airtable calendar")

- An [Asana account](https://asana.com/). You will need to get your Personal Access Token (PAT), user ID, and workspace name. User ID and workspace name can be found at the following links once logged in, respectively: [https://app.asana.com/api/1.0/users](https://app.asana.com/api/1.0/users), [https://app.asana.com/api/1.0/workspaces](https://app.asana.com/api/1.0/workspaces). You can find instructions on how to get a PAT here: [https://developers.asana.com/docs/#authentication-quick-start](https://developers.asana.com/docs/#authentication-quick-start)

### Installation and Usage
1. Clone the repo
    ```sh
    $ git clone https://github.com/dansjack/airsana.git
    ```
2. Fill in the fields (the ones in all caps) of ```profile_example.json``` or make a new profile in ```profiles.json```

   Note: Make sure not to upload any of your sensitive data to Github. Add ```profile_example.json``` and ```profiles.json``` to your ```.gitignore``` if you intend to fill them with sensitive info

3. start the program
    ```sh
    $ python3 airsana
    ```
4. When prompted, enter ```3``` to run the script from the example profile in ```profile_example.json``` (given you filled in the required fields), or enter ```1``` if you have an existing profile inside ```profiles.json```.  
   ```
   **************************************
   *************   Airsana   ************
   **************************************

     Enter 'q' to quit at any time

   Commands:
   1. Run script with existing profile
   2. Make new profile
   3. Run script with test profile
   Enter a command by digit: 3
   ```

5. The script will run and give status updates before exiting:
   ```
   Running script with test profile...
   GETTING latest createdTime...
   GETTING matches with createdTime later than 2015-06-05T23:08:42.000Z
   GETTING latest createdTime...
   SETTING latest createdTime...
   Task named "Is a luxury stay worth it?" added to workspace
   Task named "Poolside views" added to workspace
   Task named "Summer-inspired bites with Sandra Key" added to workspace
   Done

           *****************************
           ********** Goodbye **********
           *****************************
   ```

6. Go to your Asana workspace to see that the tasks have been uploaded and assigned to you
![picture of Asana workspace](https://github.com/dansjack/airsana/blob/master/images/asana_workspace.png "Asana workspace")

#### Profiles
A profile is where your Asana and Airtable credentials are stored, along with other important info like what you want to filter table rows by and how you want to structure the data being sent to the Asana API  

Example profile:
```sh
{   
    "name": "TEST PROFILE",
    "asana": {
        "name": "ASANA USERNAME",
        "pat": "ASANA PAT",
        "id": "ASANA ID",
        "workspace_name": "ASANA WORKSPACE NAME",
        "note_fields": [
            "section",
            "status"
        ]
    },
    "airtable": {
        "api": "AIRTABLE API",
        "base": "AIRTABLE BASE",
        "table": "Content production",
        "latest_createdTime": "2015-06-05T23:08:42.000Z",
        "filter": "Author",
        "filter_value": "Cameron Toth",
        "match_structure": {
            "title": "Headline",
            "section": "Section",
            "status": "Status"
        }
    }
}
```
##### Profile Fields
* name: Name of this profile   
* asana: Asana account details
  * name: username
  * pat: Personal Access Token (PAT)
  * id: user id
  * workspace_name: Name of user's workspace
  * note_fields: list of the Airtable object fields you want to send to Asana
* airtable: Airtable account details
  * filter_value: value of the filter field
  * api: API key
  * base: base id
  * table: name of a table belonging to the base
  * latest_createdTime: the created time of the row fetched the last time the program was ran (or what the user set it to in profiles.json, manually)
  * filter: the Airtable field to filter the Airtable object by
  * match_structure: structure of the dicts returned by ```TableMatcher.prep_matches()```

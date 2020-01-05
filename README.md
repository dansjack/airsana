# Airtable to Asana

## About
A tool to automatically add a task to a user's Asana workspace when a blog post is
assigned to that user in an Airtable calendar

This is a work in progress. See below for details on how to run this script with example data

### Details
The TableMatcher object takes in an Airtable object from the Airtable API. The TableMatcher then filters out rows that don't match the filter value provided by
the current profile. After getting all rows that match, the TableMatcher

## Getting started

### Prerequisites
- Python3
```sh
brew install python3
```

- [Asana api](https://github.com/asana/python-asana)
```sh
pip install asana
```

- [Airtable api](https://github.com/gtalarico/airtable-python-wrapper/blob/master/docs/source/index.rst)
```sh
pip install airtable-python-wrapper
```
- An [Airtable account](https://airtable.com/). You will need your Content calendar api key and base id. See [Airtable's API documentation](https://airtable.com/api) on how to find this information for your Content calendar. The test script pulls data from the Content production table within the Content calendar base

- An [Asana account](https://app.asana.com/). You will need to get your Personal Access Token (PAT), user ID ([Click here once logged in](https://app.asana.com/api/1.0/users)) and workspace name ([Click here once logged in](https://app.asana.com/api/1.0/workspaces))

### Installation & Usage
1. Clone the repo
    ```sh
    git clone https://github.com/dansjack/airtable-to-asana.git
    ```
2. Create ```credentials.json``` in ```airtable-to-asana/``` and make a new profile, or fill in the fields (the ones in all caps) of ```cred_example.json```

 Note: Don't upload any of your sensitive data to Github. Add ```cred_example.json``` to ```.gitignore``` if you intend to use it with your personal data, or copy/paste the example profile into ```credentials.json```

3. start the program
    ```sh
    python3 airtable-to-asana
    ```
4. When prompted, enter ```3``` to run the script from the example profile in ```cred_example.json``` (given you filled in the required fields), or enter ```1``` if you have an existing profile inside ```credentials.json```

  ```sh
  **************************************
  ********** Airtable to Asana *********
  **************************************

    Enter 'q' to quit at any time

  Commands:
  1. Run script with existing profile
  2. Make new profile
  3. Run script with test profile
  Enter a command by digit: 3
  ```

5. The script will run and give status updates before exiting:

  ```sh
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

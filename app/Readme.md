## About

This folder contains the code to run the twitter data extraction interface.


## Content

It contains the 
- `main.py` : which contains all the code to search for twitter IDs and extract tweets. It also contain code to parse the output and return the result as CSV files. The raw data is stored in `data/` directory. The cleaned data is stored in the `cleaned/` directory.


## To run locally
- Clone the repo to your local repository
- Change directory to app `cd app` in the terminal
- Install the python requirements. `pip install -r requirements.txt` file.
- Run `python main.py` in the terminal and provide the needed arguments.


### Sample code

`python main.py --usernames PeterObi,atiku --search_fields author_id,text --clean_data False`
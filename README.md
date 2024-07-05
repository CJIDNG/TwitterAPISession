# TwitterAPISession
This repository contains files that will be used for CJID's workshop in July

## Get Started 
1. Visit the Twitter Developer API url
2. Sign up for access.
3. Once approved, create a new project 
4. After creating the project, generate the tokens and key secrets 
5. Run the notebook 

## How the notebook works
1. Install the required packages
2. Create a `.env` file and save the generated tokens there 
3. Get the names of the individuals you want to extract their tweet and add it to `usernames` field in the `create_url` function.
4. Run the next cell to get the twitter Ids for each of the individuals you want to extract their data.
5. Add the id from the response to the `user_id` field in the `create_url` function.
6. Decide what metrics you want to retrieve. Add it to the `tweets.fields` field in the `get_params` function
6. Run the next cell to get the tweets for each individual 
7. Save the response to `csv` 

# TwitterAPISession
This repository contains files that will be used for CJID's workshop in July

## Get Started 
1. [Visit the Twitter Developer API url](https://developer.x.com/en/docs/twitter-api/tools-and-libraries/v2)
2. Sign up for access.
3. Once approved, create a new project and follow the on-screen prompts
<img width="1253" alt="Screenshot 2024-07-05 at 10 24 20" src="https://github.com/CJIDNG/TwitterAPISession/assets/54020973/bd36a70f-2988-40ee-9b00-3eda85dee1d7">

5. After creating the project, generate the tokens and key secrets
<img width="1251" alt="Screenshot 2024-07-05 at 10 23 31" src="https://github.com/CJIDNG/TwitterAPISession/assets/54020973/25f81cda-cdee-4df4-8e5e-a197fc5655b6">

7. Run the notebook 

## How to run the notebook
1. Click on [twitter-api.ipynb](https://colab.research.google.com/drive/1a99KZxJvn0EL3MZwedMz1JS1dHJC5D7s?usp=sharing). It will take you to Google Colab 
2. Install the required packages
3. Create a `.env` file and save the generated tokens there 
3. Get the names of the individuals you want to extract their tweet and add it to `usernames` field in the `create_url` function.
5. Run the next cell to get the twitter Ids for each of the individuals you want to extract their data.
6. Add the id from the response to the `user_id` field in the `create_url` function.
7. Decide what metrics you want to retrieve. Add it to the `tweets.fields` field in the `get_params` function
8. Run the next cell to get the tweets for each individual
9. The following cells show you how to clean the data yiu have gotten.
10. Save the response to `csv` 

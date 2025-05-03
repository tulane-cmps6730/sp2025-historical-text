# Historical Text Generator
![image](https://github.com/user-attachments/assets/65fd838f-83df-4f7c-b2c7-25c082378a72)

## Background

As a lover of all things history and machine learning, I always wondered how LLMs such as ChatGPT were able to easily harbor and output data based on any query or criteria that was given to it. As someone who is
deeply inquistive regarding what has happened in our past as humans, I thought creating a project where I generate historical texts based on a user inputting a year, and location would not only finetune my 
machine learning skills but also satisfy my aptitide for historical knowledge.

## Goals

The goal of this project is to develop a natural language generation model that produces historically accurate and coherent text based on user inputs such as a specific year, time period, or location. The generated outputs aim to reflect the language, tone, and context of the chosen setting. This model could help surface insights from lesser-known historical regions or events, like Southeast Asia during WWI or the Caribbean during WWII, offering a richer view of global history.

## Method

### Data Collection

In order for the model to be fluent, coherent, as well be diverse enough where it will be able to take as many user inputs as possible, I would need to gather a large dataset that includes diverse sources. 
I did this by creating mini "loader" scripts for each of my sources, and a main "pipeline" script where I those loaders end up being used to extract and append all of the data together into one large csv file. 
During the process of appendage, the csv is structured such that the metadata that is collected from the loaders are placed into columns. For example, when reading an article about Ancient Rome on Wikipedia, the loader is able to extract the year, the region, and the actual text itself, all in their designated [YEAR], [REGION] and [TEXT] columns. 

The sources used were: 
 - Chronicalling America
       -Around 200 peices of text (wasn't able to collect any more)
       -Mainly focused on the largest states (Florida, Texas, New York)
       -Comprised of early 19th century journals, newspapers and diaries
 -Wikipedia
       -Around 100 articles
       -Comprised of Global Ancient history
 -Gutenburg Project
       

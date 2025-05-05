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
I did this by creating mini "loader" scripts for each of my sources, and a main ["pipeline"](https://github.com/tulane-cmps6730/sp2025-historical-text/blob/main/nlp/pipeline.py) script where I those loaders end up being used to extract and append all of the data together into one large csv file. 
During the process of appendage, the csv is structured such that the metadata that is collected from the loaders are placed into columns. For example, when reading an article about Ancient Rome on Wikipedia, the loader is able to extract the year, the region, and the actual text itself, all in their designated [YEAR], [REGION] and [TEXT] columns. 

The sources used were: 
 * Chronicalling America
     + Around 200 peices of text (wasn't able to collect any more)
     + Mainly focused on the largest states (Florida, Texas, New York) since the site wouldnt allow for me to collect to much
     + Comprised of early 19th century journals, newspapers and diaries
     + Collected using the requests library, scrapping the webpage
     + Code: [Chronicling_america.py](https://github.com/tulane-cmps6730/sp2025-historical-text/blob/main/nlp/chronicling_america.py)
* Wikipedia
     + Around 400 articles
     + Comprised of Global Ancient history
     + Collected using the wikipedia python library
     + Code: [Wikipedia_loader.py](https://github.com/tulane-cmps6730/sp2025-historical-text/blob/main/nlp/wikipedia_loader.py)
* Gutenburg Project
     + Around 400 peices of text
     + Contained Literature and Journals from the Late Middle Ages as well as text from the 1600s-1900s
     + Fucused mainly on the Europe, the Americas, and some of Asia and Africa
     + Collected using Beautiful Soup
     + Code: [colonial_soucebook_loader.py](https://github.com/tulane-cmps6730/sp2025-historical-text/blob/main/nlp/colonial_sourcebook_loader.py), [gutenburg_loader.py](https://github.com/tulane-cmps6730/sp2025-historical-text/blob/main/nlp/gutenburg_loader.py)
 
### Training and Testing 

To train this model I used DistilGPT-2 on the dataset (which was then eventually stored in a .csv file). I preprocessed the data by removing any rows with missing field, split the data into a training and evaluation set. 
I tokenized the text using GPT2Tokenizer and trained the data using HuggingFace with a maximum of 1000 steps (took 3.5 hours). I then saved the model and tokenizer for later generatioon. 

![image](https://github.com/user-attachments/assets/e98b1cde-1d4d-4355-8c89-ec90b58392ed)


### Generating New Text

Utilized model.generate() with sampling top_k, top_p, and temperature to promote diversity

![image](https://github.com/user-attachments/assets/634b5eac-0f96-4510-9f19-f34d3ae9c68e) 
Example of generated text using the Prompt 1800 for Year and France for Region


## Evaluation

Evaluated using BLEU and ROUGE Scores (for lexical overlap) and BERTScore (for semantic similarity). Found that while surface-level matches were quite low, semantic similarity was moderate at 0.76. 
 
![image](https://github.com/user-attachments/assets/da12b653-7a78-4f5a-8822-f457d1d7ee68)

Full notebook is located [here](https://github.com/tulane-cmps6730/sp2025-historical-text/blob/main/notebooks/Hostorical_Text_Generation_Notebook.ipynb)

  
       

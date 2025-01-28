Points System:
3+1+1 = 5
-Data is not provided in a standardized format: 3pts
For example, the MSDS files had some common elements but they were far from standardized, the LD 50 was expressed in many different ways
- Data is split up across multiple files to begin with: 1pt
Data is in a format other than one of the following: 2pts
CSV, JSON
-Data contains strings with punctuation (quotes or commas): 1pt
Data set is larger than 1GB in size: 1pt
Data set is composed of more than one type of related data: 2pts
For example there is a table of products and a table of orders
Data set needs to be accessed in a way other than connecting to a database or downloading a file: 1pt
I had to mount a virtual hard drive to get access to the MSDS files
You might need to make HTTP requests to an API

0-3: You should probably find a more interesting data set
4-6: This is a reasonable dataset to work with
7+: This is going to be... interesting.



Assignment Requirements
Describe your dataset, how you obtained it and why you chose it as well as an estimate of the points for complexity.
This dataset contains transaction records from multiple banks and bank accounts. I obtained them by downloading the csv files online. I chose this set because I personally want to track all my expenses and categories in one location. Other platforms that do a similar job either do not track old data or do not categorize well enough. The complexity of this dataset is estimated to be 5.

You should create one or more CSV or TSV files that include data that you are interested in working on from your data-set.
You should create one or more JSON files that include data that you are interested in working on from your data set.
You should write a program that can convert your data set from JSON to CSV, and another program that converts CSV back to JSON
You should load your data into a tool which will allow you to do analysis of your data.
This could be R, a SQL database or a Python data package like matplotlib
You should show evidence that you are able to do basic operations on the data in your data package,  e.g.  json.load parse results without error, R  descriptive statistics output, etc. 
You should briefly describe what interesting questions deeper analysis of this data may answer and why these may be interesting to look at for the midterm project




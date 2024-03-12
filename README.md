# Data Inferer
![Static Badge](https://img.shields.io/badge/Python-blue)
![Static Badge](https://img.shields.io/badge/Django-brightgreen)
![Static Badge](https://img.shields.io/badge/React-red)

This is the take-home assignment for Rhombus AI. The task is inferring the best datatype for each column for input data. Data is processed into a Pandas DataFrame, then modified to fit the best-guessed dtype for the current column.

## Prerequisites
- Python installed (Use Python 3.12 for seamless package installation experience).
- Node.js and npm (Node Package Manager) installed.

## Setup

### 1. Clone the Repository
- Use Virtual Environment (recommended)

### 2. Install Dependencies
- Install Python dependencies:
```
# navigate to project directory
$ pip install -r requirements.txt
```
- Install Node.js dependencies:
```
$ cd data_inferer
$ npm install
```

## Start the server
```
# run the next two commands in separate terminal
$ python manage.py runserver
# remember to change into data_inferer directory before npm start
$ npm start
```

## Notes for judges

Check out `dtype_inference/infer_file.py` for my main script to test (with comments). Other than that:

I consider this project to be one of the starting points before any manual data cleaning. Which is why:
- I didn't downcast (reduce size) datatypes
- Integer columns with NaN values are treated as float columns. That's because 1. NaN is a float and 2. I could have converted these NaNs into min_int, but there would be issues with arithmetic operations, and 3. User Interface treats both int and float as Number anyway.
- Datetime construction from UNIX epoch is not considered.
- No Boolean consideration. It lacks context to consider whether value is True or is False, which better be defined by the user. Also, it's very similar to Categorical with 2 values.
- Non-atomic categories (such as Thriller, Action, Horror in the same cell) are out of scope.

UI limitations:
- Cannot handle large files, which requires pagination and lazy loading. But my script can handle them normally!
- Do not let user set custom dtypes. It adds unnecessary complexity to the app while users can just modify the Dataframe directly in their workflow. I also don't think this is the main focus of the assignment.

Possible improvements to my algorithm:
- Can remove redundant linear traversals for columns to optimize speed.
- Can downcast dtypes for better memory.

This is the first proper Django app I built. I also learned React from scratch and tried to put my best one. It took me a total of 8 days.

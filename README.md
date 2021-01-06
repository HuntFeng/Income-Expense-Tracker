# Income Expense Tracker
A free (at least for now) dash-based webapp deployed on Google Cloud Platform.

## For normal users
Click into this link



Drop your csv file containing transaction, then you can see the results.

## The format of csv file
| Date  | Description             | Debit | Credit |
|-|-|-|-|
|12/30/2020 | transaction description | 10 | 0 |
|12/30/2020 | transaction description | 0 | 10 |

- Header is not necessary

---

## For developer
Create a new virtual environment, install the requirements, then run the app.

`pip install -r requirements.txt`

`cd income_expense_tracker`

`python app.py`


## File structure
- `main.py`: The main program.
- `dataframe_preprocess.py`: Preprocess the dataframe when csv is read. 
- `app.yaml`: For deployment on google cloud platform.

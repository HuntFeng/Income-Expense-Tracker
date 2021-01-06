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
Create a new virtual environment, then install the requirements

`pip install -r requirements.txt`

cd to the `/income_expense_tracker` folder then run the app

`cd income_expense_tracker`

`python app.py`

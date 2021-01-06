EXPENSE_TYPES = {
    "TOYOTA": r".*TOYOTA.*",
    "E-Transfer": r".*Internet Banking E.*",
    "Internal Transfer": r".*Internet Banking INTERNET TRANSFER.*",
    "TFSA": "Electronic Funds Transfer PREAUTHORIZED DEBIT CIBC",
    "ATM Withdrawal": r".*ATM WITHDRAWAL.*",
    "Interactive Brokers": r".*BILL PAY.*INTERACTIVE BROKERS.*",
    "ICBC": r".*PREAUTHORIZED DEBIT.*ICBC.*",
    "Tuition Fee": r".*BILL PAY.*SIMON FRASER UNIVERSITY.*",
    "Medical Insurance": r".*PREAUTHORIZED DEBIT PROVINCE OF BC.*",
    "Monthly Fee": r".*MONTHLY FEE.*",
    "Overdraft Fee": r".*OVERDRAFT.*",
    "Service Charge": r".*SERVICE CHARGE ADD.*"
}

INCOME_TYPES = {
    "SFU": r".*SFU.*",
    "ATM Deposit": r".*ATM DEPOSIT.*",
    "Credit Memo": r".*CREDIT MEMO.*", # This one must be below SFU since some SFU payment are also credit memo type
    "Internet Deposit": r".*Internet Banking INTERNET DEPOSIT.*"
}

def clean_up_dataframe(df):
    df.rename(columns={0: "Date", 1: "Desc", 2: "Debit", 3: "Credit"}, inplace=True)
    df.fillna(0, inplace=True)
    df["Type"] = df["Desc"].apply(lambda s: s.split("-")[0].strip())

def transform_types(df):
    for type_short, type_long in EXPENSE_TYPES.items():
        df["Type"].replace(regex=type_long, value=type_short, inplace=True)

    for type_short, type_long in INCOME_TYPES.items():
        df["Type"].replace(regex=type_long, value=type_short, inplace=True)

def preprocess_dataframe(df):
    clean_up_dataframe(df)
    transform_types(df)

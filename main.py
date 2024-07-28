import pandas as pd
import csv
from datetime import datetime

from data_entry import get_amount, get_date, get_category, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']
    FORMAT  = '%d-%m-%Y'
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)

        except FileNotFoundError:
            
            # DATA FRAME - object within pandas that allows us to access different rows/col from a csv file

            df = pd.DataFrame(columns=[
                'date',
                'amount',
                'category',
                'description'
            ])

            # Convert to csv file from dataframe with the finance_data.csv name

            df.to_csv(cls.CSV_FILE, index = False)

    @classmethod
    def add_entry(cls, data, amount, category, description):

        # store in python dictionary

        new_entry = {
            'date': data,
            'amount': amount,
            'category': category,
            'description': description
        }

        # a = open a file
        # store the opened file in a variable (csv_file)
        with open(cls.CSV_FILE, 'a', newline="") as csv_file:

            #CSV Writer
            # Take a dictionary and write it into a csv file

            writer = csv.DictWriter(csv_file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

        print('Entry added successfuly!')

    
    @classmethod
    def get_transactions(cls, start_date, end_date):

        # read the csv file as a dataframe
        df = pd.read_csv(cls.CSV_FILE)

        # accesssing date column from dataframe converted to date objects
        df['date'] = pd.to_datetime(df['date'], format=CSV.FORMAT)

        # get start and end dates to datetime objects
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # Mask
        # Something that apply to the different rows inside of a dataframe to see of we could select that row or not

        # checking the date is between the start date and end date
        # filtered different rows inside the dataframe
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)

        # return the filtered dataframe where the mask is true
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}:")

            print(filtered_df.to_string(
                
                index=False, formatters={'date': lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df['category'] == "Income"]["amount"].sum()

            total_expense = filtered_df[filtered_df['category'] == "Expense"]["amount"].sum()

            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")

            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)

    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entry(date, amount, category, description)

CSV.get_transactions("24-01-2024", "30-07-2024")

#add()


def plot_transactions(df):
    # find the different rows and entries using the date column
    df.set_index('date', inplace=True)

    #Daily Frequency (Resample)
    #take the filtered dataframe with the transcations and row them by day
    income_df = df[df['category'] == "Income"].resample('D').sum().reindex(df.index, fill_value = 0) # take the values and add them together

    expense_df = df[df['category'] == "Expense"].resample('D').sum().reindex(df.index, fill_value = 0)

    #setting up the screen/canvas for the plot
    plt.figure(figsize=(10, 6))
    # x axis is the index and y axis is the amount
    plt.plot(income_df.index, income_df['amount'], label='Income', color='green')

    plt.plot(expense_df.index, expense_df['amount'], label='Expense', color='red')

    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income and Expenses Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

    


def main():
    while True:
        print("\n1, Add a new transaction")
        print("2, View transactions and a summary within a data range")
        print("3, Exit")

        choice = int(input("Enter your choice (1-3): "))

        if choice == 1:
            add()

        elif choice == 2:

            start_date = input("Enter the start date (dd-mm-yyyy): ")
            end_date = input("Enter the end date (dd-mm-yyyy): ")

            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot the transactions? (y/n): ").lower() == "y":
                plot_transactions(df)


        elif choice == 3:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()
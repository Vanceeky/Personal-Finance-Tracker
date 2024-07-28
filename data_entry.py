from datetime import datetime




date_format = "%d-%m-%Y"
categories = {
    'I': 'Income',
    'E': 'Expense'
}
# recurvsive function to get valid date

def get_date(prompt, allow_default=False):
    
    date_str = input(prompt)
    
    if allow_default and not date_str:
        # get today's date and format it to dd-mm-yyyy
        return datetime.today().strftime(date_format)
    
    try:
        # take the date string and convert it to a valid datetime object
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print('Invalid date format. Please entry the date in dd-mm-yyyy format')
        return get_date(prompt, allow_default)
    

#Keep calling the function until a valid amount is entered
def get_amount():
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            raise ValueError('Amount must be a non-negative non-zero value')
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input("Enter the category ( 'I' for Income or 'E' for Expense): ").upper()
    if category in categories:
        return categories[category]
    
    print("Invalid category, Please enter 'I' for Income or 'E' for Expense")
    return get_category()



def get_description():
    return input('Enter a description (optional): ')

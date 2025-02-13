# Import libraries
from flask import Flask, redirect, render_template, url_for, request

# Instantiate Flask functionality

app = Flask("Transaction Listing App")

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    #print(total_balance())
    return render_template('transactions.html',transactions=transactions,total_balance=total_balance(transactions))

# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,            # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'],           # Get the 'date' field value from the form
            'amount': float(request.form['amount']) # Get the 'amount' field value from the form and convert it to a float
        }
        # Append the new transaction to the transactions list
        transactions.append(transaction)
        # Redirect to the transactions list page after adding the new transaction
        return redirect(url_for("get_transactions"))
        # If the request method is GET, render the form template to display the add transaction form
    return render_template("form.html")

# Update operation: Display edit transaction form
# Route to handle the editing of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']           # Get the 'date' field value from the form
        amount = float(request.form['amount'])# Get the 'amount' field value from the form and convert it to a float
        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Update the 'date' field of the transaction
                transaction['amount'] = amount   # Update the 'amount' field of the transaction
                break                            # Exit the loop once the transaction is found and updated
        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)
    # If the transaction with the specified ID is not found, handle this case (optional)
    return {"message": "Transaction not found"}, 404

# Delete operation: Delete a transaction
# Route to handle the deletion of an existing transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Remove the transaction from the transactions list
            break  # Exit the loop once the transaction is found and removed
    # Redirect to the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))

# Search
@app.route("/search", methods=["GET", "POST"])
def search_transaction():
    search_range = {"min":0, "max":1000000}
    found_transactions =[]
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        amount_min = float(request.form['min_amount'])# Get the 'min amount' field value from the form and convert it to a float
        amount_max = float(request.form['max_amount'])# Get the 'max amount'
        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['amount'] >= amount_min and transaction['amount'] <= amount_max:
                found_transactions.append(transaction)                           # Exit the loop once the transaction is found and updated
        # Redirect to the transactions list page after updating the transaction
        if len(found_transactions) > 0:
            return render_template('transactions.html',transactions=found_transactions, total_balance=total_balance(found_transactions))
        else:
           # If the transaction with the specified ID is not found, handle this case (optional)
            return {"message": "Transaction not found"}, 404 
    
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    return render_template("search.html", search_range=search_range)

# Total balance

@app.route("/balance")
def total_balance(my_transactions):
    total = 0
    # Check if the request method is POST (form submission)
    for transaction in my_transactions:
        total += transaction['amount']
    return {"Balance": total}, 201                          
                

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)


    


    
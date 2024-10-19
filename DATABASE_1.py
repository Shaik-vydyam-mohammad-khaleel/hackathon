import pandas as pd
import sqlite3
from flask import Flask, request, render_template
from sqlalchemy import create_engine

# Step 1: Define the dataset and database connection
DATABASE_NAME = "example.db"
DATASET_CSV = "HACKTHON.CSV"  # Path to your dataset

# Function to create and populate the database from the CSV
def create_database_from_csv(csv_file, db_name):
    # Load the dataset into a Pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Create an SQLite connection
    conn = sqlite3.connect(db_name)
    
    # Save the DataFrame to an SQLite table
    df.to_sql('data_table', conn, if_exists='replace', index=False)
    
    # Close the connection
    conn.close()

# Step 2: Create the database
create_database_from_csv(DATASET_CSV, DATABASE_NAME)

# Step 3: Set up the Flask web interface
app = Flask(__name__)
engine = create_engine(f'sqlite:///{DATABASE_NAME}', echo=False)

# Step 4: Define routes
@app.route('/')
def home():
    return render_template('index.html')  # HTML page for the interface

@app.route('/query', methods=['GET', 'POST'])
def query_database():
    query = ''
    results = None
    
    if request.method == 'POST':
        # Get the SQL query from the form
        query = request.form['query']
        
        # Execute the query on the database
        with engine.connect() as connection:
            results = pd.read_sql(query, connection)
    
    return render_template('query.html', query=query, results=results)

# Step 5: Run the application
if __name__ == '__main__':
    app.run(debug=True)

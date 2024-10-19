import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog

# Step 1: Create a database connection
def create_connection(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connected to SQLite database: {db_name}")
        return conn
    except sqlite3.Error as e:
        print(f"Error creating connection: {e}")
    return conn

# Step 2: Create a table schema
def create_table(conn, table_name, columns):
    cursor = conn.cursor()
    columns_schema = ", ".join([f"{col} TEXT" for col in columns])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_schema});"
    try:
        cursor.execute(create_table_sql)
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

# Step 3: Insert dataset into the database
def insert_data(conn, table_name, data):
    cursor = conn.cursor()
    for row in data:
        placeholders = ", ".join(["?" for _ in row])
        cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)
    conn.commit()
    print(f"Inserted {len(data)} rows into '{table_name}'")

# Step 4: GUI to select file and insert into the database
def load_dataset():
    # Open file dialog to select CSV
    filepath = filedialog.askopenfilename(title="Select Dataset", filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return
    # Load CSV using pandas
    df = pd.read_csv(filepath)
    # Create table and insert data into SQLite
    conn = create_connection("my_database.db")
    create_table(conn, "my_table", df.columns)
    insert_data(conn, "my_table", df.values)
    conn.close()
    messagebox.showinfo("Success", f"Dataset inserted into database successfully!")

# Step 5: Create a simple Tkinter GUI
def create_gui():
    window = tk.Tk()
    window.title("Database Loader")
    window.geometry("300x150")

    # Button to load the dataset
    load_btn = tk.Button(window, text="Load Dataset", command=load_dataset)
    load_btn.pack(pady=20)

    window.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
DATABASE_NAME = "example.db"
DATASET_CSV = "dataset.CSV"  # Path to your dataset

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


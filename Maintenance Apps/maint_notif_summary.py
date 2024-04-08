import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
from datetime import datetime, timedelta

# Function to load specific notification fields from an Excel file, with filtering
def load_notifications_from_excel(excel_file_path):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path, engine='openpyxl')

    # Ensure the specified columns are present in the DataFrame
    expected_columns = ['Work Order', 'Work Description', 'Start Date', 'Material Status']
    for col in expected_columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in the Excel file.")

    # Convert 'Start Date' to datetime if it's not already
    df['Start Date'] = pd.to_datetime(df['Start Date'])

    # Calculate the date 8 days from today
    eight_days_from_today = datetime.now() + timedelta(days=8)

    # Filter rows where 'Material Status' is 'INCOMPLETE' and 'Start Date' is within 8 days from today
    filtered_df = df[(df['Material Status'] == 'INCOMPLETE') & 
                     (df['Start Date'] <= eight_days_from_today) &
                     (df['Start Date'] >= datetime.now())]

    # Convert the filtered DataFrame to a list of strings (one per row), formatting each row's data
    notifications = filtered_df.apply(lambda row: f"Work Order: {row['Work Order']}, "
                                                  f"Work Description: {row['Work Description']}, "
                                                  f"Start Date: {row['Start Date'].strftime('%Y-%m-%d') if pd.notnull(row['Start Date']) else 'N/A'}, "
                                                  f"Material Status: {row['Material Status']}",
                                      axis=1).tolist()
    return notifications

# Simple Tkinter GUI to display notifications
def display_notifications_gui(notifications):
    root = tk.Tk()
    root.title("Notification Review")

    # Use a scrolled text area to display notifications
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Insert notifications into the text area
    for notification in notifications:
        text_area.insert(tk.END, notification + '\n\n')  # Add two newlines to separate notifications

    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    excel_file_path = r"C:\Users\FrancisChong.AzureAD\OneDrive - TrackOne\Datasets\WO_temp_test.xlsx"
    notifications = load_notifications_from_excel(excel_file_path)
    display_notifications_gui(notifications)

import pandas as pd
from datetime import datetime
from plyer import notification  # For system notifications

# Load work orders from an Excel file
def load_work_orders(excel_path):
    return pd.read_excel(excel_path, engine='openpyxl')

# Filter work orders based on the 'incomplete' material status and specific date range
def filter_work_orders(df):
    today = datetime.now()
    end_date = datetime(2024, 4, 15)  # Specific end date: April 8, 2024
    df['start_date'] = pd.to_datetime(df['Start Date'])  # Ensure start_date is in datetime format

    # Apply filtering criteria
    filtered_df = df[(df['Material Status'] == 'INCOMPLETE') &
                     (df['start_date'] >= today) &
                     (df['start_date'] <= end_date)]
    return filtered_df

# Send system notifications with detailed information
def send_notifications(work_orders):
    for _, row in work_orders.iterrows():
        days_until_start = (row['start_date'] - datetime.now()).days
        # Construct message with additional details
        message = (
            f"Work Order: {row['Work Order']}\n"
            f"Plant Description: {row['Plant Description']}\n"
            f"Work Description: {row['Work Description']}\n"
            f"Priority: {row['Priority']}\n"
            f"Start Date: {row['start_date'].strftime('%Y-%m-%d')} (in {days_until_start} days)\n"
            "Material availability status: incomplete."
        )
        notification.notify(
            title="Work Order Notification",
            message=message,
            timeout=10  # Notification display duration in seconds
        )

# Main function to orchestrate the process
def main(excel_path):
    df = load_work_orders(excel_path)
    filtered_work_orders = filter_work_orders(df)
    if not filtered_work_orders.empty:
        send_notifications(filtered_work_orders)
    else:
        print("No work orders match the criteria.")

if __name__ == "__main__":
    excel_path = r"C:\Users\FrancisChong.AzureAD\OneDrive - TrackOne\Datasets\WO_temp_test.xlsx"  # Specify the path to your Excel file
    main(excel_path)

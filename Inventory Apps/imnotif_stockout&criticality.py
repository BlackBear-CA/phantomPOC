import pandas as pd
from plyer import notification

def send_summary_notification(df):
    # Filter the DataFrame
    critical_products = df[(df['material criticality'] == 'PRODUCTION STOPPER') & (df['stock_on_hand'] == 0)]

    # Count the filtered products
    count_critical_products = len(critical_products)

    # Send notification
    notification.notify(
        title="Stock Criticality Summary",
        message=f"This is the number of products under 'Production Stopper' criticality with 0 stock: {count_critical_products}",
        app_name="Stock Summary Notification",
        timeout=30  # Duration in seconds
    )
    print(f"Notification sent with count: {count_critical_products}")

# Load the data
def load_data(file_path):
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        return None

# Main function to run the application
def main(file_path):
    df = load_data(file_path)
    if df is not None:
        send_summary_notification(df)

# Replace with the path to your Excel file
excel_file_path = r"C:\Users\FrancisChong.AzureAD\OneDrive - TrackOne\Datasets\Inventory ReportV1.xlsx"
main(excel_file_path)

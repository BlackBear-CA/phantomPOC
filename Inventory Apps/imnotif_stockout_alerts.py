import pandas as pd
from plyer import notification

def check_stock_and_notify(excel_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Loop through the rows and check stock against ROP
    for index, row in df.iterrows():
        product_description = row['product description']
        stock_on_hand = row['stock_on_hand']
        rop = row['rop']

        # Check if stock on hand is less than ROP
        if stock_on_hand < rop:
            # Send notification
            notification.notify(
                title=f"Low Stock Alert for {product_description}",
                message=f"Stock on hand: {stock_on_hand} is below ROP: {rop}",
                app_name="Stock Level Checker",
                timeout=10  # Duration in seconds
            )
            print(f"Notification sent for {product_description}")

# Use the file path provided by the user
file_path = r"C:\Users\FrancisChong.AzureAD\OneDrive - TrackOne\Datasets\Inventory ReportV1.xlsx"
check_stock_and_notify(file_path)

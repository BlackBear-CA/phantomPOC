import os
import pandas as pd
from plyer import notification
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

def read_form_data(path):
    # Read the Excel file and return a dictionary with the form data.
    df = pd.read_excel(path, header=None, engine='openpyxl', usecols=[0, 1])
    form_data = {}
    for _, row in df.iterrows():
        if pd.notnull(row[0]) and pd.notnull(row[1]):
            key = str(row[0]).strip().lower()
            value = str(row[1])
            form_data[key] = value
    return form_data

class Handler(FileSystemEventHandler):
    def __init__(self, log_directory):
        self.log_directory = log_directory

    def process(self, file_path):
        if file_path.endswith('.xlsx'):
            form_data = read_form_data(file_path)
            
            product_id = form_data.get('product_id', 'Unknown_ProductID').replace(' ', '_').replace('/', '_')
            purchasing_document = form_data.get('purchasing document', 'Unknown_Document').replace(' ', '_').replace('/', '_')
            net_price = float(form_data.get('net price', 0))
            requested_modified_price = float(form_data.get('requested modified price', 0))
            
            # Calculate price variance
            price_variance = requested_modified_price - net_price
            
            log_filename = f"{product_id}_{purchasing_document}_log.txt"
            log_file_path = os.path.join(self.log_directory, log_filename)

            with open(log_file_path, 'w') as log_file:
                for key, value in form_data.items():
                    log_file.write(f"{key.title()}: {value}\n")
                # Log price variance and approval line
                log_file.write(f"Price Variance: {price_variance:.2f}\n")
                log_file.write("Reviewed and Approved By: \n")
            print(f"Log file created: {log_file_path}")

            notification.notify(
                title='Log File Created',
                message=f'Log file for product {product_id} and document {purchasing_document} has been saved. Price Variance: {price_variance:.2f}',
                app_icon=None,
                timeout=10,
            )

    def on_created(self, event):
        if not event.is_directory:
            self.process(event.src_path)

def start_watching(watch_directory, log_directory):
    event_handler = Handler(log_directory)
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=False)
    observer.start()
    print(f"Watching '{watch_directory}' for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    forms_folder_path = r"C:\Users\FrancisChong.AzureAD\OneDrive - TrackOne\Supplier Request Forms"
    logs_folder_path = r"C:\Users\FrancisChong.AzureAD\OneDrive - TrackOne\Request Logs"
    start_watching(forms_folder_path, logs_folder_path)

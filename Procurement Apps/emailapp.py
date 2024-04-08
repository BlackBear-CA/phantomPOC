
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import re
import win32com.client as win32
import pythoncom

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Regex pattern to match "product_id_Purchasing Document_log.txt"
        pattern = re.compile(r'^(\d+)_(\d+)_log\.txt$')
        
        filename = os.path.basename(event.src_path)
        match = pattern.match(filename)
        
        if match:
            product_id, purchasing_document = match.groups()
            print(f'Matched log file: {filename} for Product ID: {product_id}, Purchasing Document: {purchasing_document}')
            self.send_email(event.src_path, product_id, purchasing_document)

    def send_email(self, file_path, product_id, purchasing_document):
        pythoncom.CoInitialize()
        
        try:
            # Reading and parsing the log file for specific details
            with open(file_path, 'r') as file:
                log_content = file.readlines()
            
            supplier_name = "Unknown Supplier"
            supplier_nos = "Unknown Supplier Nos"
            product_description = "Unknown Product Description"

            for line in log_content:
                if 'supplier name:' in line.lower():
                    supplier_name = line.split(':', 1)[1].strip()
                elif 'supplier_nos:' in line.lower():
                    supplier_nos = line.split(':', 1)[1].strip()
                elif 'product description:' in line.lower():
                    product_description = line.split(':', 1)[1].strip()

            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            
            sharepoint_base_url = "https://trackone-my.sharepoint.com/:f:/g/personal/francischong_trackone_onmicrosoft_com/ElVWap8G-dZKshdXU9Ce0uEBn7uB9KmyC3t1dGcLdVtdjA?e=4LUMAn"
            sharepoint_file_url = f"{sharepoint_base_url}/{os.path.basename(file_path)}"

            mail.Subject = f'Price Modification: {supplier_name} {supplier_nos}, Doc: {purchasing_document}'
            mail.To = 'chong.francisp@gmail.com'  # Update with the recipient's email address
            mail.HTMLBody = f"""\
            <html>
            <body>
            <p>A price modification request for "{supplier_name}" ("{supplier_nos}"), Purchasing Document {purchasing_document}, "{product_id}" and "{product_description}" has been logged and it requires your review and approval. You can access the details through the following SharePoint link:</p>
            <p><a href="{sharepoint_file_url}">Access Log File</a></p>
            <p>Best regards,</p>
            <p>System Administrator, Powered using PhantomAIP by Black Bear Technologies LLC, Nanaimo, British Columbia, Canada</p>
            </body>
            </html>
            """
            mail.Display()  # Display the email before sending for review
            # mail.Send()  # Uncomment to send automatically
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
        finally:
            pythoncom.CoUninitialize()

if __name__ == "__main__":
    watch_dir = r"C:\Users\FrancisChong.AzureAD\OneDrive - TrackOne\Request Logs"
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=False)
    observer.start()
    print(f'Watching for new log files in {watch_dir}...')

    try:
        while True:
            time.sleep(10)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

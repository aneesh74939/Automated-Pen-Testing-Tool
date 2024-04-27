import tkinter as tk
import subprocess


# Function to start the Burp Suite scan
def start_burp_scan():
    target_ip = target_entry.get()

    burpsuite_scan_command = f'/home/kali/BurpSuiteCommunity -crawl -scan -save -control http://{target_ip}:8080/'

    try:
        subprocess.Popen(burpsuite_scan_command, shell=True)
        result_label.config(text="Scan started successfully.")
    except Exception as e:
        result_label.config(text=f"Error starting scan: {str(e)}")


# Create the main application window
window = tk.Tk()
window.title("Burp Suite Scan GUI")

# Target IP input
target_label = tk.Label(window, text="Target IP Address:")
target_label.pack()
target_entry = tk.Entry(window)
target_entry.pack()

# Scan button
scan_button = tk.Button(window, text="Start Scan", command=start_burp_scan)
scan_button.pack()

# Result label
result_label = tk.Label(window, text="")
result_label.pack()

# Start the GUI main loop
window.mainloop()

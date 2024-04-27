import os
import sys
import tkinter as tk
import threading
import subprocess


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def quit_application():
    sys.exit()


# Define a lock for protecting the shared resource
output_text_lock = threading.Lock()


def scan_ports(target_host, start_port, end_port, output):
    try:
        nmap_command = f"nmap -p {start_port}-{end_port} {target_host}"
        nmap_output = subprocess.check_output(nmap_command, shell=True, text=True)

        # Acquire the lock before modifying the shared resource
        with output_text_lock:
            # Configure the Text widget to be in NORMAL state to insert text
            output.config(state=tk.NORMAL)
            output.insert(tk.END, nmap_output)
            output.update()  # This is the important line

        # Print the output in the console
        print(nmap_output)

    except subprocess.CalledProcessError as e:
        error_message = f"Error running Nmap: {e}\n"

        # Acquire the lock before modifying the shared resource
        with output_text_lock:
            output.config(state=tk.NORMAL)
            output.insert(tk.END, error_message)
            output.update()


def perform_scan(scan_type):
    target_host = target_ip_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())

    if scan_type == "open_ports":
        nmap_command = f"nmap -p {start_port}-{end_port} {target_host}"
    elif scan_type == "version_detection":
        nmap_command = f"nmap -sV -p {start_port}-{end_port} {target_host}"
    elif scan_type == "os_scan":
        nmap_command = f"nmap -O -p {start_port}-{end_port} {target_host}"
    else:
        print("Invalid scan type")
        return

    try:
        nmap_output = subprocess.check_output(nmap_command, shell=True, text=True)

        # Acquire the lock before modifying the shared resource
        with output_text_lock:
            # Configure the Text widget to be in NORMAL state to insert text
            output_text.config(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)  # Clear previous output
            output_text.insert(tk.END, nmap_output)
            output_text.update()  # This is the important line

        # Print the output in the console
        print(nmap_output)

    except subprocess.CalledProcessError as e:
        error_message = f"Error running Nmap: {e}\n"

        # Acquire the lock before modifying the shared resource
        with output_text_lock:
            output_text.config(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)  # Clear previous output
            output_text.insert(tk.END, error_message)
            output_text.update()


def run_vulnerability_scan():
    subprocess.Popen(["python", "vuln_scan.py"])


# Create the main window
window = tk.Tk()
window.geometry('620x660+200+200')
window.config(background='#e6ffe6')
window.title("Network Scanner")

# Port scanning section
scan_label = tk.Label(window, text="Port Scanning:")
scan_label.grid(row=7, column=0, padx=5, pady=5)
scan_label.config(bg='#e6ffe6')

target_ip_label = tk.Label(window, text="Enter target IP address:")
target_ip_label.config(bg='#e6ffe6')
target_ip_label.grid(row=8, column=0, padx=5, pady=5)
target_ip_entry = tk.Entry(window)
target_ip_entry.grid(row=8, column=1, padx=5, pady=5)

start_port_label = tk.Label(window, text="Start Port:")
start_port_label.config(bg='#e6ffe6')
start_port_label.grid(row=9, column=0, padx=5, pady=5)
start_port_entry = tk.Entry(window)
start_port_entry.grid(row=9, column=1, padx=5, pady=5)
start_port_entry.insert(0, "1")  # Default start port

end_port_label = tk.Label(window, text="End Port:")
end_port_label.config(bg='#e6ffe6')
end_port_label.grid(row=10, column=0, padx=5, pady=5)
end_port_entry = tk.Entry(window)
end_port_label.grid(row=10, column=0, padx=5, pady=5)
end_port_entry.grid(row=10, column=1, padx=5, pady=5)
end_port_entry.insert(0, "1024")  # Default end port

# Buttons for different scan types
scan_type_label = tk.Label(window, text="Select Scan Type:")
scan_type_label.config(bg='#e6ffe6')
scan_type_label.grid(row=11, column=0, padx=5, pady=5)

port_scan_button = tk.Button(window, text="Scan Open Ports", command=lambda: perform_scan("open_ports"))
port_scan_button.grid(row=11, column=1, padx=5, pady=5)
port_scan_button.config(bg='#4da6ff', fg="white", font=('Sans', '10', 'bold'))

version_scan_button = tk.Button(window, text="Service Version Detection",
                                command=lambda: perform_scan("version_detection"))
version_scan_button.grid(row=11, column=2, padx=5, pady=5)
version_scan_button.config(bg='#4da6ff', fg="white", font=('Sans', '10', 'bold'))

os_scan_button = tk.Button(window, text="OS Scan", command=lambda: perform_scan("os_scan"))
os_scan_button.grid(row=11, column=3, padx=5, pady=5)
os_scan_button.config(bg='#4da6ff', fg="white", font=('Sans', '10', 'bold'))

# Output text area
output_text = tk.Text(window, wrap=tk.WORD, height=10, width=60)
output_text.grid(row=12, column=0, columnspan=4, padx=5, pady=10)
output_text.config(bg='#FFFFFF')

vulnerability_scan_button = tk.Button(window, text="Vulnerability Scan", command=run_vulnerability_scan)
vulnerability_scan_button.grid(row=6, column=1, padx=5, pady=5)
vulnerability_scan_button.config(bg='#4da6ff', fg="white", font=('Sans', '10', 'bold'))

# Start the GUI main loop
window.mainloop()

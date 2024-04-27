import subprocess
import tkinter as tk


def on_submit():
    selected_option = choice_var.get()
    if selected_option == 1:
        subprocess.Popen(["python", "port_scan.py"])
        pass
    elif selected_option == 2:
        subprocess.Popen(["python", "vuln_scan.py"])
        pass
    elif selected_option == 3:
        subprocess.Popen(["python", "generate_payload.py"])
        pass


window = tk.Tk()
window.geometry('620x660+300+300')
window.config(background='#e6ffe6')
window.title("Choose an option")

# Heading Label
heading_label = tk.Label(window, text="Choose an option", font=('Sans', '16', 'bold'))
heading_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='w')
heading_label.config(bg='#e6ffe6')

# Create the payload options
label = tk.Label(window, text="Select an option:", font=('Sans', '12'))
label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='w')
label.config(bg='#e6ffe6')

choice_var = tk.IntVar()
choice_var.set(1)

radio1 = tk.Radiobutton(window, text="Port Scan", variable=choice_var, value=1, font=('Sans', '12'))
radio1.config(bg='#e6ffe6')
radio1.grid(row=2, column=0, padx=20, pady=5, sticky='w')

radio2 = tk.Radiobutton(window, text="Vulnerability Analysis", variable=choice_var, value=2, font=('Sans', '12'))
radio2.config(bg='#e6ffe6')
radio2.grid(row=3, column=0, padx=20, pady=5, sticky='w')

radio3 = tk.Radiobutton(window, text="Payload Generator", variable=choice_var, value=3, font=('Sans', '12'))
radio3.config(bg='#e6ffe6')
radio3.grid(row=4, column=0, padx=20, pady=5, sticky='w')

# Submit button
submit_button = tk.Button(window, text="Submit", command=on_submit, font=('Sans', '12', 'bold'))
submit_button.grid(row=5, column=0, padx=10, pady=20)

window.mainloop()

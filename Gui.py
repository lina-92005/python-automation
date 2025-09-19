# gui_automation_launcher
import PySimpleGUI as sg
import os

# ------------------------
# GUI THEME AND LAYOUT
# ------------------------
sg.theme("DarkTeal9")  # Modern and professional theme

# Custom fonts and colors
button_font = ("Helvetica", 12, "bold")
title_font = ("Helvetica", 16, "bold")
text_color = "#FFFFFF"  # White text

layout = [
    [sg.Text("🛠 Python Automation Launcher", font=title_font, text_color=text_color, justification='center', expand_x=True)],
    [sg.Text("Select a tool to run:", font=("Helvetica", 13), text_color=text_color, justification='center', expand_x=True)],
    [sg.Button("📧 Email Sender", size=(20, 2), font=button_font, button_color=("white", "#1F77B4"))],
    [sg.Button("🗣 Speech Tool", size=(20, 2), font=button_font, button_color=("white", "#FF7F0E"))],
    [sg.Button("⚙️ Extra Tool Placeholder", size=(20, 2), font=button_font, button_color=("white", "#2CA02C"))],
    [sg.HorizontalSeparator()],
    [sg.Button("❌ Exit", size=(20, 1), font=button_font, button_color=("white", "#D62728"))]
]

# ------------------------
# CREATE THE WINDOW
# ------------------------
window = sg.Window("Python Automation Tools", layout, size=(400, 350), element_justification='c', resizable=True)

# ------------------------
# EVENT LOOP
# ------------------------
while True:
    event, values = window.read()
    
    if event in (sg.WINDOW_CLOSED, "❌ Exit"):
        break
    
    elif event == "📧 Email Sender":
        os.system(r'python "C:\Users\LENOVO\Desktop\Python-Automation-20Days\email_sender.py"')# use the script path (it can be found in my github repository)
    
    elif event == "🗣 Speech Tool":
        os.system(r'python "C:\Users\LENOVO\Desktop\Python-Automation-20Days\speech_tools.py"')
    
    elif event == "⚙️ Extra Tool Placeholder":
        sg.popup("This is a placeholder for future tools!", font=("Helvetica", 12), text_color="#FFFFFF", background_color="#2CA02C")

# ------------------------
# CLOSE THE WINDOW
# ------------------------
window.close()

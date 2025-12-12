import os
import sys
import cv2
import glob 
import time
import tkinter as tk
from picamera2 import Picamera2, Preview

picam2 = Picamera2()

data_dir = "db/faces_data/"
name_of_person = ""       
text_widget = None        
status_label = None       
num_images = None
count_entry = None

placeholder_text = "Enter Name of Persin here"

def clear_placeholder(event):
    if text_widget.get() == placeholder_text:
        text_widget.delete(0, "end")
        text_widget.config(fg="black")

def add_placeholder(event):
    if not text_widget.get():
        text_widget.insert(0, placeholder_text)
        text_widget.config(fg="grey")

def submit(event=None):
    global name_of_person
    global num_images
    value = text_widget.get()
    # handling empty placeholder
    if value == placeholder_text:
        value = ""
    # name_of_person = value
    name_of_person = str.capitalize(value)
    try:
        num_images = int(count_entry.get())
        if num_images < 1:
            num_images = 0
    except Exception as e:
        print(e)
        num_images = 0

    # global name for reuse
    print("Updated of peprson =", name_of_person)
    if status_label is not None:
        shown = name_of_person if name_of_person else "(empty)"
        qty = num_images if (isinstance(num_images, int) and num_images > 0) else "(default)"
        status_label.config(text=f"Received: {shown}, Number_of_Imagese: {qty}")
    text_widget.delete(0, tk.END)

    window.destroy()

window = tk.Tk()
window.title("Enter Name of Person to capture")

os.makedirs(data_dir, exist_ok=True)

tk.Label(window, text="Data of faces:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))

# Cutrent database of faces
names_frame = tk.Frame(window)
names_frame.pack(fill="x", padx=10)
for name in sorted(os.listdir(data_dir)):
    tk.Label(names_frame, text=f"• {name}").pack(anchor="w")

entry_frame = tk.Frame(window)
entry_frame.pack(padx=10, pady=10, fill="x")

tk.Label(entry_frame, text="New Person:").pack(anchor="w")
tk.Label(window, text="Number of IMages").pack(anchor="w")

text_widget = tk.Entry(entry_frame, width=30)
text_widget.pack(anchor="w", pady=(4, 6))
# img num
count_entry = tk.Entry(entry_frame, width=10)
count_entry.pack(anchor="w", pady=(0, 6))
count_entry.insert(0, "100")

text_widget.insert(0, placeholder_text)
text_widget.config(fg="grey")
text_widget.bind("<FocusIn>", clear_placeholder)
text_widget.bind("<FocusOut>", add_placeholder)

btn = tk.Button(entry_frame, text="Submit", command=submit)
btn.pack(anchor="w")

window.bind("<Return>", submit)

status_label = tk.Label(window, text="Saved: (none yet)")
status_label.pack(anchor="w", padx=10, pady=(0, 10))

window.geometry("600x400")
window.resizable(True, True)

print("Name of Person Entered (before GUI) =", name_of_person)

# tkinter guui
window.mainloop()

print("Name of Person Entered (after GUI) =", name_of_person)

# Logic for Capturing faces from the Rpi cameraa

# 1. how many pcis to take
# 2. save to data folder of entered name
# 3. file name incremental

number_of_pics  = 100
if isinstance(num_images, int) and num_images > 0:
    number_of_pics = num_images

# camera_config = picam2.create_still_configuration(main={"size": (640, 480)}, display="lores")
camera_config = picam2.create_still_configuration(main={"size": (640, 480)})

picam2.configure(camera_config)

picam2.start()
time.sleep(2)


fil = "Dvi.jpg"
filename = f"{data_dir}{name_of_person}"
filaa = data_dir + name_of_person + fil
# picam2.capture_file(filaa)
# picam2.capture_file(filename + "/DD.jpg")
person_dir = os.path.join(data_dir, name_of_person)
os.makedirs(person_dir, exist_ok=True)

existing_img = [f for f in os.listdir(person_dir) if f.startswith(name_of_person) 
                and f.endswith(".jpg")]

if existing_img:
    numbers = []
    for f in existing_img:
        try: 
            num = int(f.split("_")[-1].split(".")[0])
            numbers.append(num)
        except ValueError:
            pass

    start_index = max(numbers) + 1 if numbers else 0

else:
    start_index = 0

for i in range(number_of_pics):
    outfile = os.path.join(person_dir, f"{name_of_person}_{start_index + i:03d}.jpg")
    picam2.capture_file(outfile)
    time.sleep(0.1)


# out_img = os.path.join(person_dir, fil)
# picam2.capture_file(out_img)
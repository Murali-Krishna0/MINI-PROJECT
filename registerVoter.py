import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import dframe as df

def registerVoter(root, frame1):
    # Clear existing widgets
    for widget in frame1.winfo_children():
        widget.destroy()

    # Set background image
    try:
        bg_image = Image.open("img/bg.png")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background image error: {e}")
        frame1.config(bg='lightgray')

    # Screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Define laptop screen boundaries (focused on display area only)
    laptop_top = screen_height * 0.18    # Top of laptop display area
    laptop_bottom = screen_height * 0.65  # Bottom of laptop display area (above keyboard)
    laptop_center_x = screen_width // 2

    # Navigation buttons (outside laptop screen area)
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'),
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=2,
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    admin_btn = Button(frame1, text="👨‍💼 Admin", font=('Helvetica', 12, 'bold'),
                      command=lambda: __import__('Admin').AdminHome(root, frame1, Frame(root)),
                      bg='lightgreen', fg='black', relief='raised', bd=2,
                      width=10, height=1, cursor='hand2')
    admin_btn.place(x=140, y=20)

    # Title positioned at top of laptop display area
    Label(frame1, text="Register Voter", font=('Helvetica', 20, 'bold'),
          bg='black', fg='white').place(x=laptop_center_x, y=laptop_top + 20, anchor='center')

    # Form positioned higher up in laptop display area
    form_start_y = laptop_top + 60
    label_x = laptop_center_x - 100
    entry_x = laptop_center_x + 20
    spacing = 40

    # Labels
    Label(frame1, text="Name:", font=('Helvetica', 12, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y, anchor='e')
    Label(frame1, text="Sex:", font=('Helvetica', 12, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y + spacing, anchor='e')
    Label(frame1, text="Zone:", font=('Helvetica', 12, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y + spacing*2, anchor='e')
    Label(frame1, text="City:", font=('Helvetica', 12, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y + spacing*3, anchor='e')
    Label(frame1, text="Password:", font=('Helvetica', 12, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y + spacing*4, anchor='e')

    # Entry fields
    name_entry = Entry(frame1, font=('Helvetica', 11), relief='sunken', bd=2, width=18)
    name_entry.place(x=entry_x, y=form_start_y, anchor='w')

    sex_var = StringVar()
    sex_combo = ttk.Combobox(frame1, textvariable=sex_var, font=('Helvetica', 11), 
                            values=["Male", "Female", "Other"], state="readonly", width=16)
    sex_combo.place(x=entry_x, y=form_start_y + spacing, anchor='w')
    sex_combo.set("Select Sex")

    zone_entry = Entry(frame1, font=('Helvetica', 11), relief='sunken', bd=2, width=18)
    zone_entry.place(x=entry_x, y=form_start_y + spacing*2, anchor='w')

    city_entry = Entry(frame1, font=('Helvetica', 11), relief='sunken', bd=2, width=18)
    city_entry.place(x=entry_x, y=form_start_y + spacing*3, anchor='w')

    password_entry = Entry(frame1, font=('Helvetica', 11), relief='sunken', bd=2, show="*", width=18)
    password_entry.place(x=entry_x, y=form_start_y + spacing*4, anchor='w')

    # Register button function
    def register():
        name_val = name_entry.get().strip()
        sex_val = sex_var.get()
        zone_val = zone_entry.get().strip()
        city_val = city_entry.get().strip()
        password_val = password_entry.get().strip()

        # Validation
        if not name_val:
            show_message("Please enter Name!", "red")
            return
        if sex_val == "Select Sex" or not sex_val:
            show_message("Please select Sex!", "red")
            return
        if not zone_val:
            show_message("Please enter Zone!", "red")
            return
        if not city_val:
            show_message("Please enter City!", "red")
            return
        if not password_val:
            show_message("Please enter Password!", "red")
            return

        try:
            # Call the database function
            voter_id = df.taking_data_voter(name_val, sex_val, zone_val, city_val, password_val)
            
            if voter_id and voter_id > 0:
                # SUCCESS - Redirect to success page
                show_success_page(voter_id)
            else:
                show_message("Registration Failed! Please try again.", "red")
                
        except Exception as e:
            error_msg = f"Registration Error: {str(e)}"
            show_message(error_msg, "red")

    def show_success_page(voter_id):
        """Show the success page strictly within laptop display area"""
        # Clear current frame
        for widget in frame1.winfo_children():
            widget.destroy()

        # Set background image for success page
        try:
            bg_image = Image.open("img/bg.png")
            bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(frame1, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Background image error: {e}")
            frame1.config(bg='lightgray')

        # Navigation buttons (outside laptop screen area)
        home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'),
                         command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                         bg='lightblue', fg='black', relief='raised', bd=2,
                         width=10, height=1, cursor='hand2')
        home_btn.place(x=20, y=20)

        admin_btn = Button(frame1, text="👨‍💼 Admin", font=('Helvetica', 12, 'bold'),
                          command=lambda: __import__('Admin').AdminHome(root, frame1, Frame(root)),
                          bg='lightgreen', fg='black', relief='raised', bd=2,
                          width=10, height=1, cursor='hand2')
        admin_btn.place(x=140, y=20)

        # Success content positioned strictly within laptop DISPLAY area (above keyboard)
        laptop_top = screen_height * 0.18
        laptop_bottom = screen_height * 0.65  # Stop before keyboard area
        laptop_center_x = screen_width // 2

        # Success message - moved higher up
        Label(frame1, text="✅ Voter Registered Successfully!", 
              font=('Helvetica', 16, 'bold'), bg='black', fg='white'
              ).place(x=laptop_center_x, y=laptop_top + 40, anchor='center')
        
        # Voter ID label
        Label(frame1, text="Voter ID:", 
              font=('Helvetica', 14, 'bold'), bg='black', fg='white'
              ).place(x=laptop_center_x, y=laptop_top + 80, anchor='center')
        
        # Voter ID in highlighted display
        Label(frame1, text=str(voter_id), 
              font=('Helvetica', 18, 'bold'), bg='#f39c12', fg='white',
              relief='raised', bd=3, padx=15, pady=8
              ).place(x=laptop_center_x, y=laptop_top + 120, anchor='center')
        
        # Instruction text
        Label(frame1, text="Please save your Voter ID for future reference!", 
              font=('Helvetica', 11), bg='black', fg='lightgray'
              ).place(x=laptop_center_x, y=laptop_top + 160, anchor='center')

        # Buttons positioned within DISPLAY area (not on keyboard)
        Button(frame1, text="Register Another Voter", font=('Helvetica', 11, 'bold'),
              command=lambda: registerVoter(root, frame1), bg='#3498db', fg='white',
              width=16, height=1, relief='raised', bd=2, cursor='hand2'
              ).place(x=laptop_center_x, y=laptop_top + 210, anchor='center')
        
        Button(frame1, text="Back to Admin", font=('Helvetica', 11, 'bold'),
              command=lambda: __import__('Admin').AdminHome(root, frame1, Frame(root)),
              bg='#2ecc71', fg='white', width=16, height=1, 
              relief='raised', bd=2, cursor='hand2'
              ).place(x=laptop_center_x, y=laptop_top + 250, anchor='center')

        frame1.pack(fill=BOTH, expand=True)

    def show_message(text, color):
        # Remove existing messages
        for widget in frame1.winfo_children():
            if isinstance(widget, Label) and widget.winfo_y() > form_start_y + spacing*5:
                widget.destroy()
        
        # Create new message within laptop display area
        msg_y = form_start_y + spacing*5 + 20
        msg = Label(frame1, text=text, font=('Helvetica', 11, 'bold'), 
                   bg=color, fg='white', relief='raised', bd=2, padx=10, pady=5)
        msg.place(x=laptop_center_x, y=msg_y, anchor='center')
        
        # Auto-remove after 5 seconds
        frame1.after(5000, msg.destroy)

    # Register button positioned within laptop DISPLAY area
    register_btn_y = form_start_y + spacing*5
    register_btn = Button(frame1, text="Register Voter", font=('Helvetica', 12, 'bold'),
                         command=register, bg='#e74c3c', fg='white', 
                         width=14, height=1, relief='raised', bd=3, cursor='hand2')
    register_btn.place(x=laptop_center_x, y=register_btn_y, anchor='center')

    # Add Enter key binding
    def on_enter(event):
        register()

    # Bind Enter key to all entry fields
    name_entry.bind('<Return>', on_enter)
    sex_combo.bind('<Return>', on_enter)
    zone_entry.bind('<Return>', on_enter)
    city_entry.bind('<Return>', on_enter)
    password_entry.bind('<Return>', on_enter)

    # Focus on first field
    name_entry.focus()

    frame1.pack(fill=BOTH, expand=True)

# For direct testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Voter Registration")
    root.state('zoomed')
    
    frame1 = Frame(root)
    registerVoter(root, frame1)
    root.mainloop()
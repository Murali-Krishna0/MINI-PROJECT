import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import socket

def voteCast(root, frame1, vote, client_socket):
    for widget in frame1.winfo_children():
        widget.destroy()

    # Set background image - ADD YOUR IMAGE PATH HERE
    try:
        bg_image = Image.open("img/cast.png")  # ← CHANGE THIS PATH
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background image error: {e}")
        # Fallback background color if image fails
        frame1.config(bg='lightgreen')

    # Center position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    laptop_center_x = screen_width // 2
    laptop_center_y = screen_height // 2

    # Home button
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'),
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=2,
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    # Send vote to server
    client_socket.send(vote.encode())
    message = client_socket.recv(1024).decode()
    print(message)

    # Vote response with better styling for the background
    if message == "Successful":
        # Success message with WHITE TEXT
        success_frame = Frame(frame1, bg='black', bd=3, relief='raised')
        success_frame.place(x=laptop_center_x, y=laptop_center_y - 50, anchor='center')
        
        Label(success_frame, text="✅ Vote Casted Successfully!",
              font=('Helvetica', 22, 'bold'), bg='black', fg='white',  # CHANGED fg='green' to fg='white'
              padx=20, pady=10).pack()
    else:
        # Error message with contrasting background
        error_frame = Frame(frame1, bg='black', bd=3, relief='raised')
        error_frame.place(x=laptop_center_x, y=laptop_center_y - 50, anchor='center')
        
        Label(error_frame, text="❌ Vote Cast Failed\nPlease Try Again",
              font=('Helvetica', 22, 'bold'), bg='black', fg='red',
              padx=20, pady=10).pack()

    # Back button
    def back_to_home():
        from homePage import Home
        for widget in frame1.winfo_children():
            widget.destroy()
        frame2 = Frame(root)
        Home(root, frame1, frame2)

    back_btn = Button(frame1, text="Back to Home", width=14, height=1,
                     font=('Helvetica', 14, 'bold'), bg='#2196F3', fg='white',
                     relief='raised', bd=3, cursor='hand2', command=back_to_home)
    back_btn.place(x=laptop_center_x, y=laptop_center_y + 50, anchor='center')

    client_socket.close()
    frame1.pack(fill=BOTH, expand=True)
    root.mainloop()


def votingPg(root, frame1, client_socket):
    root.title("Cast Your Vote")
    for widget in frame1.winfo_children():
        widget.destroy()

    # Laptop background
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

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    laptop_center_x = screen_width // 2

    # 🧩 Adjust vertical placement slightly upward to fit perfectly
    screen_top = screen_height * 0.14   # moved up (was 0.20)
    screen_bottom = screen_height * 0.68  # moved up (was 0.73)
    available_height = screen_bottom - screen_top
    start_y = screen_top + (available_height * 0.05)

    # Home button
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'),
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=2,
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    # Title (within laptop screen)
    Label(frame1, text="🗳️ Cast Your Vote", font=('Helvetica', 22, 'bold'),
          bg='black', fg='white').place(x=laptop_center_x, y=start_y, anchor='center')

    # Party details
    parties = [
        ("BJP", "Narendra Modi", "img/bjp.png", "bjp"),
        ("Congress", "Rahul Gandhi", "img/cong.jpg", "cong"),
        ("DMK", "M. K. Stalin", "img/dmk.jpg", "dmk"),
        ("ADMK", "Edappadi K. Palaniswami", "img/admk.jpg", "admk"),
        ("TVK", "Vijay", "img/tvk.jpg", "tvk"),
        ("NOTA", "None of the Above", "img/nota.jpg", "nota")
    ]

    y_gap = 47  # Compact spacing
    y_pos = start_y + 60
    logo_size = (42, 42)
    vote = StringVar(frame1, "-1")

    # Buttons and logos
    for party, leader, img_path, value in parties:
        try:
            logo_img = Image.open(img_path).resize(logo_size, Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = Label(frame1, image=logo_photo, bg='black')
            logo_label.image = logo_photo
            logo_label.place(x=laptop_center_x - 120, y=y_pos, anchor='center')
        except:
            Label(frame1, text=party, font=('Helvetica', 8, 'bold'),
                  bg='black', fg='white').place(x=laptop_center_x - 120, y=y_pos, anchor='center')

        Radiobutton(frame1, text=f"{party} - {leader}", variable=vote, value=value,
                    indicator=0, height=1, width=28, font=('Helvetica', 10, 'bold'),
                    bg='black', fg='white', selectcolor='darkblue', cursor='hand2',
                    command=lambda v=value: voteCast(root, frame1, v, client_socket)
                    ).place(x=laptop_center_x + 65, y=y_pos, anchor='center')
        y_pos += y_gap

    frame1.pack(fill=BOTH, expand=True)
    root.mainloop()

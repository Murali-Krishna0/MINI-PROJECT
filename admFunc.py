import tkinter as tk
import dframe as df
from tkinter import *
from dframe import *
from PIL import ImageTk, Image


# ------------------- RESET ALL FUNCTION -------------------
def resetAll(root, frame1):
    for widget in frame1.winfo_children():
        widget.destroy()

    # === Background Setup ===
    try:
        bg_image = Image.open("img/bg.png")
        bg_image = bg_image.resize(
            (root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background image error: {e}")
        frame1.config(bg='lightgray')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Position centered above laptop
    laptop_center_x = screen_width // 2
    laptop_center_y = screen_height // 2 - 100

    # === Navigation Buttons ===
    Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'),
           command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
           bg='lightblue', fg='black', width=10, height=1, cursor='hand2').place(x=20, y=20)

    Button(frame1, text="👨‍💼 Admin", font=('Helvetica', 12, 'bold'),
           command=lambda: __import__('Admin').AdminHome(root, frame1, Frame(root)),
           bg='lightgreen', fg='black', width=10, height=1, cursor='hand2').place(x=140, y=20)

    Label(frame1, text="Reset Complete", font=('Helvetica', 16, 'bold'),
          bg='black', fg='green').place(x=laptop_center_x, y=laptop_center_y, anchor='center')

    def go_back():
        for widget in frame1.winfo_children():
            widget.destroy()
        from Admin import AdminHome
        frame3 = root.winfo_children()[1]
        AdminHome(root, frame1, frame3)

    Button(frame1, text="Back to Admin", width=12, height=1, font=('Helvetica', 14, 'bold'),
           command=go_back, bg='#2196F3', fg='white', cursor='hand2').place(
               x=laptop_center_x, y=laptop_center_y + 60, anchor='center')

    frame1.pack(fill=BOTH, expand=True)
    root.mainloop()


# ------------------- SHOW VOTES FUNCTION -------------------
def showVotes(root, frame1):
    result = df.show_result()
    root.title("Vote Count")

    for widget in frame1.winfo_children():
        widget.destroy()

    # === Background ===
    try:
        bg_image = Image.open("img/bg.png")
        bg_image = bg_image.resize(
            (root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background image error: {e}")
        frame1.config(bg='lightgray')

    # === Screen size ===
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # === Position for laptop screen area - RAISED HIGHER ===
    laptop_center_x = screen_width // 2
    screen_area_top = screen_height * 0.18  # Raised from 0.20
    screen_area_bottom = screen_height * 0.58  # Raised from 0.60

    # === Top Buttons ===
    Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'),
           command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
           bg='lightblue', fg='black', width=10, cursor='hand2').place(x=20, y=20)

    Button(frame1, text="👨‍💼 Admin", font=('Helvetica', 12, 'bold'),
           command=lambda: __import__('Admin').AdminHome(root, frame1, Frame(root)),
           bg='lightgreen', fg='black', width=10, cursor='hand2').place(x=140, y=20)

    # === Calculate form start position ===
    available_height = screen_area_bottom - screen_area_top
    form_start_y = screen_area_top + (available_height * 0.1)

    # === Title ===
    Label(
        frame1,
        text="Vote Count",
        font=('Helvetica', 20, 'bold'),
        bg="black",
        fg="white"
    ).place(x=laptop_center_x, y=form_start_y, anchor='center')

    # === Party Data ===
    parties = [
        ("BJP", "img/bjp.png", "bjp"),
        ("Congress", "img/cong.jpg", "cong"),
        ("DMK", "img/dmk.jpg", "dmk"),
        ("ADMK", "img/admk.jpg", "admk"),
        ("TVK", "img/tvk.jpg", "tvk"),
        ("NOTA", "img/nota.jpg", "nota")
    ]

    # Start position for parties list - RAISED HIGHER
    row_y = form_start_y + 30  # Reduced from 35

    for party, img_path, key in parties:
        try:
            logo = Image.open(img_path).resize((30, 30), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(logo)
            logo_label = Label(frame1, image=logo_img, bg="black")
            logo_label.image = logo_img
            logo_label.place(x=laptop_center_x - 130, y=row_y)
        except Exception as e:
            print(f"Image error for {party}: {e}")
            Label(frame1, text="[IMG]", bg="black", fg="white", font=('Helvetica', 8)).place(x=laptop_center_x - 130, y=row_y)

        # Party name
        Label(frame1, text=f"{party}:", font=('Helvetica', 12, 'bold'),
              bg="black", fg='white').place(x=laptop_center_x - 90, y=row_y + 2)

        # Vote count
        Label(frame1, text=str(result.get(key, 0)), font=('Helvetica', 12, 'bold'),
              bg='yellow', fg='black', width=4).place(x=laptop_center_x + 30, y=row_y + 2)

        row_y += 40

    frame1.pack(fill=BOTH, expand=True)
    root.mainloop()
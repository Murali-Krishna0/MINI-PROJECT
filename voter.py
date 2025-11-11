import tkinter as tk
import socket
from tkinter import *
from VotingPage import votingPg
from PIL import Image, ImageTk

def establish_connection():
    try:
        host = socket.gethostname()
        port = 4001
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)  # 5 second timeout
        client_socket.connect((host, port))
        print(f"Connected to server: {client_socket}")
        message = client_socket.recv(1024)
        if message.decode() == "Connection Established":
            return client_socket
        else:
            print("Server connection failed")
            return 'Failed'
    except Exception as e:
        print(f"Connection error: {e}")
        return 'Failed'

def failed_return(root, frame1, client_socket, message):
    for widget in frame1.winfo_children():
        widget.destroy()
    
    # Set background
    try:
        bg_image = Image.open("img/bg.png")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        frame1.config(bg='lightgray')
    
    # Screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Define laptop screen boundaries
    laptop_top = screen_height * 0.18
    laptop_bottom = screen_height * 0.65
    laptop_center_x = screen_width // 2
    laptop_center_y = (laptop_top + laptop_bottom) // 2

    # Navigation buttons
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'),
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=3, cursor='hand2')
    home_btn.place(x=20, y=20)

    # Error message within laptop screen
    message = message + "... \nTry again..."
    Label(frame1, text=message, font=('Helvetica', 18, 'bold'), bg='black', fg='red'
          ).place(x=laptop_center_x, y=laptop_center_y - 50, anchor='center')
    
    # Back button within laptop screen
    back_btn = Button(frame1, text="Back to Login", font=('Helvetica', 14, 'bold'),
                     command=lambda: voterLogin(root, frame1),
                     bg='#2196F3', fg='white', relief='raised', bd=3, cursor='hand2',
                     width=15, height=1)
    back_btn.place(x=laptop_center_x, y=laptop_center_y + 30, anchor='center')
    
    if client_socket != 'Failed':
        client_socket.close()

def log_server(root, frame1, client_socket, voter_ID, password):
    try:
        message = voter_ID + " " + password
        client_socket.send(message.encode()) #2

        message = client_socket.recv(1024) #Authentication message
        message = message.decode()
        print(f"Authentication response: {message}")

        if message == "Authenticate":
            votingPg(root, frame1, client_socket)
        elif message == "VoteCasted":
            message = "Vote has Already been Cast"
            failed_return(root, frame1, client_socket, message)
        elif message == "InvalidVoter":
            message = "Invalid Voter ID or Password"
            failed_return(root, frame1, client_socket, message)
        else:
            message = "Server Error - Please try again"
            failed_return(root, frame1, client_socket, message)

    except Exception as e:
        print(f"Error in log_server: {e}")
        failed_return(root, frame1, client_socket, "Connection Error")

def voterLogin(root, frame1):
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

    # Home button
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'),
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=2, 
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    # Screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Define laptop screen boundaries
    laptop_top = screen_height * 0.18
    laptop_bottom = screen_height * 0.65
    laptop_center_x = screen_width // 2
    laptop_center_y = (laptop_top + laptop_bottom) // 2

    # Title within laptop screen
    Label(frame1, text="Voter Login", font=('Helvetica', 30, 'bold'), 
          bg='black', fg='white').place(x=laptop_center_x, y=laptop_top + 40, anchor='center')

    # Labels and entries within laptop screen
    form_start_y = laptop_top + 100
    label_x = laptop_center_x - 120
    entry_x = laptop_center_x + 30
    spacing = 60

    Label(frame1, text="Voter ID:", font=('Helvetica', 16, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y, anchor='e')
    Label(frame1, text="Password:", font=('Helvetica', 16, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y + spacing, anchor='e')

    voter_ID = tk.StringVar()
    password = tk.StringVar()

    e1 = Entry(frame1, textvariable=voter_ID, font=('Helvetica', 14), width=18, bd=2, relief='sunken')
    e1.place(x=entry_x, y=form_start_y, anchor='w')
    
    e3 = Entry(frame1, textvariable=password, show='*', font=('Helvetica', 14), width=18, bd=2, relief='sunken')
    e3.place(x=entry_x, y=form_start_y + spacing, anchor='w')

    def perform_voter_login():
        # First establish connection
        client_socket = establish_connection()
        if client_socket == 'Failed':
            failed_return(root, frame1, client_socket, "Server Connection Failed")
        else:
            log_server(root, frame1, client_socket, voter_ID.get(), password.get())

    # Login button within laptop screen
    sub = Button(frame1, text="Login", width=12, height=1, font=('Helvetica', 16, 'bold'),
                command=perform_voter_login, bg='#4CAF50', fg='white', relief='raised', bd=3, cursor='hand2')
    sub.place(x=laptop_center_x, y=form_start_y + spacing*2, anchor='center')

    # Enter key binding
    def on_enter(event):
        perform_voter_login()

    root.bind('<Return>', on_enter)
    e1.bind('<Return>', on_enter)
    e3.bind('<Return>', on_enter)

    frame1.pack(fill=BOTH, expand=True)

# if __name__ == "__main__":
#     root = Tk()
#     root.geometry('500x500')
#     frame1 = Frame(root)
#     voterLogin(root, frame1)
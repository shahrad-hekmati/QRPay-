import os
import sys
from pyzbar.pyzbar import decode
import qrcode
from PIL import Image, ImageTk
import PIL.Image
import cv2
from tkinter import *
from tkinter import ttk
from tkinter import Label
import pandas as pd

# Set the background and foreground colors
bg_color = '#241571'  # Berry
fg_color = '#63C5DA'  # Sky

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__ if "__file__" in locals() else os.getcwd()))

# Define the path to the bank CSV file
bank_csv_path = os.path.join(current_dir, "bank.csv")

df = pd.read_csv(bank_csv_path)
names = df['id'].tolist()

product_prices = {
    "Coca Cola": 9.00,
    "Fanta": 8.00,
    "Pepsi": 10.00,
}

total_price = 0.0

class QRPaymentApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # Set the main window to fullscreen
        self.root.configure(bg=bg_color)
        self.payee = ''
        self.main_window_destroyed = False  # Flag to track if the main window is destroyed
        self.cap = None  # Initialize cap as None
        self.account_balance_label = None
        self.error_label = None
        self.front_page = None  # Store a reference to the front page window
        self.payment_page = None  # Store a reference to the payment page window
        self.product_selection_page = None  # Store a reference to the product selection page
        self.show_qrcode_page = None  # Store a reference to the "Show QRCode" page
        self.qr_code_image_label = None
        self.names = names
        self.confirmation_label = None
        
        self.total_price_label = Label(self.product_selection_page, text=f"", font=("Helvetica", 12, "bold"), bg=bg_color, fg=fg_color)
        self.total_price_label.pack(pady=20)
        self.total_price = 0.0
        self.df = df 

        # Initialize quantity_comboboxes as an empty dictionary
        self.quantity_comboboxes = {}
        self.dropdown_values_changed = False  # Initialize dropdown values change status

        welcome_label = Label(self.root, text="Welcome to QRcode pay program", font=("Helvetica", 24, "bold"), bg=bg_color, fg=fg_color)
        welcome_label.pack(pady=20)

        user_management_image = PIL.Image.open(os.path.join(current_dir, "assets", "user_ui.png"))
        user_management_image = ImageTk.PhotoImage(user_management_image)
        self.user_management_btn = Button(self.root, image=user_management_image, border=0, command=self.open_user_management)
        self.user_management_btn.image = user_management_image
        self.user_management_btn.place(x=900, y=200)

        user_management_label = Label(self.root, text="User Management", font=("Helvetica", 14, "bold"), bg=bg_color, fg='#0dd354')
        user_management_label.place(x=970, y=480)

        self.frontpage_paybtnimg = PhotoImage(file=os.path.join(current_dir, "assets", "pay.png"))
        self.paybtn = Button(self.root, image=self.frontpage_paybtnimg, command=self.open_product_selection, border=0)  # Open product selection directly
        self.paybtn.image = self.frontpage_paybtnimg
        self.paybtn.place(x=400, y=200)

        webcam_label = Label(self.root, text="Buy", font=("Helvetica", 14, "bold"), bg=bg_color, fg='#0dd354')
        webcam_label.place(x=525, y=480)
        
        self.message_label = Label(self.root, text="", font=("Helvetica", 14), bg=bg_color)
        self.message_label.pack()
        
        exit_button = Button(self.front_page, text="Exit", font=("Helvetica", 14, "bold"), bg="red", fg="white", command=self.exit_program)
        exit_button.place(x=750, y=800)

    def exit_program(self):
        self.root.destroy()  # Close the main window
        sys.exit()
    
    def check(self):
        self.video = cv2.VideoCapture(0)
        self.cap = True
        self.payfun()

    def payfun(self):
        while self.cap:
            check, frame = self.video.read()
            d = decode(frame)
            for obj in d:
                name = d[0].data.decode()

                # Convert the QR code value to an integer
                qr_code_value = int(name)

                # Print the current QR code's value for debugging
                print("Current QR code's value:", qr_code_value)

                # Debug: Print the list of IDs for comparison
                print("List of IDs from bank.csv:", self.names)

                # Check if the QR code's value is in the list of IDs
                if qr_code_value in self.names:
                    print(f"'{qr_code_value}' is in the list of IDs in bank.csv")
                    self.payee = qr_code_value
                    self.video.release()
                    cv2.destroyAllWindows()
                    self.cap = False
                    self.open_payment_page(self.payee)
                else:
                    print(f"'{qr_code_value}' is not in the list of IDs in bank.csv")

            cv2.imshow("QRcode payment", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        self.video.release()
        cv2.destroyAllWindows()


    def open_product_selection(self):
        if not self.main_window_destroyed:  # Check if the main window still exists
            if self.product_selection_page is not None:
                self.product_selection_page.destroy()  # Close the product selection page if it's open

            self.product_selection_page = Toplevel(self.root)
            self.product_selection_page.attributes('-fullscreen', True)  # Set the product selection page to fullscreen
            self.product_selection_page.configure(bg=bg_color)

            # Initialize the total price variable
            self.total_price = 0.0

            self.total_price_label = Label(self.product_selection_page, text=f"Total Price: $0.00", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            self.total_price_label.pack(pady=20)

            products_info = {
                "Coca Cola": {"price": "$9.00", "image_path": "Coca-Cola.png"},
                "Fanta": {"price": "$8.00", "image_path": "Fanta.png"},
                "Pepsi": {"price": "$10.00", "image_path": "Pepsi.png"},
            }

            x_coord = 150  # Set the initial x coordinate
            button_size = 300  # Button image size

            # Dictionary to store Combobox (dropdown) widgets
            self.quantity_comboboxes = {}

            def update_total_price():
                # Reset the total price to zero before recalculating
                self.total_price = 0.0
                for product_name, combobox in self.quantity_comboboxes.items():
                    quantity = int(combobox.get())
                    self.total_price += quantity * product_prices[product_name]
                self.total_price_label.config(text=f"Total Price: ${self.total_price:.2f}")

                # Check if the dropdown values have changed
                if any(int(combobox.get()) > 0 for combobox in self.quantity_comboboxes.values()):
                    self.dropdown_values_changed = True
                else:
                    self.dropdown_values_changed = False

                # Update the state of the "Finalize Payment" button
                if self.dropdown_values_changed:
                    self.finalize_pay_button.config(state=NORMAL)
                else:
                    self.finalize_pay_button.config(state=DISABLED)

            for product_name, info in products_info.items():
                image = PhotoImage(file=os.path.join(current_dir, "products", info["image_path"]))
                button = Button(self.product_selection_page, image=image, command=lambda name=product_name: self.select_product(name))
                image.image = image
                button.place(x=x_coord, y=200)  # Set the x coordinate to 150 and y to 200

                label = Label(self.product_selection_page, text=product_name, font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
                label.place(x=x_coord, y=200 + button_size + 5)  # Place the name label slightly below the button

                price_label = Label(self.product_selection_page, text=f"Price: {info['price']}", font=("Helvetica", 12, "bold"), bg=bg_color, fg=fg_color)
                price_label.place(x=x_coord, y=200 + button_size + 30)  # Place the price label further below the button

                # Create a Combobox (dropdown) with numbers from 0 to 10
                quantity_combobox = ttk.Combobox(self.product_selection_page, values=list(range(11)), state="readonly")
                quantity_combobox.set("0")  # Set the default value to 0
                quantity_combobox.place(x=x_coord, y=200 + button_size + 60)  # Place the dropdown below the price label
                quantity_combobox.config(font=("Helvetica", 12))
                # Store the Combobox in the dictionary
                self.quantity_comboboxes[product_name] = quantity_combobox

                x_coord += (button_size + 150)  # Increase the x coordinate for the next button

            # Create the "Calculate Price" button
            calculate_price_button = Button(self.product_selection_page, text="Calculate Price", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=update_total_price)
            calculate_price_button.place(x=695, y=60)

            # Create the "Finalize Payment" button, initially deactivated
            self.finalize_pay_button = Button(self.product_selection_page, text="Finalize Payment", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, state=DISABLED, command=self.read_qr_and_finalize_payment)
            self.finalize_pay_button.place(x=686, y=119)

            # Create the "Back" button
            back_button = Button(self.product_selection_page, text="Back", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=self.close_product_selection)
            back_button.place(x=695, y=800)

    def close_product_selection(self):
        if self.product_selection_page:
            self.product_selection_page.destroy()

    def select_product(self, product_name):
        products_info = {
            "Coca Cola": "$9.00",
            "Fanta": "$8.00",
            "Pepsi": "$10.00",
        }

        quantity_combobox = self.quantity_comboboxes.get(product_name)
        if quantity_combobox:
            if quantity_combobox.get() == "0":
                quantity_combobox["state"] = "readonly"
            else:
                quantity_combobox["state"] = "normal"

                def on_combobox_select(event):
                    selected_value = quantity_combobox.get()
                    if selected_value == "0":
                        quantity_combobox["state"] = "readonly"
                    else:
                        quantity_combobox["state"] = "normal"

                # Bind the event handler to the Combobox selection
                quantity_combobox.bind("<<ComboboxSelected>>", on_combobox_select)

    def read_qr_and_finalize_payment(self):
        if not self.cap:
            self.cap = True
            self.check()  # Open the webcam to read the QR code

    def open_payment_page(self, user_id):
        if user_id and not self.main_window_destroyed:
            self.product_selection_page.destroy()
            self.payment_page = Toplevel(self.root)
            self.payment_page.attributes('-fullscreen', True)
            self.payment_page.configure(bg=bg_color)

            user_index = names.index(user_id)
            account_balance = float(df.loc[user_index, 'money'])
            full_name = df.loc[user_index, 'full_name']

            user_info_label = Label(self.payment_page, text=f"User Name: {full_name}", font=("Helvetica", 16, "bold"), bg=bg_color, fg=fg_color)
            user_info_label.pack(pady=20)

            account_balance_text = f"Account Balance: ${account_balance:.2f}"
            self.account_balance_label = Label(self.payment_page, text=account_balance_text, font=("Helvetica", 16, "bold"), bg=bg_color, fg=fg_color)
            self.account_balance_label.pack(pady=20)

            # Label to display the total price
            self.total_price_label = Label(self.payment_page, text=f"Total Price: ${self.total_price:.2f}", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            self.total_price_label.pack(pady=20)

            # Load the "payment.png" image from the assets folder
            payment_image = PhotoImage(file=os.path.join(current_dir, "assets", "payment.png"))

            # Create the payment button and set the image
            payment_button = Button(self.payment_page, image=payment_image, command=self.check_payment)
            payment_button.image = payment_image  # Ensure the image is not garbage collected
            payment_button.pack(pady=20)

            # Create a "Back" button to return to the product selection page and close the payment page
            back_button = Button(self.payment_page, text="Back", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=self.go_back_to_product_selection)
            back_button.pack(pady=20)

            # Create an error label
            self.error_label = Label(self.payment_page, text="", font=("Helvetica", 14, "bold"), bg=bg_color, fg='red')
            self.error_label.pack(pady=20)

            self.payment_page.protocol("WM_DELETE_WINDOW", self.go_back_to_product_selection)  # Handle window close event
    def go_back_to_product_selection(self):
        self.payment_page.destroy()
        self.open_product_selection()
            
    def check_payment(self):
        try:
            pay_amount_str = self.total_price_label.cget("text")
            pay_amount = float(pay_amount_str.replace("Total Price: $", ""))
            user_index = names.index(self.payee)
            current_balance = float(df.loc[user_index, 'money'])

            if pay_amount <= current_balance:
                df.loc[user_index, 'money'] = current_balance - pay_amount
                df.to_csv(bank_csv_path, index=False)
                account_balance_text = f"Account Balance: ${current_balance - pay_amount:.2f}"
                self.account_balance_label.config(text=account_balance_text)
                self.total_price_label.config(text="Total Price: $0.00")
                self.error_label.config(text="", fg='red')

                # Close the payment page
                self.payment_page.destroy()  # Add this line to close the payment page

            else:
                self.error_label.config(text="Insufficient funds", fg='red')
        except ValueError:
            self.error_label.config(text="Invalid input (must be a valid amount)", fg='red')

    def open_front_page(self):
        self.front_page = Toplevel(self.root)
        self.front_page.attributes('-fullscreen', True)  # Set the front page to fullscreen
        self.front_page.configure(bg=bg_color)
        
    def open_user_management(self):
        if not self.main_window_destroyed:  # Check if the main window still exists
            self.user_management_page = Toplevel(self.root)
            self.user_management_page.attributes('-fullscreen', True)  # Set the user management page to fullscreen
            self.user_management_page.configure(bg=bg_color)

            # Load and display the admin image
            admin_image = PhotoImage(file=os.path.join(current_dir, "assets", "admin.png"))
            admin_image_label = Label(self.user_management_page, image=admin_image, bg=bg_color)
            admin_image_label.image = admin_image
            admin_image_label.pack(pady=20)

            # Create and place a label and text box for Admin Name
            admin_name_label = Label(self.user_management_page, text="Admin Name:", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            admin_name_label.pack()
            admin_name_entry = Entry(self.user_management_page, font=("Helvetica", 12))
            admin_name_entry.pack()

            # Create and place a label and text box for Password
            password_label = Label(self.user_management_page, text="Password:", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            password_label.pack()
            password_entry = Entry(self.user_management_page, show="*", font=("Helvetica", 12))
            password_entry.pack()

            # Create a Confirm button
            confirm_button = Button(self.user_management_page, text="Confirm", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=lambda: self.check_admin_credentials(admin_name_entry.get(), password_entry.get()))
            confirm_button.pack(pady=20)

            # Create a StringVar to update the message label text and color
            self.message_var = StringVar()
            self.message_var.set("")  # Initially, set it to an empty string

            # Create the message label
            self.message_label = Label(self.user_management_page, textvariable=self.message_var, font=("Helvetica", 14), bg=bg_color)
            self.message_label.pack()
            
            back_button = Button(self.user_management_page, text="Back", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=self.close_user_management_page)
            back_button.pack(pady=20)
            
    def close_user_management_page(self):
        if self.user_management_page:
            self.user_management_page.destroy()

    def check_admin_credentials(self, admin_name, password):
        # Replace this logic with your actual admin name and password verification.
        # Here, we assume that admin_name is "shahrad" and password is "1234".
        if admin_name == "shahrad" and password == "1234":
            # Admin name and password are correct, destroy the user management page and open the "users_and_cash" page.
            self.user_management_page.destroy()
            self.open_users_and_cash_page()
            # Check if the message_label exists before configuring it
            if self.message_label:
                self.message_var.set("Confirmed")
                self.message_label.config(fg='green')
        else:
            # Admin name or password was wrong. Check if the message_label exists before configuring it.
            if self.confirmation_label:
                self.confirmation_label.config(text="User name or password was wrong", fg='red')

    def open_users_and_cash_page(self):
        if not self.main_window_destroyed:
            self.users_and_cash_page = Toplevel(self.root)
            self.users_and_cash_page.attributes('-fullscreen', True)
            self.users_and_cash_page.configure(bg=bg_color)

            # Load the "add_user.png" image from the assets folder
            add_user_image = PhotoImage(file=os.path.join(current_dir, "assets", "pic_add_user.png"))

            # Create and place the "Add User" button with the image
            add_user_button = Button(self.users_and_cash_page, image=add_user_image, command=self.open_add_user_page)
            add_user_button.image = add_user_image
            add_user_button.place(x=100, y=100)
            
            add_user_label = Label(self.users_and_cash_page, text="Add User", font=("Helvetica", 20, "bold"), bg=bg_color, fg=fg_color)
            add_user_label.place(x=100, y=570)
            
            credits_image = PhotoImage(file=os.path.join(current_dir, "assets", "credits.png"))

            # Create and place the "Credit Management" button with the image
            credit_management_image = PhotoImage(file=os.path.join(current_dir, "assets", "credits.png"))
            credit_management_button = Button(self.users_and_cash_page, image=credit_management_image, command=self.open_credit_management_page)
            credit_management_button.image = credit_management_image
            credit_management_button.place(x=120 + add_user_image.width() + 200, y=100)

            # Create a label for "Credits" text
            credits_label = Label(self.users_and_cash_page, text="Credits", font=("Helvetica", 20, "bold"), bg=bg_color, fg=fg_color)
            credits_label.place(x=120 + add_user_image.width() + 200, y=570)
            
            back_button = Button(self.users_and_cash_page, text="Back", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=self.close_users_and_cash_page)
            back_button.place(x=695, y=800)  # Adjust the coordinates as needed
            
    def close_users_and_cash_page(self):
        if self.users_and_cash_page:
            self.users_and_cash_page.destroy()        
            
    def open_credit_management_page(self):
        if not self.main_window_destroyed:
            self.credit_management_page = Toplevel(self.root)
            self.credit_management_page.attributes('-fullscreen', True)
            self.credit_management_page.configure(bg=bg_color)

            # Create labels and text entry fields for user input
            full_name_label = Label(self.credit_management_page, text="Full Name:", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            full_name_label.pack()

            full_name_entry = Entry(self.credit_management_page, font=("Helvetica", 12))
            full_name_entry.pack()

            amount_label = Label(self.credit_management_page, text="Amount:", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            amount_label.pack()

            amount_entry = Entry(self.credit_management_page, font=("Helvetica", 12))
            amount_entry.pack()

            # Create a Label to display the confirmation message
            self.confirmation_label = Label(self.credit_management_page, text="", font=("Helvetica", 14), bg=bg_color)
            self.confirmation_label.pack()

            # Create the "Confirm" button
            confirm_button = Button(self.credit_management_page, text="Confirm", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=lambda: self.confirm_credit(full_name_entry.get(), amount_entry.get()))
            confirm_button.pack(pady=20)

            finish_button = Button(self.credit_management_page, text="Finish", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=self.close_credit_management_page)
            finish_button.pack(pady=20)
            
    def close_credit_management_page(self):
        if self.credit_management_page:
            self.credit_management_page.destroy()

    def confirm_credit(self, full_name, amount):
        try:
            amount = float(amount)
            user_index = self.df[self.df['full_name'] == full_name].index

            if len(user_index) > 0:
                user_index = user_index[0]
                current_balance = self.df.loc[user_index, 'money']
                self.df.loc[user_index, 'money'] = current_balance + amount
                self.df.to_csv(bank_csv_path, index=False)
                self.confirmation_label.config(text="Confirmed", fg="green")

                # Show the user's name and money under the confirmation message
                user_info = f"{full_name}: ${current_balance:.2f}"
                user_info_label = Label(self.credit_management_page, text=user_info, font=("Helvetica", 18, "bold"), bg=bg_color, fg=fg_color)
                user_info_label.pack(pady=20)

            else:
                self.confirmation_label.config(text="User didn't exist", fg="red")

        except ValueError:
            self.confirmation_label.config(text="Invalid input (must be a valid amount)", fg="red")

    def close_credit_management_page(self):
        if self.credit_management_page:
            self.credit_management_page.destroy()
            
    def open_add_user_page(self):
        if not self.main_window_destroyed:
            self.add_user_page = Toplevel(self.root)
            self.add_user_page.attributes('-fullscreen', True)
            self.add_user_page.configure(bg=bg_color)

            # Create labels and text entry fields for user input
            id_label = Label(self.add_user_page, text="ID:", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            id_label.pack()
            id_entry = Entry(self.add_user_page, font=("Helvetica", 12))
            id_entry.pack()

            fullname_label = Label(self.add_user_page, text="Full Name:", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            fullname_label.pack()
            fullname_entry = Entry(self.add_user_page, font=("Helvetica", 12))
            fullname_entry.pack()

            credit_label = Label(self.add_user_page, text="Credit:", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            credit_label.pack()
            credit_entry = Entry(self.add_user_page, font=("Helvetica", 12))
            credit_entry.pack()

            # Create the "Confirm" button
            confirm_button = Button(self.add_user_page,text="Confirm" ,font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=lambda: self.add_user(id_entry.get(), fullname_entry.get(), credit_entry.get()))
            confirm_button.pack(pady=20)

            # Close the "Credit and Users" page
            if self.users_and_cash_page:
                self.users_and_cash_page.destroy()

    def add_user(self, id, fullname, credit):
        # Create a QR code for the user's ID
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(id)
        qr.make(fit=True)
        qr_code = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image to the 'qrcodes' directory
        qr_codes_dir = os.path.join(current_dir, "qrcodes")
        if not os.path.exists(qr_codes_dir):
            os.makedirs(qr_codes_dir)
        qr_code_filename = os.path.join(qr_codes_dir, f"{fullname}.png")
        qr_code.save(qr_code_filename)

        # Add user's information to the bank CSV file
        new_user = {'id': id, 'full_name': fullname, 'money': float(credit)}
        self.df = pd.concat([self.df, pd.DataFrame([new_user])], ignore_index=True)
        self.df.to_csv(bank_csv_path, index=False)

        # Open the "Show QRCode" page and display the generated QR code
        self.open_show_qrcode_page()
        
        # Destroy the 'add_user_page'
        self.add_user_page.destroy()
        
    def open_show_qrcode_page(self):
        if not self.main_window_destroyed:
            self.show_qrcode_page = Toplevel(self.root)
            self.show_qrcode_page.attributes('-fullscreen', True)
            self.show_qrcode_page.configure(bg=bg_color)

            search_label = Label(self.show_qrcode_page, text="Search:", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color)
            search_label.pack()

            search_entry = Entry(self.show_qrcode_page, font=("Helvetica", 12))
            search_entry.pack()

            search_button = Button(self.show_qrcode_page, text="Search QR Code", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=lambda: self.search_qrcode(search_entry.get()))
            search_button.pack(pady=20)

            self.qr_code_image_label = Label(self.show_qrcode_page, bg=bg_color)
            self.qr_code_image_label.pack()

            back_button = Button(self.show_qrcode_page, text="Back", font=("Helvetica", 14, "bold"), bg=bg_color, fg=fg_color, command=self.close_show_qrcode_page)
            back_button.pack(pady=20)

    def close_show_qrcode_page(self):
        if self.show_qrcode_page:
            self.show_qrcode_page.destroy()

    def search_qrcode(self, search_text):
        qr_code_path = os.path.join(current_dir, "qrcodes", f"{search_text}.png")
        if os.path.exists(qr_code_path):
            qr_code_image = PIL.Image.open(qr_code_path)
            qr_code_image = ImageTk.PhotoImage(qr_code_image)

            # Display the found QR code image
            if self.qr_code_image_label:
                self.qr_code_image_label.config(image=qr_code_image)
                self.qr_code_image_label.image = qr_code_image
        else:
            # If the QR code image is not found, show an error message
            if self.qr_code_image_label:
                self.qr_code_image_label.config(text="QR Code not found", font=("Helvetica", 14, "bold"), fg='red')
    
            
if __name__ == "__main__":
    root = Tk()

    # Set the icon for the application
    icon_path = os.path.join(current_dir, "assets", "qrcode_icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    root.title("QRPAY")

    app = QRPaymentApp(root)
    root.mainloop()

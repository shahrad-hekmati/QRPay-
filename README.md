# QRPay-

Description:
The QR Payment System is an open-source Python application designed to simplify and secure payment. It allows users to make payments by scanning QR codes, manages user accounts, and maintains account balances. The system provides a graphical user interface (GUI) for ease of use and a more interactive experience.

Features:

1. **User Management:** The system includes a user management feature, where administrators can add new users by providing user IDs, full names, and initial credit amounts. This is useful for managing accounts and keeping track of user balances.

2. **QR Code Payment:** Users can make payments by scanning QR codes generated for their accounts. The system reads the QR code to identify the user and performs the transaction if the user's balance is sufficient.

3. **Product Selection:** The application allows users to select products to purchase from a list. It calculates the total price based on the selected quantities and updates it in real time. Users can then proceed to make the payment.

4. **Real-time Balances:** The user's account balance is displayed on the payment page, ensuring they have enough credit for their purchase.

5. **Error Handling:** The system provides error messages for cases where a user has insufficient funds, enters invalid input, or if the administrator provides incorrect credentials.

6. **Admin Panel:** An administrator can access an admin panel to manage user accounts, add new users, and manage their credit.

7. **User-friendly GUI:** The application offers a user-friendly graphical interface with interactive buttons and clear labels, making it easy to navigate.

8. **Responsive Design:** The system's pages are responsive and adapt to various screen sizes, including full-screen mode for better visibility.

9. **Data Persistence:** User account data is stored in a CSV file, ensuring user information and balances are maintained between sessions.

10. **Customizable:** The system is customizable, allowing users to add or remove products, modify the initial credit of new users, and more.

11. **Search QR Code:** Users can search for QR codes by entering a user's full name and viewing the QR code associated with that user.

12. **Exit Functionality:** Users can exit the application gracefully.

How to Use:

- Clone the repository and run the Python script.
- Access the admin panel to manage users and their credits.
- Users can select products, see the total price, and make payments by scanning their QR codes.
- If you want to customize the product list or add new users, you can edit the respective CSV files.

This QR Payment System is suitable for small businesses or organizations seeking a straightforward payment solution with user management capabilities. It provides an easy and efficient way to manage user accounts, enable secure payments, and offer a seamless customer experience.

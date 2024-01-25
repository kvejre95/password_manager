from cryptography.fernet import InvalidToken
from crypt import FernetCrypt
from db import DataLayer


class PasswordManager:
    """
    A class to manage passwords securely.
    """

    def __init__(self):
        self.crypt = FernetCrypt()
        self.data_layer = DataLayer("my_passdb.db")

    def create_table(self):
        """
        Create a table for storing password information.
        """
        self.data_layer.create_table(
            "SecurityInfo",
            ["id INTEGER PRIMARY KEY", "app_name TEXT", "user_name TEXT", "hint TEXT", "password TEXT"]
        )

    def insert_data(self, app_name: str, user_name: str, hint: str, password: str):
        """
        Insert User information into the database.

        :param app_name: The name of the application or service.
        :param user_name: The username for the service.
        :param hint: A hint for the password.
        :param password: The plaintext password.
        """
        cipher_suite = self.crypt.get_fernet()
        self.data_layer.insert_data(
            "SecurityInfo",
            [app_name, user_name, self.__encrypt_password(cipher_suite, hint),
             self.__encrypt_password(cipher_suite, password)]
        )

    def get_data(self, id: int):
        """
        Retrieve password information from the database.

        :param id: The ID of the record to retrieve.
        :return: A list containing the decrypted password information.
        """
        data_tuple = self.data_layer.fetch_data("SecurityInfo", id)
        if data_tuple:
            cipher_suite = self.crypt.get_fernet()
            data_list = list(data_tuple[0])
            data_list[-1] = self.__decrypt_password(cipher_suite, data_list[-1])
            data_list[-2] = self.__decrypt_password(cipher_suite, data_list[-2])
            return data_list
        return []

    def close_connection(self):
        """
        Close the database connection.
        """
        self.data_layer.close_connection()

    def __encrypt_password(self, cipher_suite, password: str) -> str:
        """
        Encrypt a password using a Fernet cipher.
        """
        cipher_text = cipher_suite.encrypt(password.encode("utf-8"))
        return cipher_text.decode("utf-8")

    def __decrypt_password(self, cipher_suite, cipher_text: str) -> str:
        """
        Decrypt an encrypted password using a Fernet cipher.
        """
        try:
            decrypted_text = cipher_suite.decrypt(cipher_text.encode("utf-8"))
            return decrypted_text.decode('utf-8')
        except InvalidToken as e:
            print("Please give the correct key", e)


if __name__ == "__main__":
    pm = PasswordManager()

    while True:
        print("\nOptions:")
        print("1. Create Table")
        print("2. Insert Data")
        print("3. Get Data")
        print("4. Quit")

        choice = input("Select an option (1/2/3/4): ")

        if choice == "1":
            pm.create_table()
            print("Table created successfully.")
        elif choice == "2":
            app_name = input("Enter the application name: ")
            user_name = input("Enter the username: ")
            hint = input("Enter the password hint: ")
            plaintext_password = input("Enter the plaintext password: ")
            pm.insert_data(app_name, user_name, hint, plaintext_password)
            print("Data inserted successfully.")
        elif choice == "3":
            record_id = input("Enter the record ID to fetch: ")
            record_id = int(record_id)
            data = pm.get_data(record_id)
            if data:
                print(f"Decrypted Record: {data}")
            else:
                print("No data found for the specified ID.")
        elif choice == "4":
            pm.close_connection()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option (1/2/3/4).")


from datetime import datetime, timedelta
from collections import defaultdict

class Birthday:
    def __init__(self, date_str):
        self.date = self._parse_date(date_str)

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Invalid date format. Please use DD.MM.YYYY.")

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phone = self._validate_phone(phone)
        self.birthday = birthday

    def _validate_phone(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Invalid phone number. Please provide a 10-digit number.")
        return phone

    def add_birthday(self, date_str):
        self.birthday = Birthday(date_str)

class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone):
        if name in self.contacts:
            raise ValueError(f"Contact '{name}' already exists.")
        self.contacts[name] = Record(name, phone)

    def change_phone(self, name, new_phone):
        contact = self._get_contact(name)
        contact.phone = contact._validate_phone(new_phone)

    def show_phone(self, name):
        contact = self._get_contact(name)
        return contact.phone

    def show_all_contacts(self):
        return list(self.contacts.keys())

    def add_birthday(self, name, date_str):
        contact = self._get_contact(name)
        contact.add_birthday(date_str)

    def show_birthday(self, name):
        contact = self._get_contact(name)
        if contact.birthday:
            return contact.birthday.date.strftime("%d.%m.%Y")
        else:
            return "No birthday set for this contact."

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        birthdays = defaultdict(list)
        for name, record in self.contacts.items():
            if record.birthday:
                if today < record.birthday.date < next_week:
                    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    weekday = record.birthday.date.strftime('%A')
                    birthdays[weekday].append(name)
        return birthdays

    def _get_contact(self, name):
        if name not in self.contacts:
            raise ValueError(f"Contact '{name}' not found.")
        return self.contacts[name]

# Bot commands

def handle_add_command(address_book, args):
    if len(args) != 3:
        return "Invalid number of arguments. Please provide name and phone number separated by a space."
    
    name = args[1]
    phone = args[2]
    
    address_book.add_contact(name, phone)
    return f"Contact {name} with phone number {phone} added successfully."

def handle_change_command(address_book, args):
    if len(args) != 3:
        return "Invalid number of arguments. Please provide name and new phone number separated by a space."
    
    name = args[1]
    new_phone = args[2]
    
    address_book.change_phone(name, new_phone)
    return f"Phone number for '{name}' changed successfully."

def handle_phone_command(address_book, args):
    if len(args) != 2:
        return "Invalid number of arguments. Please provide name."
    
    name = args[1]
    return address_book.show_phone(name)

def handle_all_command(address_book, args):
    return address_book.show_all_contacts()

def handle_add_birthday_command(address_book, args):
    if len(args) != 3:
        return "Invalid number of arguments. Please provide name and birthday in format DD.MM.YYYY separated by a space."
    
    name = args[1]
    birthday = args[2]
    
    address_book.add_birthday(name, birthday)
    return f"Birthday added for '{name}'."

def handle_show_birthday_command(address_book, args):
    if len(args) != 2:
        return "Invalid number of arguments. Please provide name."
    
    name = args[1]
    return address_book.show_birthday(name)

def handle_birthdays_command(address_book, args):
    return address_book.get_birthdays_per_week()

def handle_hello_command(address_book, args):
    return "Hello! How can I assist you today?"

def handle_close_command(address_book, args):
    return "Closing the app. Goodbye!"

# function to handle bot commands

def handle_command(command, address_book):
    command = command.lower().strip()
    if command.startswith("add "):
        return handle_add_command(address_book, command[4:].split())
    elif command.startswith("change "):
        return handle_change_command(address_book, command[7:].split())
    elif command.startswith("phone "):
        return handle_phone_command(address_book, command[6:].split())
    elif command == "all":
        return handle_all_command(address_book, [])
    elif command.startswith("add-birthday "):
        return handle_add_birthday_command(address_book, command[13:].split())
    elif command.startswith("show-birthday "):
        return handle_show_birthday_command(address_book, command[14:].split())
    elif command == "birthdays":
        return handle_birthdays_command(address_book, [])
    elif command == "hello":
        return handle_hello_command(address_book, [])
    elif command in ["close", "exit"]:
        return handle_close_command(address_book, [])
    else:
        return "Invalid command. Type 'help' for a list of commands."
    
# This main function initializes an instance of AddressBook,
# then enters a loop to continuously prompt the user 
# for commands. It processes each command using the handle_command function
# and prints the result. If the user enters 'close' or 'exit', it breaks out of the loop and closes the application.

def main():
    address_book = AddressBook()
    print("Welcome to my Address Book!")
    while True:
        command = input("Enter a command: ")
        if command.lower() in ["close", "exit"]:
            print(handle_close_command(address_book, []))
            break
        else:
            print(handle_command(command, address_book))

if __name__ == "__main__":
    main()

        
# Testing of my bot:
    
# add Pawel Ciosmak 5059722030
# change Pawel Ciosmak 5059722031
# phone Pawel Ciosmak
# all
# add-birthday Pawel Ciosmak 22.03.1984
# show-birthday Pawel Ciosmak
# birthdays
# hello
# close
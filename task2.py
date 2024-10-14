from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
class Name(Field):
    pass
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Zly numer telefonu")
        super().__init__(value)
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = Phone(new_phone)
    def find_phone(self, phone):
        if phone in self.phones:
            return phone
        else:
            return None
    def __str__(self):
        return f"Imię: {self.name}, numery telefonów: {', '.join(str(phone) for phone in self.phones)}"
class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
    def add_record(self, record):
        self.data[record.name.value] = record
    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None
    def delete(self, name):
        if name in self.data:
            del self.data[name]
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Podaj poprawne dane, np. 'add [imię] [numer telefonu]'"
        except IndexError:
            return "Brak wymaganych argumentów, spróbuj ponownie"
        except KeyError:
            return "Kontakt nie istnieje."
    return inner
@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    contacts.add_record(Record(name))
    contacts[name].add_phone(phone)
    return "Kontakt dodany."
@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    if name in contacts.data:
        contacts[name].add_phone(phone)
        return "Zaktualizowalem kontakt."
    else:
        raise KeyError
@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise ValueError
    name = args[0]
    if name in contacts.data:
        return str(contacts[name])
    else:
        raise KeyError
@input_error
def show_all(contacts):
    if not contacts.data:
        return "Brak zapisanych kontaktów."
    else:
        return "\n".join([str(record) for record in contacts.data.values()])
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args
def main():
    contacts = AddressBook()
    print("Witaj w asystencie!")
    while True:
        user_input = input("Wpisz polecenie: ")
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Do widzenia!")
            break
        elif command == "hello":
            print("Jak mogę pomóc?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Nieprawidłowe polecenie.")
if __name__ == "__main__":
    main()

        #testowanie - ma dzialac tak:
    #Wpisz polecenie: add John 1234567890
    #Kontakt dodany.
    #Wpisz polecenie: change John 0987654321
    #Zaktualizowalem kontakt.
    #Wpisz polecenie: phone John
    #Imię: John, numery telefonów: 1234567890, 0987654321
    #Wpisz polecenie: all
    #Imię: John, numery telefonów: 1234567890, 0987654321
    #Wpisz polecenie: exit
    #Do widzenia!
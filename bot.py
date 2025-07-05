from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self.value = value.strip()

class Phone(Field):
    # реалізація класу
    def __init__(self, phone):
        if not isinstance(phone, str) or not phone.strip():
            raise ValueError("Phone must be a non-empty string.")
        value = phone.strip()
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        self.value = value
        if len(value) != 10:
            raise ValueError("Phone number must be 10 digits long.")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def remove_phone(self, phone):
        phone_to_remove = Phone(phone)
        self.phones = [p for p in self.phones if p.value != phone_to_remove.value]
    def find_phone(self, phone):
        if not isinstance(phone, str) or not phone.strip():
            raise ValueError("Phone must be a non-empty string.")
        phone = phone.strip()
        if any(p.value == phone for p in self.phones):
            return phone
        raise ValueError("Phone number not found")
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return
        raise ValueError("Phone number not found.")
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Only Record instances can be added.")
        self.data[record.name.value] = record
    def find(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        return self.data[name.strip()]
    def delete(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        name = name.strip()
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact '{name}' not found.")

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane") 
        
#==========================================
# Old bot code

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid input. Format: add <name> <phone_number>."
        except IndexError:
            return "Invalid input. Format: phone <name>."
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    # try:
        name, phone = args
        contacts[name] = phone
        return "Contact added."
    # except ValueError:
    #     return "Invalid input. Format: add <name> <phone_number>."

@input_error
def change_contact(args, contacts):
    # try:
        name, phone = args
        if name in contacts:
            contacts[name] = phone
            return "Contact updated."
        else:
            return "Contact not found."
    # except ValueError:
    #     return "Invalid input. Format: change <name> <new_phone_number>."

@input_error
def show_phone(args, contacts):
    # try:
        name = args[0]
        if name in contacts:
            return f"{name}'s phone number is {contacts[name]}."
        else:
            return "Contact not found."
    # except IndexError:
    #     return "Invalid input. Format: phone <name>."

@input_error
def show_all(contacts):
    list = "All contacts:\n"
    if contacts:
        for name, phone in contacts.items():
            list +=(f"  {name}: {phone}\n")
        return list
    else:
        return "No contacts available."

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

# if __name__ == "__main__":
#     main()




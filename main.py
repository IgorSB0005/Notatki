import os

notes_directory = "Notes"
def create_notes_directory():
    try:
        if not os.path.exists(notes_directory):
            os.makedirs(notes_directory)
    except Exception as e:
        print("Error during directory creation:", e)

def add_note():
    note_name = input("Name of your note: ")
    note_content = input("Write down your thoughts: ")
    file_name = os.path.join(notes_directory, note_name)

    try:
        with open (file_name, "w") as file:
            file.write(note_content)
            print("Your note is recorded successfully.")
    #04_ Obsługa błędów, wyjątki
    except Exception as e:
        print(f"An error occurred while recording the note: {e}")

def list_files():
    if not os.path.exists(notes_directory):
        print(f"Directory '{notes_directory}' does not exist.")
        return

    files = os.listdir(notes_directory)

    print("Your notes:")
    for file in files:
        print(file)

def main():
    create_notes_directory()
    print("Welcome to the super duper program")
    while True:
        print("1: Add note\n"
              "2: View notes\n"
              "3: Quit the program"
              "")
        action = str(input("choose an action:"))
        os.system("cls")
        match action:
            case '1':
                add_note()
            case '2':
                list_files()
            case '3':
                break

if __name__ == "__main__":
    main()
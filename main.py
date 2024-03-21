import os

def create_notes_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Directory successfully created:", directory)
        else:
            print("Directory already exists:", directory)
    except Exception as e:
        print("Error during directory creation:", e)

def add_note():
    note_name = input("Name of your note: ")
    note_content = input("Write down your thoughts: ")
    file_name = f"{note_name}.txt"

    try:
        with open (file_name, "w") as file:
            file.write(note_content)
            print("Your note is recorded successfully.")
    #04_ Obsługa błędów, wyjątki
    except Exception as e:
        print(f"An error occurred while recording the note: {e}")

def list_files(directory):
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    files = os.listdir(directory)

    print("Your notes:")
    for file in files:
        print(file)

def main():
    while True:
      add_note()
      new_note = input("Would you like to add one more note? (yes/no) ")
      while new_note.lower() != "yes" and new_note.lower() != "no":
        print(f"Cannot understand your answer.")
        new_note = input("Would you like to add one more note? (yes/no) ")
      if new_note.lower() == "no":
        print("menu***") #тут коли зробим меню його додамо, ми ж його зробим?

if __name__ == "__main__":
    main()

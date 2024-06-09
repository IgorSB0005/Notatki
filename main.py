import customtkinter
import os
import re


notes_directory = os.path.expanduser("~/Documents/Notes")
listNotes = []

class ScrollableCheckboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []
        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class CreatingAndFillingNote(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Note creation")
        self.geometry("400x100")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(width=False, height=False)

        self.nameNote = customtkinter.StringVar()
        self.contentNote = customtkinter.StringVar()

        entry_name = customtkinter.CTkEntry(self, textvariable=self.nameNote)
        entry_content = customtkinter.CTkEntry(self, textvariable=self.contentNote)
        buttonCreation = customtkinter.CTkButton(self, text="creation", command=self.destroy)

        customtkinter.CTkLabel(self, text="Name of your note:").grid(row=0, column=0,padx=10, pady=(10, 0), sticky="w")
        customtkinter.CTkLabel(self, text="Write down your thoughts:").grid(row=1, column=0,padx=10, pady=(10, 0), sticky="w")
        entry_name.grid(row=0, column=1, padx=20, pady=(5, 0), sticky="w")
        entry_content.grid(row=1, column=1, padx=20, pady=(5, 0), sticky="w", columnspan=5)
        buttonCreation.grid(row=3, columnspan=2)


    def open(self):
        self.wait_window()
        name = self.nameNote.get()
        content = self.contentNote.get()
        return name,content

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Notes app")
        self.geometry("600x440")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.scrollable_checkbox_frame = ScrollableCheckboxFrame(self, title="Notes", values=listNotes)
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.buttonAdd = customtkinter.CTkButton(self, text="Add", command=self.add_note)
        self.buttonAdd.grid(row=4, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.buttonRead = customtkinter.CTkButton(self, text="Read(choose one)", command=self.read_notes)
        self.buttonRead.grid(row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.buttonSearch = customtkinter.CTkButton(self, text="Search", command=self.search_window)
        self.buttonSearch.grid(row=6, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.buttonDelete = customtkinter.CTkButton(self, text="Delete", command=self.delete_notes)
        self.buttonDelete.grid(row=7, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.buttonRefresh = customtkinter.CTkButton(self, text='⟳', command=self.refresh_list_notes)
        self.buttonRefresh.configure(width=20, height=20)
        self.buttonRefresh.grid(column=2, row=1, sticky="ne", pady=10)


    def search_window(self):
        searchWindow = customtkinter.CTkToplevel()
        searchWindow.title("Search notes")
        searchWindow.geometry("400x200")
        searchWindow.grid_columnconfigure(0, weight=1)
        searchWindow.grid_rowconfigure(1, weight=1)
        searchWindow.resizable(width=False, height=False)

        self.entrySearch = customtkinter.StringVar()

        entry_search = customtkinter.CTkEntry(searchWindow, textvariable=self.entrySearch)
        buttonSearch = customtkinter.CTkButton(searchWindow, text="Search", command=self.search_note)
        buttonCancel = customtkinter.CTkButton(searchWindow, text="Cancel", command=searchWindow.destroy)

        customtkinter.CTkLabel(searchWindow, text="Enter your request:").grid(row=0, column=0, padx=20, pady=(5, 0), sticky="w", columnspan=2)
        entry_search.grid(row=1, column=0, padx=20, pady=(5, 0), sticky="w", columnspan=2)
        buttonSearch.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        buttonCancel.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    def initialize_notes(self):
        self.create_notes_directory()
        self.ReadListNotes()
        self.refresh_list_notes()

    def create_notes_directory(self):
        try:
            os.makedirs(notes_directory, exist_ok=True)
        except Exception as e:
            print("Error during directory creation:", e)

    def add_note(self):
        note = CreatingAndFillingNote().open()
        note_name = note[0]
        note_content = note[1]
        if note_name != "" and note_content != "":
            file_name = os.path.join(notes_directory, note_name)

            try:
                with open(file_name, "w") as file:
                    file.write(note_content)
                    print("Your note is recorded successfully.")
            # 04_ Obsługa błędów, wyjątki
            except Exception as e:
                print(f"An error occurred while recording the note: {e}")
            listNotes.append(note_name)
            self.refresh_list_notes()

    def ReadListNotes(self):
        if not os.path.exists(notes_directory):
            print(f"Directory '{notes_directory}' does not exist.")
            return

        files = os.listdir(notes_directory)

        for file in files:
            listNotes.append(file)

    def refresh_list_notes(self):
        self.scrollable_checkbox_frame.destroy()
        self.scrollable_checkbox_frame = ScrollableCheckboxFrame(self, title="Notes", values=listNotes)
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)

    def delete_notes(self):
        checked_notes = self.scrollable_checkbox_frame.get()
        for note in checked_notes:
            file_name = os.path.join(notes_directory,note)
            try:
                os.remove(file_name)
                listNotes.remove(note)
            except Exception as e:
                print(f"Deleting error")
        self.refresh_list_notes()

    def search_note(self):
        search_query = self.entrySearch.get()
        matched_notes = []

        if search_query:
            for note in listNotes:
                file_path = os.path.join(notes_directory, note)
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                        if re.search(search_query, content, re.IGNORECASE):
                            matched_notes.append(note)
                except Exception as e:
                    print(f"An error occurred while searching: {e}")
        self.scrollable_checkbox_frame.destroy()
        self.scrollable_checkbox_frame = ScrollableCheckboxFrame(self, title="Notes", values=matched_notes)
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)

    def read_notes(self):
        checked_notes = self.scrollable_checkbox_frame.get()
        if len(checked_notes) == 1:
            read_window = customtkinter.CTkToplevel()
            read_window.title("Read Notes")
            read_window.geometry("1050x650")
            read_window.grid_columnconfigure(0, weight=1)
            read_window.grid_rowconfigure(0, weight=1)
            read_window.text_area = customtkinter.CTkTextbox(read_window)
            read_window.text_area.grid(row=0, column=0, sticky="nsew", columnspan=1)
            read_window.text_area.configure(height= 600, width= 1000)
            for note_file in checked_notes:
                note_path = os.path.join(notes_directory, note_file)
                with open(note_path, "r") as file:
                    note_content = file.read()
                    read_window.text_area.insert("0.0", f"Note: {note_content}\n")
                    read_window.text_area.insert("0.0", f"{note_file}\n")

        buttonCreation = customtkinter.CTkButton(read_window, text="Cancel", command=read_window.destroy)
        buttonCreation.grid(row=1, columnspan=2)

if __name__ == "__main__":
    app = App()
    app.initialize_notes()
    app.mainloop()
    

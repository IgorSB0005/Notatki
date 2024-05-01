import customtkinter
import os

notes_directory = "Notes"
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

        self.ReadListNotes()
        self.title("Notes app")
        self.geometry("600x440")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.scrollable_checkbox_frame = ScrollableCheckboxFrame(self, title="Notes", values=listNotes)
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.create_notes_directory()
        self.buttonAdd = customtkinter.CTkButton(self, text="Add", command=self.add_note)
        self.buttonAdd.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.buttonDelete = customtkinter.CTkButton(self, text="Delete", command=self.delete_notes)
        self.buttonDelete.grid(row=4, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def create_notes_directory(self):
        try:
            if not os.path.exists(notes_directory):
                os.makedirs(notes_directory)
        except Exception as e:
            print("Error during directory creation:", e)

    def add_note(self):
        note = CreatingAndFillingNote().open()
        note_name = note[0]
        note_content = note[1]
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
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

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




if __name__ == "__main__":
    App().mainloop()
# *********************************************************************************************************************
from tkinter import *
from tkinter import messagebox
from selection import *
from file_handling import *
import os
import io
import csv
# *********************************************************************************************************************


print("Function: Data Prep")
print("Release: 0.0.1")
print("Date: 2020-02-14")
print("Author: Brian Neely and David Liau")
print()
print()
print(".")
print()
print()


# Sets up a frame
class File_Encoder(Frame):

    # When a class is initialized, this is called as per any class
    def __init__(self, master):

        # Similar to saying MyFrame = Frame(master)
        Frame.__init__(self, master)

        # Puts the frame on a grid. If you had two frames on one window, you would do the row, column keywords (or not...)
        self.grid(padx=5, pady=5, sticky=(N, W, E, S))

        Grid.rowconfigure(master, 0, weight=1)
        Grid.rowconfigure(master, 1, weight=1)
        Grid.columnconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 1, weight=1)

        global output_loc

        # Function to put the widgets on the frame. Can have any name!
        self.create_widgets()

    # Function that performs an encoding change on the selected file(s).
    def encode(self):

        # ----- Temp set delimiter
        delimiter = ','

        # Extracting selected files
        files = self.listbox.curselection()
        files = [os.path.join(os.getcwd(), self.listbox.get(f)) for f in files]

        for file_in in files:
            # Open output file
            print("Select or name output file.")
            file_out = select_file_out_csv(file_in)

            # Attempt to auto find encoder?
            if y_n_question("Attempt to auto find encoding (y/n): "):
                encoder_in = encoder_finder(file_in, ",")
            else:
                # Ask for input encoder
                encoder_in = encoding_selection("Select encoding of input file.")

            # Ask for output encoder
            encoder_out = encoding_selection("Select encoding of output file.")

            # Read table and write results to label box.
            with open(file_in, newline="", encoding=encoder_in) as file:
                reader = csv.reader(file, delimiter=delimiter)
                r = 0
                for col in reader:
                    if r > 5:
                        break
                    c = 0
                    for row in col:
                        self.label = Label(text=row)
                        self.label.grid(row=r + 3, column=c, sticky=SW)
                        c += 1
                    r += 1

            # Read and write file
            try:
                with io.open(file_in, 'r', encoding=encoder_in) as f:
                    text = f.read()
                with io.open(file_out, 'w', encoding=encoder_out) as f:
                    f.write(text)

                input("Program Complete, Press [Enter] to continue.")
            except UnicodeEncodeError:
                print(
                    "An error has occurred encoding text into " + encoder_out + ". This typically occurs when a character in"
                                                                                "present in the input encoder, but doesn't"
                                                                                "exists in the output encoder.")
                print("Please try again with a different output encoder.")
                input("Press [Enter] to continue.")
            except UnicodeDecodeError:
                print("An error has occurred decoding the input file using" + encoder_in + ".")
                print("Please try again with another input encoder.")
                input("Press [Enter] to continue.")
            except:
                print(sys.exc_info()[0])
                print("An unexpected error has occurred.")
                input("Press [Enter] to continue.")

        return

    def applyall(self):
        return

    def cancel(self):
        if messagebox.askokcancel('Cancel', 'Are you sure you want to cancel?'):
            root.destroy()

    def out_file_loc(self):
        # Open output file
        print("Select or name output file.")
        file_out = select_file_out_csv(os.getcwd())

        output_loc = file_out

        return

    def create_widgets(self):
        # Give the grid, column of each widget weight...
        for rows in range(3):
            Grid.rowconfigure(self, rows, weight=1)
        for columns in range(3):
            Grid.columnconfigure(self, columns, weight=1)

        text = "No data selected!"
        output_loc = StringVar()
        output_loc = "No file output"

        # File List
        self.listbox = Listbox(self, relief=GROOVE, height=6, selectmode=EXTENDED)
        self.listbox.grid(row=0, column=0, sticky=W)
        for name in os.listdir():
            if name[0] != '.':
                self.listbox.insert('end', name)

        # Data Text
        self.label = Label(root, width=10, height=2, text="", relief=RIDGE)
        self.label.grid(row=3, column=0, sticky=SW)

        # Side Buttons
        self.encode = Button(self, text="Encoding", command=self.encode).grid(column=1, row=0, sticky=N)
        self.delim = Button(self, text="Delimiter", command=self.cancel).grid(column=1, row=0)
        self.apply_all = Checkbutton(self, text="Apply to All", command=self.applyall).grid(column=2, row=0, sticky=NE)

        self.output = Button(self, text="Output Location", command=self.out_file_loc).grid(column=1, row=2, padx=15,
                                                                                           sticky=N)
        self.out_file = Label(self, textvariable=output_loc).grid(column=2, row=2, sticky=NE)

        self.cancel = Button(self, text="Cancel", command=self.cancel).grid(column=1, row=2, padx=15, sticky=SW)
        self.submit = Button(self, text="Submit", command=self.cancel).grid(column=2, row=2, sticky=SE)

root = Tk()
root.title('File Encoder')
app = File_Encoder(root)

root.mainloop()

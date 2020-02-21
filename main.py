# *********************************************************************************************************************
from tkinter import *
from tkinter import messagebox
from selection import *
from file_handling import *
import os
import io
import csv
# *********************************************************************************************************************

# --------------- Path is set to get current working directory.... Need to fix
# --------------- Tab in delimiter doesn't work

print("Function: Data Prep")
print("Release: 0.0.1")
print("Date: 2020-02-14")
print("Author: Brian Neely and David Liau")
print()
print()
print(".")
print()
print()


#Sets up a frame
class File_Encoder(Frame):

    #When a class is initialized, this is called as per any class
    def __init__(self, master):

        #Similar to saying MyFrame = Frame(master)
        Frame.__init__(self, master)

        #Puts the frame on a grid. If you had two frames on one window, you would do the row, column keywords (or not...)
        self.grid(padx=5, pady=5, sticky=(N, W, E, S))

        # Configuring the masterframe so that it's flexible for resizing.
        # Right now it is not working.
        Grid.rowconfigure(master, 0, weight=1)
        Grid.rowconfigure(master, 1, weight=1)
        Grid.columnconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 1, weight=1)

        # File Path
        self.fpath = ""

        # Initialize output file variable
        self.out_file_label = StringVar()
        # Not initializing as StringVariable because we won't be updating any labels
        self.out_file = ""

        encode_list = ['utf_8', 'latin1', 'utf_16',
                         'ascii', 'big5', 'big5hkscs', 'cp037', 'cp424',
                         'cp437', 'cp500', 'cp720', 'cp737', 'cp775',
                         'cp850', 'cp852', 'cp855', 'cp856', 'cp857',
                         'cp858', 'cp860', 'cp861', 'cp862', 'cp863',
                         'cp864', 'cp865', 'cp866', 'cp869', 'cp874',
                         'cp875', 'cp932', 'cp949', 'cp950', 'cp1006',
                         'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252',
                         'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257',
                         'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr',
                         'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp',
                         'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext',
                         'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4',
                         'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9',
                         'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15',
                         'iso8859_16', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic',
                         'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish',
                         'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32',
                         'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le',
                         'utf_7', 'utf_8', 'utf_8_sig']
        self.encoding_options = { encode_list[i] : i for i in range(0, len(encode_list))}
        #encode_list = sorted(list(encode_list))
        #self.encoding_options = { encode_list[i] : i for i in range(0, len(encode_list))}
        self.in_encode = StringVar()
        self.out_encode = StringVar()
        self.in_delim = StringVar()
        self.out_delim = StringVar()

        #Function to put the widgets on the frame. Can have any name!
        self.create_widgets()

#     def applyall(self):
#         return

    # This function closes out the tkinter mainframe, destroying all widgets.
    def cancel(self):
        if messagebox.askokcancel("Cancel", "Are you sure you want to cancel?"):
            root.destroy()
            sys.exit(0)

        # This function previews the selected dataset, displaying the first five rows and columns.
    def preview(self):
        # Get file from selection list
        files = self.file_list.curselection()
        if len(files) == 0:
            messagebox.showwarning("Warning", "Please select a file from the list.")
            return
        file_in_list = [os.path.join(self.fpath, self.file_list.get(f)) for f in files]
        file_in = file_in_list[0]

        # Get enconder and delimiter
        delimiter_in = self.in_delim.get()
        encoder_in = self.in_encode.get()

        # Give error if no delimiter
        if delimiter_in is None or delimiter_in == "":
            messagebox.showwarning("Warning", "Please select an input delimiter.")
            return

        # Open new window for preview results
        preview_window = Toplevel(root)

        # Preview Data Label
        self.data = Label(preview_window, width=10, height=2, text="", relief=RIDGE)

        # Read table and write results to label box.
        try:
            with open(file_in, newline="", encoding=encoder_in) as file:
                if '\\' in delimiter_in:
                    reader = csv.reader(file, delimiter='\\' + delimiter_in)
                else:
                    reader = csv.reader(file, delimiter=delimiter_in)
                r = 0
                for col in reader:
                    if r > 5:
                        break
                    c = 0
                    for row in col:
                        self.data = Label(preview_window, text=row, relief=RIDGE)
                        self.data.grid(row=r + 1, column=c, padx=20)
                        c += 1
                    r += 1
        except:
            messagebox.showerror("Error", "Cannot read a character in the file. Please choose a different encoder.")

    # This function allows the user to choose the input folder.
    def set_in_file(self):
        # Choose input folder
        self.fpath = select_folder()

        self.file_list.delete(0, 'end')

        with os.scandir(self.fpath) as listOfEntries:
            for entry in listOfEntries:
                # print all entries that are files
                if entry.is_file() and entry.name[0] != '.':
                    self.file_list.insert('end', entry.name)


    # This function allows the user to choose the output file.
    def set_out_file(self):
        # Open output file
        try:
            file_out = select_file_out_csv(os.getcwd())

            # Setting output file
            self.out_file = file_out

            # Setting output file label
            output_label = file_out[file_out.rfind('/')+1:]
            self.out_file_label.set(output_label)
        except SystemExit:
            messagebox.showinfo("Cancelled", "The operation was cancelled.")
            return

    # This function runs the encoding and delimiting operations on the selected file(s).
    def submit(self):
        # Extracting selected files
        files = self.file_list.curselection()
        files = [os.path.join(self.fpath, self.file_list.get(f)) for f in files]

        if len(files) == 0:
            messagebox.showwarning("Warning", "Please select a file from the list.")
            return

        # Declaring all necessary files, encoders and decoders running operations
        file_out = self.out_file
        encoder_in = self.in_encode.get()
        encoder_out = self.out_encode.get()
        delimiter_in = self.in_delim.get()
        delimiter_out = self.out_delim.get()

        if file_out is None or file_out == "No file selected." or len(file_out) == 0:
            messagebox.showwarning("Warning", "Please select an output file.")
            return
        if delimiter_in is None or delimiter_in == "":
            messagebox.showwarning("Warning", "Please select an input delimiter.")
            return
        if delimiter_out is None or delimiter_out == "":
            messagebox.showwarning("Warning", "Please select an output delimiter.")
            return

        # For each file, perform encoding/delimiting
        for file_in in files:
            # Read and write file
            try:
                with open(file_in, 'r', newline="", encoding=encoder_in) as file:
                    if "\\" in delimiter_in:
                        reader = csv.reader(file, delimiter='\t')
                    else:
                        reader = csv.reader(file, delimiter=delimiter_in)
                    data = [r for r in reader]

                with open(file_out, 'w', newline="", encoding=encoder_out) as file:
                    if "\\" in delimiter_out:
                        writer = csv.writer(file, delimiter='\t')
                    else:
                        writer = csv.writer(file, delimiter=delimiter_out)
                    writer.writerows(data)

                messagebox.showinfo("Success", "Program Complete, Press [Enter] to continue.")
            except UnicodeEncodeError:
                messagebox.showerror("Error", "An error has occurred encoding text into " + encoder_out \
                                     + ". This typically occurs when a character is"
                                                                                  "present in the input encoder, but doesn't"
                                                                                  "exist in the output encoder.")
                print("Please try again with a different output encoder.")
            except UnicodeDecodeError:
                messagebox.showerror("Error", "An error has occurred decoding the input file using" \
                                     + encoder_in + ". Please try again with another input encoder.")

            except:
                print(sys.exc_info()[0])
                messagebox.showerror("Error", "An unexpected error has occurred.")

    # This function initializes and creates all widgets. It is the baseline for tkinter.
    def create_widgets(self):
        # Give the grid, column of each widget weight...
        for rows in range(3):
            Grid.rowconfigure(self, rows, weight=1)
        for columns in range(3):
            Grid.columnconfigure(self, columns, weight=1)

        text = "No data selected!"

        self.out_file_label.set("No file selected.")

        # File List
        self.file_list = Listbox(self, relief=GROOVE, height=8, selectmode=SINGLE)
        self.file_list.grid(row=0, column=0, sticky=W)
        with os.scandir() as listOfEntries:
            for entry in listOfEntries:
                # print all entries that are files
                if entry.is_file() and entry.name[0] != '.':
                    self.file_list.insert('end', entry.name)

        ## Encoding/Delimiter ##
        inp = Label(self, text="Input").grid(column=2, row=0, padx=20, sticky=N)
        outp = Label(self, text="Output").grid(column=3, row=0, sticky=N)
        encode = Label(self, text="Encoding").grid(column=1, row=0, pady=35, sticky=N)
        delim = Label(self, text="Delimiter").grid(column=1, row=0, pady=35, sticky=S)

        # Initialize default selected variables
        self.in_encode.set('utf-8')
        self.out_encode.set('utf-8')

        # Encoding Lists
        in_encode_list = OptionMenu(self, self.in_encode, *self.encoding_options)
        in_encode_list.grid(column=2, row=0, pady=30, sticky=N)
        out_encode_list = OptionMenu(self, self.out_encode, *self.encoding_options)
        out_encode_list.grid(column=3, row=0, pady=30, sticky=N)

        # Delimiter Entry
        # Needs self because the value will be referenced in submit()
        self.in_delim = Entry(self, width=10, justify=CENTER)
        self.in_delim.grid(column=2, row=0, pady=35, sticky=S)
        self.out_delim = Entry(self, width=10, justify=CENTER)
        self.out_delim.grid(column=3, row=0, pady=35, sticky=S)

        # Preview Button
        preview = Button(self, text="Preview", command=self.preview).grid(column=2, row=1)

        # Apply to All Checkbox
        # self.apply_all = Checkbutton(self, text="Apply to All", command=self.applyall).grid(column=2, row=0, sticky=NE)

        ## Input/Output Location ##
        input_button = Button(self, text="Input Location", command=self.set_in_file).grid(column=0, row=2, padx=15)
        output_button = Button(self, text="Output Location", command=self.set_out_file).grid(column=1, row=2, padx=15)
        output_label = Label(self, textvariable=self.out_file_label).grid(column=1, row=1)

        ## Submit/Cancel Buttons ##
        cancel = Button(self, text="Cancel", command=self.cancel).grid(column=2, row=2, padx=15, sticky=SW)
        submit = Button(self, text="Submit", command=self.submit).grid(column=3, row=2, padx=15, sticky=SE)

root = Tk()
root.title('File Encoder')
app = File_Encoder(root)

# Should end process when root.destroy() is called, but isn't working
# root.protocol("WM_DELETE_WINDOW", app.cancel)
root.mainloop()

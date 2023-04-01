import math
import tkinter as tk
from tkinter import filedialog as fd
import os
import csv
import Functions.special_fn as specialFunctions
import Functions.subordinate_fn as subordinateFunctions
from tkinter import messagebox

from Parsing import convert_str_to_num, parse_string_multi_values


#Colors
DISPLAY_LABEL_COLOR = "#E7EBEA"
BUTTON_PAD_COLOR = "#FFFFFF"
BUTTON_OPERATOR_COLOR = "#E1E1E1"
BUTTON_EQUAL_COLOR = "#F19120"
LABEL_COLOR = "#000000"
LABEL_SMALL_FONT_STYLE = ("ARIAL", 14)
LABEL_SMALLER_FONT_STYLE = ("ARIAL", 14)
LABEL_LARGE_FONT_STYLE = ("ARIAL", 35, "bold")
PAD_FONT_STYLE = ("Inter", 30)


class Eternity:
    
    """---------------------------------------------------------------------------------------------
    INITIALIZATIONS
    ---------------------------------------------------------------------------------------------"""

    def __init__(self):
        self.start = True
        self.window = tk.Tk()
        self.child_window_result = ""
        self.destroy_child = False
        self.recall_window = ""

        #set the size of the window
        self.window.geometry("700x500")
        #disable resizing
        self.window.resizable(0,0)
        self.window.title("Eternity")

        #Creating the frames
        self.display_frame = self.initialize_display_frames()
        self.buttons_frame = self.initialize_buttons_frame()

        #Creating the Labels to show total and current calculation
        self.total = ""
        self.currentCalculation = ""
        self.total_label, self.current_label = self.initialize_display_labels()
        self.savedValues = []

        #Initialize the pad buttons
        self.pad_values = {
            1: (4, 0),
            2: (4, 1),
            3: (4, 2),

            4: (3, 0),
            5: (3, 1),
            6: (3, 2),

            7: (2, 0),
            8: (2, 1),
            9: (2, 2),

            0: (5, 2),
            '.': (5,1),
            '√': (5,0)
        }

        #list of regular operations
        self.operations = {'+':'+', '-':'-', '*':'\u00d7', '/':'\u00F7'}
        #list of special operators
        self.special_operations = {'Del':'\u2190', 'e':'\u2107', 'PI': '\u03c0'}
        #list of Parenthesis
        self.parenthesis = {'(' : '\u0028', ')' : '\u0029'}
        #list of functions
        self.functions = {'Save' : 'Save', 'Gamma': '\u0393\u0028x\u0029', 'ab^n' : 'ab\u207f', 'x_power_n': 'x\u207f',  'Recall' : 'Recall', 'arccos' : 'arccos\u0028x\u0029',
                          'sinh':'sinh\u0028x\u0029','logb':'log\u2090\u0028x\u0029', 'MAD':'MAD', 'sd' : '\u03c3'
                          }

        #Initialize the buttons frame
        self.self_buttons_frame = self.initialize_buttons_frame()
        #Add the pad buttons
        self.initialize_pad_buttons()
        #add the operations buttons
        self.initialize_operators_button()
        #add the special operators
        self.initialize_special_operators_button()
        #add the equal button
        self.initialize_equal_button()
        #add the Parenthesis buttons
        self.initialize_parenthesis()
        #add functions buttons
        self.initialize_functions_buttons()

        #To Occupy all the space available
        self.self_buttons_frame.rowconfigure(0, weight=1)
        self.self_buttons_frame.columnconfigure(0, weight=1)
        for x in range(1,5):
            self.self_buttons_frame.rowconfigure(x, weight=1)
            self.self_buttons_frame.columnconfigure(x, weight=1)
        self.binding_keyboard_keys()

    #Initialize the Total and Current Calculation labels
    def initialize_display_labels(self):
        total_label = tk.Label(self.display_frame, text = self.total, anchor=tk.E, bg=DISPLAY_LABEL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        current_label = tk.Label(self.display_frame, text = self.currentCalculation, anchor=tk.E, bg=DISPLAY_LABEL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_LARGE_FONT_STYLE)
        current_label.pack(expand=True, fill="both")

        return total_label, current_label

    #Initialize the frames where the labels will reside
    def initialize_display_frames(self):
        frame = tk.Frame(self.window, height = 100, bg = DISPLAY_LABEL_COLOR)
        frame.pack(expand=True, fill="both")
        return frame
    
    #Initialize the frames where the buttons will reside
    def initialize_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    #Initialize the pad numbers
    def initialize_pad_buttons(self):
        for value, grid_loc in self.pad_values.items():
            baground_color = BUTTON_OPERATOR_COLOR
            if isinstance(value, int):
                baground_color = BUTTON_PAD_COLOR
            button = tk.Button(self.self_buttons_frame, text = str(value), bg = baground_color, fg = LABEL_COLOR, font=PAD_FONT_STYLE, borderwidth=0, padx=10, command=lambda x=value: self.add_to_current(x))
            button.grid(row=grid_loc[0], column=grid_loc[1], sticky=tk.NSEW, padx=5, pady=5)
            
    #Initialize the operations buttons
    def initialize_operators_button(self):
        i = 2
        for operator, sign in self.operations.items():
            button = tk.Button(self.self_buttons_frame, text = sign, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, padx=10, command=lambda x=operator: self.append_operation(x))
            button.grid(row = i, column = 3, sticky=tk.NSEW, padx=5, pady=5)
            i+=1

    #Initialize the special operations buttons
    def initialize_special_operators_button(self):
        i = 0
        for symbol, value in self.special_operations.items():
            baground_color = BUTTON_OPERATOR_COLOR
            font_color = LABEL_COLOR
            button = tk.Button(self.self_buttons_frame, text = value, bg = baground_color, fg = font_color, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, pady=20, command=lambda x=symbol: self.add_special_operations(x))
            button.grid(row = 1, column = i, sticky=tk.NSEW, padx=5, pady=5)
            i+=1
        
        button = tk.Button(self.self_buttons_frame, text = 'AC', bg = BUTTON_EQUAL_COLOR, fg = BUTTON_PAD_COLOR, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, command=self.clear_calculation)
        button.grid(row = 1, column = i, sticky=tk.NSEW, padx=5, pady=5)

    #Initialize the equal button
    def initialize_equal_button(self):
        button = tk.Button(self.self_buttons_frame, text = '=', bg = BUTTON_EQUAL_COLOR, fg = BUTTON_PAD_COLOR, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, command=self.evaluate_current_Calculation)
        button.grid(row = 4, column = 5, rowspan = 2, sticky=tk.NSEW, padx=5, pady=5)

    def initialize_parenthesis(self):
        i = 1
        for operator, symbol in self.parenthesis.items():
            button = tk.Button(self.self_buttons_frame, text = symbol, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, command=lambda x=operator: self.append_operation(x))
            button.grid(row = 3 + i, column = 4, sticky=tk.NSEW, padx=5, pady=5)
            i += 1
    
    def initialize_functions_buttons(self):
        i = 0
        span = 2
        _column = 4
        for function, symbol in self.functions.items():
            button = tk.Button(self.self_buttons_frame, text = symbol, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, pady=20, command=lambda x=function: self.functions_buttons_click(x))
            button.grid(row = 0 + i, column = _column, columnspan = span, sticky=tk.NSEW, padx=5, pady=5)
            i += 1
            if i > 3 and _column == 4:
                i = 0
                _column = _column + span

    """---------------------------------------------------------------------------------------------
    HANDLE BUTTONS CLICK FOR SPECIAL FUNCTIONS
    ---------------------------------------------------------------------------------------------"""

    def functions_buttons_click(self, function):
        print(function)
        if function == "ab^n":
            self.handle_functions_buttons_call("ab^n", 0, 1, 1, 1)
        if function == "Gamma":
            self.handle_functions_buttons_call("Gamma", 1, 0, 0, 0)
        if function == "x_power_n":
            self.handle_functions_buttons_call("x_power_n", 1, 1, 0, 0)
        if function == "arccos":
            self.handle_functions_buttons_call("arccos", 1, 0, 0, 0)
        if function == "sinh":
            self.handle_functions_buttons_call("sinh", 1, 0, 0, 0)
        if function == "logb":
            self.handle_functions_buttons_call("logb", 1, 0, 1, 0)
        if function == "MAD":
            self.handle_multiple_inputs("MAD")
        if function == "sd":
            self.handle_multiple_inputs("SD")
        if function == "Save":
            self.save_results(self.currentCalculation)
        if function == "Recall":
            if len(self.savedValues) > 0:
                self.recall_results("main")
            else:
                messagebox.showerror("Recall Error", "Error: There is no saved result to recall!")

    """---------------------------------------------------------------------------------------------
    CHILD WINDOW FOR MAD/SD FUNCTIONS
    ---------------------------------------------------------------------------------------------"""

    def handle_multiple_inputs(self, callingFunction):
        self.child_window_result = tk.Toplevel(self.window)
        self.child_window_result.geometry("550x150")
        self.child_window_result.grab_set()
        _width = 50
        self.child_window_result.resizable(0, 0)
        self.child_window_result.x_input = tk.Entry()
        self.child_window_result.x = tk.StringVar()
        
        frame = tk.Frame( self.child_window_result, height = 50, bg = BUTTON_EQUAL_COLOR)
        frame.pack(expand=True, fill="both")
        function_name = ""
        for function, functionName in self.functions.items():
            if callingFunction == function:
                function_name = str(functionName)
                break
        self.child_window_result.title("Input for function: " + function_name)

        isSample = True

        x_label = tk.Label(frame, text="Values seprated by ',' :",  bg=BUTTON_EQUAL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
        x_label.grid(row=1, column=1, sticky=tk.E + tk.W, padx=5, pady=5)

        self.child_window_result.input = tk.StringVar()
        self.child_window_result.input.trace('w', self.validate_input_mad_sd)

        self.child_window_result.x_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_result.x, width=_width)
        self.child_window_result.x_input.grid(row=1, column=2, sticky=tk.E + tk.W, padx=5, pady=5)

        button_calc = tk.Button(frame, text="Calculate", command= lambda:self.calculate_using_inputedValues(isSample, callingFunction))
        button_calc.grid(row=2, column= 2, padx=5, pady=5,sticky = tk.E + tk.W)

        y_label = tk.Label(frame, text="Or Import a CSV file: ",  bg=BUTTON_EQUAL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
        y_label.grid(row=3, column=1, sticky=tk.E + tk.W, padx=5, pady=5)

        button = tk.Button(frame, text="Import", command = lambda:self.open_file_dialogue(isSample, callingFunction))
        button.grid(row=3, column= 2, padx=5, pady=5,sticky = tk.E + tk.W)

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)

    def validate_input_mad_sd(self, *args):
        legalCharachters = set("123456789.,")
        if len(self.child_window_result.x_input.get()) > 0:
            if not legalCharachters.issuperset(str(self.child_window_result.x_input.get()[-1]).strip()):
                self.child_window_result.x_input.delete(len(str(self.child_window_result.x_input.get())) - 1, tk.END)
        
    def calculate_using_inputedValues(self, isSample, callingFunction):
        input = str(self.child_window_result.x_input.get())
        array = input.split(',')
        data_points_floats = [float(i) for i in array]
        if callingFunction == "MAD":
                result = specialFunctions.mad(data_points_floats)
                fnName = "MAD = " + str(result)
        elif callingFunction == "SD":
                result = specialFunctions.standard_deviation(data_points_floats, isSample)
                fnName = "SD = " + str(result)
        self.total_label.config(text = fnName)
        self.currentCalculation = str(result)
        self.update_current()
        self.child_window_result.destroy()

    def open_file_dialogue(self, isSample, callingFunction):
        self.child_window_result.x_input.delete(0, tk.END)
        #Launch the dialogue in the same directory where the application is running
        filepath = fd.askopenfilename(initialdir=os.getcwd(), title="File to import", filetypes=(("CSV", "*.csv"),))
        with open(filepath, 'r') as file:
            #print(file.read())
            csvreader = csv.reader(file, delimiter=',')
            data_points = []
            for row in csvreader:
                for i in range(len(row)):
                    data_points.append(row[i])
            sum = 0
            # for i in range(len(data_points)):
            #     sum += int(data_points[i])
            #print("AVG: " + str((sum / len(data_points))))
            data_points_floats = [float(i) for i in data_points]
            #print(specialFunctions.mad(data_points_floats))
            fnName = ""
            result = 0.0
            if callingFunction == "MAD":
                result = specialFunctions.mad(data_points_floats)
                fnName = "MAD = " + str(result)
            elif callingFunction == "SD":
                result = specialFunctions.standard_deviation(data_points_floats, isSample)
                fnName = "SD = " + str(result)
            self.total_label.config(text = fnName)
            self.currentCalculation = str(result)
            self.update_current()
            self.child_window_result.destroy()

            #print(data_points)

    """---------------------------------------------------------------------------------------------
    CHILD WINDOW FOR ARCCOS/SINH(X)/GAMMA/X^Y/AB^X/LOGB(X)
    ---------------------------------------------------------------------------------------------"""

    def handle_functions_buttons_call(self, *arg):
        labels = ['x', 'n', 'a', 'b']
        self.child_window_result = tk.Toplevel(self.window)
        self.child_window_result.geometry("500x300")
        _width = 20
        self.child_window_result.resizable(1, 1)
        self.child_window_result.x = tk.StringVar()
        self.child_window_result.n = tk.StringVar()
        self.child_window_result.a = tk.StringVar()
        self.child_window_result.b = tk.StringVar()

        self.child_window_result.x_input = tk.Entry()
        self.child_window_result.n_input = tk.Entry()
        self.child_window_result.a_input = tk.Entry()
        self.child_window_result.b_input = tk.Entry()

        frame_button = tk.Frame( self.child_window_result, height = 250, bg = BUTTON_EQUAL_COLOR)
        frame_button.pack(expand=True, fill="both", anchor=tk.CENTER)
        frame = tk.Frame( frame_button, height = 250, bg = BUTTON_EQUAL_COLOR)
        #frame.pack(expand=True, fill="both", anchor=tk.CENTER)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        function_name = ""
        for function, functionName in self.functions.items():
            if arg[0] == function:
                function_name = str(functionName)
                break
        self.child_window_result.title("Input for function: " + function_name)

        i = 1
        for symbol, value in self.special_operations.items():
            if (symbol != "Del"):
                baground_color = BUTTON_OPERATOR_COLOR
                font_color = LABEL_COLOR
                button = tk.Button(frame, text = value, bg = baground_color, fg = font_color, font = PAD_FONT_STYLE, borderwidth = 0, command=lambda x=symbol: self.child_add_special_operations(x))
                button.grid(row = 0, column = i, sticky=tk.W, padx=5, pady=5)
                i+=1
        
        button_sqrt = tk.Button(frame, text = "√", bg = baground_color, fg = font_color, font = PAD_FONT_STYLE, borderwidth = 0, command=lambda x="sqrt": self.child_add_special_operations(x))
        button_sqrt.grid(row = 0, column = i, sticky=tk.NSEW, padx=5, pady=5)
        i += 1
        button_recall = tk.Button(frame, text = "Recall", bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, command=lambda x="recall": self.child_add_special_operations(x))
        button_recall.grid(row = 0, column = i, columnspan = 3, sticky=tk.NSEW, padx=5, pady=5)

        if (arg[1] != 0):
            x_label = tk.Label(frame, text="x:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            x_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_result.x_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_result.x, width=_width)
            self.child_window_result.x_input.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
            self.child_window_result.x_input.focus()
        
        if (arg[2] != 0):
            n_label = tk.Label(frame, text="n:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            n_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_result.n_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_result.n, width=_width)
            self.child_window_result.n_input.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
            if (arg[1] == 0):
                self.child_window_result.n_input.focus()
        
        if (arg[3] != 0):
            a_label = tk.Label(frame, text="a:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            a_label.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_result.a_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_result.a, width=_width)
            self.child_window_result.a_input.grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)

        if (arg[4] != 0):
            b_label = tk.Label(frame, text="b:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            b_label.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_result.b_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_result.b, width=_width, borderwidth = 0)
            self.child_window_result.b_input.grid(row=4, column=2, sticky=tk.W, padx=5, pady=5)
        
        # frame.rowconfigure(0, weight=1)
        # frame.columnconfigure(0, weight=1)

         #Order of arguments: x, n, a, b
        button = tk.Button(frame, text="Calculate", command=lambda x = arg[0]: self.validate_and_execute_special_fn(x), width=20, pady=5)
        button.grid(row=5, column= 1, columnspan=3, padx=5, pady=5)

    # input e/pi/square root/recall values in current textbox
    def child_add_special_operations(self, symbol):
        value = 0
        entry = self.child_window_result.focus_get()
        if isinstance(entry, tk.Entry):
            if symbol == 'e':
                value = str(subordinateFunctions.EULER)
            if symbol == 'PI':
                value = str(subordinateFunctions.PI)
            if symbol == 'sqrt':
                if len(entry.get()) > 0:
                    value = subordinateFunctions.sqrt(convert_str_to_num(entry.get()))
            if symbol == "recall":
                value = self.recall_results("child", entry)
                return
            entry.delete(0, tk.END)
            entry.insert(0, value)

    # method to validate each input variable of a function and call execute function if validated True
    def validate_and_execute_special_fn(self, function):
        if (function == "Gamma"):
            x = self.child_window_result.x_input.get()
            if (self.is_a_number(x) and convert_str_to_num(x) > 0):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter a real number greater than 0!")
        if (function == "sinh"):
            x = self.child_window_result.x_input.get()
            if (self.is_a_number(x)):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter a real number!")
        if (function == "arccos"):
            x = self.child_window_result.x_input.get()
            if (self.is_a_number(x) and convert_str_to_num(x) >= -1 and convert_str_to_num(x) <= 1):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter a real number between -1 and 1!")
        if (function == "ab^n"):
            a = self.child_window_result.a_input.get()
            b = self.child_window_result.b_input.get()
            n = self.child_window_result.n_input.get()
            if (self.is_a_number(a, b, n)):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter a real numbers for a, b, n!")
        if (function == "x_power_n"):
            x = self.child_window_result.x_input.get()
            n = self.child_window_result.n_input.get()
            if (self.is_a_number(x, n)):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter real numbers for x, n!")
        if (function == "logb"):
            x = self.child_window_result.x_input.get()
            a = self.child_window_result.a_input.get()
            if (self.is_a_number(x, a) and convert_str_to_num(a) != 1 and convert_str_to_num(x) > 0 and convert_str_to_num(a) > 0):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Error: Please enter real numbers greater than 0 for a, x and a cannot be 1!")

    # method to check if passed string(s) can be converted to a number
    def is_a_number(self, str1 = None, str2 = None, str3 = None, str4 = None):
        for s in (str1, str2, str3, str4):
            if (s is not None):
                if (convert_str_to_num(s) is None):
                    return False
        return True
        

    """---------------------------------------------------------------------------------------------
    EXECUTE SPECIAL FUNCTIONS
    ---------------------------------------------------------------------------------------------"""

    # method to perform calculations for special functions
    def execute_function(self, function):
        print("Clicked! " + function)
        if (function == "MAD" or function == "SD"):
            self.child_window_result.x = self.child_window_result.x_input.get()
        else:
            self.child_window_result.x = self.child_window_result.x_input.get()
            self.child_window_result.n = self.child_window_result.n_input.get()
            self.child_window_result.a = self.child_window_result.a_input.get()
            self.child_window_result.b = self.child_window_result.b_input.get()

        #Here is where we will call our functions
        # 3 real numbers
        if function == "ab^n":
            self.total_label.config(text = self.child_window_result.a + "*" + self.child_window_result.b + "**" + self.child_window_result.n)
            self.currentCalculation = str(specialFunctions.natural_exp(convert_str_to_num(self.child_window_result.a), convert_str_to_num(self.child_window_result.b), convert_str_to_num(self.child_window_result.n)))
            self.update_current()
        # 1 real numbers > 0
        if function == "Gamma":
            self.total_label.config(text = "Γ(" + self.child_window_result.x + ")")
            self.currentCalculation = str(specialFunctions.gamma(convert_str_to_num(self.child_window_result.x)))
            self.update_current()
        # 2 real numbers
        if function == "x_power_n":
            self.total_label.config(text = self.child_window_result.x + "**" + self.child_window_result.n)
            self.currentCalculation = str(specialFunctions.power(convert_str_to_num(self.child_window_result.x), convert_str_to_num(self.child_window_result.n)))
            self.update_current()
        # 1 x between -1 and 1
        if function == "arccos":
            self.total_label.config(text = "arccos(" + self.child_window_result.x + ")")
            self.currentCalculation = str(specialFunctions.arccos(convert_str_to_num(self.child_window_result.x)))
            self.update_current()
        # 1 real number
        if function == "sinh":
            self.total_label.config(text = "sinh(" + self.child_window_result.x + ")")
            self.currentCalculation = str(specialFunctions.sinh(convert_str_to_num(self.child_window_result.x)))
            self.update_current()
        # x, b > 0, b != 1
        if function == "logb":
            self.total_label.config(text = "log" + self.child_window_result.a + "(" + self.child_window_result.x + ")")
            self.currentCalculation = str(math.log(convert_str_to_num(self.child_window_result.x), convert_str_to_num(self.child_window_result.a)))
            self.update_current()
        self.child_window_result.destroy()        

    """---------------------------------------------------------------------------------------------
    SAVE/RECALL OPERATIONS
    ---------------------------------------------------------------------------------------------"""
    
    # save the results from current calculation
    def save_results(self, currentCalculation):
        # only allow 7 saves, remove earliest save if exceeding 7
        if (len(self.savedValues) >= 7):
            self.savedValues = self.savedValues[1:]
        value_to_save = convert_str_to_num(currentCalculation)
        if (currentCalculation != "" and value_to_save is not None):
            # if the value is a valid number, add to array of saved results
            self.savedValues.append(value_to_save)
        else:
            # otherwise output error window
            messagebox.showerror("Save Error", "Error: Need a valid number to save!")

    # recall results that were saved
    def recall_results(self, main_or_child, entry=None):
        # create window
        self.recall_window = tk.Toplevel(self.window)
        self.recall_window.geometry("300x340")
        self.recall_window.grab_set()
        self.recall_window.resizable(0, 0)
        frame = tk.Frame(self.recall_window, height = 50, bg = BUTTON_EQUAL_COLOR)
        frame.pack(expand=True, fill="both")
        self.recall_window.title("Recall")

        # message to inform user they can recall up to 7 values
        message = tk.Label(frame, text="Recall up to 7 saved results", bg=BUTTON_EQUAL_COLOR, fg = LABEL_COLOR, padx=25, font=LABEL_SMALLER_FONT_STYLE)
        message.grid(row=1, column=1, columnspan=2, sticky=tk.E + tk.W, padx=5, pady=5)

        # create Listbox to display all values saved
        listbox_saved_values = tk.Listbox(frame, selectmode=tk.SINGLE, font=LABEL_SMALLER_FONT_STYLE)
        listbox_saved_values.grid(row=2, column=1, columnspan=2, sticky=tk.E + tk.W, padx=5, pady=5)
        for value in self.savedValues:
            listbox_saved_values.insert(tk.END, value)
        
        # automatically select the 1st value
        listbox_saved_values.select_set(0)
  
        # create delete button and when clicked, calls method to delete the selected value
        button_del = tk.Button(frame, text="Delete", font=LABEL_SMALLER_FONT_STYLE, command=lambda:self.remove_saved_value(listbox_saved_values))
        button_del.grid(row=3, column=1, padx=5, pady=5,sticky = tk.E + tk.W)
        
        # create a recall button, which behaves differently if we recall to the main window or a child window
        button_recall = tk.Button(frame, text="Recall", font=LABEL_SMALLER_FONT_STYLE, command = lambda:self.recall_saved_value(listbox_saved_values, main_or_child, entry))
        button_recall.grid(row=3, column=2, padx=5, pady=5,sticky = tk.E + tk.W)

    # method to remove a certain saved value
    def remove_saved_value(self, listbox):
        selected_entry = listbox.curselection()
        # output error window if there's no entry to delete
        if (len(selected_entry) == 0):
            messagebox.showerror("Delete Error", "Error: There is no saved result to delete!")
        # delete the entry from listbox and array of saved values
        selected_value = listbox.get(selected_entry[0])
        listbox.delete(selected_entry)
        self.savedValues.remove(selected_value)
        # select the 1st entry again (if available)
        listbox.select_set(0)

    # method to recall a saved value to the main window or a child window
    def recall_saved_value(self, listbox, main_or_child, entry):
        selected_entry = listbox.curselection()
        # output error window if there's no entry to delete
        if (len(selected_entry) == 0):
            messagebox.showerror("Recall Error", "Error: There is no saved result to recall!")
        selected_value = listbox.get(selected_entry[0])
        # if recalling to main, add the value to main window's current calculation label
        if (main_or_child == "main"):
            self.currentCalculation = ""
            self.add_to_current(convert_str_to_num(selected_value))
        # if recalling to child, replace whatever's in textbox with the recalled value
        else:
            entry.delete(0, tk.END)
            entry.insert(0, convert_str_to_num(selected_value))
        # close recall window
        self.recall_window.destroy()

    """---------------------------------------------------------------------------------------------
    OTHER CALCULATOR OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    def clear_variables(self):
        self.child_window_result = ""

    def add_special_operations(self, addedvalue):
        #        self.special_operations = {'Del':'\u2190', 'e':'\u2107', 'PI': '\u03c0'}
        if addedvalue == 'Del':
            self.currentCalculation = self.currentCalculation[0:len(self.currentCalculation) - 1]
        if addedvalue == 'e':
            self.currentCalculation = str(subordinateFunctions.EULER)
        if addedvalue == 'PI':
            self.currentCalculation = str(subordinateFunctions.PI)
        self.update_current()

    #Add the number to the current Calculation
    def add_to_current(self, addedvalue):
        value_to_add = addedvalue
        if addedvalue == '.':
          if self.currentCalculation.find('.') > 0:
              value_to_add = ""
        self.currentCalculation += str(value_to_add)
        self.update_current()

    #Add the operation to the current Calculation
    def append_operation(self, operator):
        self.currentCalculation += operator
        self.total += self.currentCalculation
        self.currentCalculation = ""
        self.update_total()
        self.update_current()

    #Update the total label
    def update_total(self):
        totalCalculation = self.total
        for operator, sign in self.operations.items():
            totalCalculation = totalCalculation.replace(operator, f' {sign} ')
        self.total_label.config(text = totalCalculation)

    #Update the current calculation label
    def update_current(self):
        self.current_label.config(text = self.currentCalculation)

    #Clear both the Total and the Current Calculation labels
    def clear_calculation(self):
        self.total = ""
        self.currentCalculation = ""
        self.update_total()
        self.update_current()
    
    #Evaluate the current calculation
    def evaluate_current_Calculation(self):
        self.total += self.currentCalculation
        self.update_total()

        try:
            self.currentCalculation = str(eval(self.total))
            self.total = ""
        except Exception as error:
            self.currentCalculation = "Error: "
            #tk.Message(error)
        finally:
            self.update_current()

    def binding_keyboard_keys(self):
        self.window.bind("<Return>", lambda event:self.evaluate_current_Calculation())
        
        for value in self.pad_values:
            if value != "√":
                self.window.bind(str(value), lambda event, addedValue=value: self.add_to_current(addedValue))
        
        for operator in self.operations:
            self.window.bind(operator, lambda event, operatation = operator: self.append_operation(operatation))


    """---------------------------------------------------------------------------------------------
    RUN CALCULATOR
    ---------------------------------------------------------------------------------------------"""
    
    def run(self):
        self.window.mainloop()




if __name__ == "__main__":
    myEternity = Eternity()
    myEternity.run()




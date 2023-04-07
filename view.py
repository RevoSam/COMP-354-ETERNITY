import tkinter as tk

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

# View class for Eternity
class EternityView:

    """---------------------------------------------------------------------------------------------
    MAIN WINDOW
    ---------------------------------------------------------------------------------------------"""

    # Constructor
    def __init__(self, controller):
        # view holds reference to controller
        self.controller = controller

        self.window = tk.Tk()
        self.child_window_functions = ""
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
        self.total_label, self.current_label = self.initialize_display_labels()

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
        total_label = tk.Label(self.display_frame, text = self.controller.get_model().get_total(), anchor=tk.E, bg=DISPLAY_LABEL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        current_label = tk.Label(self.display_frame, text = self.controller.get_model().get_current_calculation(), anchor=tk.E, bg=DISPLAY_LABEL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_LARGE_FONT_STYLE)
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
            button = tk.Button(self.self_buttons_frame, text = str(value), bg = baground_color, fg = LABEL_COLOR, font=PAD_FONT_STYLE, borderwidth=0, padx=10, command=lambda x=value: self.controller.add_to_current(x))
            button.grid(row=grid_loc[0], column=grid_loc[1], sticky=tk.NSEW, padx=5, pady=5)
            
    #Initialize the operations buttons
    def initialize_operators_button(self):
        i = 2
        for operator, sign in self.operations.items():
            button = tk.Button(self.self_buttons_frame, text = sign, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, padx=10, command=lambda x=operator: self.controller.append_operation(x))
            button.grid(row = i, column = 3, sticky=tk.NSEW, padx=5, pady=5)
            i+=1

    #Initialize the special operations buttons
    def initialize_special_operators_button(self):
        i = 0
        for symbol, value in self.special_operations.items():
            baground_color = BUTTON_OPERATOR_COLOR
            font_color = LABEL_COLOR
            button = tk.Button(self.self_buttons_frame, text = value, bg = baground_color, fg = font_color, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, pady=20, command=lambda x=symbol: self.controller.add_special_operations(x))
            button.grid(row = 1, column = i, sticky=tk.NSEW, padx=5, pady=5)
            i+=1
        
        button = tk.Button(self.self_buttons_frame, text = 'AC', bg = BUTTON_EQUAL_COLOR, fg = BUTTON_PAD_COLOR, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, command=self.controller.clear_calculation)
        button.grid(row = 1, column = i, sticky=tk.NSEW, padx=5, pady=5)

    #Initialize the equal button
    def initialize_equal_button(self):
        button = tk.Button(self.self_buttons_frame, text = '=', bg = BUTTON_EQUAL_COLOR, fg = BUTTON_PAD_COLOR, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, command=self.controller.calculate_result)
        button.grid(row = 4, column = 5, rowspan = 2, sticky=tk.NSEW, padx=5, pady=5)

    def initialize_parenthesis(self):
        i = 1
        for operator, symbol in self.parenthesis.items():
            button = tk.Button(self.self_buttons_frame, text = symbol, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, command=lambda x=operator: self.controller.append_operation(x))
            button.grid(row = 3 + i, column = 4, sticky=tk.NSEW, padx=5, pady=5)
            i += 1
    
    def initialize_functions_buttons(self):
        i = 0
        span = 2
        _column = 4
        for function, symbol in self.functions.items():
            button = tk.Button(self.self_buttons_frame, text = symbol, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = LABEL_SMALLER_FONT_STYLE, borderwidth = 0, padx=10, pady=20, command=lambda x=function: self.controller.functions_buttons_click(x))
            button.grid(row = 0 + i, column = _column, columnspan = span, sticky=tk.NSEW, padx=5, pady=5)
            i += 1
            if i > 3 and _column == 4:
                i = 0
                _column = _column + span

    """---------------------------------------------------------------------------------------------
    CHILD WINDOW FOR MAD/SD
    ---------------------------------------------------------------------------------------------"""

    # create the child window for multiple values input functions like MAD / SD
    def create_mad_sd_window(self, callingFunction):
        self.child_window_functions = tk.Toplevel(self.window)
        self.child_window_functions.geometry("640x220")
        self.child_window_functions.grab_set()
        _width = 50
        self.child_window_functions.resizable(0, 0)
        self.child_window_functions.x_input = tk.Entry()
        self.child_window_functions.x = tk.StringVar()
        
        frame = tk.Frame( self.child_window_functions, height = 50, bg = BUTTON_EQUAL_COLOR)
        frame.pack(expand=True, fill="both")
        function_name = ""
        for function, functionName in self.functions.items():
            if callingFunction == function:
                function_name = str(functionName)
                break
        self.child_window_functions.title("Input for function: " + function_name)
        x_label = tk.Label(frame, text="Values seprated by ',' :",  bg=BUTTON_EQUAL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
        x_label.grid(row=1, column=1, sticky=tk.E + tk.W, padx=5, pady=5)
        
        isSample = True

        if (callingFunction == "SD"):
            isSample = tk.IntVar()
            sample_chkbox = tk.Checkbutton(frame, text="Sample", variable=isSample, bg=BUTTON_EQUAL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            sample_chkbox.grid(row=2, column=1, sticky=tk.E + tk.W, padx=5, pady=5)

        self.child_window_functions.input = tk.StringVar()
        self.child_window_functions.input.trace('w', self.controller.validate_input_mad_sd())

        self.child_window_functions.x_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_functions.x, width=_width)
        self.child_window_functions.x_input.grid(row=1, column=2, sticky=tk.E + tk.W, padx=5, pady=5)
        self.child_window_functions.x_input.focus()

        button_calc = tk.Button(frame, text="Calculate", command= lambda:self.controller.validate_and_calculate_using_inputedValues(isSample, callingFunction))
        button_calc.grid(row=2, column= 2, padx=5, pady=5,sticky = tk.E + tk.W)

        y_label = tk.Label(frame, text="Or Import a CSV file: ",  bg=BUTTON_EQUAL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
        y_label.grid(row=3, column=1, sticky=tk.E + tk.W, padx=5, pady=5)

        button = tk.Button(frame, text="Import", command = lambda:self.controller.open_file_dialogue(isSample, callingFunction))
        button.grid(row=3, column= 2, padx=5, pady=5,sticky = tk.E + tk.W)

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)

    """---------------------------------------------------------------------------------------------
    CHILD WINDOW FOR ARCCOS/SINH(X)/GAMMA/X^Y/AB^X/LOGB(X)
    ---------------------------------------------------------------------------------------------"""

    # create child windows for other Eternity special functions
    def create_special_function_window(self, *arg):
        # create window layout
        self.child_window_functions = tk.Toplevel(self.window)
        self.child_window_functions.geometry("500x300")
        _width = 20
        self.child_window_functions.grab_set()
        self.child_window_functions.resizable(1, 1)
        
        self.child_window_functions.x = tk.StringVar()
        self.child_window_functions.n = tk.StringVar()
        self.child_window_functions.a = tk.StringVar()
        self.child_window_functions.b = tk.StringVar()
        
        self.child_window_functions.x_input = tk.Entry()
        self.child_window_functions.n_input = tk.Entry()
        self.child_window_functions.a_input = tk.Entry()
        self.child_window_functions.b_input = tk.Entry()

        frame_button = tk.Frame( self.child_window_functions, height = 250, bg = BUTTON_EQUAL_COLOR)
        frame_button.pack(expand=True, fill="both", anchor=tk.CENTER)
        frame = tk.Frame( frame_button, height = 250, bg = BUTTON_EQUAL_COLOR)
        #frame.pack(expand=True, fill="both", anchor=tk.CENTER)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        function_name = ""
        for function, functionName in self.functions.items():
            if arg[0] == function:
                function_name = str(functionName)
                break
        self.child_window_functions.title("Input for function: " + function_name)

        i = 1
        for symbol, value in self.special_operations.items():
            if (symbol != "Del"):
                baground_color = BUTTON_OPERATOR_COLOR
                font_color = LABEL_COLOR
                button = tk.Button(frame, text = value, bg = baground_color, fg = font_color, font = PAD_FONT_STYLE, borderwidth = 0, command=lambda x=symbol: self.controller.child_add_special_operations(x))
                button.grid(row = 0, column = i, sticky=tk.W, padx=5, pady=5)
                i+=1
        
        button_sqrt = tk.Button(frame, text = "√", bg = baground_color, fg = font_color, font = PAD_FONT_STYLE, borderwidth = 0, command=lambda x="sqrt": self.controller.child_add_special_operations(x))
        button_sqrt.grid(row = 0, column = i, sticky=tk.NSEW, padx=5, pady=5)
        i += 1
        button_recall = tk.Button(frame, text = "Recall", bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, command=lambda x="recall": self.controller.child_add_special_operations(x))
        button_recall.grid(row = 0, column = i, columnspan = 3, sticky=tk.NSEW, padx=5, pady=5)

        if (arg[1] != 0):
            x_label = tk.Label(frame, text="x:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            x_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_functions.x_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_functions.x, width=_width)
            self.child_window_functions.x_input.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
            self.child_window_functions.x_input.focus()
        
        if (arg[2] != 0):
            n_label = tk.Label(frame, text="n:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            n_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_functions.n_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_functions.n, width=_width)
            self.child_window_functions.n_input.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
            if (arg[1] == 0):
                self.child_window_functions.n_input.focus()
        
        if (arg[3] != 0):
            a_label = tk.Label(frame, text="a:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            a_label.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_functions.a_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_functions.a, width=_width)
            self.child_window_functions.a_input.grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)

        if (arg[4] != 0):
            b_label = tk.Label(frame, text="b:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            b_label.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_functions.b_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_functions.b, width=_width, borderwidth = 0)
            self.child_window_functions.b_input.grid(row=4, column=2, sticky=tk.W, padx=5, pady=5)
        
        # frame.rowconfigure(0, weight=1)
        # frame.columnconfigure(0, weight=1)

         #Order of arguments: x, n, a, b
        button = tk.Button(frame, text="Calculate", command=lambda x = arg[0]: self.controller.validate_and_execute_special_fn(x), width=20, pady=5)
        button.grid(row=5, column= 1, columnspan=3, padx=5, pady=5)

    """---------------------------------------------------------------------------------------------
    RECALL WINDOW
    ---------------------------------------------------------------------------------------------"""

    # create recall window displaying results that were saved
    def create_recall_window(self, main_or_child, entry=None):
        # create window layout
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
        savedValues = self.controller.get_model().get_saved_results()
        for value in savedValues:
            listbox_saved_values.insert(tk.END, value)
        
        # automatically select the 1st value
        listbox_saved_values.select_set(0)
  
        # create delete button and when clicked, calls method to delete the selected value
        button_del = tk.Button(frame, text="Delete", font=LABEL_SMALLER_FONT_STYLE, command=lambda:self.controller.remove_saved_value(listbox_saved_values, main_or_child))
        button_del.grid(row=3, column=1, padx=5, pady=5,sticky = tk.E + tk.W)
        
        # create a recall button, which behaves differently if we recall to the main window or a child window
        button_recall = tk.Button(frame, text="Recall", font=LABEL_SMALLER_FONT_STYLE, command = lambda:self.controller.recall_saved_value(listbox_saved_values, main_or_child, entry))
        button_recall.grid(row=3, column=2, padx=5, pady=5,sticky = tk.E + tk.W)

    """---------------------------------------------------------------------------------------------
    UI OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    # update the current calculation label
    def update_current_label(self, str):
        self.current_label.config(text = str)

    # update the total calculation label
    def update_total_label(self, str):
        self.total_label.config(text = str)

    # Keyboard binding
    def binding_keyboard_keys(self):
        self.window.bind("<Return>", lambda event:self.controller.calculate_result())
        
        for value in self.pad_values:
            if value != "√":
                self.window.bind(str(value), lambda event, addedValue=value: self.controller.add_to_current(addedValue))
        
        for operator in self.operations:
            self.window.bind(operator, lambda event, operatation = operator: self.controller.append_operation(operatation))

    """---------------------------------------------------------------------------------------------
    MAIN METHOD
    ---------------------------------------------------------------------------------------------"""
    
    # runs tk mainloop
    def main(self):
        self.window.mainloop()
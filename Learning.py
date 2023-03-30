import tkinter as tk
from tkinter import filedialog as fd
import math as xMath
import os
import csv
import Functions.special_fn as specialFunctions

#Colors
DISPLAY_LABEL_COLOR = "#E7EBEA"
BUTTON_PAD_COLOR = "#FFFFFF"
BUTTON_OPERATOR_COLOR = "#E7EBEA"
BUTTON_EQUAL_COLOR = "#F19120"
LABEL_COLOR = "#000000"
LABEL_SMALL_FONT_STYLE = ("ARIAL", 14)
LABEL_LARGE_FONT_STYLE = ("ARIAL", 35, "bold")
PAD_FONT_STYLE = ("Inter", 30)


class Eternity:
    def __init__(self):

        self.start = True
        self.window = tk.Tk()
        self.child_window_result = ""
        self.destroy_child = False

        #set the size of the window
        self.window.geometry("700x500")
        #disable resizing
        self.window.resizable(0,0)
        self.window.title("Eternity")

        #Creating the frames
        self.display_frame = self.initialize_display_frames()
        self_buttons_frame = self.initialize_buttons_frame()

        #Creating the Labels to show total and current calculation
        self.total = ""
        self.currentCalculation = ""
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
        self.functions = {'Save' : 'Save', 'Gamma': '\u0393\u0028x\u0029', 'ab^n' : 'ab\u207f', 'x_power_n': 'x\u207f',  'Recal' : 'Recall', 'arccos' : 'arccos\u0028x\u0029',
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
            button.grid(row = i, column = 3, sticky=tk.NSEW)
            i+=1

    #Initialize the special operations buttons
    def initialize_special_operators_button(self):
        i = 0
        for symbol, value in self.special_operations.items():
            baground_color = BUTTON_OPERATOR_COLOR
            font_color = LABEL_COLOR
            button = tk.Button(self.self_buttons_frame, text = value, bg = baground_color, fg = font_color, font = PAD_FONT_STYLE, borderwidth = 0, padx=10, command=lambda x=symbol: self.add_special_operations(x))
            button.grid(row = 1, column = i, sticky=tk.NSEW)
            i+=1
        
        button = tk.Button(self.self_buttons_frame, text = 'AC', bg = BUTTON_EQUAL_COLOR, fg = BUTTON_PAD_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, padx=10, command=self.clear_calculation)
        button.grid(row = 1, column = i, sticky=tk.NSEW)

    #Initialize the equal button
    def initialize_equal_button(self):
        button = tk.Button(self.self_buttons_frame, text = '=', bg = BUTTON_EQUAL_COLOR, fg = BUTTON_PAD_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, padx=10, command=self.evaluate_current_Calculation)
        button.grid(row = 4, column = 5, rowspan = 2, sticky=tk.NSEW)

    def initialize_parenthesis(self):
        i = 1
        for operator, symbol in self.parenthesis.items():
            button = tk.Button(self.self_buttons_frame, text = symbol, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, padx=10, command=lambda x=operator: self.append_operation(x))
            button.grid(row = 3 + i, column = 4, sticky=tk.NSEW)
            i += 1
    
    def initialize_functions_buttons(self):
        i = 0
        span = 2
        _column = 4
        for function, symbol in self.functions.items():
            button = tk.Button(self.self_buttons_frame, text = symbol, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, padx=10, command=lambda x=function: self.functions_buttons_click(x))
            button.grid(row = 0 + i, column = _column, columnspan = span, sticky=tk.NSEW)
            i += 1
            if i > 3 and _column == 4:
                i = 0
                _column = _column + span
    
    def functions_buttons_click(self, function):
        #        self.functions = {'Save' : 'Save', 'Gamma': '\u0393\u0028x\u0029', 'ab^n' : 'ab\u207f', 'x_power_n': 'x\u207f',  'Recal' : 'Recall', 'arccos' : 'arccos\u0028x\u0029',
        #                  'sinh':'sinh\u0028x\u0029','logb':'log\u2090\u0028x\u0029', 'MAD':'MAD', 'sd' : '\u03c3'
        #                 }
        #Order of arguments: x, n, a, b
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
        

    def handle_multiple_inputs(self, callingFunction):
        i = 1
        self.child_window_result = tk.Toplevel(self.window)
        self.child_window_result.geometry("550x100")
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



        x_label = tk.Label(frame, text="Values seprated by ',':",  bg=BUTTON_EQUAL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
        x_label.grid(row=1, column=1, sticky=tk.E + tk.W, padx=5, pady=5)

        self.child_window_result.x_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_result.x, width=_width)
        self.child_window_result.x_input.grid(row=1, column=2, sticky=tk.E + tk.W, padx=5, pady=5)

        y_label = tk.Label(frame, text="Or Import a CSV file: ",  bg=BUTTON_EQUAL_COLOR, fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
        y_label.grid(row=2, column=1, sticky=tk.E + tk.W, padx=5, pady=5)

        button = tk.Button(frame, text="Import", command= self.open_file_dialogue)
        button.grid(row=2, column= 2, padx=5, pady=5,sticky = tk.E + tk.W)

        
        self.child_window_result.rowconfigure(1, weight=1)
        self.child_window_result.columnconfigure(1, weight=1)

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)

        



    def open_file_dialogue(self):
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
            for i in range(len(data_points)):
                sum += int(data_points[i])
            #print("AVG: " + str((sum / len(data_points))))
            data_points_floats = [float(i) for i in data_points]
            print(specialFunctions.mad(data_points_floats))
            #print(data_points)



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
            if symbol != "Del":
                baground_color = BUTTON_OPERATOR_COLOR
                font_color = LABEL_COLOR
                button = tk.Button(frame, text = value, bg = baground_color, fg = font_color, font = PAD_FONT_STYLE, borderwidth = 0, command=lambda x=symbol: self.child_add_special_operations(x))
                button.grid(row = 0, column = i, sticky=tk.W, padx=5, pady=5)
                i+=1
        
        button_sqrt = tk.Button(frame, text = "√", bg = baground_color, fg = font_color, font = PAD_FONT_STYLE, borderwidth = 0, command=lambda x="sqrt": self.child_add_special_operations(x))
        button_sqrt.grid(row = 0, column = i, sticky=tk.NSEW, padx=5, pady=5)
        i += 1
        button_recall = tk.Button(frame, text = "Recall", bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, command=lambda x=function: print("Not Implemented"))
        button_recall.grid(row = 0, column = i, columnspan = 3, sticky=tk.NSEW, padx=5, pady=5)

        if (arg[1] != 0):
            x_label = tk.Label(frame, text="x:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            x_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_result.x_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_result.x, width=_width)
            self.child_window_result.x_input.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        if (arg[2] != 0):
            n_label = tk.Label(frame, text="n:",  fg = LABEL_COLOR, padx=25, font = LABEL_SMALL_FONT_STYLE)
            n_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

            self.child_window_result.n_input = tk.Entry(frame, bg=BUTTON_PAD_COLOR, textvariable=self.child_window_result.n, width=_width)
            self.child_window_result.n_input.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        
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

        # frame.rowconfigure(1, weight=1)
        # frame.columnconfigure(1, weight=1)

         #Order of arguments: x, n, a, b
        button = tk.Button(frame, text="Submit", command=lambda x = arg[0]: self.execute_function(x), width=20, pady=5)
        button.grid(row=5, column= 1, columnspan=3, padx=5, pady=5)

    def child_add_special_operations(self, symbol):
        value = 0
        entry = self.child_window_result.focus_get()
        if isinstance(entry, tk.Entry):
            if symbol == 'e':
                value = str(xMath.e)
            if symbol == 'PI':
                value = str(xMath.pi)
            if symbol == 'sqrt':
                if len(entry.get()) > 0:
                    value = float(entry.get())**0.5
            entry.delete(0, tk.END)
            entry.insert(0, value)

        
        

    def execute_function(self, function):
        print("Clicked! " + function)
        self.child_window_result.x = self.child_window_result.x_input.get()
        self.child_window_result.n = self.child_window_result.n_input.get()
        self.child_window_result.a = self.child_window_result.a_input.get()
        self.child_window_result.b = self.child_window_result.b_input.get()

        #Here is where we will call our functions
        if function == "ab^n":
            print(self.child_window_result.x + " " + self.child_window_result.n + " " + self.child_window_result.a + " " + self.child_window_result.b)
        if function == "Gamma":
            print(self.child_window_result.x + " " + self.child_window_result.n + " " + self.child_window_result.a + " " + self.child_window_result.b)
        if function == "x_power_n":
            print(self.child_window_result.x + " " + self.child_window_result.n + " " + self.child_window_result.a + " " + self.child_window_result.b)
        if function == "arccos":
            print(self.child_window_result.x + " " + self.child_window_result.n + " " + self.child_window_result.a + " " + self.child_window_result.b)
        if function == "sinh":
            print(self.child_window_result.x + " " + self.child_window_result.n + " " + self.child_window_result.a + " " + self.child_window_result.b)
        if function == "logb":
            print(self.child_window_result.x + " " + self.child_window_result.n + " " + self.child_window_result.a + " " + self.child_window_result.b)
        if function == "MAD":
            print(self.child_window_result.x + " " + self.child_window_result.n + " " + self.child_window_result.a + " " + self.child_window_result.b)
        if function == "sd":
            print(self.child_window_result.x + " " + self.child_window_result.n + " " + self.child_window_result.a + " " + self.child_window_result.b)
        
        self.child_window_result.destroy()

    
    def clear_variables(self):
        self.child_window_result = ""


    def add_special_operations(self, addedvalue):
        #        self.special_operations = {'Del':'\u2190', 'e':'\u2107', 'PI': '\u03c0'}
        if addedvalue == 'Del':
            self.currentCalculation = self.currentCalculation[0:len(self.currentCalculation) - 1]
        if addedvalue == 'e':
            self.currentCalculation = str(xMath.e)
        if addedvalue == 'PI':
            self.currentCalculation = str(xMath.pi)
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
            self.currentCalculation = "Error: " + str(error)
        finally:
            self.update_current()

    def binding_keyboard_keys(self):
        self.window.bind("<Return>", lambda event:self.evaluate_current_Calculation())
        
        for value in self.pad_values:
            if value != "√":
                self.window.bind(str(value), lambda event, addedValue=value: self.add_to_current(addedValue))
        
        for operator in self.operations:
            self.window.bind(operator, lambda event, operatation = operator: self.append_operation(operatation))

    #Run method
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    myEternity = Eternity()
    myEternity.run()




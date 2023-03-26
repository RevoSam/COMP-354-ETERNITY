import tkinter as tk
import math as xMath

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
            button.grid(row=grid_loc[0], column=grid_loc[1], sticky=tk.NSEW)
            
           
    
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
        #       self.functions = {'Gamma': '\u0393', 'ab^x' : 'ab_power_x', 'x^y': 'x_power_y', 'Save' : 'Save', 'Recal' : 'Recall', 'arccos' : 'arccos\u0028x\u0029',
        #                  'sinh':'sinh\u0028x\u0029','logb':'log\u2090\u0028x\u0029', 'MAD':'MAD', 'sd' : '\u03c3'
        #                 }

        for function, symbol in self.functions.items():

            button = tk.Button(self.self_buttons_frame, text = symbol, bg = BUTTON_OPERATOR_COLOR, fg = LABEL_COLOR, font = PAD_FONT_STYLE, borderwidth = 0, padx=10)
            button.grid(row = 0 + i, column = _column, columnspan = span, sticky=tk.NSEW)
            i += 1
            if i > 3 and _column == 4:
                i = 0
                _column = _column + span

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



import tkinter as tk
import math
from tkinter import filedialog as fd
import os
import csv
import Functions.special_fn as specialFunctions
import Functions.subordinate_fn as subordinateFunctions
from tkinter import messagebox
from model import EternityModel
from view import EternityView
from Helpers.parsing import convert_str_to_num, is_numerical, parse_string_multi_values

# Controller class for Eternity
class EternityController:
    
    # Constructor
    def __init__(self):
        # create new Model and View members
        self.model = EternityModel()
        self.view = EternityView(self)

    """---------------------------------------------------------------------------------------------
    HANDLE BUTTONS CLICK FOR SPECIAL FUNCTIONS
    ---------------------------------------------------------------------------------------------"""

    # method to handle button click of special functions
    def functions_buttons_click(self, function):
        if function == "ab^n":
            self.view.create_special_function_window("ab^n", 0, 1, 1, 1)
        elif function == "Gamma":
            self.view.create_special_function_window("Gamma", 1, 0, 0, 0)
        elif function == "x_power_n":
            self.view.create_special_function_window("x_power_n", 1, 1, 0, 0)
        elif function == "arccos":
            self.view.create_special_function_window("arccos", 1, 0, 0, 0)
        elif function == "sinh":
            self.view.create_special_function_window("sinh", 1, 0, 0, 0)
        elif function == "logb":
            self.view.create_special_function_window("logb", 1, 0, 1, 0)
        elif function == "MAD":
            self.view.create_mad_sd_window("MAD")
        elif function == "sd":
            self.view.create_mad_sd_window("SD")
        elif function == "Save":
            self.save_results(self.model.get_current_calculation())
        elif function == "Recall":
            # open recall window, else show error if there's no saved result to recall
            if len(self.model.get_saved_results()) > 0:
                self.view.create_recall_window("main")
            else:
                messagebox.showerror("Recall Error", "There is no saved result to recall.")

    """---------------------------------------------------------------------------------------------
    CONTROL MAD/SD CHILD WINDOW OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    def validate_input_mad_sd(self, *args):
        legalCharachters = set("123456789.,")
        if len(self.view.child_window_functions.x_input.get()) > 0:
            if not legalCharachters.issuperset(str(self.view.child_window_functions.x_input.get()[-1]).strip()):
                self.view.child_window_functions.x_input.delete(len(str(self.view.child_window_functions.x_input.get())) - 1, tk.END)
        
    # method to process manual input data and calculate MAD / SD
    def calculate_using_manual_input(self, isSample, callingFunction):
        # convert user input to a list
        input = str(self.view.child_window_functions.x_input.get())
        data_points = input.split(',')
        # call function to process input and calculate
        self.execute_mad_or_sd("manual", data_points, isSample, callingFunction)
        
    # method to process imported CSV and calculate MAD / SD
    def calculate_using_imported_csv(self, isSample, callingFunction):
        # delete manual input textbox if user imported csv
        self.view.child_window_functions.x_input.delete(0, tk.END)
        #Launch the dialogue in the same directory where the application is running
        filepath = fd.askopenfilename(initialdir=os.getcwd(), title="File to import", filetypes=(("CSV", "*.csv"),))
        # get data from csv
        with open(filepath, 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            data_points = []
            for row in csvreader:
                for i in range(len(row)):
                    data_points.append(row[i])
        # call function to process input and calculate
        self.execute_mad_or_sd("csv", data_points, isSample, callingFunction)

    # method to calculate descriptive stats, MAD/SD and update view
    def execute_mad_or_sd(self, input_mode, data_points, isSample, callingFunction):
        # remove any leading/trailing space and/or empty values
        # but any other non-numerical input is preserved for user to check/correct themselves
        data_points = [value.strip(' ') for value in data_points if len(value) != 0 and len(value.strip(' ')) != 0]
        # parse the data points
        data_points_floats = parse_string_multi_values(data_points)
        # if data points are not valid,
        if data_points_floats is None:
            if input_mode == "csv":
                # only output error if user chose to import csv
                messagebox.showerror("Invalid Input Error", "CSV may only contain numerical values.")
            elif input_mode == "manual":
                # update the textbox with processed input and output error if user input manually
                self.view.child_window_functions.focus_get().delete(0, tk.END)
                self.view.child_window_functions.focus_get().insert(0, ','.join(data_points))
                messagebox.showerror("Invalid Input Error", "Please enter 2 or more real numbers separated by commas.")
        else:
            # if data points are valid, calculate descriptive stats and mad/sd
            count = len(data_points_floats)
            total = sum(data_points_floats)
            mean = total / count
            fnName = ("n = " + str(count) + ", \u2211 = " + str(convert_str_to_num(round(total, 4))) + ", \u0078\u0304 = " + str(convert_str_to_num(round(mean, 4))) + ", ")
            result = 0.0
            if callingFunction == "MAD":
                result = specialFunctions.mad(data_points_floats)
                fnName += "MAD = " + str(convert_str_to_num(round(result, 4)))
            elif callingFunction == "SD":
                bool = True if (isSample.get() == 1) else False
                result = specialFunctions.standard_deviation(data_points_floats, bool)
                fnName += "\u03c3 = " + str(convert_str_to_num(round(result, 4)))
            # update model and view members
            self.view.update_total_label(fnName)
            self.model.set_current_calculation(str(result))
            self.view.update_current_label(self.model.get_current_calculation())
            self.view.child_window_functions.destroy()

    """---------------------------------------------------------------------------------------------
    CONTROL ARCCOS/SINH(X)/GAMMA/X^Y/AB^X/LOGB(X) CHILD WINDOW OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    # input e/pi/square root/recall values in current texbox of special function window
    def child_add_special_operations(self, symbol):
        value = 0
        entry = self.view.child_window_functions.focus_get()
        if isinstance(entry, tk.Entry):
            if symbol == 'e':
                value = str(subordinateFunctions.EULER)
            elif symbol == 'PI':
                value = str(subordinateFunctions.PI)
            elif symbol == 'sqrt':
                if len(entry.get()) > 0:
                    value = subordinateFunctions.sqrt(convert_str_to_num(entry.get()))
            elif symbol == "recall":
                # open the recall window, else show error if there's no saved result to recall
                if len(self.model.get_saved_results()) > 0:
                    self.view.create_recall_window("child", entry)
                else:
                    messagebox.showerror("Recall Error", "There is no saved result to recall.")
            # replace content in current textbox with special value
            entry.delete(0, tk.END)
            entry.insert(0, value)

# method to validate each input variable of a function and call execute function if validated True
    def validate_and_execute_special_fn(self, function):
        # initialize list of user inputs
        string_inputs = []
        
        if (function == "Gamma"):
            # get user input
            x = self.view.child_window_functions.x_input.get()
            string_inputs.append(x)
            # execute special function if input is numerical and within function's domain
            if (is_numerical(string_inputs) and convert_str_to_num(x) > 0):
                self.execute_function(function)
            else:
                # else output error message
                messagebox.showerror("Invalid Input Error", "Please enter a positive real number.")
        
        elif (function == "sinh"):
            x = self.view.child_window_functions.x_input.get()
            string_inputs.append(x)
            if (is_numerical(string_inputs)):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Please enter a real number.")
        
        elif (function == "arccos"):
            x = self.view.child_window_functions.x_input.get()
            string_inputs.append(x)
            if (is_numerical(string_inputs) and convert_str_to_num(x) >= -1 and convert_str_to_num(x) <= 1):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Please enter a real number between -1 and 1.")
        
        elif (function == "ab^n"):
            a = self.view.child_window_functions.a_input.get()
            b = self.view.child_window_functions.b_input.get()
            n = self.view.child_window_functions.n_input.get()
            string_inputs.extend([a, b, n])
            if (is_numerical(string_inputs) and convert_str_to_num(b) > 0 and convert_str_to_num(b) != 1 and convert_str_to_num(a) != 0):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Please enter real numbers for a, b, n: \n(1) a cannot be 0 \n(2) b cannot be 1 \n(3) b must be a positive real number")
        
        elif (function == "x_power_n"):
            x = self.view.child_window_functions.x_input.get()
            n = self.view.child_window_functions.n_input.get()
            string_inputs.extend([x, n])
            if (is_numerical(string_inputs)):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Please enter real numbers for x, n.")
        
        elif (function == "logb"):
            x = self.view.child_window_functions.x_input.get()
            a = self.view.child_window_functions.a_input.get()
            string_inputs.extend([x, a])
            if (is_numerical(string_inputs) and convert_str_to_num(a) != 1 and convert_str_to_num(x) > 0 and convert_str_to_num(a) > 0):
                self.execute_function(function)
            else:
                messagebox.showerror("Invalid Input Error", "Please enter positive real numbers for a, x: \n(1) a cannot be 1")


    """---------------------------------------------------------------------------------------------
    EXECUTE SPECIAL FUNCTIONS
    ---------------------------------------------------------------------------------------------"""

    # method to perform calculations for special functions
    def execute_function(self, function):
        self.view.child_window_functions.x = self.view.child_window_functions.x_input.get()
        self.view.child_window_functions.n = self.view.child_window_functions.n_input.get()
        self.view.child_window_functions.a = self.view.child_window_functions.a_input.get()
        self.view.child_window_functions.b = self.view.child_window_functions.b_input.get()

        #Here is where we will call our functions
        # a != 0, b > 0, b!= 1
        if function == "ab^n":
            self.view.update_total_label(self.view.child_window_functions.a + "*" + self.view.child_window_functions.b + "**" + self.view.child_window_functions.n)
            self.model.set_current_calculation(str(specialFunctions.natural_exp(convert_str_to_num(self.view.child_window_functions.a), convert_str_to_num(self.view.child_window_functions.b), convert_str_to_num(self.view.child_window_functions.n))))
            self.view.update_current_label(self.model.get_current_calculation())
        # x > 0
        elif function == "Gamma":
            self.view.update_total_label("Γ(" + self.view.child_window_functions.x + ")")
            self.model.set_current_calculation(str(specialFunctions.gamma(convert_str_to_num(self.view.child_window_functions.x))))
            self.view.update_current_label(self.model.get_current_calculation())
        # x, n are real numbers
        elif function == "x_power_n":
            self.view.update_total_label(self.view.child_window_functions.x + "**" + self.view.child_window_functions.n)
            self.model.set_current_calculation(str(specialFunctions.power(convert_str_to_num(self.view.child_window_functions.x), convert_str_to_num(self.view.child_window_functions.n))))
            self.view.update_current_label(self.model.get_current_calculation())
        # x >= -1 and x <= 1
        elif function == "arccos":
            self.view.update_total_label("arccos(" + self.view.child_window_functions.x + ")")
            self.model.set_current_calculation(str(specialFunctions.arccos(convert_str_to_num(self.view.child_window_functions.x))))
            self.view.update_current_label(self.model.get_current_calculation())
        # x is a real number
        elif function == "sinh":
            self.view.update_total_label("sinh(" + self.view.child_window_functions.x + ")")
            self.model.set_current_calculation(str(specialFunctions.sinh(convert_str_to_num(self.view.child_window_functions.x))))
            self.view.update_current_label(self.model.get_current_calculation())
        # x, b > 0, b != 1
        elif function == "logb":
            self.view.update_total_label("log" + self.view.child_window_functions.a + "(" + self.view.child_window_functions.x + ")")
            self.model.set_current_calculation(str(math.log(convert_str_to_num(self.view.child_window_functions.x), convert_str_to_num(self.view.child_window_functions.a))))
            self.view.update_current_label(self.model.get_current_calculation())
        self.view.child_window_functions.destroy()

    """---------------------------------------------------------------------------------------------
    SAVE/RECALL OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    # save the results from current calculation
    def save_results(self, currentCalculation):
        # only allow 7 saves, remove earliest save if exceeding 7
        if (len(self.model.get_saved_results()) >= 7):
            self.model.set_saved_results(self.model.get_saved_results()[1:])
        value_to_save = convert_str_to_num(currentCalculation)
        if (currentCalculation != "" and value_to_save is not None):
            # if the value is a valid number, add to array of saved results
            self.model.add_saved_result(value_to_save)
        else:
            # otherwise output error window
            messagebox.showerror("Save Error", "There is no valid number to save.")

    # method to remove a certain saved value
    def remove_saved_value(self, listbox, main_or_child):
        selected_entry = listbox.curselection()
        # output error message and close recall window if there's no entry to delete
        if (len(selected_entry) == 0):
            messagebox.showerror("Delete Error", "There is no saved result to delete.")
            self.close_recall_window(main_or_child)
        else:
            # delete the entry from listbox and array of saved values
            selected_value = listbox.get(selected_entry[0])
            listbox.delete(selected_entry)
            self.model.remove_saved_result(selected_value)
            # select the 1st entry again (if available)
            if len(selected_entry) != 0:
                listbox.select_set(0)
                
    # method to recall a saved value to the main window or a child window
    def recall_saved_value(self, listbox, main_or_child, entry):
        selected_entry = listbox.curselection()
        # output error message if there's no entry to delete
        if (len(selected_entry) == 0):
            messagebox.showerror("Recall Error", "There is no saved result to recall.")
        else:
            selected_value = listbox.get(selected_entry[0])
            # if recalling to main, add the value to main window's current calculation label
            if (main_or_child == "main"):
                self.model.set_current_calculation(convert_str_to_num(selected_value))
                self.view.update_current_label(self.model.get_current_calculation())
            # if recalling to child, replace whatever's in textbox with the recalled value
            else:
                entry.delete(0, tk.END)
                entry.insert(0, convert_str_to_num(selected_value))
        # close recall window
        self.close_recall_window(main_or_child)

    # close recall window and return focus to the last window
    def close_recall_window(self, main_or_child):
        self.view.recall_window.destroy()
        if (main_or_child == "child"):
            self.view.child_window_functions.grab_set()

    """---------------------------------------------------------------------------------------------
    GENERAL CALCULATOR OPERATIONS
    ---------------------------------------------------------------------------------------------"""

    def add_special_operations(self, addedvalue):
        # self.special_operations = {'Del':'\u2190', 'e':'\u2107', 'PI': '\u03c0'}
        if addedvalue == 'Del':
            self.model.set_current_calculation(self.model.get_current_calculation()[0:len(self.model.get_current_calculation()) - 1])
        elif addedvalue == 'e':
            self.model.set_current_calculation(str(subordinateFunctions.EULER))
        elif addedvalue == 'PI':
            self.model.set_current_calculation(str(subordinateFunctions.PI))
        self.view.update_current_label(self.model.get_current_calculation())

    #Add the number to the current Calculation
    def add_to_current(self, addedvalue):
        value_to_add = addedvalue
        current_calc = self.model.get_current_calculation()
        if addedvalue == '.'  or len(current_calc) == 0:
            if self.model.get_current_calculation().find('.') > 0:
                value_to_add = ""
        if addedvalue == '√':
            if len(current_calc) > 0:
                    addedvalue = subordinateFunctions.sqrt(convert_str_to_num(current_calc))
                    self.model.set_total("√(" + str(current_calc) + ")")
                    value_to_add = str(addedvalue)
                    self.model.set_current_calculation("")
                    self.update_total()
            elif len(current_calc) == 0:
                value_to_add = ""
                messagebox.showerror("Invalid Input Error", "First enter a number then click √ to get its square root.")
        self.model.set_current_calculation(self.model.get_current_calculation() + str(value_to_add))
        self.view.update_current_label(self.model.get_current_calculation())

    #Add the operation to the current Calculation
    def append_operation(self, operator):
        for ch in str(self.model.get_total()):
            if ch == '√':
                self.model.set_total("")
                break
        self.model.set_current_calculation(self.model.get_current_calculation() + operator)
        self.model.set_total(self.model.get_total() + self.model.get_current_calculation())
        self.model.set_current_calculation("")
        self.update_total()
        self.view.update_current_label(self.model.get_current_calculation())

    #Update the Total calculation + its label
    def update_total(self):
        totalCalculation = self.model.get_total()
        for operator, sign in self.view.operations.items():
            totalCalculation = totalCalculation.replace(operator, f' {sign} ')
        self.view.update_total_label(totalCalculation)

    #Clear both the Total and Current Calculation + their labels
    def clear_calculation(self):
        self.model.set_total("")
        self.model.set_current_calculation("")
        self.update_total()
        self.view.update_current_label(self.model.get_current_calculation())
        
    #Evaluate the current calculation
    def calculate_result(self):
        # if there is some calculation to perform
        if len(self.model.get_total()) != 0:
            # update total math expression with current number
            self.model.set_total(self.model.get_total() + self.model.get_current_calculation())
            self.update_total()

            # evaluate and display result
            result = self.model.evaluate()
            self.model.set_current_calculation(result)
            self.model.set_total("")
            self.view.update_current_label(self.model.get_current_calculation())
            
            # output error if cannot evaluate expression
            if result == "Error":
                messagebox.showerror("Math Error", "Unable to calculate the math expression.")

    """---------------------------------------------------------------------------------------------
    GETTER
    ---------------------------------------------------------------------------------------------"""
    
    # getter for controller's model
    def get_model(self):
        return self.model

    """---------------------------------------------------------------------------------------------
    MAIN METHOD
    ---------------------------------------------------------------------------------------------"""
    
    # call main method of view
    def main(self):
        self.view.main()



if __name__ == "__main__":
    myEternity = EternityController()
    myEternity.main()
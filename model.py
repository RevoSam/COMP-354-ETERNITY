
# Model class for Eternity
class EternityModel:

    # Constructor
    def __init__(self):
        # initialize members
        self._total = ""
        self._currentCalculation = ""
        self._savedResults = []

    # call eval for basic arithmetics
    def evaluate(self):
        try:
            result = str(eval(self.get_total()))
        except Exception:
            return "Error"
        return result

    """---------------------------------------------------------------------------------------------
    GETTERS
    ---------------------------------------------------------------------------------------------"""

    # get total result
    def get_total(self):
        return self._total
    
    # get string of current calculation
    def get_current_calculation(self):
        return self._currentCalculation
    
    # get list of saved results
    def get_saved_results(self):
        return self._savedResults
    
    """---------------------------------------------------------------------------------------------
    SETTERS
    ---------------------------------------------------------------------------------------------"""
    
    # set value for total result
    def set_total(self, newTotal):
        self._total = newTotal

    # set string for current calculation
    def set_current_calculation(self, newCalculation):
        self._currentCalculation = newCalculation

    # set list of saved results
    def set_saved_results(self, newSavedResults):
        self._savedResults = newSavedResults

    # add a value to list of saved results
    def add_saved_result(self, newValue):
        self._savedResults.append(newValue)

    # remove value from list of saved results
    def remove_saved_result(self, valueToRemove):
        self._savedResults.remove(valueToRemove)
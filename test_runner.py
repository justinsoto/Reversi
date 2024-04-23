import unittest
from model.model_unittests.test_player import TestPlayer
from model.model_unittests.test_board import TestBoard
from model.model_unittests.test_game import TestGame
from model.model_unittests.test_ai import TestAI
from model.model_unittests.test_ai_strategy import TestMiniMaxStrategy, TestMiniMaxAlphaBeta, TestRandomStrategy

class CustomTestResult(unittest.TextTestResult):
    """
    A custom test result class that extends unittest.TextTestResult to provide enhanced output formatting for test results.
    
    This custom implementation adds numbering and highlights to the test output, making it easier to track which tests pass or fail during execution.
    
    Attributes:
        stream (io.TextIOWrapper): The stream to write output to.
        descriptions (bool): Flag to determine if test descriptions should be included in the output.
        verbosity (int): Level of verbosity for the output.
    """    
    def __init__(self, stream, descriptions, verbosity):
        """
        Initializes the CustomTestResult instance with a specific stream, descriptions setting, and verbosity level.

        Parameters:
        stream (io.TextIOWrapper): The output stream for result text.
        descriptions (bool): If true, includes test descriptions in output.
        verbosity (int): The verbosity level of the output.
        """        
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.i = 1
    def addSuccess(self, test):
        """
        Handles a test passing. Overrides to add specific formatting to the success message.

        Parameters:
        test (TestCase): The test case that passed.
        """        
        super().addSuccess(test)
        self.stream.writeln(f"\033[4mTEST-{self.i}:\033[0m {test} - Passed")
        self.i+=1

    def addError(self, test, err):
        """
        Handles a test that raises an error. Overrides to add specific formatting to the error message.

        Parameters:
        test (TestCase): The test case that encountered an error.
        err (tuple): A tuple containing exception type, value, and traceback.
        """        
        super().addError(test, err)
        self.stream.writeln(f"\033[4mTEST-{self.i}:\033[0m {test} - Error: {err}")
        self.i+=1

def test_suite():
    """
    Constructs a test suite that aggregates tests from various test classes within the application.

    Returns:
    TestSuite: A unittest.TestSuite object containing all the tests to be run.
    """    
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMiniMaxStrategy))
    suite.addTest(unittest.makeSuite(TestMiniMaxAlphaBeta))
    suite.addTest(unittest.makeSuite(TestRandomStrategy))
    suite.addTest(unittest.makeSuite(TestAI))
    suite.addTest(unittest.makeSuite(TestPlayer))
    suite.addTest(unittest.makeSuite(TestBoard))
    suite.addTest(unittest.makeSuite(TestGame))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=CustomTestResult)
    result = runner.run(test_suite())
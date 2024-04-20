import unittest
from model.model_unittests.test_player import TestPlayer
from model.model_unittests.test_board import TestBoard
from model.model_unittests.test_game import TestGame
from model.model_unittests.test_ai import TestAI
from model.model_unittests.test_ai_strategy import TestMiniMaxStrategy, TestMiniMaxAlphaBeta, TestRandomStrategy

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.i = 1
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln(f"\033[4mTEST-{self.i}:\033[0m {test} - Passed")
        self.i+=1

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.writeln(f"\033[4mTEST-{self.i}:\033[0m {test} - Error: {err}")
        self.i+=1

def test_suite():
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
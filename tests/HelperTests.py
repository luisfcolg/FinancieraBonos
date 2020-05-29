import unittest
from helpers import FunctionHelpers


class HelperTests(unittest.TestCase):

    def testCompareDates(self):
        before = "2019-05-27"
        after = "2015-03-20"

        result = FunctionHelpers.compareDates(before, after)

        self.assertNotEqual(result, True, 'Valid credentials')
        self.assertEqual(result, False, 'Valid credentials')


    def testGenerateIsin(self):
        currency = "MXN"

        result = FunctionHelpers.generateIsin(currency)

        validateChar = True
        for i in range(2):
            if ord(result[i]) < 65 or ord(result[i]) > 90:
                validateChar = False
                break

        validateNums = True
        for i in range(2, 12):
            if ord(result[i]) < 48 or ord(result[i]) > 58:
                validateNums = False
                break

        self.assertNotEqual(validateChar and validateNums, False, "Valid ISIN")
        self.assertEqual(validateChar and validateNums, True, "Valid ISIN")
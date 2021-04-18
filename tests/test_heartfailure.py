import unittest

import heartfailure


class HeartfailureTestCase(unittest.TestCase):
    def setUp(self):
        self.app = heartfailure.app.test_client()


if __name__ == '__main__':
    unittest.main()

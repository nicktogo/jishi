import unittest
import auth


class MyTestCase(unittest.TestCase):
    def test_login(self):
        self.assertEqual(auth.valid_login('tzx', '2131'), True)


if __name__ == '__main__':
    unittest.main()

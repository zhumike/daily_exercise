import unittest


from faker import Faker

fake = Faker()

"""
https://faker.readthedocs.io/en/master/
"""

class MyTestCase(unittest.TestCase):
    def test_something(self):
        name = fake.name()
        print(name)

        address = fake.address()
        print(address)

        email = fake.email()
        print(email)

        phone_number = fake.phone_number()
        print(phone_number)



if __name__ == '__main__':
    unittest.main()

from faker import Faker

f = Faker(['pl_PL', 'de_DE'])
# pip install Faker
#https://faker.readthedocs.io/en/master/

print(f.name())
print(f.address())
print(f.ssn())
print(f.phone_number())
w = f.email()
print(w, w[:w.index('@')])
print(f.text())
print(f.latitude(), f.longitude())
print(f.url())
# https://www.geeksforgeeks.org/python-faker-library/

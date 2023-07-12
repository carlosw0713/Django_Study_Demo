from django.test import TestCase

# Create your tests here.


# tempStr = "Hello Python, this is a new world!"
# xxx=input('请输入')
# print(tempStr.replace('Python',xxx))


def contains_substring(a, b):


        return b.find(a)


a="112"
b="211"
print(contains_substring(a,b))

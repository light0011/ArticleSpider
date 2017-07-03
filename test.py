class test(object):

    def say(self):
        yield 1
        yield 2
        yield 3
        yield 4


a = test()

print(a.say())

for i in a.say():
    print(i)
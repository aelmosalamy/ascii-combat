import dicts.weapons_skills as ws

# Name strip test
def test2():    
    mystring = 'ferocious Bear'
    if not mystring.startswith('Dead'):
        if len(mystring.split(' ')) < 2:
            mystring = 'Dead %s' % mystring
        else:
            no_variation = mystring.split(' ', 1)
            print(no_variation)
            mystring = no_variation[1]
            print(mystring)
            mystring = '{} {}'.format('Dead', mystring)    
    print(mystring)

var = 2
def myfunc():
    var = 5
    return var

# OR test
def or_test():
    i = 3
    if i == 2 or i == 3:
     print('i is %s' % i)
    else:
        print('None')

def func_return_test():
    print(myfunc())
    print(var)
    myfunc()
    print(var)

def imp_test():
    x = ws.SKILLS['doubletrouble']
    print(x)

def dict_test():
    mydictionary = {'apple': 'red', 'banana': 'yellow'}
    item = mydictionary['apple']
    print(mydictionary['apple'])

def main():
    imp_test()

if __name__ == '__main__':
    main()

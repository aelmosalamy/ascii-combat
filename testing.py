import ac_dicts
import combat

# Monster specie and names test
def test1():
    ms = []
    for i in range(5):
        m = ac_dicts.give_monster('wolf')
        ms.append(m)

    for i in ms:
        print(i.name)    

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
    
def func_return_test():
    print(myfunc())
    print(var)
    myfunc()
    print(var)


def dict_test():
    mydictionary = {'apple': 'red', 'banana': 'yellow'}
    item = mydictionary['apple']
    print(mydictionary['apple'])

def main():
    func_return_test()


if __name__ == '__main__':
    main()

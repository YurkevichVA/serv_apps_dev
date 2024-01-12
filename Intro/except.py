x = 10


def throw_with_message() -> None:
    print('Raising ValueError...')
    raise ValueError('ValueError message')


def main() -> None:
    try:
        #throw_with_message()
        pass
    except ValueError as err:
        print("Got message '%s'" %(err))
    except:
        print('Exception detected')
    else:
        print('Else action')
    finally:
        print('Finally action')

    
if __name__ == '__main__': main()
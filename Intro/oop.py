class MyClass:
    x = 10


def demo1():
    obj1 = MyClass()
    obj2 = MyClass()
    print(obj1.x, obj2.x, MyClass.x)    # 10 10 10
    MyClass.x = 20                  
    print(obj1.x, obj2.x, MyClass.x)    # 20 20 20
    obj1.x = 15
    print(obj1.x, obj2.x, MyClass.x)    # 15 20 20
    MyClass.x = 30
    print(obj1.x, obj2.x, MyClass.x)    # 15 30 30
    obj2.y = 5
    obj1.w = 7
    del obj1.x
    print(obj1.x, obj2.x, MyClass.x)
    pass


class TheClass:
    x = 10

    def __init__(self, a: int = 1, b: int = 2) -> None :
        self.a = a
        self.b = b
        pass

    def __str__(self) -> str:
        return f"{self.a}, {self.b}"
    
    def magnitude(self) -> int:
        return self.a + self.b



def demo2() -> None:
    obj1 = TheClass()
    print(obj1.a, obj1.b)
    print(TheClass(10, 20))
    print(TheClass(30))
    print(TheClass(b=40))
    print(obj1.magnitude())


def main() -> None:
    demo2()


if __name__ == "__main__":
    main()
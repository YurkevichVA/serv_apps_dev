class Fraction:
    def __init__(self, numerator:int=0, denominator:int=1) -> None:
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self) -> str:
        return f"({self.numerator}/{self.denominator})"
    
    def gcd(self, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def reduce(self) -> None:
        common_divisor = self.gcd(self.numerator, self.denominator)
        self.numerator //= common_divisor
        self.denominator //= common_divisor
        return self
    

def main():
    print(Fraction())
    print(Fraction(3))
    print(Fraction(denominator=4))
    print(Fraction(14, 7))
    print(Fraction(14, 7).reduce())


if __name__ == "__main__":
    main()

        
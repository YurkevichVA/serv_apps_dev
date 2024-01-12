counter = 10
while counter > 0:
    print(counter)
    counter -= 1

print( range(10) )

print( "range(10):", end=' ' )
for i in range(10):
    print(i, end=' ')
print()

print( "range(1, 10):", end=' ' )
for i in range(1, 10):
    print(i, end=' ')
print()

print( "range(1, 10, 2):", end=' ' )
for i in range(1, 10, 2):
    print(i, end=' ')
print()

x = 10
y = 20 if x < 10 else 5

x, y = 1, 2
print(x, y)
x, y = y, x
print(x, y)
x, y = y, x + y
print(x, y)


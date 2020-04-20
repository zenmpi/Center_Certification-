inp = str(input())
result = ''
romans = (
    ('C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM', ''),
    ('X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC', ''),
    ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', '')
)

for i in range(len(inp)):
    if i == 0 and len(inp) == 4:
        result += 'M' * int(inp[i])
    else:
        result += romans[(i - len(inp)) % 3][int(inp[i]) - 1]

print(result)
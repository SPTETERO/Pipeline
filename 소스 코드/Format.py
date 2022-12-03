def HexFormat(num):

    complement = False
    if num < 0:
        complement = True
        num += 1
        num *= -1
        

    result = ""

    for i in range(8):
        n = num % 16
        
        if complement:
            n = 16 - (n + 1) 

        num //= 16

        if n < 10:
            result += str(n)
        elif n == 10:
            result += "a"
        elif n == 11:
            result += "b"
        elif n == 12:
            result += "c"
        elif n == 13:
            result += "d"
        elif n == 14:
            result += "e"
        elif n == 15:
            result += "f"

    return "0x" + "".join(reversed(list(result)))
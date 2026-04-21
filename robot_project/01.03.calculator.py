def add(a, b):
    return a+ b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    return a / b

def calculator():
    """로봇 SW 개발 입문용 계산기 메인 함수"""

    while True:
        try:
            calc = input("calc : ")
            
            if calc == 'q':
                break

            if calc not in ['+', '-', '*', '/']:
                continue

            num1 = float(input("num 1 : "))
            num2 = float(input("num 2 : "))

            if calc == '+':
                print(add(num1, num2))
            elif calc == '-':
                print(sub(num1, num2))
            elif calc == '*':
                print(mul(num1, num2))
            elif calc == '/':
                print(div(num1, num2))

        except ValueError as e:
            print(e)
        except ZeroDivisionError as e:
            print(e)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    calculator()
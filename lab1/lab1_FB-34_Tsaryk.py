def number_of_words(c):
    result = []
    
    inside_brackets = False
    temp = []

    for word in c:
        if word.startswith("(") and word.endswith(")"):
            result.append(word)
        elif word.startswith("("):
            inside_brackets = True
            temp = [word]
        elif word.endswith(")") and inside_brackets:
            temp.append(word)
            result.append(" ".join(temp))
            inside_brackets = False
        elif inside_brackets:
            temp.append(word)
        else:
            result.append(word)
    return len(result)

def is_correct(x):
    allowed_all = set("QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm_1234567890")
    allowed_first = set("QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm")
    if x[0] not in allowed_first:
        return False
    for ch in x:
        if ch not in allowed_all:
            return False
    return True

def create(c):
    is_var1_correct = is_correct(c[1])
    if not is_var1_correct:
        print('ERROR: variable entered incorrectly.')
        return;

def insert(c):
    return;

def select(c):
    return;
    

def read_until():
    command = ""
    while True:
        line = input()
        command = command + line + "\n"
        if ";" in line:
            command = command.split(';', 1)[0]
            break
    return command

def analize(c):
    len_c_words = number_of_words(c)
    first = c[0]
    first = first.lower()
    match first:
        case "create":
            if len_c_words < 3:
                print('ERROR: Command does not contain enough tokens.')
                return
            create(c);
            return
        case "insert":
            if len_c_words <  3:
                print('ERROR: Command does not contain enough tokens.')
                return
            second = c[1]
            second = second.lower()
            if (second == "into")and(len_c_words < 4):
                print('ERROR: Command does not contain enough tokens.')
                return
            insert(c)
            return
        case "select":
            if len_c_words <  3:
                print('ERROR: Command does not contain enough tokens.')
                return
            second = c[1]
            second = second.lower()
            if (second != "from"):
                print('ERROR: The command was written incorrectly.')
                return
            select(c)
            return
        case "stop":
            global start
            start = False
            return
        case _:
            print('EROR: Сommand not recognized.')
            return

start = True;
print("Accepts commands (case insensitive): CREATE, INSERT INTO, INSERT, SELECT FROM")
print("Variable names (first character is a letter, other letters/digits/_)")
print("Command is read until ';'")
print("To finish, type 'stop;'\n")
while start:
    print('c: ', end="")
    command = read_until()
    c = command.split()
    analize(c)
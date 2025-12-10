import string

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

def words_inside_brackets(tokens):
    result = []
    inside = False
    temp = []

    for tok in tokens:
        if tok.startswith("(") and tok.endswith(")"):
            inner = tok.strip("()")
            inner = inner.translate(str.maketrans('', '', string.punctuation))
            result.extend(inner.split())
        elif tok.startswith("("):
            inside = True
            temp = [tok.lstrip("(")]
        elif tok.endswith(")") and inside:
            temp.append(tok.rstrip(")"))
            joined = " ".join(temp)
            joined = joined.translate(str.maketrans('', '', string.punctuation))
            result.extend(joined.split())
            inside = False
        elif inside:
            temp.append(tok)
    return result

def is_correct(x):
    allowed_all = set("QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm_1234567890")
    allowed_first = set("QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm")
    if x[0] not in allowed_first:
        return False
    for ch in x:
        if ch not in allowed_all:
            return False
    return True

#CREATE students (name, group);
def create(c):
    is_var1_correct = is_correct(c[1])
    if not is_var1_correct:
        print('ERROR: variable entered incorrectly.')
        return
    global table;
    for tbl in tables:
        if tbl[0] == c[1]:
            print(f'ERROR: cannot create "{c[1]}" again.')
            return
    columns = words_inside_brackets(c)
    tables.append([c[1], columns])
    print(f'Table "{c[1]}" was created.') 
    
#INSERT INTO owners(“1”, “Vasya”, “30”);
#INSERT cats (“10”, “1”, “Murzik”); 
def insert(c, is_into):
    if is_into:
        table_name = c[2]
    else:
        table_name = c[1]
    row_values = words_inside_brackets(c)  
    global tables
    global values
    for tbl in tables:
        if tbl[0] == table_name:
            if len(row_values) != len(tbl[1]):
                print('ERROR: number colums != number values.')
                return
            values.append([table_name, row_values])
            print(f'Values were inserted into "{table_name}".')
            return
    print(f'ERROR: no table with name "{table_name}".')

def get_rows(table_name):
    result = []
    for tbl_name, row in values:
        if tbl_name == table_name:
            result.append(row)
    return result

def check_table(table_name):
    for tbl in tables:
        if tbl[0] == table_name:
            return True
    print(f'ERROR: no table with name "{table_name}".')
    return False

def print_table(table_name, table_rows):
    if (table_name == None) or (table_rows == None):
        print('ERROR: Columns or rows are not found.')
        return
    print(table_name)
    print('------------')
    for row in table_rows:
        print(row)

def join_on(table_name_1, table_name_2, on, column_1, column_2):
    if (check_table(table_name_1)) and (check_table(table_name_2)):
        rows1 = get_rows(table_name_1)
        rows2 = get_rows(table_name_2)
        cols1 = None
        cols2 = None

        for t in tables:
            if t[0] == table_name_1:
                cols1 = t[1]
            if t[0] == table_name_2:
                cols2 = t[1]

        if not on:
            joined_rows = []
            for r1 in rows1:
                for r2 in rows2:
                    joined_rows.append(r1 + r2)
            joined_cols = cols1 + cols2
            return joined_cols, joined_rows

        if column_1 not in cols1 or column_2 not in cols2:
            print("ERROR: column name not found.")
            return None, None

        i1 = cols1.index(column_1)
        i2 = cols2.index(column_2)

        joined_rows = []

        for r1 in rows1:
            for r2 in rows2:
                if r1[i1] == r2[i2]:
                    joined_rows.append(r1 + r2)
        joined_cols = cols1 + cols2
        return joined_cols, joined_rows
    else:
        return None, None

def where(columns, rows, col, op, val):
    if col not in columns:
        print(f"ERROR: column '{col}' not found.")
        return None, None
    
    col_index = columns.index(col)
    val_clean = val.strip('"')

    if op not in ['>', '<', '=']:
        print(f"ERROR: unknown operator '{op}'. Use one of: >, <, =")
        return None, None

    result = []
    for row in rows:
        cell_value = row[col_index]

        if (
            (op == '>' and cell_value > val_clean) or
            (op == '<' and cell_value < val_clean) or
            (op == '=' and cell_value == val_clean)
        ):
            result.append(row)

    return columns, result
    

#SELECT FROM table_name_1 [JOIN table_name_2 [ON t1_column = t2_column]] [WHERE condition]; 
def select(c, len_c_words):    
    if ('join' in c)and('where' in c):
        if 'on' in c:
            name, rows = join_on(c[2], c[4], True, c[6], c[8])
            columns, result = where(name, rows, c[10], c[11], c[12])
            print_table(columns, result)
        else:
            name, rows = join_on(c[2], c[4], False, None, None)
            columns, result = where(name, rows, c[6], c[7], c[8])
            print_table(columns, result)
        return
            
    elif 'join' in c:
        if 'on' in c:
            name, rows = join_on(c[2], c[4], True, c[6], c[8])
        else:
            name, rows = join_on(c[2], c[4], False, None, None)
        print_table(name, rows)
        return
    elif 'where' in c:
        if check_table(c[2]):
            cols = None
            for t in tables:
                if t[0] == c[2]:
                    cols = t[1]
            rows = get_rows(c[2])
            columns, result = where(cols, rows, c[4], c[5], c[6])
            print_table(columns, result)
        return
    elif (len_c_words == 3):
        if check_table(c[2]):
            cols = None
            for t in tables:
                if t[0] == c[2]:
                    cols = t[1]
            rows = get_rows(c[2])
            print_table(cols, rows)
        return
    else:
        print('ERROR: failed to recognize command keywords.')
        print('Try: SELECT FROM table_name_1 [JOIN table_name_2 [ON t1_column = t2_column]] [WHERE condition];')
        return

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
            if (second == "into"):
                insert(c, True);
            else:
                insert(c, False);
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
            select(c, len_c_words)
            return
        case "stop":
            global start
            start = False
            return
        case _:
            print('EROR: Сommand not recognized.')
            return

start = True;
tables = []
values = []
print("Accepts commands (case insensitive): CREATE, INSERT INTO, INSERT, SELECT FROM")
print("Variable names (first character is a letter, other letters/digits/_)")
print("Command is read until ';'")
print("To finish, type 'stop;'\n")
while start:
    print('c: ', end="")
    command = read_until()
    c = command.split()
    analize(c)


import string

class Node:
    def __init__(self, key):
        self.key = key
        self.row_ids = []  
        self.left = None
        self.right = None

class Binary_Tree:
    def __init__(self):
        self.root = None

    def insert(self, key, row_id):
        self.root = self._insert(self.root, key, row_id)

    def _insert(self, node, key, row_id):
        if node is None:
            n = Node(key)
            n.row_ids.append(row_id)
            return n
        if key < node.key:
            node.left = self._insert(node.left, key, row_id)
        elif key > node.key:
            node.right = self._insert(node.right, key, row_id)
        else:
            node.row_ids.append(row_id)
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return []
        if key == node.key:
            return node.row_ids
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)  
    
    def print_tree(self, node=None, level=0, prefix="Root: "):
        if node is None:
            node = self.root 
        if node.right:
            self.print_tree(node.right, level + 1, "R----") 
        print("     " * level + prefix + str(node.key))     
        if node.left:
            self.print_tree(node.left, level + 1, "L----")  

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

def find_table(table_name):
    for name, cols in tables:
        if name == table_name:
            return cols
    return None

def print_table(table_name, table_rows):
    if (table_name == None) or (table_rows == None):
        print('ERROR: Columns or rows are not found.')
        return
    print(table_name)
    print('------------')
    for row in table_rows:
        print(row)

# CREATE table (columns [INDEXED]);
def create(c):
    is_var1_correct = is_correct(c[1])
    if not is_var1_correct:
        print('ERROR: variable entered incorrectly.')
        return
    global tables
    global need_index
    for tname, _ in tables:
        if tname == c[1]:
            print(f'ERROR: cannot create "{c[1]}" again.')
            return

    columns = words_inside_brackets(c)

    if "INDEXED" in columns:
        while "INDEXED" in columns:
            idx = columns.index("INDEXED")
            col_name = columns[idx - 1]
            need_index.append(f"{c[1]}_{col_name}")
            del columns[idx]

    tables.append([c[1], columns])
    print(f'Table "{c[1]}" was created.')


def insert(c, is_into):
    if is_into:
        table_name = c[2]
    else:
        table_name = c[1]

    global tables, values, i, indexes, need_index

    cols = find_table(table_name)
    if cols is None:
        print(f'ERROR: no table with name "{table_name}".')
        return

    row_vals = words_inside_brackets(c)
    if len(row_vals) != len(cols):
        print('ERROR: number colums != number values.')
        return

    values.append([table_name, i, row_vals])
    print(f'Values were inserted into "{table_name}".')

    for col_index, col_name in enumerate(cols):
        idx_name = f"{table_name}_{col_name}"
        if idx_name in need_index:
            if idx_name not in indexes:
                indexes[idx_name] = Binary_Tree()
            indexes[idx_name].insert(row_vals[col_index], i)
            #indexes[idx_name].print_tree();

    i += 1


def get_rows(table_name):
    result = []
    for tname, row_id, vals in values:
        if tname == table_name:
            result.append(vals)
    return result


def check_table(table_name):
    return find_table(table_name) is not None


def join_on(table_name_1, table_name_2, on, column_1, column_2):
    if not (check_table(table_name_1) and check_table(table_name_2)):
        return None, None

    rows1 = get_rows(table_name_1)
    rows2 = get_rows(table_name_2)

    cols1 = find_table(table_name_1)
    cols2 = find_table(table_name_2)

    if cols1 is None or cols2 is None:
        return None, None

    if not on:
        joined_rows = [r1 + r2 for r1 in rows1 for r2 in rows2]
        return cols1 + cols2, joined_rows

    if column_1 not in cols1 or column_2 not in cols2:
        print("ERROR: column name not found.")
        return None, None

    i1 = cols1.index(column_1)
    i2 = cols2.index(column_2)

    index_name = f"{table_name_2}_{column_2}"
    global indexes

    if index_name in indexes:
        print(f"Index used for JOIN: {index_name}")

        tree = indexes[index_name]
        joined_rows = []

        for r1 in rows1:
            key = r1[i1]
            matching_ids = tree.search(key)

            for t2, rid2, r2 in values:
                if rid2 in matching_ids and t2 == table_name_2:
                    joined_rows.append(r1 + r2)

        return cols1 + cols2, joined_rows

    joined_rows = []
    for r1 in rows1:
        for r2 in rows2:
            if r1[i1] == r2[i2]:
                joined_rows.append(r1 + r2)

    return cols1 + cols2, joined_rows


def where(columns, rows, col, op, val):
    global indexes, tables, values

    if col not in columns:
        print(f"ERROR: column '{col}' not found.")
        return None, None

    col_index = columns.index(col)
    val_clean = val.strip('"')

    table_name = None
    for tname, cols in tables:
        if cols == columns:
            table_name = tname
            break

    index_name = f"{table_name}_{col}"

    if op == "=" and index_name in indexes:
        print(f"Index used for WHERE: {index_name}")

        tree = indexes[index_name]
        row_ids = tree.search(val_clean)

        result = []
        for tname, rid, rowvals in values:
            if rid in row_ids and tname == table_name:
                result.append(rowvals)

        return columns, result

    if op not in ['>', '<', '=']:
        print(f"ERROR: unknown operator '{op}'. Use: > < =")
        return None, None

    result = []
    for row in rows:
        cell_value = row[col_index]

        if ((op == '>' and cell_value > val_clean) or
            (op == '<' and cell_value < val_clean) or
            (op == '=' and cell_value == val_clean)):
            result.append(row)

    return columns, result


def select(c, len_c_words):
    if ('join' in c) and ('where' in c):
        if 'on' in c:
            name, rows = join_on(c[2], c[4], True, c[6], c[8])
            columns, result = where(name, rows, c[10], c[11], c[12])
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
            cols = find_table(c[2])
            rows = get_rows(c[2])
            columns, result = where(cols, rows, c[4], c[5], c[6])
            print_table(columns, result)
        return

    elif len_c_words == 3:
        if check_table(c[2]):
            cols = find_table(c[2])
            rows = get_rows(c[2])
            print_table(cols, rows)
        return

    print("ERROR: failed to recognize command keywords.")

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
i = 0              
need_index = []
indexes = {}
print("Accepts commands (case insensitive): CREATE, INSERT INTO, INSERT, SELECT FROM")
print("Variable names (first character is a letter, other letters/digits/_)")
print("Command is read until ';'")
print("To finish, type 'stop;'\n")
while start:
    print('c: ', end="")
    command = read_until()
    c = command.split()
    analize(c)
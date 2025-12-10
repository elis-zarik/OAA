import subprocess
import time
import threading

def run_program(filename, commands, log_filename):

    proc = subprocess.Popen(
        ["python", filename],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    log_file = open(log_filename, "w", encoding="utf-8")

    output_buffer = []

    def reader_thread():
        for line in proc.stdout:
            output_buffer.append(line)
            log_file.write(line)

    t = threading.Thread(target=reader_thread, daemon=True)
    t.start()

    results = {}

    for cmd_name, cmd_text in commands:

        output_buffer.clear()

        proc.stdin.write(cmd_text + "\n")
        proc.stdin.flush()

        start = time.perf_counter()

        while True:
            time.sleep(0.0005)   
            if len(output_buffer) > 0:
                break

        end = time.perf_counter()

        if cmd_name.startswith("SELECT"):
            results[cmd_name] = end - start

    proc.terminate()
    log_file.close()
    return results

commands = [
    ("CREATE1",      'create cat (1, 2, 3, 4);'),
    ("INSERT11",     'insert cat (a, b, c, d);'),
    ("INSERT12",     'insert cat (a, a, e, f);'),
    ("INSERT13",     'insert cat (a, a, a, g);'),
    ("INSERT14",     'insert cat (a, a, a, a);'),
    ("INSERT15",     'insert cat (a, b, c, d);'),
    ("INSERT16",     'insert cat (a, a, e, f);'),
    ("INSERT17",     'insert cat (a, a, a, g);'),
    ("INSERT18",     'insert cat (a, a, a, a);'),
    
    ("CREATE2",      'create dog (5, 6, 7, 8);'),
    ("INSERT21",     'insert dog (b, b, b, b);'),
    ("INSERT22",     'insert dog (a, a, a, a);'),
    ("INSERT23",     'insert dog (i, j, k, l);'),
    ("INSERT24",     'insert dog (a, j, d, c);'),
    ("INSERT25",     'insert dog (b, b, b, b);'),
    ("INSERT26",     'insert dog (a, a, a, a);'),
    ("INSERT27",     'insert dog (i, j, k, l);'),
    ("INSERT28",     'insert dog (a, j, d, c);'),

    ("SELECT_ALL_JOIN",        "select from cat join dog;"),
    ("SELECT_JOIN_ON",      "select from cat join dog on 3 = 8;"),
    ("SELECT_WHERE_<",       "select from cat where 2 < b;"),
    ("SELECT_WHERE_=",       "select from cat where 4 = a;"),
    ("SELECT_WHERE_JOIN", "select from cat join dog on 1 = 5 where 8 = a;"),
    
    ("STOP", "stop;")
]

commands_i = [
    ("CREATE1",      'create cat (1 INDEXED, 2 INDEXED, 3 INDEXED, 4 INDEXED);'),
    ("INSERT11",     'insert cat (a, b, c, d);'),
    ("INSERT12",     'insert cat (a, a, e, f);'),
    ("INSERT13",     'insert cat (a, a, a, g);'),
    ("INSERT14",     'insert cat (a, a, a, a);'),
    ("INSERT15",     'insert cat (a, b, c, d);'),
    ("INSERT16",     'insert cat (a, a, e, f);'),
    ("INSERT17",     'insert cat (a, a, a, g);'),
    ("INSERT18",     'insert cat (a, a, a, a);'),
    
    ("CREATE2",      'create dog (5 INDEXED, 6 INDEXED, 7 INDEXED, 8 INDEXED);'),
    ("INSERT21",     'insert dog (b, b, b, b);'),
    ("INSERT22",     'insert dog (a, a, a, a);'),
    ("INSERT23",     'insert dog (i, j, k, l);'),
    ("INSERT24",     'insert dog (a, j, d, c);'),
    ("INSERT25",     'insert dog (b, b, b, b);'),
    ("INSERT26",     'insert dog (a, a, a, a);'),
    ("INSERT27",     'insert dog (i, j, k, l);'),
    ("INSERT28",     'insert dog (a, j, d, c);'),

    ("SELECT_ALL_JOIN",        "select from cat join dog;"),
    ("SELECT_JOIN_ON",      "select from cat join dog on 3 = 8;"),
    ("SELECT_WHERE_<",       "select from cat where 2 < b;"),
    ("SELECT_WHERE_=", "select from cat where 4 = a;"),
    ("SELECT_WHERE_JOIN", "select from cat join dog on 1 = 5 where 8 = a;"),
    
    ("STOP", "stop;")
]

all_res = {}
print('NO INDEXED')
print("Running file without arrey...")
r1 = run_program("lab3_FB-34_Tsaryk.py", commands, "log_1.txt")

print("Running file with arrey...")
r2 = run_program("lab3_FB-34_Tsaryk_array.py", commands, "log_2.txt")

for key in r1:
    if key.startswith("SELECT"):
        print(f"{key}: no_arrey={r1[key]:.6f}s   arrey={r2[key]:.6f}s")

print("FASTER VERSION:")
t1 = sum(r1[k] for k in r1 if k.startswith("SELECT"))
t2 = sum(r2[k] for k in r2 if k.startswith("SELECT"))
print("without arrey" if t1 < t2 else "with arrey")
all_res['No_i without array'] = t1
all_res['No_i with array'] = t2

print('INDEXED')
print("Running file without arrey...")
r1i = run_program("lab3_FB-34_Tsaryk.py", commands_i, "log_i1.txt")

print("Running file with arrey...")
r2i = run_program("lab3_FB-34_Tsaryk_array.py", commands_i, "log_i2.txt")

for key in r1i:
    if key.startswith("SELECT"):
        print(f"{key}: no_arrey_i={r1i[key]:.6f}s   arrey_i={r2i[key]:.6f}s")
        
print("FASTER VERSION:")
t1i = sum(r1i[k] for k in r1i if k.startswith("SELECT"))
t2i = sum(r2i[k] for k in r2i if k.startswith("SELECT"))
print("without arrey" if t1i < t2i else "with arrey")
all_res['With_i without array'] = t1i
all_res['With_i with array'] = t2i


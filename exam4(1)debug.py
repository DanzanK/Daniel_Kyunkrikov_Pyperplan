import subprocess
import os
import logging
from threading import Thread
from queue import Queue, Empty

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

domain_file = "domain.pddl"
problem_file = "problem.pddl"

def parse_action_line(line):
    if "Applying action" in line:
        start = line.find('(')
        end = line.find(')')
        if start != -1 and end != -1:
            action_str = line[start+1:end]
            parts = action_str.split()
            action_name = parts[0]
            agent = parts[1]
            params = parts[2:]
            
            if action_name == "pickup_from_table":
                return f"{agent} picks up {params[0]} from table (в процессе планирования)"
            elif action_name == "pickup_from_block":
                return f"{agent} picks up {params[0]} from {params[1]} (в процессе планирования)"
            elif action_name == "place_on_table":
                return f"{agent} places {params[0]} on table (в процессе планирования)"
            elif action_name == "place_on_block":
                return f"{agent} places {params[0]} on {params[1]} (в процессе планирования)"
    return None

def read_output(stream, queue):
    for line in iter(stream.readline, ''):
        queue.put(line)
    stream.close()
    
def parse_plan(plan_str):
    actions = []
    for line in plan_str.strip().splitlines():
        if line.startswith('('):
            action_str = line[1:-1]  
            parts = action_str.split()
            action_name = parts[0]
            agent = parts[1]
            params = parts[2:]
            
            if action_name == "pickup_from_table":
                action = f"{agent} picks up {params[0]} from table"
            elif action_name == "pickup_from_block":
                action = f"{agent} picks up {params[0]} from {params[1]}"
            elif action_name == "place_on_table":
                action = f"{agent} places {params[0]} on table"
            elif action_name == "place_on_block":
                action = f"{agent} places {params[0]} on {params[1]}"
            else:
                action = f"UNKNOWN ACTION: {action_str}"
            actions.append(action)
    return actions

if os.path.exists(domain_file) and os.path.exists(problem_file):
    try:
        logging.info("Запускаем Pyperplan...")
        
        # Запускаем процесс с буферизацией вывода
        proc = subprocess.Popen(
            ["python", "-m", "pyperplan", "--loglevel", "debug", domain_file, problem_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Очередь для захвата вывода
        q = Queue()
        thread = Thread(target=read_output, args=(proc.stdout, q))
        thread.daemon = True
        thread.start()

        print("\nХод планирования:")
        while True:
            try:
                line = q.get_nowait()
                # Пытаемся распарсить действие
                action = parse_action_line(line)
                if action:
                    print(f"► {action}")
                # Выводим весь лог
                print(line, end='')
            except Empty:
                if proc.poll() is not None:
                    break
                continue

        # Завершаем процесс
        proc.wait()
        
        if proc.returncode == 0:
            solution_file = problem_file + ".soln"
            if os.path.exists(solution_file):
                with open(solution_file, "r") as f:
                    plan = f.read()
                parsed_plan = parse_plan(plan)
                print("\nФинальный план действий:")
                for step, action in enumerate(parsed_plan, 1):
                    print(f"Шаг {step}: {action}")
            else:
                print("Файл решения не найден.")
        else:
            print("Ошибка при запуске Pyperplan")
            
    except FileNotFoundError:
        print("Ошибка: Убедитесь, что Pyperplan установлен и доступен.")
else:
    print("Ошибка: Один из PDDL-файлов не найден.")
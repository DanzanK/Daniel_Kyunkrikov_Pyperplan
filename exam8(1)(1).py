import sys
import os
import logging

def is_debug_mode():
 
    return sys.gettrace() is not None

def setup_logging():
    if is_debug_mode():
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s, %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            force=True
        )
        logging.debug("Логгирование в режиме отладки (DEBUG).")
    else:
        logging.basicConfig(
            level=logging.WARNING,
            format='%(asctime)s, %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            force=True
        )
        logging.warning("Логгирование в обычном режиме (WARNING).")

setup_logging()


logging.debug("Это сообщение DEBUG (будет видно только в режиме отладки).")
logging.info("Это сообщение INFO (не будет видно, если не DEBUG).")
logging.warning("Это сообщение WARNING (видно всегда).")

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True
)

domain_file = "domain.pddl"
problem_file = "problem.pddl"

def parse_plan(plan_str):
    actions = plan_str.strip().splitlines()
    parsed_actions = []
    for action in actions:
        parts = action[1:-1].split()
        action_name = parts[0]
        agent = parts[1]
        params = parts[2:]
        if action_name == "pickup_from_table":
            action_str = f"{agent} picks up {params[0]} from table"
        elif action_name == "pickup_from_block":
            action_str = f"{agent} picks up {params[0]} from {params[1]}"
        elif action_name == "place_on_table":
            action_str = f"{agent} places {params[0]} on table"
        elif action_name == "place_on_block":
            action_str = f"{agent} places {params[0]} on {params[1]}"
        else:
            action_str = f"{action_name} {params}"
        parsed_actions.append(action_str)
    return parsed_actions

if os.path.exists(domain_file) and os.path.exists(problem_file):
    try:
        logging.info("Запускаем Pyperplan с уровнем логирования DEBUG...")

        sys.argv = ["pyperplan", "--loglevel", "debug", domain_file, problem_file]
        
        # Импорт главного модуля Pyperplan и запуск main()
        import pyperplan.__main__ as py_main
        try:
            py_main.main()
        except SystemExit as e:
            logging.debug("Pyperplan завершился с кодом: %s", e)
        
        # После выполнения Pyperplan читается файл решения
        solution_file = problem_file + ".soln"
        if os.path.exists(solution_file):
            with open(solution_file, "r") as f:
                plan = f.read()
            parsed_plan = parse_plan(plan)
            print("План действий:")
            for step, action in enumerate(parsed_plan, 1):
                print(f"Шаг {step}: {action}")
        else:
            print("Файл решения не найден.")
    except Exception as e:
        print("Ошибка при запуске Pyperplan:")
        print(e)
else:
    print("Ошибка: Один из PDDL-файлов не найден.")

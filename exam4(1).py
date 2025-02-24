import subprocess
import os
import logging

logging.basicConfig(level=logging.DEBUG)

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
        # Запуск Pyperplan как модуля Python
        print("Запускаем Pyperplan...")
        result = subprocess.run(
            ["python", "-m", "pyperplan", domain_file, problem_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
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
            print("\nПолный вывод Pyperplan:\n", result.stdout)
        else:
            print("Ошибка при запуске Pyperplan:")
            print(result.stderr)
    except FileNotFoundError:
        print("Ошибка: Убедитесь, что Pyperplan установлен и доступен.")
else:
    print("Ошибка: Один из PDDL-файлов не найден.")
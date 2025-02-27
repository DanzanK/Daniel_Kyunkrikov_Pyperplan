#
# This file is part of pyperplan.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

"""
Implements the breadth first search algorithm.
"""

from collections import deque
import logging
import sys

from . import searchspace

def debug_breakpoint():
    """
    Вызывает breakpoint(), только если запущен отладчик (sys.gettrace() != None).
    """
    if sys.gettrace() is not None:
        breakpoint()

def breadth_first_search(planning_task):
    """
    Searches for a plan on the given task using breadth first search and duplicate detection.
    """
    iteration = 0
    queue = deque()
    queue.append(searchspace.make_root_node(planning_task.initial_state))
    closed = {planning_task.initial_state}
    
    while queue:
        iteration += 1
        logging.debug("breadth_first_search: Iteration %d, #unexplored=%d", iteration, len(queue))
        
        # Останавливаемся в отладчике только при наличии активного дебаггера
        debug_breakpoint()
        
        node = queue.popleft()
        
        if planning_task.goal_reached(node.state):
            logging.info("Goal reached. Start extraction of solution.")
            logging.info("%d Nodes expanded", iteration)
            return node.extract_solution()
        
        for operator, successor_state in planning_task.get_successor_states(node.state):
            if hasattr(operator, "parameters") and operator.parameters:
                agent = operator.parameters[0]
            elif isinstance(operator, str):
                parts = operator.strip("()").split()
                agent = parts[1] if len(parts) > 1 else "N/A"
            else:
                agent = "N/A"
            
            logging.debug(
                "Из состояния %s рассматривается оператор '%s' для агента '%s', "
                "приводящий к состоянию %s",
                node.state, operator, agent, successor_state
            )
            
            # Вторая точка останова (тоже только в режиме отладки)
            debug_breakpoint()
            
            if successor_state not in closed:
                queue.append(searchspace.make_child_node(node, operator, successor_state))
                closed.add(successor_state)
                
    logging.info("No operators left. Task unsolvable.")
    logging.info("%d Nodes expanded", iteration)
    return None


# Daniel_Kyunkrikov_Pyperplan
Examination

Задание: Создание мультиагентного планировщика с использованием Pyperplan, задачей которого является построение башни из четырёх блоков (A, B, C, D) двумя агентами, A1 и A2, с учётом ограничений на то, какие блоки каждый агент может обрабатывать.

Для данной задачи были созданы два файла PDDL: domain.pddl и problem.pddl.
Файлы были разработаны вручную на основе классической задачи "мира блоков" (Blocks World), но адаптированы для мультиагентного сценария. 

Домен был расширен добавлением типа agent и предиката can-handle, чтобы ограничить действия каждого агента конкретными блоками.

domain.pddl:

![image](https://github.com/user-attachments/assets/05aa18b2-f468-436b-9db1-608e815bf8eb)


Проблема была составлена с учётом конкретного начального состояния (все блоки на столе) и целевого состояния (башня A-B-C-D).

problem.pddl:

![image](https://github.com/user-attachments/assets/d47f3375-ff53-4faa-ae8d-070beef74bc6)




![image](https://github.com/user-attachments/assets/8a97bfd8-dafd-4aac-a619-76575fba660a)

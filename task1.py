import networkx as nx
import matplotlib.pyplot as plt

from collections import deque


# Створюємо граф
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю
edges = [
    (0,  2, 25),  # Термінал 1 -> Склад 1
    (0,  3, 20),  # Термінал 1 -> Склад 2
    (0,  4, 15),  # Термінал 1 -> Склад 3
    (1,  4, 15),  # Термінал 2 -> Склад 3
    (1,  5, 30),  # Термінал 2 -> Склад 4
    (1,  3, 10),  # Термінал 2 -> Склад 2
    (2,  6, 15),  # Склад 1 -> Магазин 1
    (2,  7, 10),  # Склад 1 -> Магазин 2
    (2,  8, 20),  # Склад 1 -> Магазин 3
    (3,  9, 15),  # Склад 2 -> Магазин 4
    (3, 10, 10),  # Склад 2 -> Магазин 5
    (3, 11, 25),  # Склад 2 -> Магазин 6
    (4, 12, 20),  # Склад 3 -> Магазин 7
    (4, 13, 15),  # Склад 3 -> Магазин 8
    (4, 14, 10),  # Склад 3 -> Магазин 9
    (5, 15, 20),  # Склад 4 -> Магазин 10
    (5, 16, 10),  # Склад 4 -> Магазин 11
    (5, 17, 15),  # Склад 4 -> Магазин 12
    (5, 18,  5),  # Склад 4 -> Магазин 13
    (5, 19, 10),  # Склад 4 -> Магазин 14
]

# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
pos = {
    0: (1, 2),  # Термінал 1
    1: (5, 2),  # Термінал 2
    2: (2, 3),  # Склад 1
    3: (4, 3),  # Склад 2
    4: (2, 1),  # Склад 3
    5: (4, 1),  # Склад 4
    6: (0, 4),  # Магазин 1
    7: (1, 4),  # Магазин 2
    8: (2, 4),  # Магазин 3
    9: (3, 4),  # Магазин 4
    10: (4, 4),  # Магазин 5
    11: (5, 4),  # Магазин 6
    12: (0, 0),  # Магазин 7
    13: (1, 0),  # Магазин 8
    14: (2, 0),  # Магазин 9
    15: (3, 0),  # Магазин 10
    16: (4, 0),  # Магазин 11
    17: (5, 0),  # Магазин 12
    18: (6, 0),  # Магазин 13
    19: (7, 0),  # Магазин 14
}

# Малюємо граф
plt.figure(figsize=(10, 6))
# plt.subplots_adjust(bottom=0.2)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# =============================================================

# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        
        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    
    return False

# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node
        
        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node
        
        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow

# Матриця пропускної здатності для каналів у мережі (capacity_matrix)
capacity_matrix = [
#    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19 
    [0,  0, 25, 20, 15,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     #  0: Термінал 1
    [0,  0,  0, 10, 15, 30,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     #  1: Термінал 2
    [0,  0,  0,  0,  0,  0, 15, 10, 20,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     #  2: Склад 1
    [0,  0,  0,  0,  0,  0,  0,  0,  0, 15, 10, 25,  0,  0,  0,  0,  0,  0,  0,  0],     #  3: Склад 2
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 20, 15, 10,  0,  0,  0,  0,  0],     #  4: Склад 3
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 20, 10, 15,  5, 10],     #  5: Склад 4
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     #  6: Магазин 1
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     #  7: Магазин 2
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     #  8: Магазин 3
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     #  9: Магазин 4
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     # 10: Магазин 5
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     # 11: Магазин 6
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     # 12: Магазин 7
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     # 13: Магазин 8
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     # 14: Магазин 9
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     # 15: Магазин 10
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     # 16: Магазин 11
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     # 17: Магазин 12
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],     # 18: Магазин 13
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]      # 19: Магазин 14
]

sources = [0, 1]
sinks = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

max_flow = 0

for source in sources:
    for sink in sinks:
        current_flow = edmonds_karp(capacity_matrix, source, sink)
        if current_flow == max_flow:
            max_flows.append((source,sink))
        if current_flow > max_flow:
            max_flow = current_flow
            max_flows = [(source,sink)]            

# Додавання тексту 
max_flow_text = f"Максимальний потік: {max_flow}\nМаршрути:{max_flows}" 
plt.suptitle(max_flow_text, x=0.8, y=0.75)

# Відображаємо граф
plt.show()
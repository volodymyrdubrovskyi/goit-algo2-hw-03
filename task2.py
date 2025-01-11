import csv
import timeit

from BTrees.OOBTree import OOBTree



def load_items(filename):
    items = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            items.append({
                'ID': int(row['ID']),
                'Name': row['Name'],
                'Category': row['Category'],
                'Price': float(row['Price'])
            })
    return items

# Створення структур
items_tree = OOBTree()
items_dict = {}


# Функції для додавання товару в структуру
def add_item_to_tree(tree, item):
    tree[item['ID']] = item

def add_item_to_dict(dictionary, item):
    dictionary[item['ID']] = item


# Функції для діапазонного запиту
def range_query_tree(tree, min_price, max_price):
    return [item for item in tree.values(min_price, max_price)]

def range_query_dict(dictionary, min_price, max_price):
    return [item for item in dictionary.values() if min_price <= item['Price'] <= max_price]


# Завантаження товарів
items = load_items('generated_items_data.csv')
min_price = 10
max_price = 100

# Додавання товарів у структури
for item in items:
    add_item_to_tree(items_tree, item)
    add_item_to_dict(items_dict, item)

# Вимірювання часу виконання для кожної структури
tree_time = timeit.timeit(lambda: range_query_tree(items_tree, min_price, max_price), number=100)
dict_time = timeit.timeit(lambda: range_query_dict(items_dict, min_price, max_price), number=100)

# Виведення часу виконання
print(f'Час виконання діапазонного запиту для OOBTree: {tree_time:.6f} секунд (за 100 запитів)')
print(f'Час виконання діапазонного запиту для dict: {dict_time:.6f} секунд (за 100 запитів)')

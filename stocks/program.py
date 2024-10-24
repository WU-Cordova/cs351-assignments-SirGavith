
from stocks.intervaltree import IntervalTree
from stocks.stock import Stock
import csv

def main():
    #parse stocks
    tree: IntervalTree[int, Stock] = IntervalTree()
    with open('./stocks/sample_stock_prices.csv') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)
        for s in reader:
            stock = Stock(*s)
            tree.insert(stock.LowPrice, stock.HighPrice, stock)
    print(tree.Tree)

    print()
    val_q = tree.value_query(155)
    print("Containing 155", len(val_q))
    [print(v) for v in val_q]

    print()
    range_q = tree.range_query(72,73)
    print("In range [72,73]", len(range_q))
    [print(v) for v in range_q]

    print()
    print("Top 5")
    [print(v) for v in tree.highest_k_values(5)]

    print()
    print("Bottom 5")
    [print(v) for v in tree.lowest_k_values(5)]


def small_interval_tree() -> IntervalTree:
    tree: IntervalTree[int, Stock] = IntervalTree()
    tree.insert(100, 150, Stock('AAPL', 'Apple Inc.', 100, 150, '2024-10-21'))
    tree.insert(200, 250, goog := Stock('GOOG', 'Alphabet Inc.', 200, 250, '2024-10-21'))
    tree.insert(150, 175, Stock('MSFT', 'Microsoft Corp.', 150, 175, '2024-10-21'))
    tree.insert(100, 160, Stock('TSLA', 'Tesla Inc.', 100, 160, '2024-10-21'))

    tree.insert(180, 200, None)
    tree.insert(160, 200, None)
    tree.insert(170, 200, None)
    print(tree.Tree)
    print()

    # tree.delete(200, 250, goog)

    print(tree.Tree)

    print(tree.value_query(175))
    print(tree.lowest_k_values(3))
    print(tree.highest_k_values(3))

if __name__ == '__main__':
    main()
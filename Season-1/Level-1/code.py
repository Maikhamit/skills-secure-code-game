'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple

# Define Order and Item
Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

def validorder(order: Order):
    if not isinstance(order.items, (list, tuple)):
        raise ValueError("Order items must be a list or tuple of Item objects.")

    net = 0
    total_order_value = 0
    MAX_AMOUNT = 10_000  # Maximum allowed per payment or product
    MAX_TOTAL_ORDER = 1_000_000  # Maximum allowed per order

    for item in order.items:
        if not isinstance(item, Item):
            raise ValueError(f"Invalid item in order: {item}")
        if not isinstance(item.quantity, int) or item.quantity <= 0:
            raise ValueError(f"Invalid quantity for item: {item.description}. Must be a positive integer.")
        if abs(item.amount) > MAX_AMOUNT:
            raise ValueError(f"Invalid amount for item: {item.description}. Must not exceed ${MAX_AMOUNT:.2f}.")

        if item.type == 'payment':
            net += item.amount
        elif item.type == 'product':
            net -= item.amount * item.quantity
            total_order_value += item.amount * item.quantity
        else:
            raise ValueError(f"Invalid item type: {item.type}")

    if total_order_value > MAX_TOTAL_ORDER:
        return "Total amount payable for an order exceeded"

    # Allow for small floating-point inaccuracies
    if abs(net) < 1e-6:
        return f"Order ID: {order.id} - Full payment received!"
    else:
        return f"Order ID: {order.id} - Payment imbalance: ${net:.2f}"


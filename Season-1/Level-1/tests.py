import unittest
import code as c

class TestOnlineStore(unittest.TestCase):

    def test_1(self):
        """Valid and successful payment for a TV"""
        tv_item = c.Item(type='product', description='tv', amount=1000.00, quantity=1)
        payment = c.Item(type='payment', description='invoice_1', amount=1000.00, quantity=1)
        order_1 = c.Order(id='1', items=[payment, tv_item])
        self.assertEqual(c.validorder(order_1), 'Order ID: 1 - Full payment received!')

    def test_2(self):
        """Detects payment imbalance as TV was never paid for"""
        tv_item = c.Item(type='product', description='tv', amount=1000.00, quantity=1)
        order_2 = c.Order(id='2', items=[tv_item])
        self.assertEqual(c.validorder(order_2), 'Order ID: 2 - Payment imbalance: $-1000.00')

    def test_3(self):
        """Detects payment imbalance when a reimbursement is made"""
        tv_item = c.Item(type='product', description='tv', amount=1000.00, quantity=1)
        payment = c.Item(type='payment', description='invoice_3', amount=1000.00, quantity=1)
        payback = c.Item(type='payment', description='payback_3', amount=-1000.00, quantity=1)
        order_3 = c.Order(id='3', items=[payment, tv_item, payback])
        self.assertEqual(c.validorder(order_3), 'Order ID: 3 - Payment imbalance: $-1000.00')

    def test_4(self):
        """Handles invalid input such as placing an invalid order with fractional quantity"""
        tv = c.Item(type='product', description='tv', amount=1000, quantity=1.5)
        order_1 = c.Order(id='4', items=[tv])
        with self.assertRaises(ValueError) as context:
            c.validorder(order_1)
        self.assertIn("Invalid quantity", str(context.exception))

    def test_5(self):
        """Handles an invalid item type like 'service'"""
        service = c.Item(type='service', description='order shipment', amount=100, quantity=1)
        order_1 = c.Order(id='5', items=[service])
        with self.assertRaises(ValueError) as context:
            c.validorder(order_1)
        self.assertIn("Invalid item type", str(context.exception))

if __name__ == '__main__':
    unittest.main()

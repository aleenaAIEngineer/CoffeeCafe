import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Coffee Cafe Management System

class MenuItem:
    """Represents a menu item in the coffee cafe"""
    def __init__(self, item_id: str, name: str, category: str, price: float, quantity: int):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
    
    def to_dict(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity
        }


class Order:
    """Represents a customer order"""
    def __init__(self, order_id: str, customer_name: str):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = []
        self.order_date = datetime.now()
        self.total = 0.0
    
    def add_item(self, menu_item: MenuItem, quantity: int):
        """Add item to order"""
        if menu_item.quantity >= quantity:
            self.items.append({
                'item_name': menu_item.name,
                'item_id': menu_item.item_id,
                'price': menu_item.price,
                'quantity': quantity,
                'subtotal': menu_item.price * quantity
            })
            self.total += menu_item.price * quantity
            return True
        else:
            print(f"Insufficient stock for {menu_item.name}. Available: {menu_item.quantity}")
            return False
    
    def get_receipt(self):
        """Generate order receipt"""
        receipt = f"\n{'='*40}\n"
        receipt += f"{'COFFEE CAFE ORDER RECEIPT':^40}\n"
        receipt += f"{'='*40}\n"
        receipt += f"Order ID: {self.order_id}\n"
        receipt += f"Customer: {self.customer_name}\n"
        receipt += f"Date: {self.order_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += f"{'-'*40}\n"
        
        for item in self.items:
            receipt += f"{item['item_name']:<25} x{item['quantity']:<2} ${item['subtotal']:>7.2f}\n"
        
        receipt += f"{'-'*40}\n"
        receipt += f"{'TOTAL:':.<32} ${self.total:>7.2f}\n"
        receipt += f"{'='*40}\n"
        return receipt
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'items': self.items,
            'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'total': self.total
        }


class CoffeeCafe:
    """Main Coffee Cafe Management System"""
    
    def __init__(self):
        self.menu = {}
        self.orders = []
        self.order_counter = 1000
        self.inventory_file = 'inventory.json'
        self.orders_file = 'orders.json'
        self.initialize_default_menu()
        self.load_inventory()
    
    def initialize_default_menu(self):
        """Initialize with default menu items"""
        default_items = [
            MenuItem('C001', 'Espresso', 'Coffee', 3.50, 50),
            MenuItem('C002', 'Cappuccino', 'Coffee', 4.50, 50),
            MenuItem('C003', 'Latte', 'Coffee', 5.00, 50),
            MenuItem('C004', 'Americano', 'Coffee', 3.75, 50),
            MenuItem('C005', 'Macchiato', 'Coffee', 4.25, 50),
            MenuItem('F001', 'Croissant', 'Pastry', 3.50, 30),
            MenuItem('F002', 'Muffin', 'Pastry', 2.50, 40),
            MenuItem('F003', 'Sandwich', 'Food', 7.50, 25),
            MenuItem('F004', 'Cookie', 'Pastry', 1.50, 100),
            MenuItem('D001', 'Orange Juice', 'Drink', 3.00, 40),
            MenuItem('D002', 'Iced Tea', 'Drink', 2.50, 50),
        ]
        
        for item in default_items:
            self.menu[item.item_id] = item
    
    def add_menu_item(self, item_id: str, name: str, category: str, price: float, quantity: int):
        """Add new menu item"""
        if item_id in self.menu:
            print(f"Item {item_id} already exists!")
            return False
        
        self.menu[item_id] = MenuItem(item_id, name, category, price, quantity)
        print(f"Menu item '{name}' added successfully!")
        return True
    
    def display_menu(self, category: Optional[str] = None):
        """Display menu items"""
        print("\n" + "="*60)
        print(f"{'COFFEE CAFE MENU':^60}")
        print("="*60)
        
        if category:
            items = [item for item in self.menu.values() if item.category == category]
            print(f"Category: {category}")
        else:
            items = list(self.menu.values())
        
        if not items:
            print("No items found!")
            return
        
        print(f"{'ID':<6} {'Name':<20} {'Category':<12} {'Price':>8} {'Stock':>8}")
        print("-"*60)
        
        for item in items:
            status = "In Stock" if item.quantity > 0 else "OUT OF STOCK"
            print(f"{item.item_id:<6} {item.name:<20} {item.category:<12} ${item.price:>7.2f}  {item.quantity:>7}")
        
        print("="*60)
    
    def create_order(self, customer_name: str, order_items: Dict[str, int]) -> Optional[Order]:
        """Create a new order"""
        self.order_counter += 1
        order = Order(f"ORD{self.order_counter}", customer_name)
        
        for item_id, quantity in order_items.items():
            if item_id not in self.menu:
                print(f"Item {item_id} not found in menu!")
                return None
            
            if not order.add_item(self.menu[item_id], quantity):
                return None
            
            self.menu[item_id].quantity -= quantity
        
        self.orders.append(order)
        return order
    
    def get_inventory_status(self):
        """Get current inventory status"""
        print("\n" + "="*60)
        print(f"{'INVENTORY STATUS':^60}")
        print("="*60)
        
        categories = set(item.category for item in self.menu.values())
        
        for category in sorted(categories):
            print(f"\n{category}:")
            print(f"  {'Name':<25} {'Quantity':>10}")
            print("  " + "-"*35)
            for item in self.menu.values():
                if item.category == category:
                    status = "✓" if item.quantity > 0 else "✗ LOW"
                    print(f"  {item.name:<25} {item.quantity:>9} {status}")
        
        print("\n" + "="*60)
    
    def restock_item(self, item_id: str, quantity: int):
        """Restock an item"""
        if item_id not in self.menu:
            print(f"Item {item_id} not found!")
            return False
        
        self.menu[item_id].quantity += quantity
        print(f"Restocked {self.menu[item_id].name} with {quantity} units.")
        return True
    
    def view_order_history(self):
        """View all orders"""
        if not self.orders:
            print("No orders yet!")
            return
        
        print("\n" + "="*60)
        print(f"{'ORDER HISTORY':^60}")
        print("="*60)
        
        for order in self.orders:
            print(f"\nOrder ID: {order.order_id}")
            print(f"Customer: {order.customer_name}")
            print(f"Date: {order.order_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Total: ${order.total:.2f}")
            print(f"Items: {len(order.items)}")
        
        print("\n" + "="*60)
    
    def get_sales_report(self):
        """Generate sales report"""
        if not self.orders:
            print("No sales data!")
            return
        
        total_sales = sum(order.total for order in self.orders)
        total_orders = len(self.orders)
        avg_order = total_sales / total_orders if total_orders > 0 else 0
        
        print("\n" + "="*60)
        print(f"{'SALES REPORT':^60}")
        print("="*60)
        print(f"Total Orders: {total_orders}")
        print(f"Total Sales: ${total_sales:.2f}")
        print(f"Average Order Value: ${avg_order:.2f}")
        
        # Popular items
        item_sales = {}
        for order in self.orders:
            for item in order.items:
                if item['item_name'] not in item_sales:
                    item_sales[item['item_name']] = {'quantity': 0, 'revenue': 0}
                item_sales[item['item_name']]['quantity'] += item['quantity']
                item_sales[item['item_name']]['revenue'] += item['subtotal']
        
        print(f"\n{'Most Popular Items':^60}")
        print("-"*60)
        print(f"{'Item Name':<25} {'Quantity':>10} {'Revenue':>15}")
        print("-"*60)
        
        for item_name in sorted(item_sales.keys(), key=lambda x: item_sales[x]['revenue'], reverse=True):
            sales_data = item_sales[item_name]
            print(f"{item_name:<25} {sales_data['quantity']:>10} ${sales_data['revenue']:>14.2f}")
        
        print("="*60)
    
    def save_inventory(self):
        """Save inventory to file"""
        data = {item_id: item.to_dict() for item_id, item in self.menu.items()}
        with open(self.inventory_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Inventory saved to {self.inventory_file}")
    
    def load_inventory(self):
        """Load inventory from file"""
        if os.path.exists(self.inventory_file):
            try:
                with open(self.inventory_file, 'r') as f:
                    data = json.load(f)
                    for item_id, item_data in data.items():
                        self.menu[item_id] = MenuItem(
                            item_data['item_id'],
                            item_data['name'],
                            item_data['category'],
                            item_data['price'],
                            item_data['quantity']
                        )
                print(f"Inventory loaded from {self.inventory_file}")
            except Exception as e:
                print(f"Error loading inventory: {e}")
    
    def save_orders(self):
        """Save orders to file"""
        data = [order.to_dict() for order in self.orders]
        with open(self.orders_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Orders saved to {self.orders_file}")
    
    def load_orders(self):
        """Load orders from file"""
        if os.path.exists(self.orders_file):
            try:
                with open(self.orders_file, 'r') as f:
                    data = json.load(f)
                    for order_data in data:
                        order = Order(order_data['order_id'], order_data['customer_name'])
                        order.items = order_data['items']
                        order.total = order_data['total']
                        self.orders.append(order)
                print(f"Orders loaded from {self.orders_file}")
            except Exception as e:
                print(f"Error loading orders: {e}")


def main_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print(f"{'COFFEE CAFE MANAGEMENT SYSTEM':^60}")
    print("="*60)
    print("1. View Menu")
    print("2. Create Order")
    print("3. View Inventory")
    print("4. Restock Item")
    print("5. View Order History")
    print("6. View Sales Report")
    print("7. Add New Menu Item")
    print("8. Save Data")
    print("9. Exit")
    print("="*60)


def main():
    """Main application loop"""
    cafe = CoffeeCafe()
    cafe.load_orders()
    
    while True:
        main_menu()
        choice = input("Choose an option (1-9): ").strip()
        
        if choice == '1':
            # View Menu
            print("\nView Menu by Category:")
            print("1. All Items")
            print("2. Coffee")
            print("3. Pastry")
            print("4. Food")
            print("5. Drink")
            cat_choice = input("Choose category: ").strip()
            
            categories = {'2': 'Coffee', '3': 'Pastry', '4': 'Food', '5': 'Drink'}
            category = categories.get(cat_choice)
            cafe.display_menu(category)
        
        elif choice == '2':
            # Create Order
            customer_name = input("Enter customer name: ").strip()
            if not customer_name:
                print("Customer name cannot be empty!")
                continue
            
            cafe.display_menu()
            order_items = {}
            
            while True:
                item_id = input("Enter item ID (or 'done' to finish): ").strip().upper()
                if item_id == 'DONE':
                    break
                
                if item_id not in cafe.menu:
                    print("Item not found!")
                    continue
                
                try:
                    quantity = int(input(f"Quantity for {cafe.menu[item_id].name}: "))
                    if quantity > 0:
                        order_items[item_id] = quantity
                except ValueError:
                    print("Invalid quantity!")
            
            if order_items:
                order = cafe.create_order(customer_name, order_items)
                if order:
                    print(order.get_receipt())
                else:
                    print("Order creation failed!")
            else:
                print("No items added to order!")
        
        elif choice == '3':
            # View Inventory
            cafe.get_inventory_status()
        
        elif choice == '4':
            # Restock Item
            cafe.display_menu()
            item_id = input("Enter item ID to restock: ").strip().upper()
            try:
                quantity = int(input("Enter quantity to add: "))
                cafe.restock_item(item_id, quantity)
            except ValueError:
                print("Invalid input!")
        
        elif choice == '5':
            # View Order History
            cafe.view_order_history()
        
        elif choice == '6':
            # View Sales Report
            cafe.get_sales_report()
        
        elif choice == '7':
            # Add New Menu Item
            try:
                item_id = input("Enter item ID: ").strip().upper()
                name = input("Enter item name: ").strip()
                category = input("Enter category: ").strip()
                price = float(input("Enter price: "))
                quantity = int(input("Enter initial quantity: "))
                cafe.add_menu_item(item_id, name, category, price, quantity)
            except ValueError:
                print("Invalid input!")
        
        elif choice == '8':
            # Save Data
            cafe.save_inventory()
            cafe.save_orders()
            print("All data saved successfully!")
        
        elif choice == '9':
            # Exit
            save = input("Save data before exiting? (y/n): ").strip().lower()
            if save == 'y':
                cafe.save_inventory()
                cafe.save_orders()
            print("Thank you for using Coffee Cafe! Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()

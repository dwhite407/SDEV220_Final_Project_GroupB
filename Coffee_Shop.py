import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget,
    QMessageBox, QStackedWidget, QHBoxLayout, QScrollArea, QFrame, QGridLayout, QComboBox, QInputDialog
)
from PyQt5.QtCore import Qt

class CoffeeShopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Little Bear Coffee")
        self.shop_window = None
        self.order_window = None
        self.payment_window = None
        self.show_shop_func = None
        self.inventory = {
            "Water": 10,
            "Espresso": 10,
            "Cappuccino": 10,
            "Latte": 10,
            "Mocha": 10,
            "Americano": 10,
            "Macchiato": 10,
            "Flat White": 10,
            "Iced Coffee": 10,
            "Hot Chocolate": 10,
            "Chai Latte": 10,
            "Green Tea": 10,
            "Black Tea": 10,
            "Herbal Tea": 10,
            "Soda": 10,
            "Lemonade": 10,
            "Sparkling Water": 10
        }
        self.initUI()
        self.showFullScreen()

    def initUI(self):
        self.show_shop_func = self.show_shop
        layout = QVBoxLayout()

        # Create a label for the welcome message
        welcome_label = QLabel("Welcome to the Little Bear Coffee Shop")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; font-family: Arial;")
        layout.addWidget(welcome_label)

        # shop button
        shop_button = QPushButton("Shop")
        shop_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
        """)
        shop_button.clicked.connect(self.show_shop)
        layout.addWidget(shop_button)

        # inventory button
        inventory_button = QPushButton("Inventory")
        inventory_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                 font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
        """)
        inventory_button.clicked.connect(self.show_inventory)
        layout.addWidget(inventory_button)

        # order details button
        order_button = QPushButton("Order Details")
        order_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                 font-size: 14px;
                height: 40px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
        """)
        order_button.clicked.connect(self.show_order)
        layout.addWidget(order_button)

        # exit button
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                 font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
        """)
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        container = QWidget()
        container.setLayout(layout)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(container)
        self.order_window = OrderWindow(self.stacked_widget, self, self.show_shop_func)
        self.payment_window = PaymentWindow(self.stacked_widget, self.show_order, [], self)
        self.stacked_widget.addWidget(self.order_window)
        self.stacked_widget.addWidget(self.payment_window)
        self.order_index = self.stacked_widget.indexOf(self.order_window)
        self.payment_index = self.stacked_widget.indexOf(self.payment_window)
        self.setCentralWidget(self.stacked_widget)

    def show_shop(self):
        if self.shop_window is None:
            self.shop_window = ShopWindow(self.stacked_widget, self, self.show_order)
            self.stacked_widget.addWidget(self.shop_window)
        shop_index = self.stacked_widget.indexOf(self.shop_window)
        self.stacked_widget.setCurrentIndex(shop_index)

    def show_inventory(self):
        inventory_text = "Inventory:\n"
        for drink, count in self.inventory.items():
            inventory_text += f"{drink}: {count}\n"
        QMessageBox.information(self, "Inventory", inventory_text)

    def show_order(self):
        self.stacked_widget.setCurrentIndex(self.order_index)

    def show_payment(self):
        # update the payment window
        self.payment_window.order = self.order_window.order
        self.payment_window.update_order_summary()
        self.stacked_widget.setCurrentIndex(self.payment_index)

class ShopWindow(QWidget):
    def __init__(self, stacked_widget, main_window, show_order_func):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.show_order_func = show_order_func
        self.setWindowTitle("Shop")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Shop Menu")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; font-family: Arial;")
        layout.addWidget(title_label)

        # Scroll area for drinks
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QFrame()
        scroll_layout = QGridLayout(scroll_content)

        self.load_drinks(scroll_layout)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
       
        # View Order Button
        view_order_button = QPushButton("View Order")
        view_order_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
        """)
        view_order_button.clicked.connect(self.show_order)
        layout.addWidget(view_order_button)
       
        # Back Button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
        """)
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

     
        self.setLayout(layout)

    # Sets the drinks for the shop page
    def load_drinks(self, scroll_layout):
        self.drinks = {
            "Water": {"type": "Water", "price": 1.00, "options": ["Iced", "Warm"]},
            "Espresso": {"type": "Coffee", "price": 3.00, "options": ["Single", "Double"]},
            "Cappuccino": {"type": "Coffee", "price": 4.00, "options": ["Regular", "Decaf"]},
            "Latte": {"type": "Coffee", "price": 4.50, "options": ["Vanilla", "Caramel", "Mocha"]},
            "Mocha": {"type": "Coffee", "price": 5.00, "options": ["Iced", "Hot"]},
            "Americano": {"type": "Coffee", "price": 3.50, "options": ["Iced", "Hot"]},
            "Macchiato": {"type": "Coffee", "price": 4.25, "options": ["Caramel", "Vanilla"]},
            "Flat White": {"type": "Coffee", "price": 4.75, "options": []},
            "Iced Coffee": {"type": "Coffee", "price": 4.00, "options": ["Sweet", "Unsweet"]},
            "Hot Chocolate": {"type": "Other", "price": 3.75, "options": ["Regular", "Dark"]},
            "Chai Latte": {"type": "Other", "price": 4.50, "options": ["Regular", "Spiced"]},
            "Green Tea": {"type": "Tea", "price": 2.75, "options": ["Hot", "Iced"]},
            "Black Tea": {"type": "Tea", "price": 2.50, "options": ["Hot", "Iced"]},
            "Herbal Tea": {"type": "Tea", "price": 3.00, "options": ["Chamomile", "Peppermint"]},
            "Soda": {"type": "Other", "price": 2.00, "options": ["Cola", "Sprite", "Fanta"]},
            "Lemonade": {"type": "Other", "price": 2.25, "options": ["Regular", "Strawberry", "Raspberry"]},
            "Sparkling Water": {"type": "Water", "price": 1.50, "options": []}
        }

        # Title labels for drinks
        col_labels = ["Water", "Coffee", "Tea", "Other"]
        col_positions = {label: i for i, label in enumerate(col_labels)}
        
        row = 0
        for label in col_labels:
            col_title_layout = QHBoxLayout()
            col_title = QLabel(label)
            col_title.setAlignment(Qt.AlignLeft)
            col_title.setStyleSheet("font-size: 20px; font-weight: bold; font-family: Arial;")
            col_title_layout.addWidget(col_title)
            scroll_layout.addLayout(col_title_layout,row,col_positions[label])
        
        
        for label in col_labels:
            col = col_positions[label]
            row = 1
            for drink_name, drink_data in self.drinks.items():
                if drink_data['type'] == label:
                    drink_layout = QVBoxLayout()

                    drink_label = QLabel(f"{drink_name}\n${drink_data['price']:.2f}")
                    drink_label.setAlignment(Qt.AlignCenter)
                    drink_label.setStyleSheet("font-size: 16px; font-family: Arial;")
                    drink_layout.addWidget(drink_label)

                    # Add Variation Option
                    if drink_data["options"]:
                        variation_combo = QComboBox()
                        variation_combo.addItems(drink_data["options"])
                        drink_layout.addWidget(variation_combo)


                    add_button = QPushButton("Add to Order")
                    add_button.setStyleSheet("""
                        QPushButton {
                            background-color: rgb(55, 77, 120);
                            color: white;
                            border: 1px solid black;
                            height: 35px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: rgb(83, 116, 181);
                            color: black;
                        }
                    """)
                    add_button.clicked.connect(lambda _, name=drink_name, price=drink_data['price'], combo=variation_combo if "options" in drink_data else None: self.add_to_order(name, price, combo))
                    drink_layout.addWidget(add_button)

                    scroll_layout.addLayout(drink_layout, row, col)
                    row += 1
    def back_to_main(self):
        # Go back to the main page
        self.stacked_widget.setCurrentIndex(0)

    def add_to_order(self, drink_name, price, variation_combo):
        selected_variation = variation_combo.currentText() if variation_combo else ""
        quantity, ok = QInputDialog.getInt(self, "Quantity", f"Enter quantity for {drink_name}:", 1, 1, 10)  # Default to 1, min 1 max 10
        if ok:
            selected_drink = {"name": drink_name, "price": price, "variation": selected_variation, "quantity": quantity}
            self.main_window.order_window.add_order(selected_drink)
            self.decrement_inventory(drink_name, quantity)
            QMessageBox.information(self, "Order Added", f"{quantity} {selected_drink['name']}(s) ({selected_variation}) added to order.")
    
    def show_order(self):
      self.show_order_func()
    
    def decrement_inventory(self, product, quantity):
        if self.main_window.inventory[product] >= quantity:
            self.main_window.inventory[product] -= quantity
        else:
            QMessageBox.information(self, "Out of Stock", f"{product} is out of stock!")

# Class for the view order page
class OrderWindow(QWidget):
    def __init__(self, stacked_widget, main_window, show_shop_func):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.show_shop_func = show_shop_func
        self.main_window = main_window  
        self.setWindowTitle("Order Details")
        self.initUI()
        self.order = []  # Stores orders

    def add_order(self, drink):
         # Check if the item is already in the order
        for item in self.order:
            if item["name"] == drink["name"] and item["variation"] == drink["variation"]:
                item["quantity"] += drink["quantity"]  # Increment the quantity
                self.update_order_display()
                return

        # Put in order
        self.order.append(drink)
        self.update_order_display()

    def initUI(self):
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Order Details")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; font-family: Arial;")
        layout.addWidget(title_label)
        
        # Background for the order list
        order_frame = QFrame()
        order_frame.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 5px;")
        order_layout = QVBoxLayout(order_frame)

        # Order Details
        self.order_details = QLabel("No orders placed yet.")
        self.order_details.setAlignment(Qt.AlignLeft)
        self.order_details.setStyleSheet("font-size: 16px; font-family: Arial;")
        order_layout.addWidget(self.order_details)
        self.order_details.setTextFormat(Qt.RichText)

        layout.addWidget(order_frame)


         # Order Total Label
        self.order_total_label = QLabel("Total: $0.00")
        self.order_total_label.setAlignment(Qt.AlignRight)
        self.order_total_label.setStyleSheet("font-size: 16px; font-family: Arial;")
        layout.addWidget(self.order_total_label)

        # Payment button
        payment_button = QPushButton("Payment")
        payment_button.setStyleSheet("""
           QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
        """)
        payment_button.clicked.connect(self.show_payment)
        layout.addWidget(payment_button)
        
         # Back to Shop Button
        back_to_shop_button = QPushButton("Back to Shop")
        back_to_shop_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
        """)
        back_to_shop_button.clicked.connect(self.show_shop)
        layout.addWidget(back_to_shop_button)

        # Back Button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
        """)
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        # Set layout
        self.setLayout(layout)

    #updates orders when added
    def update_order_display(self):
        if self.order:
            order_text = ""
            total = 0
            for item in self.order:
                item_total = item['price'] * item['quantity']
                order_text += f"- <span style='font-weight: bold;'>{item['name']}</span>"
                if item["variation"]:
                    order_text += f" ({item['variation']})"
                order_text += f' x {item["quantity"]} <span style="float: right;">${item_total:.2f}</span><br>'
                total += item_total
                
            self.order_details.setText(f"<div style='padding: 10px;'>{order_text}</div>")
            self.order_total_label.setText(f"Total: ${total:.2f}")
        else:
            self.order_details.setText("No orders placed yet.")
            self.order_total_label.setText("Total: $0.00")

    def show_payment(self):
        self.main_window.show_payment()
    
    def show_shop(self):
         self.show_shop_func()

    #back to main menu button
    def back_to_main(self):
        self.stacked_widget.setCurrentIndex(0)

#payment page
class PaymentWindow(QWidget):
    def __init__(self, stacked_widget, show_order_func, order, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.show_order_func = show_order_func
        self.main_window = main_window
        self.setWindowTitle("Payment")
        self.order = order
        self.initUI()

    def initUI(self):
       layout = QVBoxLayout()

        # Title Label
       title_label = QLabel("Payment")
       title_label.setAlignment(Qt.AlignCenter)
       title_label.setStyleSheet("font-size: 28px; font-weight: bold; font-family: Arial;")
       layout.addWidget(title_label)

       # Display the order summary
       self.order_summary = QLabel()
       self.order_summary.setAlignment(Qt.AlignLeft)
       self.order_summary.setStyleSheet("font-size: 16px; font-family: Arial;")
       self.update_order_summary()
       layout.addWidget(self.order_summary)
       self.order_summary.setTextFormat(Qt.RichText)


       # Payment options
       payment_options_layout = QHBoxLayout()

       cash_button = QPushButton("Cash")
       cash_button.setStyleSheet("""
           QPushButton {
              background-color: rgb(55, 77, 120);
              color: white;
              border: 1px solid black;
              height: 40px;
              font-size: 14px;
           }
           QPushButton:hover {
              background-color: rgb(83, 116, 181);
              color: black;
            }
       """)
       cash_button.clicked.connect(self.complete_payment)
       payment_options_layout.addWidget(cash_button)


       card_button = QPushButton("Credit Card")
       card_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                font-size: 14px;
            }
            QPushButton:hover {
               background-color: rgb(83, 116, 181);
               color: black;
            }
       """)
       card_button.clicked.connect(self.complete_payment)
       payment_options_layout.addWidget(card_button)
       
       layout.addLayout(payment_options_layout)

       # Back to Order button
       back_button = QPushButton("Back to Order")
       back_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                font-size: 14px;
            }
            QPushButton:hover {
               background-color: rgb(83, 116, 181);
               color: black;
            }
       """)
       back_button.clicked.connect(self.back_to_order)
       layout.addWidget(back_button)
       
       # Back to shop button
       back_to_shop_button = QPushButton("Back to Shop")
       back_to_shop_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                font-size: 14px;
            }
            QPushButton:hover {
               background-color: rgb(83, 116, 181);
               color: black;
            }
       """)
       back_to_shop_button.clicked.connect(self.show_shop)
       layout.addWidget(back_to_shop_button)


       self.setLayout(layout)

    def update_order_summary(self):
        if self.order:
            order_text = ""
            total = 0
            for item in self.order:
                item_total = item['price'] * item['quantity']
                order_text += f"- <span style='font-weight: bold;'>{item['name']}</span>"
                if item["variation"]:
                   order_text += f" ({item['variation']})"
                order_text += f' x {item["quantity"]} <span style="float: right;">${item_total:.2f}</span><br>'
                total += item_total
                
            self.order_summary.setText(f'<div style="padding: 10px;">{order_text} <hr> Total: <span style="float: right;">${total:.2f}</span></div>')
        else:
           self.order_summary.setText("No orders placed yet.")

    def back_to_order(self):
       self.main_window.show_order()
    
    def show_shop(self):
        self.main_window.show_shop()
    
    def complete_payment(self):
       QMessageBox.information(self, "Payment Successful", "Payment was successful")
       # Clear the order 
       self.main_window.order_window.order.clear() 
       self.main_window.order_window.update_order_display() 
       self.main_window.show_order()
       
# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #EBEEF7; /* Makes whole app background white */
        }

        QPushButton {
                background-color: rgb(55, 77, 120);
                color: white;
                border: 1px solid black;
                height: 40px;
                 font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgb(83, 116, 181);
                color: black;
            }
    """)
    main_window = CoffeeShopApp()
    main_window.show()
    sys.exit(app.exec_())

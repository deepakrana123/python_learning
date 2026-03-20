class OrderState:
    def next(self,order):
        pass
    def previous(self,order):
        pass
    def status(self):
        pass


class PendingState(OrderState):
    def next(self,order):
        print('order is shipped')
        order.set_state(ShippedState())
    def previous(self,order):
        print("Order is already in Pending state.")
    def status(self):
        return 'Pending'
class ShippedState(OrderState):
    def next(self,order):
        print('order is shipped')
        order.set_state(DeliverdState())
    def previous(self,order):
        print("Order is already in delivered state.")
        order.set_state(PendingState())
    def status(self):
        return 'Shipped'
class DeliverdState(OrderState):
    def next(self,order):
        print('order is reached')
    def previous(self,order):
        print("Order is already in shipped state.")
        order.set_state(ShippedState())
    def status(self):
        return 'Delivered'


class Order:
    def __init__(self):
        self.state=PendingState()
    def set_state(self,state):
        self.state=state
    def next_state(self):
        return self.state.next()
    def prev_state(self):
        return self.state.previous()
    def status(self):
        return self.state.status



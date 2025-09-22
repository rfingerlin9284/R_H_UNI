"""
Order Execution with RICK compliance
Extract from OANDA_CBA_UNIBOT working implementation
"""

import time
from datetime import datetime, timedelta


class OrderExecutor:
    def __init__(self, broker_client):
        self.broker = broker_client
        self.max_ttl = timedelta(hours=6)

    def place_order_with_oco(self, order_params):
        """Place order with OCO and TTL enforcement."""
        # Set TTL
        order_params['expire_time'] = datetime.utcnow() + self.max_ttl

        # Place primary order
        primary = self.broker.place_order(order_params)

        # Place OCO orders
        stop_loss = self.broker.place_stop(
            order_id=primary['id'],
            price=order_params['stop_loss']
        )

        take_profit = self.broker.place_limit(
            order_id=primary['id'],
            price=order_params['take_profit']
        )

        return {
            'primary': primary,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'ttl': order_params['expire_time']
        }

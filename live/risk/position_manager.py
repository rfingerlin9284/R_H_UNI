"""
Position and Risk Management
Extracted from proven profitable systems
"""

class PositionManager:
    def __init__(self):
        self.max_risk_per_trade = 0.01  # 1%
        self.max_daily_loss = 0.05  # 5%
        self.max_concurrent = 3

    def calculate_position_size(self, account_balance, stop_distance, risk_override=None):
        """Kelly-criterion inspired sizing from profitable runs."""
        # EXTRACT from working position sizing in OANDA_CBA_UNIBOT
        risk = risk_override or self.max_risk_per_trade
        risk_amount = account_balance * risk
        if stop_distance == 0:
            return 0.0
        position_size = risk_amount / stop_distance

        # Apply leverage constraints
        max_leverage = 2.0  # Proven safe leverage
        max_position = account_balance * max_leverage

        return min(position_size, max_position)

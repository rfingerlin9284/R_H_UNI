"""Bearish regime wolf pack template

This pack delegates to the extracted adapter when available. Import is
performed lazily in __init__ to keep module import lightweight.
"""
from ._base import WolfPackBase


class BearishWolfPack(WolfPackBase):
    def __init__(self):
        try:
            from .extracted_oanda import ExtractedFuturesStrategy
            self._strategy = ExtractedFuturesStrategy()
        except Exception:
            self._strategy = None

    def calculate_indicators(self, market_data):
        if self._strategy is None:
            return {'vol': None}
        # reuse extracted adapter method where available
        return self._strategy.calculate_technical_signals(market_data)

    def generate_signals(self, market_data):
        if self._strategy is None:
            return {'side': 'sell', 'notional': 15000, 'risk_reward': 3.2}

        tech = self.calculate_indicators(market_data)
        final = self._strategy.apply_sentiment_filter(tech, None)
        size = self._strategy.calculate_position_size(final, account_balance=10000)
        side = final.get('signal', 'SELL')
        return {
            'side': side.lower() if isinstance(side, str) else 'sell',
            'notional': float(size),
            'risk_reward': final.get('confidence', 0.3) * 3.0,
            'confidence': final.get('confidence', 0.0),
        }

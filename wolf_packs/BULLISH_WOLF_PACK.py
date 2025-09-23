"""Bullish regime wolf pack template

This file is a template assembled for human review. It contains placeholders and
high-level method wiring; any concrete strategy methods found by the agent should
be inserted or adapted here.
"""
from ._base import WolfPackBase


class BullishWolfPack(WolfPackBase):
    """Bullish regime wolf pack that delegates signal calculations
    to the extracted OANDA adapter when available.

    The import of the heavier adapter is done lazily inside __init__ so
    module import remains lightweight (no pandas/numpy required).
    """
    def __init__(self):
        # lazy import so module import stays light
        try:
            from .extracted_oanda import ExtractedFuturesStrategy
            self._strategy = ExtractedFuturesStrategy()
        except Exception:
            # Fallback to None — keep API stable but degrade gracefully
            self._strategy = None

    def calculate_indicators(self, market_data):
        if self._strategy is None:
            return {'ma_fast': None, 'ma_slow': None}
        return self._strategy.calculate_technical_signals(market_data)

    def generate_signals(self, market_data):
        """Produce a unified signal dict for the wolf pack consumer.

        market_data can be a pandas DataFrame or a lightweight list-of-dicts;
        the extracted adapter handles both in a conservative way.
        """
        if self._strategy is None:
            return {'side': 'hold', 'notional': 0.0, 'risk_reward': 0.0}

        tech = self.calculate_indicators(market_data)
        # sentiment may be embedded in market_data
        sentiment = None
        if isinstance(market_data, dict):
            sentiment = market_data.get('sentiment')

        final = self._strategy.apply_sentiment_filter(tech, sentiment)
        size = self._strategy.calculate_position_size(final, account_balance=10000)
        side = final.get('signal', 'HOLD')
        return {
            'side': side.lower() if isinstance(side, str) else 'hold',
            'notional': float(size),
            'risk_reward': final.get('confidence', 0.3) * 3.0,
            'confidence': final.get('confidence', 0.0),
        }

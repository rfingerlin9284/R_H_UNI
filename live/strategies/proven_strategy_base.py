"""
Base Strategy - Extract ONLY proven profitable logic
NO DETERMINISTIC ELEMENTS
"""

import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Optional


class ProvenStrategyBase(ABC):
    """Base class for proven strategies only."""

    def __init__(self):
        # NO SEEDS, NO DETERMINISTIC ELEMENTS
        self.performance_threshold = {
            'min_sharpe': 0.8,
            'min_win_rate': 0.55,
            'max_drawdown': 0.30,
            'min_expectancy': 0.0
        }

    @abstractmethod
    def calculate_signal(self, data: pd.DataFrame) -> Dict:
        """Must be implemented by proven strategies."""
        pass

    def validate_market_conditions(self, data: pd.DataFrame) -> bool:
        """Real market condition checks - NO DETERMINISTIC."""
        try:
            volatility = data['close'].pct_change().rolling(20).std().iloc[-1]
            volume = data['volume'].iloc[-1]
            spread = (data['high'].iloc[-1] - data['low'].iloc[-1]) / data['close'].iloc[-1]
        except Exception:
            return False

        return all([
            volatility > 0.0001,  # Market is moving
            volume > 0,  # Has volume
            spread < 0.01  # Reasonable spread
        ])

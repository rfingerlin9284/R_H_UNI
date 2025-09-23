"""Wolf Pack base helpers and interfaces"""
from typing import Dict, Any
from abc import ABC, abstractmethod

class WolfPackBase(ABC):
    """Abstract base class for regime specialized wolf packs."""

    @abstractmethod
    def generate_signals(self, market_data) -> Dict[str, Any]:
        """Return signals dict: {'side': 'buy'|'sell'|'hold', 'notional': float, ...}"""
        raise NotImplementedError()

    @abstractmethod
    def calculate_indicators(self, market_data):
        raise NotImplementedError()

    def validate_rick_constraints(self, signal: Dict[str, Any]) -> bool:
        """Basic RICK charter constraints check (minimal)."""
        # Example constraints (can be tuned by consumer)
        if signal.get('notional', 0) < 15000:
            return False
        if signal.get('risk_reward', 0) < 3.2:
            return False
        return True

"""Non-deterministic helpers and ImprovedWolfPack implementation.

This module provides small, import-safe utilities to avoid deterministic
poisoning (no global seeds), add market-style noise, detect regimes (stub),
and a high-level ImprovedWolfPack implementation for human review.
"""
from typing import Dict, Any
import numpy as np
import math


def add_market_noise(price: float, volatility: float) -> float:
    """Add light, realistic microstructure noise to a price.

    Note: This function does NOT seed the RNG. Use only in backtests or
    simulations where randomness is expected. Never set global seeds here.
    """
    noise = np.random.normal(0, max(1e-8, volatility * 0.001))
    return float(price * (1.0 + noise))


class MarketRegimeDetector:
    """Very small stub for regime detection.

    This detector uses simple volatility / trend heuristics. It's lightweight
    and intended as a placeholder; replace with a more robust detector when
    extracting methods from other repos.
    """
    def __init__(self, lookback: int = 50):
        self.lookback = lookback

    def detect(self, df) -> str:
        """Return one of: 'bullish', 'bearish', 'sideways'.

        df is expected to be a pandas-like DataFrame with a `close` column.
        """
        try:
            closes = df['close'].astype(float)
            recent = closes[-self.lookback:]
            ret = (recent.iloc[-1] - recent.iloc[0]) / recent.iloc[0]
            vol = recent.pct_change().std()
        except Exception:
            # If input is not as expected, default to 'sideways'
            return 'sideways'

        if ret > 0.02 and vol < 0.05:
            return 'bullish'
        if ret < -0.02 and vol < 0.05:
            return 'bearish'
        return 'sideways'


class ImprovedWolfPack:
    """High-level, non-deterministic wolf pack orchestrator.

    This class ties a simple regime detector to per-regime strategy stubs and
    demonstrates non-deterministic entry logic (no counters, no global seeds).
    Replace strategy stubs with extracted methods from other repos when available.
    """
    def __init__(self, avg_volatility: float = 0.01):
        self.regime_detector = MarketRegimeDetector()
        self.avg_volatility = avg_volatility

    def calculate_dynamic_confluence(self, signals: Dict[str, float]) -> float:
        # Very simple weighted confluence metric
        weights = {'trend': 0.4, 'momentum': 0.3, 'volume': 0.2, 'volatility': 0.1}
        conf = 0.0
        for k, w in weights.items():
            conf += w * float(signals.get(k, 0.0))
        # Normalize to 0..1
        return 1.0 / (1.0 + math.exp(-conf))

    def calculate_market_confidence(self, data, regime: str) -> float:
        # Simple heuristic: stronger trending regimes yield higher confidence
        return 0.6 if regime == 'bullish' else (0.6 if regime == 'bearish' else 0.45)

    def determine_action(self, confluence: float, confidence: float) -> str:
        score = confluence * confidence
        if score > 0.65:
            return 'buy'
        if score < 0.35:
            return 'sell'
        return 'hold'

    def dynamic_position_size(self, confidence: float, data) -> float:
        # Very small position sizing example: scale with confidence
        base = 15000.0
        return base * max(0.5, min(1.5, confidence * 1.0))

    def adaptive_stops(self, data, regime: str) -> Dict[str, float]:
        # Placeholder adaptive stops
        return {'stop_loss': 0.01, 'take_profit': 0.03}

    def calculate_entry(self, data) -> Dict[str, Any]:
        regime = self.regime_detector.detect(data)
        # Example signal stubs (replace with extracted methods)
        # For safety, we avoid using counters or fixed RNG seeds here
        signals = {
            'trend': 0.7 if regime == 'bullish' else (-0.7 if regime == 'bearish' else 0.0),
            'momentum': 0.6,
            'volume': 1.0,
            'volatility': 0.5,
        }

        confluence = self.calculate_dynamic_confluence(signals)
        confidence = self.calculate_market_confidence(data, regime)

        return {
            'action': self.determine_action(confluence, confidence),
            'size': self.dynamic_position_size(confidence, data),
            'stops': self.adaptive_stops(data, regime),
            'regime': regime,
            'confluence': confluence,
            'confidence': confidence,
        }

"""Adapted extraction of candidate methods from OANDA_CBA_UNIBOT

This module provides a lightweight, import-safe wrapper around the
futures signal logic discovered in the cloned repo. It intentionally
avoids heavy imports at module import time (no pandas/numpy at top-level)
so it can be imported in environments without those dependencies.

Use these methods as adapters that accept plain Python structures (lists/dicts)
or pandas DataFrames (the functions will import pandas locally when needed).
"""
from typing import Dict, Any, Optional


class ExtractedFuturesStrategy:
    """Lightweight adapter with methods copied/adapted from the futures engine.

    Methods here are conservative and designed to be easy to test and adapt.
    """

    def __init__(self, rsi_oversold: int = 30, rsi_overbought: int = 70,
                 volatility_threshold: float = 5.0, confidence_threshold: float = 0.65):
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.volatility_threshold = volatility_threshold
        self.confidence_threshold = confidence_threshold

    def calculate_technical_signals(self, df) -> Dict[str, Any]:
        """Calculate technical signals.

        Accepts either a pandas DataFrame-like object with columns:
        ['RSI','close','SMA_20','SMA_50','volatility'] or a list of dicts.
        Returns a dict with keys: signal, confidence, reasons, rsi, price, volatility
        """
        # Local import to avoid hard dependency at module import time
        try:
            import pandas as _pd
        except Exception:
            _pd = None

        # Normalize input
        if _pd is not None and hasattr(df, "__class__") and _pd.api.types.is_list_like(df):
            # if it's list-like but not a DataFrame, attempt conversion
            try:
                df = _pd.DataFrame(df)
            except Exception:
                pass

        # Try to access last row values via dictionary fallback
        try:
            latest = df.iloc[-1] if hasattr(df, 'iloc') else df[-1]
            get = lambda k: latest[k]
        except Exception:
            # Fallback: if df is a list of dicts
            if isinstance(df, list) and len(df) > 0:
                latest = df[-1]
                get = lambda k: latest.get(k)
            else:
                return {'signal': 'HOLD', 'confidence': 0.0, 'reasons': [], 'rsi': None, 'price': None, 'volatility': None}

        signals = []

        try:
            rsi = float(get('RSI')) if get('RSI') is not None else None
        except Exception:
            rsi = None

        if rsi is not None:
            if rsi < self.rsi_oversold:
                signals.append(('BUY', 0.3, 'RSI Oversold'))
            elif rsi > self.rsi_overbought:
                signals.append(('SELL', 0.3, 'RSI Overbought'))

        # Moving average signals
        try:
            close = float(get('close'))
            sma20 = float(get('SMA_20')) if get('SMA_20') is not None else None
            sma50 = float(get('SMA_50')) if get('SMA_50') is not None else None
            if sma20 is not None and sma50 is not None:
                if close > sma20 > sma50:
                    signals.append(('BUY', 0.25, 'Bullish MA'))
                elif close < sma20 < sma50:
                    signals.append(('SELL', 0.25, 'Bearish MA'))
        except Exception:
            pass

        # Volatility signals
        try:
            vol = float(get('volatility')) if get('volatility') is not None else None
            if vol is not None and vol > self.volatility_threshold:
                signals.append(('HOLD', 0.2, 'High volatility'))
        except Exception:
            vol = None

        # Aggregate
        buy_weight = sum(w for s, w, _ in signals if s == 'BUY')
        sell_weight = sum(w for s, w, _ in signals if s == 'SELL')

        if buy_weight > sell_weight and buy_weight > 0.5:
            final_signal = 'BUY'
            confidence = min(buy_weight, 1.0)
        elif sell_weight > buy_weight and sell_weight > 0.5:
            final_signal = 'SELL'
            confidence = min(sell_weight, 1.0)
        else:
            final_signal = 'HOLD'
            confidence = 0.3

        return {
            'signal': final_signal,
            'confidence': confidence,
            'reasons': [r for _, _, r in signals],
            'rsi': rsi,
            'price': (close if 'close' in locals() else None),
            'volatility': vol
        }

    def apply_sentiment_filter(self, technical_signal: Dict[str, Any], sentiment: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply a simple sentiment adjustment to a technical signal.

        sentiment is expected as dict with key 'overall' (float).
        """
        if sentiment is None:
            return technical_signal
        try:
            score = float(sentiment.get('overall', 0.0))
            strength = abs(score)
            if technical_signal['signal'] == 'BUY' and score > 0:
                technical_signal['confidence'] = min(1.0, technical_signal['confidence'] + strength * 0.2)
                technical_signal['reasons'].append(f"Positive sentiment ({score:.2f})")
            elif technical_signal['signal'] == 'SELL' and score < 0:
                technical_signal['confidence'] = min(1.0, technical_signal['confidence'] + strength * 0.2)
                technical_signal['reasons'].append(f"Negative sentiment ({score:.2f})")
            elif strength > 0.5:
                technical_signal['confidence'] *= (1 - strength * 0.3)
                technical_signal['reasons'].append(f"Conflicting sentiment ({score:.2f})")
        except Exception:
            pass
        return technical_signal

    def calculate_position_size(self, signal: Dict[str, Any], account_balance: float, risk_per_trade: float = 0.02) -> float:
        """Compute position size from confidence and volatility.

        Returns rounded position size in account currency.
        """
        try:
            confidence = float(signal.get('confidence', 0.0))
        except Exception:
            confidence = 0.0
        try:
            vol = float(signal.get('volatility', 0.0))
        except Exception:
            vol = 0.0
        base_risk = account_balance * risk_per_trade
        volatility_factor = max(0.5, 1 - (vol / 20)) if vol is not None else 1.0
        position_size = base_risk * max(0.1, confidence) * volatility_factor
        return round(position_size, 2)

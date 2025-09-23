"""Wolf pack orchestrator with lightweight regime detection and triage.

This module is intentionally lightweight: imports are lazy and heavy deps are
avoided so tests and imports remain fast.
"""
from typing import Optional


class WolfPackOrchestrator:
    """Selects a wolf pack based on a very small set of heuristic rules and
    applies triage/mitigation logic before returning signals.

    This is intentionally conservative: real regime detection should replace
    the heuristics here, but the orchestrator demonstrates wiring and
    emergency-stop behavior.
    """

    def __init__(self, bull=None, bear=None, sideways=None):
        # accept pack instances or None; if None, import lazily when needed
        self._bull = bull
        self._bear = bear
        self._sideways = sideways
        # triage thresholds
        self.max_drawdown_pct = 0.25  # emergency stop threshold
        self.reduce_size_on_volatility = True

    def _get_pack(self, regime: str):
        if regime == 'bull':
            if self._bull is None:
                from .BULLISH_WOLF_PACK import BullishWolfPack
                self._bull = BullishWolfPack()
            return self._bull

        if regime == 'bear':
            if self._bear is None:
                from .BEARISH_WOLF_PACK import BearishWolfPack
                self._bear = BearishWolfPack()
            return self._bear

        # default to sideways
        if self._sideways is None:
            from .SIDEWAYS_WOLF_PACK import SidewaysWolfPack
            self._sideways = SidewaysWolfPack()
        return self._sideways

    def detect_regime(self, market_data) -> str:
        """Naive regime detector: looks for simple indicators in market_data.

        Returns one of: 'bull', 'bear', 'sideways'. This should be replaced by
        a proper detector when available.
        """
        # if market_data provides a 'trend' hint, use it
        try:
            if isinstance(market_data, dict):
                trend = market_data.get('trend')
                if trend in ('bull', 'bear', 'sideways'):
                    return trend
        except Exception:
            pass

        # fallback: use last price movement if provided
        try:
            if isinstance(market_data, dict) and 'last_return' in market_data:
                lr = float(market_data.get('last_return', 0.0))
                if lr > 0.002:
                    return 'bull'
                if lr < -0.002:
                    return 'bear'
        except Exception:
            pass

        return 'sideways'

    def triage_and_generate(self, market_data, account_state: Optional[dict] = None):
        """Detect regime, route to appropriate pack, and apply mitigation.

        account_state can include 'balance' and 'drawdown_pct'.
        """
        regime = self.detect_regime(market_data)
        pack = self._get_pack(regime)

        sig = pack.generate_signals(market_data)

        # apply simple triage rules
        balance = None
        drawdown = 0.0
        if account_state:
            balance = account_state.get('balance')
            drawdown = float(account_state.get('drawdown_pct', 0.0))

        if drawdown >= self.max_drawdown_pct:
            # emergency stop: force no exposure
            return {
                'side': 'hold',
                'notional': 0.0,
                'risk_reward': 0.0,
                'confidence': 0.0,
                'regime': regime,
                'triage': 'emergency_stop',
            }

        # reduce notional if volatility mitigation enabled and signal is aggressive
        if self.reduce_size_on_volatility and sig.get('confidence', 0.0) < 0.2:
            sig['notional'] = float(sig.get('notional', 0.0)) * 0.5
            sig['triage'] = 'reduced_size_for_low_confidence'

        sig['regime'] = regime
        return sig

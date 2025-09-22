"""
RICK Charter Enforcement Module
Immutable trading rules and constraints
"""
import os

class RickCharter:
    """Enforces all RICK charter rules."""

    # IMMUTABLE CONSTRAINTS
    MAX_HOLD_HOURS = 6
    ALLOWED_TIMEFRAMES = ['M15', 'M30', 'H1']
    MIN_NOTIONAL = 15000
    MIN_RISK_REWARD = 3.2
    DAILY_LOSS_LIMIT = 0.05  # 5%

    # SPREAD GATES
    FX_SPREAD_GATE = 0.15  # × ATR
    CRYPTO_SPREAD_GATE = 0.10  # × ATR

    # STOP LOSS MULTIPLIERS
    FX_SL_MULTIPLIER = 1.2  # × ATR
    CRYPTO_SL_MULTIPLIER = 1.5  # × ATR

    # OCO TIMINGS (ms)
    OCO_CANCEL_TIMEOUT_MS = 300
    OCO_WARNING_MS = 500
    OCO_HALT_MS = 1000

    @staticmethod
    def validate_trade(trade_params):
        """Validate trade against charter.
        """
        # PIN gate check
        if os.environ.get('RICK_PIN') != '841921':
            raise PermissionError("Invalid PIN - trade rejected")

        # Notional check
        if trade_params.get('notional', 0) < RickCharter.MIN_NOTIONAL:
            return False, "Below minimum notional"

        # Risk/Reward check
        tp = trade_params.get('take_profit')
        sl = trade_params.get('stop_loss')
        if tp is None or sl is None or sl == 0:
            return False, "Missing stop or take profit"
        rr_ratio = tp / sl
        if rr_ratio < RickCharter.MIN_RISK_REWARD:
            return False, f"RR ratio {rr_ratio:.2f} below minimum {RickCharter.MIN_RISK_REWARD}"

        # Timeframe check
        if trade_params.get('timeframe') not in RickCharter.ALLOWED_TIMEFRAMES:
            return False, f"Timeframe {trade_params.get('timeframe')} not allowed"

        return True, "Charter validated"

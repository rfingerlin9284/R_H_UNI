def test_extracted_oanda_imports():
    from wolf_packs import extracted_oanda
    s = extracted_oanda.ExtractedFuturesStrategy()
    assert hasattr(s, 'calculate_technical_signals')
    assert hasattr(s, 'apply_sentiment_filter')
    assert hasattr(s, 'calculate_position_size')

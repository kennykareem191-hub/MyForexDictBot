# dictionary_data.py
# Comprehensive Forex terminology database

FOREX_DICT = {
    # Basic Terms
    "pip": "The smallest price move that a given exchange rate can make. For most currency pairs, it's 0.0001 (4th decimal place).",
    "spread": "The difference between the bid (sell) and ask (buy) price of a currency pair. Measured in pips.",
    "leverage": "Using borrowed capital to increase the potential return of an investment. Common ratios: 1:100, 1:500.",
    "margin": "The amount of money required in your account to open and maintain a leveraged position.",
    
    # Market Sentiment
    "bullish": "A market outlook expecting prices to rise. Characterized by optimism and buying pressure.",
    "bearish": "A market outlook expecting prices to fall. Characterized by pessimism and selling pressure.",
    "long": "Buying a currency pair with the expectation that its value will increase over time.",
    "short": "Selling a currency pair with the expectation that its value will decrease.",
    
    # Orders & Execution
    "stop loss": "An order placed to close a trade at a specific price to limit potential losses.",
    "take profit": "An order placed to close a trade at a specific price to secure profits.",
    "limit order": "An order to buy or sell at a specific price or better.",
    "market order": "An order to buy or sell immediately at the current market price.",
    
    # Price Levels
    "ask price": "The price at which you can buy a currency pair. Also known as the 'offer' price.",
    "bid price": "The price at which you can sell a currency pair.",
    "support": "A price level where an asset tends to find buying interest, preventing further decline.",
    "resistance": "A price level where an asset tends to find selling interest, preventing further rise.",
    
    # Analysis & Trading
    "candlestick": "A type of price chart used in technical analysis showing open, high, low, and close prices.",
    "trend": "The general direction in which a market is moving (upward, downward, or sideways).",
    "volatility": "A statistical measure of price variation. High volatility means significant price swings.",
    "liquidity": "The ability to buy or sell an asset without causing significant price movement.",
    "hedge": "An investment strategy to offset potential losses in another position.",
    
    # Analysis Types
    "fundamental analysis": "Evaluating currencies based on economic indicators, news, and geopolitical events.",
    "technical analysis": "Forecasting price direction by analyzing historical price data and chart patterns.",
    
    # Economic Indicators
    "gdp": "Gross Domestic Product - measures a country's total economic output. Key indicator for currency strength.",
    "interest rate": "Central bank rate affecting currency values. Higher rates typically strengthen currency.",
    "inflation": "The rate of price increase for goods and services. Central banks aim to control inflation.",
    "employment": "Key economic indicator showing job creation. Strong employment often strengthens currency.",
    
    # Currency Pairs
    "major pairs": "Most traded currency pairs: EUR/USD, USD/JPY, GBP/USD, USD/CHF, USD/CAD, AUD/USD, NZD/USD.",
    "minor pairs": "Pairs not including USD: EUR/GBP, EUR/JPY, GBP/JPY, etc.",
    "exotic pairs": "Pairs involving major currency and developing economy currency: USD/TRY, USD/ZAR, USD/MXN.",
    
    # Additional Terms
    "slippage": "Difference between expected trade price and actual executed price. Common in volatile markets.",
    "lot size": "Standardized trade units. Standard lot = 100,000 units, Mini = 10,000, Micro = 1,000.",
    "swap": "Interest differential between currencies in overnight trades. Can be positive or negative.",
    "margin call": "When account equity falls below required margin, broker demands additional funds.",
    "stop out": "When broker automatically closes positions if margin level falls below required threshold.",
    "euro": "Currency of the European Union (EUR). Second most traded currency after USD.",
    "british pound": "Currency of the United Kingdom (GBP). Also called 'cable' when paired with USD.",
    "japanese yen": "Currency of Japan (JPY). Major safe-haven currency in Asian trading.",
    "swiss franc": "Currency of Switzerland (CHF). Known as a safe-haven currency.",
    "australian dollar": "Currency of Australia (AUD). Correlated with commodity prices.",
    "canadian dollar": "Currency of Canada (CAD). Correlated with oil prices.",
    "new zealand dollar": "Currency of New Zealand (NZD). Correlated with dairy prices.",
    "us dollar": "United States Dollar (USD). World's primary reserve currency.",
    "central bank": "Institution managing country's currency, money supply, and interest rates.",
    "fed": "Federal Reserve - US Central Bank. Most influential central bank globally.",
    "ecb": "European Central Bank - Manages Euro currency policy.",
    "boj": "Bank of Japan - Japan's central bank. Known for intervention in markets.",
    "boe": "Bank of England - UK's central bank. One of the oldest central banks.",
    "snb": "Swiss National Bank - Known for maintaining CHF stability.",
    "rba": "Reserve Bank of Australia - Australia's central bank.",
    "rbnz": "Reserve Bank of New Zealand - Known for inflation targeting.",
    "boc": "Bank of Canada - Canada's central bank.",
    "nz": "New Zealand - Major commodity exporter, influences NZD.",
    "au": "Australia - Major commodity exporter, influences AUD.",
    "ca": "Canada - Major oil exporter, influences CAD.",
    "ch": "Switzerland - Banking hub, influences CHF.",
    "jp": "Japan - Major manufacturing economy, influences JPY.",
    "uk": "United Kingdom - Major financial center, influences GBP.",
    "us": "United States - World's largest economy, influences USD.",
    "risk sentiment": "Market's appetite for risk. Risk-on means buying risky assets, risk-off means buying safe-havens.",
    "safe haven": "Assets that retain value during market turbulence (e.g., USD, CHF, JPY, Gold)."
}

def search_term(term):
    """Search for a term in the dictionary (case-insensitive, partial match)"""
    if not term:
        return []
    
    term_lower = term.lower().strip()
    
    # Exact match first
    if term_lower in FOREX_DICT:
        return [(term_lower, FOREX_DICT[term_lower])]
    
    # Partial match search
    results = []
    for key, value in FOREX_DICT.items():
        if term_lower in key.lower():
            results.append((key, value))
        if len(results) >= 10:  # Limit results
            break
    
    return results

def get_all_terms():
    """Return all terms in the dictionary"""
    return FOREX_DICT

def get_random_terms(count=5):
    """Return a random selection of terms for quiz"""
    import random
    keys = list(FOREX_DICT.keys())
    if len(keys) < count:
        count = len(keys)
    selected = random.sample(keys, count)
    return {k: FOREX_DICT[k] for k in selected}

def get_term_count():
    """Return total number of terms"""
    return len(FOREX_DICT)

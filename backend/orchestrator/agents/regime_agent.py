from orchestrator.agents.base import BaseAgent
from orchestrator.context import SharedContext
from database import SessionLocal
from market_data.storage.models import MarketCandle
import pandas as pd
import numpy as np
import asyncio
from sqlalchemy import desc

class RegimeClassifierAgent(BaseAgent):
    def __init__(self):
        super().__init__("RegimeClassifier")

    async def run(self, context: SharedContext) -> bool:
        self.log_event(context, f"Starting regime analysis for {context.asset} ({context.timeframe})...")
        
        # 1. Fetch historical data for analysis
        db = SessionLocal()
        try:
            candles = db.query(MarketCandle).filter(
                MarketCandle.symbol == context.asset,
                MarketCandle.timeframe == context.timeframe
            ).order_by(desc(MarketCandle.timestamp)).limit(500).all()
            
            if not candles:
                self.log_event(context, "Error: No market data found for analysis.")
                return False
                
            # Convert to DataFrame
            df = pd.DataFrame([{
                "timestamp": c.timestamp,
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.volume
            } for c in candles])
            
            # Ensure chronological order
            df = df.sort_values("timestamp")
            
            # 2. Calculate Metrics
            # Volatility (Rolling Std Dev of Returns)
            df['returns'] = df['close'].pct_change()
            volatility = df['returns'].std() * np.sqrt(365 * 24) # Annualized approx
            
            # Trend (EMA Distance)
            df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
            price_vs_ema = (df['close'].iloc[-1] - df['ema_200'].iloc[-1]) / df['ema_200'].iloc[-1]
            trend_slope = (df['ema_50'].iloc[-1] - df['ema_50'].iloc[-10]) / df['ema_50'].iloc[-10]
            
            # Liquidity (Volume-weighted turnover)
            avg_volume = df['volume'].tail(50).mean()
            avg_price = df['close'].tail(50).mean()
            liquidity_score = avg_volume * avg_price
            
            # 3. Classify Regime
            regime = "NEUTRAL"
            if volatility > 0.8: # High volatility
                regime = "STORM" if price_vs_ema < 0 else "BULL_RUSH"
            elif volatility < 0.3: # Low volatility
                regime = "CALM"
            else:
                regime = "CHOPPY" if abs(trend_slope) < 0.01 else "TRENDING"

            # 4. Strategy Suitability Assessment
            # Heuristic: If trend-following strategy, suitability is high in TRENDING/BULL_RUSH
            suitability = 50
            if "rsi" in context.strategy_code.lower() or "mean" in context.strategy_code.lower():
                # Mean reversion likes CHOPPY or CALM
                suitability = 85 if regime in ["CHOPPY", "CALM"] else 40
            else:
                # Default assume trend following
                suitability = 85 if regime in ["TRENDING", "BULL_RUSH"] else 30

            analysis_result = {
                "regime": regime,
                "volatility_score": round(volatility * 100, 2),
                "trend_strength": round(trend_slope * 100, 2),
                "liquidity_quality": "HIGH" if liquidity_score > 1000000 else "LOW",
                "price_to_ema200": round(price_vs_ema * 100, 2),
                "suitability_score": suitability,
                "reasoning": f"Detected {regime} regime with {round(volatility*100,1)}% annualized volatility. "
                             f"Price is {round(price_vs_ema*100,1)}% relative to 200 EMA."
            }
            
            context.regime_analysis = analysis_result
            self.log_event(context, f"Regime detected: {regime} (Volatility: {analysis_result['volatility_score']})")
            self.log_event(context, f"Strategy suitability: {suitability}/100")
            self.log_event(context, "Analysis complete.")
            return True
            
        except Exception as e:
            self.log_event(context, f"Analysis failed: {str(e)}")
            return False
        finally:
            db.close()

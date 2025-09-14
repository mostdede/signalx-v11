from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
app = FastAPI(title="SignalX API", version="1.0.0")
class IndicatorsRequest(BaseModel):
    prices: list[float]; rsi_period: int = 14; ema_period: int = 20
def ema(values, period):
    if len(values) < period: return []
    k = 2 / (period + 1); ema_vals = [sum(values[:period]) / period]
    for v in values[period:]: ema_vals.append(v * k + ema_vals[-1] * (1 - k))
    return [None]*(period-1) + ema_vals
def rsi(values, period=14):
    if len(values) < period + 1: return []
    gains, losses = [], []
    for i in range(1, len(values)):
        ch = values[i]-values[i-1]; gains.append(max(ch,0)); losses.append(max(-ch,0))
    avg_gain = sum(gains[:period]) / period; avg_loss = sum(losses[:period]) / period
    rsis = [None]*period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain*(period-1) + gains[i]) / period
        avg_loss = (avg_loss*(period-1) + losses[i]) / period
        rs = float('inf') if avg_loss == 0 else (avg_gain / avg_loss)
        rsis.append(100 - (100/(1+rs)))
    return rsis
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/indicators")
def indicators(req: IndicatorsRequest):
    if not req.prices: raise HTTPException(status_code=400, detail="Empty price series")
    return {"ema": ema(req.prices, req.ema_period), "rsi": rsi(req.prices, req.rsi_period)}
if __name__ == "__main__":
    import uvicorn; port = int(os.getenv("BACKEND_PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

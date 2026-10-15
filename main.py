from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# 1. Path parameter: part of the URL, identifies a resource
#    GET /products/abc123
@app.get("/products/{product_id}")
def get_product(product_id: str):
    return {"product_id": product_id}

# 2. Query parameter: optional settings after "?"
#    GET /recommendations/abc123?k=3
@app.get("/recommendations/{product_id}")
def recommend(product_id: str, k: int = 3):
    if k < 1:
        raise HTTPException(status_code=422, detail="k must be >= 1")
    return {"product_id": product_id, "k": k, "items": []}

# 3. Request body: structured JSON input (typical for ML predictions)
#    POST /predict  with  {"title": "Red cotton t-shirt", "price": 19.99}
class PredictRequest(BaseModel):
    title: str = Field(min_length=1)
    price: float = Field(gt=0)

class PredictResponse(BaseModel):
    category: str
    confidence: float

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # a real model would go here
    return PredictResponse(category="apparel", confidence=0.87)
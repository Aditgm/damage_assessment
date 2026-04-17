import os
import uuid
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

try:
    from inference_sdk import InferenceHTTPClient  # type: ignore
    _HAS_INFERENCE_SDK = True
except Exception:
    InferenceHTTPClient = None  
    _HAS_INFERENCE_SDK = False

load_dotenv()

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
ROBOFLOW_MODEL_ID = os.getenv("ROBOFLOW_MODEL_ID", "disaster-djl38/3")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

if not ROBOFLOW_API_KEY:
    print("Warning: ROBOFLOW_API_KEY not set. Using fallback stub client for local development.")

app = FastAPI(title="Damage Assessment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if _HAS_INFERENCE_SDK and InferenceHTTPClient is not None and ROBOFLOW_API_KEY:
    client = InferenceHTTPClient(api_url="https://serverless.roboflow.com", api_key=ROBOFLOW_API_KEY)
    print("✅ Roboflow InferenceHTTPClient initialized successfully.")
else:
    # Local stub client with a compatible `run_workflow` method used by the app
    class _StubClient:
        def __init__(self, *args, **kwargs):
            pass

        def run_workflow(self, workspace_name, workflow_id, images, use_cache=True):
            return [{
                "annotated_image": {"type": "base64", "value": ""},
                "predictions": {
                    "predictions": [{"class": "Simulated Fire", "class_id": 0, "confidence": 0.85}],
                    "top": "Simulated Fire",
                    "confidence": 0.85,
                    "prediction_type": "classification"
                }
            }]

    client = _StubClient()
    print("⚠️ Using stub client (no real inference).")


@app.post("/scan")
async def scan_image(file: UploadFile = File(...)):
    """
    Receives image from frontend, sends to Roboflow for inference, 
    and returns results securely without exposing API keys to the browser.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")


    
    try:
        # Read upload into memory
        content = await file.read()
        
        # Encode as base64 for the Roboflow serverless API
        import base64
        image_b64 = base64.b64encode(content).decode("utf-8")
            
        ROBOFLOW_WORKSPACE_NAME = os.getenv("ROBOFLOW_WORKSPACE_NAME", "aditya-ga6vp")
        ROBOFLOW_WORKFLOW_ID = os.getenv("ROBOFLOW_WORKFLOW_ID", "disaster-damage-assessment-pipeline-1776326906649")
        
        print(f"Executing workflow: {ROBOFLOW_WORKFLOW_ID}...")
        
        workflow_result = client.run_workflow(
            workspace_name=ROBOFLOW_WORKSPACE_NAME,
            workflow_id=ROBOFLOW_WORKFLOW_ID,
            images={
                "image": f"data:image/jpeg;base64,{image_b64}"
            },
            use_cache=False
        )
        
        print(f"Raw workflow result keys: {list(workflow_result[0].keys()) if isinstance(workflow_result, list) and len(workflow_result) > 0 else 'EMPTY'}")
           result = {}
        if isinstance(workflow_result, list) and len(workflow_result) > 0:
            item = workflow_result[0]
            preds_data = item.get("predictions", {})
            
            if isinstance(preds_data, dict):
                result["top"] = preds_data.get("top", None)
                result["confidence"] = preds_data.get("confidence", None)
                result["prediction_type"] = preds_data.get("prediction_type", "classification")
                result["predictions"] = preds_data.get("predictions", [])
            
            damage_pct = item.get("damage_percentage", None)
            if damage_pct is not None:
                result["damage_percentage"] = damage_pct
            
            if not result.get("top") and result.get("predictions"):
                inner = result["predictions"]
                if isinstance(inner, list) and len(inner) > 0:
                    # Pick the highest confidence prediction
                    best = max(inner, key=lambda p: p.get("confidence", 0))
                    result["top"] = best.get("class", "Unknown")
                    result["confidence"] = best.get("confidence", 0)
            if not result.get("top") or result.get("top") == "Unknown":
                # Use damage_percentage as a signal — if it exists, the model DID classify
                if damage_pct is not None and damage_pct >= 0:
                    # No structured class name available — use a generic label
                    # The annotated image visually shows the class  
                    result["top"] = "Disaster Detected"
                    result["confidence"] = max(damage_pct / 100.0 if damage_pct > 1 else damage_pct, 0.5)
                    result["prediction_type"] = "classification"
            annotated = item.get("annotated_image", None)
            if isinstance(annotated, str) and len(annotated) > 100:
                # NEW format: raw base64 string
                result["annotated_base64"] = annotated
            elif isinstance(annotated, dict) and annotated.get("value"):
                # OLD format: {"type": "base64", "value": "..."}
                result["annotated_base64"] = annotated["value"]
            
            # Ensure predictions is always a list
            if not isinstance(result.get("predictions"), list):
                result["predictions"] = []
                
        else:
            result = {"predictions": [], "top": "N/A", "confidence": 0}
        
        print(f"Returning to frontend: top={result.get('top')}, confidence={result.get('confidence')}, damage_pct={result.get('damage_percentage')}, has_annotated={bool(result.get('annotated_base64'))}")
        
            
        return JSONResponse(content=result)
        
    except Exception as e:
        print(f"CRITICAL ERROR during scan: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500, 
            content={"error": "Inference failed", "details": str(e)}
        )

@app.get("/health")
async def health_check():
    return {"status": "active", "model": ROBOFLOW_MODEL_ID}

if __name__ == "__main__":
    print("==========================================")
    print("DAMAGE ASSESSMENT SECURE SERVER STARTING")
    print("==========================================")
    print(f"Target Model: {ROBOFLOW_MODEL_ID}")
    print(f"Endpoint: http://{HOST}:{PORT}/scan")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")

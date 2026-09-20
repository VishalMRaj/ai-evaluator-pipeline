from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()


class PipelineStatus(BaseModel):
    status: str
    message: str


@app.get("/run-pipeline")
async def run_pipeline():
    # Trigger the pipeline script sequence
    try:
        subprocess.run(["python", "src/rules.py"], check=True)
        subprocess.run(["python", "src/evaluator.py"], check=True)
        subprocess.run(["python", "src/scorer.py"], check=True)
        subprocess.run(["python", "src/reporter.py"], check=True)
        return {"status": "success", "message": "Pipeline completed successfully"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

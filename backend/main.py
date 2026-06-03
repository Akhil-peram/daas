from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Dashboard as a Service API is running"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read the file content
        contents = await file.read()
        
        # Process based on file type
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            return {"error": "Unsupported file type. Please upload a CSV or Excel file."}

        # Get data types and missing values
        info = pd.DataFrame({
            "type": df.dtypes.astype(str),
            "missing": df.isnull().sum(),
            "unique": df.nunique()
        }).to_dict(orient="index")

        # Get categorical summaries (top values)
        categorical_summary = {}
        for col in df.select_dtypes(include=['object', 'category']).columns:
            counts = df[col].value_counts().head(15).to_dict()
            categorical_summary[col] = [{"name": str(k), "value": int(v)} for k, v in counts.items()]

        # Numeric statistics
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        stats = {}
        for col in numeric_cols:
            stats[col] = {
                "mean": float(df[col].mean()) if not df[col].empty else 0,
                "median": float(df[col].median()) if not df[col].empty else 0,
                "min": float(df[col].min()) if not df[col].empty else 0,
                "max": float(df[col].max()) if not df[col].empty else 0,
                "std": float(df[col].std()) if not df[col].empty else 0,
            }

        # Numeric data for correlation
        numeric_df = df.select_dtypes(include=['number'])
        correlation = numeric_df.corr().fillna(0).to_dict() if not numeric_df.empty else {}

        # Sample data for raw table (limit to first 100 rows)
        sample_data = df.head(100).fillna("").to_dict(orient="records")

        # Return comprehensive results
        return {
            "filename": file.filename,
            "columns": df.columns.tolist(),
            "numeric_columns": numeric_cols,
            "categorical_columns": df.select_dtypes(include=['object', 'category']).columns.tolist(),
            "row_count": len(df),
            "info": info,
            "stats": stats,
            "categorical_summary": categorical_summary,
            "correlation": correlation,
            "sample_data": sample_data
        }
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

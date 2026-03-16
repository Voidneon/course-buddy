import os
import sys
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- FIX 1: Missing Imports ---
from supabase import create_client, Client 
import import_logic 
import exp
import testexport


if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(sys.executable)
else:
    basedir = os.path.dirname(os.path.abspath(__file__))

TEMP_DIR = os.path.join(tempfile.gettempdir(), "library_buddy_uploads")
import os
import sys
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- FIX: Supabase and Logic Imports ---
from supabase import create_client, Client 
import import_logic 
import exp
import testexport

# Find the directory of the running file (script or .exe)
if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(sys.executable)
else:
    basedir = os.path.dirname(os.path.abspath(__file__))

# --- FIX: Windows Permission-Safe Temp Directory ---
# Using tempfile.gettempdir() ensures we don't crash in C:\Program Files
TEMP_DIR = os.path.join(tempfile.gettempdir(), "library_buddy_uploads")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR, exist_ok=True)

# Load .env if it exists
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)

app = FastAPI()

# 1. CORS: Allow React to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Embedded Keys ---
SUPABASE_URL = "https://yalejerenkwsginegaax.supabase.co"
SUPABASE_KEY = "sb_secret_VQWVY5qONGmTQtE_6zeTOQ_buga429v"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
async def root():
    # Redirect users to the documentation page automatically
    return RedirectResponse(url="/docs")

# --- BUTTON 1: IMPORT TEMPLATES ---
@app.post("/import/templates")
async def upload_templates(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        import_logic.ingest_course_templates(file_path)
        return {"status": "success", "message": "Templates processed successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_error:
            print(f"Warning: Could not delete temp file: {cleanup_error}")

# --- BUTTON 2: IMPORT ACQUISITIONS ---
@app.post("/import/acquisitions")
async def upload_acquisitions(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        import_logic.ingest_acquisitions(file_path)
        return {"status": "success", "message": "Acquisitions processed successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass

# --- BUTTON 3: EXPORT SUMMARY ---
@app.get("/export/summary")
async def export_summary():
    try:
        excel_file = testexport.generate_full_library_report()
        if not excel_file:
            raise HTTPException(status_code=404, detail="No data generated")
        excel_file.seek(0)
        headers = {'Content-Disposition': 'attachment; filename="Library_Summary_2026.xlsx"'}
        return StreamingResponse(excel_file, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- BUTTON 4: EXPORT DETAILED ---
@app.get("/export/detailed")
async def export_detailed(dept: str = Query(..., description="Department Code (CS, IT, IS)")):
    try:
        excel_file = exp.generate_detailed_book_report(dept)
        if not excel_file:
            raise HTTPException(status_code=404, detail=f"No data found for {dept}")
        excel_file.seek(0)
        filename = f"Detailed_Holdings_{dept}.xlsx"
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        return StreamingResponse(excel_file, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR, exist_ok=True)



# Load .env if it exists, though embedding keys makes this a backup
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)



# 1. CORS: Allow React to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp folder
TEMP_DIR = os.path.join(basedir, "temp_uploads")
os.makedirs(TEMP_DIR, exist_ok=True)

# --- FIX 2: Corrected Embedded Keys Syntax ---
SUPABASE_URL = "https://yalejerenkwsginegaax.supabase.co"
SUPABASE_KEY = "sb_secret_VQWVY5qONGmTQtE_6zeTOQ_buga429v"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# --- BUTTON 1: IMPORT TEMPLATES ---
@app.post("/import/templates")
async def upload_templates(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        import_logic.ingest_course_templates(file_path)
        return {"status": "success", "message": "Templates processed successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_error:
            print(f"Warning: Could not delete temp file: {cleanup_error}")

# --- BUTTON 2: IMPORT ACQUISITIONS ---
@app.post("/import/acquisitions")
async def upload_acquisitions(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        import_logic.ingest_acquisitions(file_path)
        return {"status": "success", "message": "Acquisitions processed successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass

# --- BUTTON 3: EXPORT SUMMARY ---
@app.get("/export/summary")
async def export_summary():
    try:
        excel_file = testexport.generate_full_library_report()
        if not excel_file:
            raise HTTPException(status_code=404, detail="No data generated")
        excel_file.seek(0)
        headers = {'Content-Disposition': 'attachment; filename="Library_Summary_2026.xlsx"'}
        return StreamingResponse(excel_file, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- BUTTON 4: EXPORT DETAILED ---
@app.get("/export/detailed")
async def export_detailed(dept: str = Query(..., description="Department Code (CS, IT, IS)")):
    try:
        excel_file = exp.generate_detailed_book_report(dept)
        if not excel_file:
            raise HTTPException(status_code=404, detail=f"No data found for {dept}")
        excel_file.seek(0)
        filename = f"Detailed_Holdings_{dept}.xlsx"
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        return StreamingResponse(excel_file, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

    
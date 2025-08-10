# src/db.py
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_analytics_result(payload: dict):
    # make sure table analytics exists with jsonb field 'result'
    data = {"result": payload}
    res = supabase.table("analytics").insert(data).execute()
    return res

def insert_transfer(transfer: dict):
    return supabase.table("transfers").insert(transfer).execute()
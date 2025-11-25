import os
from supabase import create_client, Client

url: str = os.getenv("SUPABASE_URL") or ""
key: str = os.getenv("SUPABASE_ANON_KEY") or ""

class SupabaseClient():
    def __init__(self):
        supabase: Client = create_client(url, key)

        self.client = supabase


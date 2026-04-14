from utils.supabase_client import supabase


async def save_report(user_id: str, topic: str, final_report: str) -> dict:
    try:
        response = supabase.table("reports").insert({
            "user_id": user_id,
            "topic": topic,
            "final_report": final_report
        }).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        print(f"⚠️ Could not save report: {str(e)}")
        return {}


async def get_user_reports(user_id: str) -> list:
    try:
        response = supabase.table("reports").select(
            "id, topic, created_at"
        ).eq("user_id", user_id).order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"⚠️ Could not fetch reports: {str(e)}")
        return []


async def get_report_by_id(report_id: str, user_id: str) -> dict:
    try:
        response = supabase.table("reports").select("*").eq(
            "id", report_id
        ).eq("user_id", user_id).single().execute()
        return response.data if response.data else {}
    except Exception as e:
        print(f"⚠️ Could not fetch report: {str(e)}")
        return {}
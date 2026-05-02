import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4


def _storage_base() -> Path:
    # Vercel serverless storage is temporary, so use /tmp there.
    if os.getenv("VERCEL"):
        return Path("/tmp/ai_storyboard_creator")

    configured = os.getenv("STORAGE_DIR", "").strip()
    if configured:
        return Path(configured)

    return Path(__file__).resolve().parents[1] / "generated"


def save_metadata(kind: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Save metadata locally when possible. The app still works if storage fails."""
    try:
        base = _storage_base() / "metadata"
        base.mkdir(parents=True, exist_ok=True)
        project_id = f"{kind}_{uuid4().hex[:10]}"
        file_path = base / f"{project_id}.json"
        payload = {
            "id": project_id,
            "kind": kind,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }
        file_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"saved": True, "id": project_id, "path": str(file_path)}
    except Exception as exc:
        return {"saved": False, "id": None, "path": None, "error": str(exc)[:160]}

import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "http://localhost:8000"
API_KEY = "secret123"

mcp = FastMCP("Linguistic Atlas")

HEADERS = {"X-API-Key": API_KEY}


async def _get(path: str, params: dict | None = None):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{BASE_URL}{path}",
                params=params,
                headers=HEADERS,
                timeout=30.0,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            return {"error": str(exc)}


@mcp.tool()
async def search_languages(name: str, limit: int = 20) -> str:
    """Search languages by name across the linguistic database."""
    data = await _get("/languages/search", {"name": name, "limit": limit})
    if isinstance(data, list):
        return "\n".join(
            f"{l['id']} — {l['name']} ({l.get('iso_code') or '—'}) [{l.get('macroarea') or '—'}]"
            for l in data
        )
    return str(data)


@mcp.tool()
async def get_language(language_id: str) -> str:
    """Get full details about a language by its Glottolog ID."""
    data = await _get(f"/languages/{language_id}")
    if isinstance(data, dict) and "error" not in data:
        return (
            f"Name: {data.get('name')}\n"
            f"ID: {data.get('id')}\n"
            f"ISO code: {data.get('iso_code') or '—'}\n"
            f"Glottocode: {data.get('glottocode') or '—'}\n"
            f"Macroarea: {data.get('macroarea') or '—'}\n"
            f"Level: {data.get('level') or '—'}\n"
            f"Countries: {data.get('countries') or '—'}\n"
            f"Family ID: {data.get('family_id') or '—'}\n"
            f"Coordinates: {data.get('latitude')}, {data.get('longitude')}\n"
            f"Is isolate: {data.get('is_isolate')}"
        )
    return str(data)


@mcp.tool()
async def get_language_classification(language_id: str) -> str:
    """Get the full family tree classification for a language."""
    data = await _get(f"/languages/{language_id}/classification")
    if isinstance(data, dict) and "classification" in data:
        chain = " → ".join(
            f"{c['name']} ({c['level']})" for c in data["classification"]
        )
        return f"{data['language_name']}: {chain}"
    return str(data)


@mcp.tool()
async def get_languages_by_macroarea(macroarea: str, limit: int = 20) -> str:
    """Get languages from a specific macroarea (Africa, Eurasia, Papunesia, etc.)"""
    data = await _get(f"/macroareas/{macroarea}/languages", {"limit": limit})
    if isinstance(data, list):
        return "\n".join(
            f"{l['id']} — {l['name']} ({l.get('iso_code') or '—'})" for l in data
        )
    return str(data)


@mcp.tool()
async def get_family_languages(family_id: str, limit: int = 20) -> str:
    """Get all languages belonging to a language family."""
    data = await _get(f"/families/{family_id}/languages", {"limit": limit})
    if isinstance(data, list):
        return "\n".join(
            f"{l['id']} — {l['name']} ({l.get('iso_code') or '—'})" for l in data
        )
    return str(data)


@mcp.tool()
async def get_languages_per_family() -> str:
    """Get statistics on how many languages each family contains."""
    data = await _get("/stats/languages-per-family")
    if isinstance(data, dict):
        sorted_families = sorted(data.items(), key=lambda x: x[1], reverse=True)
        return "\n".join(
            f"{family}: {count} languages" for family, count in sorted_families[:20]
        )
    return str(data)


@mcp.tool()
async def get_languages_per_macroarea() -> str:
    """Get a count of languages per geographic macroarea."""
    data = await _get("/stats/languages-per-macroarea")
    if isinstance(data, dict):
        sorted_areas = sorted(data.items(), key=lambda x: x[1], reverse=True)
        return "\n".join(f"{area}: {count} languages" for area, count in sorted_areas)
    return str(data)


@mcp.tool()
async def get_random_language() -> str:
    """Get a random language from the database."""
    data = await _get("/languages/random")
    if isinstance(data, dict) and "error" not in data:
        return (
            f"Name: {data.get('name')}\n"
            f"ID: {data.get('id')}\n"
            f"Macroarea: {data.get('macroarea') or '—'}\n"
            f"ISO code: {data.get('iso_code') or '—'}\n"
            f"Countries: {data.get('countries') or '—'}"
        )
    return str(data)


@mcp.tool()
async def create_language_set(title: str, description: str = "") -> str:
    """Create a new language set for grouping and comparing languages."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{BASE_URL}/language-sets",
                json={"user_id": 1, "title": title, "description": description},
                headers=HEADERS,
                timeout=30.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return f"Created language set '{data['title']}' with ID {data['id']}"
        except Exception as exc:
            return f"Error: {exc}"


@mcp.tool()
async def add_language_to_set(set_id: int, language_id: str) -> str:
    """Add a language to an existing language set."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{BASE_URL}/language-sets/{set_id}/items",
                json={"language_id": language_id},
                headers=HEADERS,
                timeout=30.0,
            )
            resp.raise_for_status()
            return f"Added language {language_id} to set {set_id}"
        except Exception as exc:
            return f"Error: {exc}"


@mcp.tool()
async def get_language_set(set_id: int) -> str:
    """Get the languages in a language set."""
    data = await _get(f"/language-sets/{set_id}/items")
    if isinstance(data, list):
        if not data:
            return "This set is empty."
        return "\n".join(
            f"{item['language_id']} — {item['name']} ({item.get('macroarea') or '—'})"
            for item in data
        )
    return str(data)


if __name__ == "__main__":
    mcp.run(transport="stdio")

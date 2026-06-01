import json
import re
from urllib.parse import quote_plus
from typing import Dict, List


PLACES = [
    {
        "name": "Highlands Coffee Vinhomes Ocean Park",
        "category": "drink",
        "area": "Ocean Park",
        "distance_km": 2.8,
        "price_level": "medium",
        "tags": ["coffee", "work", "indoor"],
        "note": "Phu hop uong ca phe, hoc bai, lam viec ngan.",
    },
    {
        "name": "The Coffee House Ocean Park",
        "category": "drink",
        "area": "Ocean Park",
        "distance_km": 3.0,
        "price_level": "medium",
        "tags": ["coffee", "quiet", "group"],
        "note": "Khong gian on dinh, phu hop gap ban hoac hoc nhom.",
    },
    {
        "name": "Katinat Ocean Park",
        "category": "drink",
        "area": "Ocean Park",
        "distance_km": 3.4,
        "price_level": "medium",
        "tags": ["milk tea", "coffee", "young"],
        "note": "Phu hop do uong nhanh, khong gian tre.",
    },
    {
        "name": "Pho Thin Ocean Park",
        "category": "food",
        "area": "Ocean Park",
        "distance_km": 2.9,
        "price_level": "medium",
        "tags": ["pho", "breakfast", "vietnamese"],
        "note": "Phu hop an sang hoac an nhanh.",
    },
    {
        "name": "Com Tam Sa Bi Chuong Ocean Park",
        "category": "food",
        "area": "Ocean Park",
        "distance_km": 3.2,
        "price_level": "medium",
        "tags": ["rice", "lunch", "dinner"],
        "note": "Phu hop an trua, an toi.",
    },
    {
        "name": "Vincom Mega Mall Ocean Park",
        "category": "mall",
        "area": "Ocean Park",
        "distance_km": 3.1,
        "price_level": "medium",
        "tags": ["shopping", "food", "cinema", "supermarket"],
        "note": "Lua chon tot neu muon an uong, mua sam va di sieu thi cung luc.",
    },
    {
        "name": "WinMart Ocean Park",
        "category": "grocery",
        "area": "Ocean Park",
        "distance_km": 2.7,
        "price_level": "medium",
        "tags": ["supermarket", "grocery", "daily goods"],
        "note": "Phu hop mua do hang ngay, thuc pham dong goi.",
    },
    {
        "name": "BRGMart Ocean Park",
        "category": "grocery",
        "area": "Ocean Park",
        "distance_km": 3.3,
        "price_level": "medium",
        "tags": ["grocery", "daily goods"],
        "note": "Them mot lua chon mua tap hoa/sieu thi gan khu Ocean Park.",
    },
    {
        "name": "Cho Da Ton",
        "category": "market",
        "area": "Gia Lam",
        "distance_km": 2.4,
        "price_level": "low",
        "tags": ["market", "fresh food", "local"],
        "note": "Phu hop mua thuc pham tuoi va do sinh hoat gia re.",
    },
    {
        "name": "Cho Trau Quy",
        "category": "market",
        "area": "Gia Lam",
        "distance_km": 4.8,
        "price_level": "low",
        "tags": ["market", "fresh food", "local"],
        "note": "Cho dia phuong lon hon, phu hop mua do tuoi.",
    },
]


LOCATION_KEYWORDS = {
    "vinuni": "VinUni",
    "vin university": "VinUni",
    "ocean park": "Ocean Park",
    "vinhomes ocean park": "Ocean Park",
    "gia lam": "Gia Lam",
    "gia lâm": "Gia Lam",
    "da ton": "Gia Lam",
    "đa tốn": "Gia Lam",
    "trau quy": "Gia Lam",
    "trâu quỳ": "Gia Lam",
}

UNSUPPORTED_LOCATION_KEYWORDS = {
    "hoc vien nong nghiep": "Hoc vien Nong nghiep Viet Nam",
    "học viện nông nghiệp": "Học viện Nông nghiệp Việt Nam",
    "vnua": "Hoc vien Nong nghiep Viet Nam",
    "cau giay": "Cau Giay",
    "cầu giấy": "Cầu Giấy",
    "ha dong": "Ha Dong",
    "hà đông": "Hà Đông",
    "hoan kiem": "Hoan Kiem",
    "hoàn kiếm": "Hoàn Kiếm",
}

CATEGORY_KEYWORDS = {
    "drink": ["cafe", "coffee", "ca phe", "cà phê", "uống", "tra sua", "trà sữa", "do uong", "đồ uống"],
    "food": ["an", "ăn", "quan an", "quán ăn", "nha hang", "nhà hàng", "bua", "bữa", "pho", "phở", "com", "cơm"],
    "grocery": ["tap hoa", "tạp hóa", "sieu thi", "siêu thị", "winmart", "mua do", "mua đồ"],
    "market": ["cho", "chợ", "market"],
    "mall": ["trung tam thuong mai", "trung tâm thương mại", "mall", "vincom", "mua sam", "mua sắm"],
}


def _normalize(text: str) -> str:
    return text.lower().strip()


def _detect_location(text: str) -> str:
    normalized = _normalize(text)
    for keyword, location in LOCATION_KEYWORDS.items():
        if keyword in normalized:
            return location
    return ""


def _detect_unsupported_location(text: str) -> str:
    normalized = _normalize(text)
    for keyword, location in UNSUPPORTED_LOCATION_KEYWORDS.items():
        if keyword in normalized:
            return location
    return ""


def _detect_category(text: str) -> str:
    normalized = _normalize(text)
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return "all"


def _parse_radius(text: str) -> float:
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*km", text.lower())
    if not match:
        return 5.0
    return float(match.group(1).replace(",", "."))


def _build_map_url(place: Dict[str, object]) -> str:
    query = f"{place['name']} {place['area']} Hanoi Vietnam"
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"


def _with_map_link(place: Dict[str, object]) -> Dict[str, object]:
    enriched = dict(place)
    enriched["map_url"] = _build_map_url(place)
    enriched["lat"] = None
    enriched["lng"] = None
    return enriched


def extract_location_and_need(query: str) -> str:
    """
    Extract location, category, and search radius from a Vietnamese user query.
    """
    location = _detect_location(query)
    unsupported_location = "" if location else _detect_unsupported_location(query)
    category = _detect_category(query)
    radius_km = _parse_radius(query)
    location_status = "supported" if location else "unsupported" if unsupported_location else "missing"

    result = {
        "location": location or unsupported_location or "missing",
        "location_status": location_status,
        "category": category,
        "radius_km": radius_km,
        "needs_clarification": location_status == "missing",
        "unsupported_location": location_status == "unsupported",
    }
    return json.dumps(result, ensure_ascii=False)


def search_nearby_places(query: str) -> str:
    """
    Search an internal nearby-place database around VinUni/Gia Lam/Ocean Park.
    Input can be a natural-language query containing location and category.
    """
    location = _detect_location(query)
    unsupported_location = "" if location else _detect_unsupported_location(query)
    category = _detect_category(query)
    radius_km = _parse_radius(query)

    if unsupported_location:
        return (
            f"ERROR_UNSUPPORTED_LOCATION: '{unsupported_location}' is outside the current internal dataset. "
            "Supported areas: VinUni, Ocean Park, Gia Lam."
        )

    if not location:
        return (
            "ERROR_MISSING_LOCATION: User did not provide a clear location. "
            "Ask the user for a specific area, for example VinUni, Ocean Park, or Gia Lam."
        )

    results: List[Dict[str, object]] = []
    for place in PLACES:
        category_ok = category == "all" or place["category"] == category
        radius_ok = float(place["distance_km"]) <= radius_km
        if category_ok and radius_ok:
            results.append(place)

    if not results:
        return (
            f"NO_RESULTS: No {category} places found within {radius_km}km near {location}. "
            "Try a larger radius or a broader category."
        )

    results = sorted(results, key=lambda item: float(item["distance_km"]))
    results = [_with_map_link(place) for place in results]
    return json.dumps(results[:5], ensure_ascii=False, indent=2)


def rank_and_recommend_places(query: str) -> str:
    """
    Rank nearby places from the internal database by distance and category match.
    Input should include the user's location and need.
    """
    raw_results = search_nearby_places(query)
    if raw_results.startswith("ERROR_") or raw_results.startswith("NO_RESULTS"):
        return raw_results

    places = json.loads(raw_results)
    lines = []
    for index, place in enumerate(places[:3], start=1):
        lines.append(
            f"{index}. {place['name']} | {place['category']} | "
            f"{place['distance_km']}km | price={place['price_level']} | "
            f"map={place.get('map_url')} | {place['note']}"
        )
    return "\n".join(lines)


def get_place_map_link(place_name: str) -> str:
    """
    Return a Google Maps search link for a place in the internal dataset.
    This does not invent latitude/longitude. It creates a stable map search URL
    from the place name and area stored in PLACES.
    """
    normalized = _normalize(place_name).strip("\"'")

    for place in PLACES:
        place_text = _normalize(f"{place['name']} {place['area']}")
        if normalized in place_text or _normalize(str(place["name"])) in normalized:
            result = {
                "name": place["name"],
                "area": place["area"],
                "category": place["category"],
                "distance_km": place["distance_km"],
                "map_url": _build_map_url(place),
                "lat": None,
                "lng": None,
                "coordinate_note": (
                    "Exact lat/lng is not stored in the internal dataset yet. "
                    "Use map_url to open Google Maps search for this place."
                ),
            }
            return json.dumps(result, ensure_ascii=False)

    query = f"{place_name} Hanoi Vietnam"
    return json.dumps({
        "name": place_name,
        "map_url": f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}",
        "lat": None,
        "lng": None,
        "coordinate_note": (
            "Place was not found in the internal dataset. "
            "This fallback map_url is a Google Maps search link, not verified coordinates."
        ),
    }, ensure_ascii=False)


TOOL_REGISTRY = {
    "extract_location_and_need": {
        "name": "extract_location_and_need",
        "description": (
            "Extract location, category, and radius from a Vietnamese nearby-place query. "
            "Input: the full user question. "
            "Use this first when you need to check whether the user provided a clear location."
        ),
        "function": extract_location_and_need,
    },
    "search_nearby_places": {
        "name": "search_nearby_places",
        "description": (
            "Search nearby food, drink, grocery, market, or mall places from an internal database. "
            "Input: natural language containing location and need, e.g. 'VinUni cafe within 5km'. "
            "If location is missing, returns ERROR_MISSING_LOCATION."
        ),
        "function": search_nearby_places,
    },
    "rank_and_recommend_places": {
        "name": "rank_and_recommend_places",
        "description": (
            "Rank and summarize the best nearby places. "
            "Input: natural language containing location and category. "
            "Use after the user's location and need are clear."
        ),
        "function": rank_and_recommend_places,
    },
    "get_place_map_link": {
        "name": "get_place_map_link",
        "description": (
            "Get a Google Maps search link for a place from the internal nearby-place dataset. "
            "Input: exact or partial place name, e.g. 'Highlands Coffee Vinhomes Ocean Park'. "
            "Returns map_url and metadata. Does not invent exact latitude/longitude."
        ),
        "function": get_place_map_link,
    },
}


def get_nearby_tools() -> list:
    return list(TOOL_REGISTRY.values())

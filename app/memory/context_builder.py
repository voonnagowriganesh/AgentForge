from app.memory.store import get_memory_profile


def build_memory_context(session_id: str):

    profile = get_memory_profile(session_id)

    lines = []

    if profile.get("name"):
        lines.append(f"Name: {profile['name']}")

    if profile.get("location"):
        lines.append(f"Location: {profile['location']}")

    if profile.get("company"):
        lines.append(f"Company: {profile['company']}")

    if profile.get("profession"):
        lines.append(f"Profession: {profile['profession']}")

    if profile.get("favorite_color"):
        lines.append(f"Favorite Color: {profile['favorite_color']}")

    if profile.get("skills"):
        lines.append(f"Skills: {profile['skills']}")

    if profile.get("education"):
        lines.append(f"Education: {profile['education']}")

    if profile.get("hobbies"):
        lines.append(f"Hobbies: {profile['hobbies']}")

    if not lines:
        return ""

    return "User Profile:\n" + "\n".join(lines)

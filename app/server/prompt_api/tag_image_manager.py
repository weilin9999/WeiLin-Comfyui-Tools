import os
from ..dao.dao import execute_query, fetch_one, tags_db_path


def _get_user_data_dir():
    """Get the user_data directory path."""
    return os.path.normpath(os.path.join(os.path.dirname(tags_db_path), "."))


def image_dir():
    d = os.path.join(_get_user_data_dir(), "tag_images")
    os.makedirs(d, exist_ok=True)
    return d


def thumb_dir():
    d = os.path.join(_get_user_data_dir(), "tag_thumbs")
    os.makedirs(d, exist_ok=True)
    return d


async def update_tag_image_path(t_uuid, image_path):
    """Set image_path and status to 'ready' for a tag."""
    query = """
        UPDATE tag_tags
        SET image_path = ?, image_status = ?
        WHERE t_uuid = ?
    """
    await execute_query("tags", query, (image_path, "ready", t_uuid))


async def update_tag_image_status(t_uuid, status, image_path=None):
    """Update image_status for a tag. Optionally also update image_path."""
    if image_path is not None:
        query = """
            UPDATE tag_tags
            SET image_status = ?, image_path = ?
            WHERE t_uuid = ?
        """
        await execute_query("tags", query, (status, image_path, t_uuid))
    else:
        query = """
            UPDATE tag_tags
            SET image_status = ?
            WHERE t_uuid = ?
        """
        await execute_query("tags", query, (status, t_uuid))


async def get_tag_image_info(t_uuid):
    """Get image_path and image_status for a tag."""
    query = """
        SELECT image_path, image_status
        FROM tag_tags
        WHERE t_uuid = ?
    """
    row = await fetch_one("tags", query, (t_uuid,))
    if row:
        return {"image_path": row[0], "image_status": row[1]}
    return None


async def reset_pending_statuses():
    """Reset all pending/generating statuses to NULL on startup."""
    query = """
        UPDATE tag_tags
        SET image_status = NULL
        WHERE image_status IN ('pending', 'generating')
    """
    await execute_query("tags", query, ())

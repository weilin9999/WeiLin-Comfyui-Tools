# Tag Preview Image — Design

**Date**: 2026-06-06
**Status**: Approved

---

## Overview

Add preview image functionality to the tag management UI (`tag_index.vue`).
Each tag card gets a thumbnail; tags without an image show a one-click generation
button.  Generation uses ComfyUI's internal queue API.

---

## Data Model

### `tag_tags` table — new columns

```
image_path   TEXT     -- NULL or relative path "tag_images/<t_uuid>.png"
image_status TEXT     -- NULL | 'pending' | 'generating' | 'ready' | 'failed'
```

### Filesystem

```
user_data/
  tag_images/<t_uuid>.png      ← original image
  tag_thumbs/<t_uuid>.webp     ← 120×120 thumbnail, generated alongside original
```

---

## API Routes

| Route | Method | Purpose |
|---|---|---|
| `/tag_image/options` | POST | Return available checkpoints, samplers, size presets |
| `/tag_image/generate` | POST | Submit generation task; returns `task_id` (409 if already in progress) |
| `/tag_image/status` | POST | Query task state by `task_id` (polling) |
| `/tag_image/status/{t_uuid}` | GET | Query task state by tag UUID (refresh recovery) |
| `/tag_image/{t_uuid}` | GET | Serve original image (static) |
| `/tag_thumb/{t_uuid}` | GET | Serve thumbnail (static) |

### GET `/tag_image/status/{t_uuid}` response

```json
{
  "status": "pending" | "generating" | "ready" | "failed" | null,
  "task_id": "xxx",
  "image_url": "/tag_image/{t_uuid}",
  "thumb_url": "/tag_thumb/{t_uuid}",
  "error_msg": null
}
```

---

## Task Queue

- Single `asyncio.Queue` + one worker coroutine, concurrency = 1
- In-memory `tasks: dict[str, dict]` tracking task state by `task_id`
- On plugin restart: reset all `pending`/`generating` statuses to `NULL`
- Worker steps:
  1. Set `image_status → 'pending'`
  2. Build ComfyUI workflow JSON (txt2img: CheckpointLoader → CLIPEncode → KSampler → VAEDecode → PreviewImage)
  3. POST `/api/prompt` to ComfyUI
  4. Set `image_status → 'generating'`
  5. Poll `/api/history/{prompt_id}` until complete
  6. Download result image to memory, save original + thumbnail to disk
  7. Set `image_status → 'ready'` and `image_path`
  8. On error: `image_status → 'failed'` with `error_msg`

---

## Frontend

### Files affected

| File | Change |
|---|---|
| `tag_index.vue` | Thumbnail area in tag card, hover overlay, generate button/status |
| `components/GenerateImageDialog.vue` | **New** — generation config dialog |
| `api/tags.js` | New API methods |

### Tag card layout (after)

```
┌─────────────────────────────────┐
│  ┌─────────────────────────┐   │
│  │  thumbnail 120×120      │   │  ← hover: 200ms debounce, show full-size overlay
│  │  or placeholder/generate │   │     loaded images cached in Map<t_uuid, blobURL>
│  └─────────────────────────┘   │
│  [bg color]  Chinese desc      │
│  Tag text                      │
│  [edit] [delete] [move]       │
└─────────────────────────────────┘
```

### Status → UI mapping

| `image_status` | Display |
|---|---|
| `NULL` | Dashed-border placeholder + "Generate" button |
| `pending` | Loading animation + "queued…" |
| `generating` | Progress animation + "generating…" |
| `ready` | Thumbnail; hover loads full image |
| `failed` | Error icon + "Retry" button |

### Generate dialog — parameters

All parameters are user-editable:

| Parameter | Control | Default |
|---|---|---|
| Model | dropdown (from `/tag_image/options`) | first available |
| Size | dropdown (presets: 512×512, 768×512, 768×768, 1024×1024) | 512×512 |
| Sampler | dropdown (from `/tag_image/options`) | euler |
| Steps | number input / slider (1–50) | 20 |
| CFG Scale | number input / slider (1–20) | 7.0 |
| Seed | number input | -1 (random) |
| Positive prompt | textarea | `{tag.text}, masterpiece, best quality` |
| Negative prompt | textarea | `worst quality, low quality, nsfw` |

### Polling

- Every 2 seconds via `POST /tag_image/status`
- Stop when status is `ready` or `failed`
- On page refresh: iterate all tags with `pending`/`generating` status, call `GET /tag_image/status/{t_uuid}` to resume polling

### Duplicate prevention

- Frontend: button disabled when `image_status` is `pending` or `generating`, tooltip "已有生成任务进行中"
- Backend: returns 409 Conflict if status conflict

---

## Error Handling

| Scenario | Behavior |
|---|---|
| ComfyUI unreachable | `status → 'failed'`, "ComfyUI service unavailable" |
| Checkpoint not found | `status → 'failed'`, "Model xxx not found" |
| Generation timeout (5 min) | `status → 'failed'`, "Generation timed out" |
| Disk full | `status → 'failed'`, "Disk space insufficient" |
| DB write failure | Rollback `image_status`, "Data save failed" |

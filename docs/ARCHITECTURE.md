# 🏢 系統架構設計文件 (ARCHITECTURE) - Food Decider (v4 雙軌解析與縣市分類版)

## 1. 系統概述與設計目標
- **核心業務目標**：提供即時地理位置查詢、會員狀態管理、歷史數據追蹤與自建資料庫管理。
- **雙軌地址解析 (Smart Geocoding)**：為了解決開源地圖地址解析不夠聰明的問題，系統導入智慧雙軌機制。當設定有 `GOOGLE_MAPS_API_KEY` 時優先走 Google 取得精確座標（支援「台北101」等模糊字詞），若失敗或無金鑰則無縫降級回 OpenStreetMap Nominatim。

## 2. 系統架構設計
```mermaid
graph TD
    Client[Browser/Mobile] -->|1. Request (Address)| Backend(FastAPI)
    Backend -->|2a. If API Key exists| GoogleAPI(Google Geocoding API)
    GoogleAPI -.->|If Fails/No Key| OSM(Nominatim API)
    Backend -->|2b. Fallback| OSM
    Backend -->|3. Calculate Haversine| DB[(SQLite: restaurants)]
    Client -->|4. Admin CRUD| Backend
```

## 3. 技術選型 (Tech Stack)
- **後端**：FastAPI + `httpx` (處理非同步 HTTP 請求)。
- **資料庫**：SQLite (內含 `restaurants` 包含 `city` 縣市分類欄位)。
- **API 整合**：Google Geocoding API 作為首選，OSM Nominatim 作為備援。

## 4. API 介面設計

### `GET /api/search`
- **邏輯變更**：若無傳入 GPS，會透過 `geocode_address` 函式進行智慧雙軌地址轉換。其餘距離與預算過濾邏輯不變。

### 管理員 API (CRUD)
- `GET /api/admin/restaurants`：取得包含 `city` 的所有餐廳列表。
- `POST /api/admin/restaurants`：接收 `city` 與模糊地址，呼叫 `geocode_address` 轉經緯度後寫入。
- `PUT /api/admin/restaurants/{res_id}`：同上，用於更新。
- `DELETE /api/admin/restaurants/{res_id}`：刪除。

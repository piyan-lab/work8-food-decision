# 📦 提交與推送計畫 (Commit Plan) - Food Decider

## 1. 變更總結
本次完成了 Food Decider 專案的 MVP (Minimum Viable Product) 開發，包含所有前期開發文件（PRD、架構、資料模型、測試清單）、後端 FastAPI 與 SQLite 快取機制，以及前端基於 HTML/Vanilla JS 的互動式轉盤與計分介面。

## 2. 標準化 Commit Message (請複製以下內容)

```text
feat(core): implement Food Decider MVP with Google Maps API

- Add SDLC documentation (PRD, Architecture, Models, Test Plan)
- Setup FastAPI backend with SQLite caching mechanism
- Integrate Google Maps Places API for location-based search
- Implement HTML/CSS/JS frontend with dual decision modes (Random Spin & Smart Score)
- Enforce default Git user Antigravity configuration

Resolves #1
```

## 3. Git 操作指令 (Git Commands)
請在終端機依序執行以下指令，注意：已透過設定檔約束將使用者名稱預設為 **Antigravity**。

```bash
# 1. 設定預設 Git 使用者名稱與信箱 (強制要求)
git config user.name "Antigravity"
git config user.email "antigravity@gemini.local"

# 2. 確認變更狀態
git status

# 3. 將所有檔案加入暫存區 (請確保 .env 已被 .gitignore 忽略，不會被加入)
git add .

# 4. 提交程式碼
git commit -m "feat(core): implement Food Decider MVP with Google Maps API" -m "- Add SDLC documentation (PRD, Architecture, Models, Test Plan)
- Setup FastAPI backend with SQLite caching mechanism
- Integrate Google Maps Places API for location-based search
- Implement HTML/CSS/JS frontend with dual decision modes
- Enforce default Git user Antigravity configuration"

# 5. 推送至遠端 (請替換 main 為您的分支名稱)
git push origin main
```

## 4. 提交前檢查清單 (Pre-commit Checklist)
- [x] `.gitignore` 已正確設定，不會追蹤 `.env` 與 `food_decider.db`。
- [ ] 您的 Google Maps API Key 確定**只有**寫在 `.env` 中，沒有不小心寫死在 `app.py` 裡。
- [ ] 程式碼可正常啟動 (`uvicorn app:app --reload`) 且沒有報錯。

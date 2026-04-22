# 作業：設計 Skill + 打造 AI 聊天機器人

> **繳交方式**：將你的 GitHub repo 網址貼到作業繳交區
> **作業性質**：個人作業

---

## 作業目標

使用 Antigravity Skill 引導 AI，完成一個具備前後端的「Food Decider 美食決策家」系統。
重點不只是「讓程式跑起來」，而是透過設計 Skill，學會用結構化的方式與 AI 協作開發，並解決外部 API 限制（如自建資料庫、智慧地址轉換等問題）。

---

## 繳交項目

你的 GitHub repo 需要包含以下內容：

### 1. Skill 設計（`.agents/skills/`）

為以下五個開發階段＋提交方式各設計一個 SKILL.md：

| 資料夾名稱        | 對應指令          | 說明                                                                           |
| ----------------- | ----------------- | ------------------------------------------------------------------------------ |
| `prd/`          | `/prd`          | 產出 `docs/PRD.md`                                                           |
| `architecture/` | `/architecture` | 產出 `docs/ARCHITECTURE.md`                                                  |
| `models/`       | `/models`       | 產出 `docs/MODELS.md`                                                        |
| `implement/`    | `/implement`    | 產出程式碼（**需指定**：HTML 前端 + FastAPI + SQLite 後端）              |
| `test/`         | `/test`         | 產出手動測試清單                                                               |
| `commit/`       | `/commit`       | 自動 commit + push（**需指定**：使用者與 email 使用 Antigravity 預設值） |

### 2. 開發文件（`docs/`）

用你設計的 Skill 產出的文件，需包含：

- `docs/PRD.md`
- `docs/ARCHITECTURE.md`
- `docs/MODELS.md`

### 3. 程式碼

一個可執行的「Food Decider 美食決策家」應用，具備以下功能：

| 功能           | 說明                                       | 是否完成 |
| -------------- | ------------------------------------------ | -------- |
| 會員與紀錄系統 | 支援註冊、登入與個人歷史消費紀錄歸檔       | O        |
| 雙定位模式     | 支援 GPS 自動定位與手動地址輸入            | O        |
| 智慧地址解析   | 支援 Google Geocoding API 與 Nominatim 備援| O        |
| 本地距離計算   | 使用 Haversine 演算法，自訂搜尋半徑過濾    | O        |
| 自建餐廳庫     | SQLite 本地資料庫，拔除外部地圖資料依賴    | O        |
| 後台管理 CRUD  | 提供前台 UI，支援 22 縣市新增、修改、刪除  | O        |

### 4. 系統截圖（`screenshots/`）

在 `screenshots/` 資料夾放入以下截圖：

- `home.png`：Food Decider 主搜尋畫面
- `admin.png`：管理員 CRUD 介面與縣市篩選
- `result.png`：決策轉盤或歷史紀錄畫面

### 5. 心得報告（本 README.md 下方）

在本 README 的**心得報告**區填寫。

---

## 專案結構範例

```
your-repo/
├── .agents/
│   └── skills/
│       ├── prd/SKILL.md
│       ├── architecture/SKILL.md
│       ├── models/SKILL.md
│       ├── implement/SKILL.md
│       ├── test/SKILL.md
│       └── commit/SKILL.md
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── MODELS.md
├── templates/
│   └── index.html
├── screenshots/
│   ├── home.png
│   ├── admin.png
│   └── result.png
├── app.py
├── database.py
├── requirements.txt
├── .env.example
└── README.md          ← 本檔案（含心得報告）
```

---

## 啟動方式

```bash
# 1. 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. 安裝套件
pip install -r requirements.txt

# 3. 設定環境變數
cp .env.example .env
# 編輯 .env，填入 GEMINI_API_KEY

# 4. 啟動伺服器
uvicorn app:app --reload
# 開啟瀏覽器：http://localhost:8000
```

---

## 心得報告

**姓名**：林湘紜
**學號**：D1438880

### 問題與反思

**Q1. 你設計的哪一個 Skill 效果最好？為什麼？哪一個效果最差？你認為原因是什麼？**

> 效果最好的應該是 /implement (實作) 與 /prd (需求定義) 技能。 因為只要在 PRD 中把需求結構化定義清楚（例如：明確要求使用 SQLite、FastAPI、以及 Haversine 球面距離演算法），AI 就能非常精準且快速地產出品質很高的前後端程式碼。尤其是在我們決定「拔除 Google API，全面改為本地自建資料庫」這種大規模重構時，AI 也能夠一次到位把 CRUD 功能與距離計算寫好，展現了極高的開發效率。

效果相對較差的是 /test (測試) 或 /commit 技能。 原因在於，這兩個階段高度依賴「真實的環境狀態」與「不可控的外部因素」。例如在實際測試時，AI會發現 Google API 會因為沒綁定信用卡而回傳 REQUEST_DENIED，且開源的 Nominatim API 又對「含有店名」的地址格式異常嚴格而頻頻報錯。必須等到真的報錯了，才能夠依賴對話讓 AI 進行除錯與加入備援機制。

---

**Q2. 在用 AI 產生程式碼的過程中，你遇到什麼問題是 AI 沒辦法自己解決、需要你介入處理的？**

> 
1. 外部 API 的權限與收費限制問題 當 AI 幫我寫好 Google Maps 的串接程式碼後，執行時卻一直發生 REQUEST_DENIED 錯誤。AI 無法自己解決這個問題，因為這牽涉到真實世界的 Google Cloud 帳號需要綁定信用卡的限制。我必須直接跟他說明不再完全依賴 Googlemaps api，而是希望用建立本地資料庫的方式，將我們手動輸入的餐廳資料。

2. 系統架構的「備援機制 (Fallback)」決策 當我們切換到免費開源的 Nominatim 地址解析服務時，遇到它無法辨識「大逢甲小辣椒 407臺中市...」這種帶有店名的複雜地址。AI 當下只會回報無法解析，它不會自己決定要怎麼辦。我必須要求它處理，最終設計「雙軌地址解析」：也就是有金鑰就可以用 Google 模糊搜尋。

3. 產品細節與本地環境配置 例如在做管理後台時，AI 預設只寫了「六都」的分類(根本就是歧視)，我要糾正它「必須包含全台 22 縣市」。另外在執行 Git 版本控制時，AI 原本會把本地測試用的 .db 檔一起 commit 上去，我也必須去修改 .gitignore 來確保版本庫的乾淨，否則會有太多混雜的資料被使用者看到。這些都顯示出 AI 雖然寫 Code 很快，但在細節的把控與產品決策上，依然需要人類來當「產品經理」的角色。
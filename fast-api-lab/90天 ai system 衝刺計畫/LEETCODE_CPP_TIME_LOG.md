# C++ & LeetCode 衝刺時間與學習紀錄 (LEETCODE_CPP_TIME_LOG.md)

本文件專門記錄 **C++ 現代語法、STL 與 LeetCode 演算法** 的練習時間與解題筆記。

---

## 📊 累積時間統計

- **本週累積時間**：1.0 小時
- **總累積時間**：2.8 小時
- **目前完成題數**：4 題

---

## 📅 每日練習明細 (Daily Log)

### 2026-08-26 (Wednesday)
- **花費時間**：1.0 小時 (複習與除錯)
- **練習內容**：LeetCode 2493. Divide Nodes Into the Maximum Number of Groups (Hard)
- **解題重點與筆記**：
  - **核心演算法**：連通分量 (Connected Components) 劃分 + 二分圖染色檢驗 + 全源 BFS 最大深度。
  - **除錯紀錄**：
    - 語法/邏輯：修正 edges 迴圈邊界、避免將 queue 賦值給 vector、補上 BFS 的 `q.pop()` 避免死循環、以及外層每次重設 `visited`。
    - 二分圖染色：將衝突判斷拉到未染色條件之外，以利正確抓出奇環。
    - 連通塊處理：各獨立連通塊的組數應取該塊內最大深度，最後將所有連通塊之最大深度相加（$\sum$），而非全域最大值。
    - 標記時機：BFS 必須在 Push 時立即標記，避免重複塞入佇列造成時空複雜度暴增。
  - **面試與考點**：
    - 為什麼能暴力搜尋？一般圖（含偶環）無法使用樹的「兩次 BFS」貪婪法尋找直徑，故全源 BFS 為最優解。
    - 樹的直徑兩次 BFS 僅適用於無環樹（Tree），面試（如台積電）掌握實作原理與適用限制即可。

---

### 2026-08-14 (Friday)
- **花費時間**：0.3 小時 (18 分鐘)
- **練習內容**：LeetCode 11. Container With Most Water (Medium)
- **解題重點與筆記**：
  - **核心演算法**：Two Pointers (相向雙指針)。
  - **貪婪策略 (Greedy Strategy)**：
    - 面積由 `min(height[left], height[right]) * (right - left)` 決定。
    - 每次移動較短板的那一邊指針（因為移動較長板的話，寬度一定變小，而高度上限仍受限於較短板，面積不可能變大）。
  - **優化點**：
    - 在指針移動時，增加了 `while` 跳過小於等於當前短板高度的柱子（Skip Optimization），進一步加速跳過無效計算。
  - **複雜度解析**：時間複雜度 **$O(N)$**，空間複雜度 **$O(1)$**。

---

### 2026-08-13 (Thursday - Session 2)
- **花費時間**：1.0 小時
- **練習內容**：LeetCode 15. 3Sum (Medium)
- **解題重點與筆記**：
  - **核心演算法**：Sorting + Two Pointers (雙指針)。
  - **複雜度解析**：時間複雜度 **$O(N^2)$**，空間複雜度 **$O(1)$**。

---

### 2026-08-13 (Thursday - Session 1)
- **花費時間**：0.5 小時
- **練習內容**：LeetCode 560. Subarray Sum Equals K (Medium)
- **解題重點與筆記**：
  - **核心演算法**：Prefix Sum (前綴和) + Hash Table (`std::unordered_map`)。
  - **複雜度解析**：時間複雜度 **$O(N)$**，空間複雜度 **$O(N)$**。

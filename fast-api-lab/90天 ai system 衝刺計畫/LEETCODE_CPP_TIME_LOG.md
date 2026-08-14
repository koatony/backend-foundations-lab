# C++ & LeetCode 衝刺時間與學習紀錄 (LEETCODE_CPP_TIME_LOG.md)

本文件專門記錄 **C++ 現代語法、STL 與 LeetCode 演算法** 的練習時間與解題筆記。

---

## 📊 累積時間統計

- **本週累積時間**：1.8 小時
- **總累積時間**：1.8 小時
- **目前完成題數**：3 題

---

## 📅 每日練習明細 (Daily Log)

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

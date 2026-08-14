# C++ & LeetCode 衝刺時間與學習紀錄 (LEETCODE_CPP_TIME_LOG.md)

本文件專門記錄 **C++ 現代語法、STL 與 LeetCode 演算法** 的練習時間與解題筆記。

---

## 📊 累積時間統計

- **本週累積時間**：1.5 小時
- **總累積時間**：1.5 小時
- **目前完成題數**：2 題

---

## 📅 每日練習明細 (Daily Log)

### 2026-08-13 (Thursday)
- **花費時間**：1.0 小時
- **練習內容**：LeetCode 15. 3Sum (Medium)
- **解題重點與筆記**：
  - **核心演算法**：Sorting + Two Pointers (雙指針)。
  - **複雜度解析**：
    - 排序為 $O(N \log N)$。
    - 外層 `for` 迴圈固定第一數 $nums[i]$，內層使用雙指針（`left` 與 `right` 向中間收縮），內層時間複雜度為 $O(N)$。
    - 總時間複雜度優化至 **$O(N^2)$**，空間複雜度 **$O(1)$**（不計輸出陣列）。
  - **關鍵避坑點（去重邏輯）**：
    - 外層去重：`if (i > 0 && nums[i] == nums[i - 1]) continue;`
    - 內層去重：當 `cur_sum == 0` 時，除了跳過相同的 `nums[left]` 與 `nums[right]`，指針仍需繼續向內移動 (`left++`, `right--`)，否則會造成死循環。

---

### 2026-08-13 (Thursday - Session 1)
- **花費時間**：0.5 小時
- **練習內容**：LeetCode 560. Subarray Sum Equals K (Medium)
- **解題重點與筆記**：
  - **核心演算法**：Prefix Sum (前綴和) + Hash Table (`std::unordered_map`)。
  - **複雜度解析**：時間複雜度 **$O(N)$**，空間複雜度 **$O(N)$**。
  - **關鍵細節**：必須預先將 `{0: 1}` 加入 Hash Table 中，以處理前綴和恰好等於 $K$ 的子陣列情況。

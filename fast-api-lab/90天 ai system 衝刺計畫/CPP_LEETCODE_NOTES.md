# 90天 AI System 衝刺計畫 — C++ 與 LeetCode 解題筆記本

本筆記本用於紀錄 **C++ 語言特性、STL 容器與演算法**，以及 **LeetCode 高頻面試題考點分析與筆記**。

---

## 📌 目錄
1. [C++ 語言特性與 STL 重點](#1-c-語言特性與-stl-重點)
2. [高頻資料結構與演算法模組](#2-高頻資料結構與演算法模組)
3. [LeetCode 刷題解題紀錄](#3-leetcode-刷題解題紀錄)

---

## 1. C++ 語言特性與 STL 重點

### 1.1 記憶體管理與指標
* **指標與引用**：Raw Pointer vs. Reference、`std::unique_ptr` 與 `std::shared_ptr` 的生命週期與計數管理。
* **移動語意 (Move Semantics)**：右值引用 `&&` 與 `std::move` 減少拷貝開銷。

### 1.2 常用 STL 容器複雜度
* `std::vector`：動態陣列，隨機存取 $O(1)$，尾端插入均攤 $O(1)$。
* `std::unordered_map` / `std::unordered_set`：哈希表實作，平均尋找/插入/刪除 $O(1)$。
* `std::priority_queue`：堆疊實作，預設大頂堆 (Max-Heap)，插入/取出 $O(\log N)$。

---

## 2. 高頻資料結構與演算法模組

* **前綴和 + Hash**：解決子陣列和等於 $K$ 的問題 (如 LeetCode 560)。
* **雙指標 (Two Pointers)**：對撞指標（解決 sorted 陣列問題如 3Sum）、快慢指標。
* **單調棧與單調佇列**：解決 Next Greater Element、滑動窗口最大值 (Sliding Window Maximum) 等問題。

---

## 3. LeetCode 刷題解題紀錄

### LeetCode 560. Subarray Sum Equals K (Medium)
* **核心思想**：前綴和 $P[j] - P[i-1] = K \implies P[i-1] = P[j] - K$。
* **空間/時間複雜度**：時間 $O(N)$，空間 $O(N)$。

---

> 📝 *後續新的 C++ 與 LeetCode 筆記將持續補充於此處。*

<aside>
<img src="i" alt="i" width="40px" />

本計畫專為 **C++ 現代語法、STL 資料結構與 LeetCode 演算法衝刺** 打造，目標在 2 個月內達標台積電 IT / 一線軟體廠演算法與 C++ 技術面試等級。

</aside>

## 📊 衝刺進度儀表板 (Dashboard)

- **總目標題數**：44 題（含台積電 IT 高頻核心題、BST/多源BFS/並查集與二分圖擴充）
- **已完成題目**：28 / 44
- **完成率**：63.6%
- **時間紀錄檔**：`LEETCODE_CPP_TIME_LOG.md`

---

## 🎯 2 個月 LeetCode & C++ 衝刺主題規劃

### 1. 陣列、前綴和與雙指針 (Array, Prefix Sum & Two Pointers)
- [x] **LeetCode 560. Subarray Sum Equals K (Medium)** — *Prefix Sum + Hash Map ($O(N)$)*
- [x] **LeetCode 15. 3Sum (Medium)** — *Sorting + Two Pointers ($O(N^2)$)*
- [x] **LeetCode 11. Container With Most Water (Medium)** — *Two Pointers 相向收縮 ($O(N)$)*
- [ ] **LeetCode 1. Two Sum (Easy)** — *Hash Table 基礎 ($O(N)$)*
- [ ] **LeetCode 53. Maximum Subarray (Medium)** — *Kadane's 演算法 / 基礎 DP ($O(N)$)*
- [ ] **LeetCode 121. Best Time to Buy and Sell Stock (Easy)** — *陣列遍歷與狀態維護 ($O(N)$)*
- [ ] **LeetCode 56. Merge Intervals (Medium)** — *區間排序與合併 ($O(N \log N)$)*
- [x] **LeetCode 42. Trapping Rain Water (Hard)** — *Two Pointers / Monotonic Stack ($O(N)$)*

---

### 2. 滑動窗口與字串 (Sliding Window & Strings)
- [x] **LeetCode 3. Longest Substring Without Repeating Characters (Medium)** — *Sliding Window + Hash Map*
- [x] **LeetCode 76. Minimum Window Substring (Hard)** — *Sliding Window + Character Count Frequency Map*
- [x] **LeetCode 438. Find All Anagrams in a String (Medium)** — *Fixed-size Sliding Window*

---

### 3. 棧、單調棧與單調隊列 (Stack, Monotonic Stack & Queue)
- [ ] **LeetCode 20. Valid Parentheses (Easy)** — *`std::stack` 基礎應用*
- [x] **LeetCode 739. Daily Temperatures (Medium)** — *Monotonic Decreasing Stack*
- [x] **LeetCode 84. Largest Rectangle in Histogram (Hard)** — *Monotonic Stack with Sentinel*
- [x] **LeetCode 239. Sliding Window Maximum (Hard)** — *Monotonic Queue (`std::deque`)*

---

### 4. 二分搜尋與 Search Space（Binary Search）
- [x] **LeetCode 33. Search in Rotated Sorted Array (Medium)** — *Modified Binary Search*
- [x] **LeetCode 153. Find Minimum in Rotated Sorted Array (Medium)** — *Binary Search Boundary Condition*
- [x] **LeetCode 875. Koko Eating Bananas (Medium)** — *Binary Search on Answer Space*
- [x] **LeetCode 4. Median of Two Sorted Arrays (Hard)** — *Binary Search Partitioning*

---

### 5. 樹狀結構與遞迴 (Binary Tree & DFS/BFS)
- [x] **LeetCode 236. Lowest Common Ancestor of a Binary Tree (Medium)** — *樹狀遞迴 DFS (Post-order / Divide & Conquer)*
- [x] **LeetCode 226. Invert Binary Tree (Easy)** — *子樹指標對調 (`swap`) / 前序或後序遞迴*
- [x] **LeetCode 101. Symmetric Tree (Easy)** — *雙指標鏡像比對 (`isMirror` 同步遞迴)*
- [x] **LeetCode 104. Maximum Depth of Binary Tree (Easy)** — *樹最大深度 / 遞迴 DFS*
- [x] **LeetCode 102. Binary Tree Level Order Traversal (Medium)** — *樹狀結構 BFS (`std::queue`)*
- [x] **LeetCode 543. Diameter of Binary Tree (Easy)** — *二叉樹直徑 / 後序遞迴 DFS (Left Depth + Right Depth)*
- [ ] **LeetCode 98. Validate Binary Search Tree (Medium)** — *BST 遞迴上下界維護 / 中序遍歷性質*
- [x] **LeetCode 105. Construct Binary Tree from Preorder and Inorder Traversal (Medium)** — *前序與中序樹狀重建 / 遞迴 Index Range*

---

### 6. 圖論、拓撲排序與二分圖（Graph, Topological Sort & Bipartite）
- [x] **LeetCode 200. Number of Islands (Medium)** — *DFS / BFS Grid Traversal*
- [x] **LeetCode 133. Clone Graph (Medium)** — *Hash Map 與圖遍歷 (DFS/BFS)*
- [x] **LeetCode 207. Course Schedule (Medium)** — *Topological Sort (Kahn's Algorithm / DFS Cycle Detection)*
- [x] **LeetCode 210. Course Schedule II (Medium)** — *Topological Sort Order Output*
- [x] **LeetCode 785. Is Graph Bipartite? (Medium)** — *Bipartite Graph Coloring BFS/DFS*
- [x] **LeetCode 886. Possible Bipartition (Medium)** — *建圖 + 二分圖著色應用題 (Bipartite Graph / Union-Find)*
- [x] **LeetCode 2493. Divide Nodes Into the Maximum Number of Groups (Hard)** — *連通分量 + 二分圖染色 + 全源 BFS 最大深度 ($O(V(V+E))$)*
- [ ] **LeetCode 994. Rotting Oranges (Medium)** — *Multi-source BFS 網格擴散模擬*
- [ ] **LeetCode 547. Number of Provinces (Medium)** — *Union-Find (並查集) 基礎 / 矩陣連通分量*

---

### 7. 動態規劃與記憶化搜尋 (Dynamic Programming)
- [ ] 📌 **LeetCode 322. Coin Change (Medium)** — *Unbounded Knapsack / DP State Transition (下次起點)*
- [ ] **LeetCode 300. Longest Increasing Subsequence (Medium)** — *DP ($O(N^2)$) & Binary Search ($O(N \log N)$)*
- [ ] **LeetCode 1143. Longest Common Subsequence (Medium)** — *2D DP Grid*
- [ ] **LeetCode 198. House Robber (Medium)** — *1D DP State Machine*
- [ ] **LeetCode 72. Edit Distance (Hard)** — *Classic 2D String DP*

---

### 8. 堆疊、優先隊列與圖最短路徑 (Heap, Priority Queue & Dijkstra)
- [ ] **LeetCode 215. Kth Largest Element in an Array (Medium)** — *`std::priority_queue` vs QuickSelect*
- [ ] **LeetCode 23. Merge k Sorted Lists (Hard)** — *Min-Heap Multi-way Merge*
- [ ] **LeetCode 743. Network Delay Time (Medium)** — *Dijkstra Algorithm with Priority Queue*

---

## 📚 歷年已解決題目清單（Mastered Inventory - 100+ 題精選備查）

（保留歷史已做過題目：包含 Linked List, Basic Sliding Window, Binary Tree 等）


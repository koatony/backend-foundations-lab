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

### LeetCode 11. Container With Most Water (Medium)
* **核心思想**：雙指標從兩端夾擊。
  * **貪心選擇策略（誰矮動誰）**：裝水量由較矮柱子決定。若移動高柱子，寬度變窄且高度上限不變，容量必變小；只有移動較矮的一側，高度上限才「有機會」變大。
  * **複雜度**：時間 $O(N)$，空間 $O(1)$。
* **跳躍式優化 (Gotcha) ⚠️**：
  * 在指標向內縮時，可以寫內層 `while` 跳過所有「矮於或等於目前柱子」的元素。
  * **邊界防線**：內層跳躍時，不能直接寫外層變數 `while(left < right)`，因為內層迴圈只更新偏移量 `i`。必須寫 `while(left + i < right)`，以防止索引越界造成 `Segmentation Fault`。

### LeetCode 2493. Divide Nodes Into the Maximum Number of Groups (Hard)
* **核心思想**：
  * **連通分量劃分**：透過 BFS / DFS 劃分獨立的連通分量 (Connected Components)。
  * **二分圖染色檢驗**：對每個連通分量進行二分圖染色檢驗（$\pm 1$ 著色）。若存在奇環（相鄰點同色），則無法劃分，直接回傳 $-1$。
  * **全源 BFS 求最大深度**：若為二分圖，則對連通塊內的每個節點作為起點跑 BFS 逐層推進（`sz = q.size()`），記錄該點出發的最大層數（即該連通塊以該點起算的最大深度）。
  * **連通分量最大值加總**：每個獨立連通塊的組數為該塊內所有點作為起點 BFS 得到的最大深度之最大值（$\max$）。最終的總組數為所有連通分量最大深度的總和（$\sum$）。
* **複雜度**：時間 $O(V(V+E))$，空間 $O(V+E)$。在 $N \le 500$ 限制下運算量僅約 $5 \times 10^6$，可順利通過。
* **易錯點與除錯脈絡 (Gotcha) ⚠️**：
  * **語法與無窮迴圈**：注意 edges 迴圈邊界越界（應為 `<` 非 `<=`）、避免將 queue 賦值給 vector、BFS 內必須呼叫 `q.pop()` 以防無窮迴圈、外層每次出發必須重設 `visited`。
  * **二分圖染色失效**：衝突判斷 `if (c[k] == c[j])` 應放在染色判斷之外，而非放在未染色 `if (c[k] == 0)` 的內部，否則條件永遠不成立，無法抓出奇環。
  * **連通塊處理錯誤**：不可誤用全域最大值 `ans = max(ans, depth)`。多個獨立連通塊時，總組數應為各連通塊最大值的總和（$\sum$），而非全域最大值。
  * **BFS 標記時機**：確認無權圖必須在節點被 **Push** 入佇列時立即標記已訪問；若在 **Pop** 出來時才標記，節點會被重複塞入佇列，造成空間與時間複雜度暴增（$O(V)$ vs $O(E)$）。
* **圖論概念與面試考點**：
  * **為什麼能暴力搜尋？**：一般圖（含偶環）無法使用樹的「兩次 BFS」貪婪法尋找直徑；因此枚舉所有點跑全源 BFS 就是此題的標準最優解。
  * **樹的直徑（兩次 BFS）**：僅適用於無環樹（Tree）。面試（如台積電）只需掌握兩次 BFS 的實作原理與適用限制，不需白板推導反證法。

### LeetCode 236. Lowest Common Ancestor of a Binary Tree (Medium)
* **學員狀態標記 ⚠️**：目前為**硬背記憶模板階段**。對遞迴思維與 Call Stack 傳遞回傳值機制尚不敏感，後續複習需著重拆解思考步驟而非死記程式碼。
* **核心思想 (分治法 / 後序遍歷)**：
  * 本題採用**後序遍歷 (Post-order Traversal)**「先探查左右子樹，再根據兩側回傳值決定當前節點狀態」的匯集機制。
* **C++ 實作範例**：
  ```cpp
  class Solution {
  public:
      TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
          // Base Case: 遇到空節點，或當前節點即為 p 或 q，向上回傳自己
          if (!root || root == p || root == q) {
              return root;
          }

          // Divide: 探查左子樹與右子樹
          TreeNode* left = lowestCommonAncestor(root->left, p, q);
          TreeNode* right = lowestCommonAncestor(root->right, p, q);

          // Combine: 依據左右子樹回傳結果進行判斷
          if (left && right) {
              return root; // 兩側皆非空 -> 當前 root 即為 LCA
          }

          return left ? left : right; // 單側非空 -> 向上傳遞該側發現的節點；兩側皆空 -> 回傳 nullptr
      }
  };
  ```
* **遞迴直覺培養指南 (從硬背轉化為理解)**：
  1. **別想太深**：不要試圖在腦中展開整個 Call Stack 的幾十層遞迴；只需專注於**「當前節點 `root` 拿到了左側 `left` 與右側 `right` 的結果後，該做什麼反應」**。
  2. **三種情境分流**：
     - 情境 A (`left && right`)：左子樹找到一個、右子樹找到一個，說明 `p` 和 `q` 分立兩側 $\implies$ 我就是最近公共祖先 (LCA)，回傳 `root`。
     - 情境 B (`left || right`)：只有一側有找到（例如左邊找到了 LCA 或某目標點），說明兩點都在同側 $\implies$ 直接把左邊的答案向上傳遞。
     - 情境 C (`!left && !right`)：左右都沒找到 $\implies$ 回傳 `nullptr`。

### LeetCode 226. Invert Binary Tree (Easy)
* **核心思想 (子樹指標對調)**：
  * **自頂向下或自底向上 (前序 / 後序遍歷)**：核心為 `swap(root->left, root->right)`，遞迴處理左右子樹。
  * **關鍵注意點**：若採用前序/後序遍歷，需注意避免單邊指標被覆蓋後遺失。

### LeetCode 101. Symmetric Tree (Easy)
* **核心思想 (雙指標鏡像比對)**：
  * **前序延伸 (同步遞迴 / Simultaneous Traversal)**：開 Helper 函式 `isMirror(t1, t2)` 同時走訪兩節點。
  * **交叉比對關鍵**：比對 `t1->val == t2->val` 並遞迴交叉比對 `t1->left` vs `t2->right` 與 `t1->right` vs `t2->left`。

---

### 🧠 二元樹核心三大遍歷模式與思維收斂 (LC 236 / LC 226 / LC 101)

| 題目 | 核心概念 | 遍歷本質 | 關鍵解題思維 |
| --- | --- | --- | --- |
| **LC 236**<br>二元樹最近公共祖先 (LCA) | **分治法 (Divide & Conquer)**<br>Bottom-Up 匯總 | **後序遍歷 (Post-order)** | 左右子樹各回報搜尋結果；若左右皆有回報，當前節點即為分叉點 (LCA)。 |
| **LC 226**<br>翻轉二元樹 (Invert Tree) | **子樹指標對調**<br>自頂向下或自底向上 | **前序 / 後序遍歷** | 核心為 `swap(root->left, root->right)`，需注意避免單邊指標被覆蓋後遺失。 |
| **LC 101**<br>對稱二元樹 (Symmetric Tree) | **雙指標鏡像比對**<br>Simultaneous Traversal | **前序延伸 (同步遞迴)** | 開 Helper 函式同時走訪兩節點，交叉比對 `t1->left` vs `t2->right` 與 `t1->right` vs `t2->left`。 |

#### 核心思維對比：
1. **單樹傳遞 vs 雙樹比對**：
   * **單一二元樹的問題**（如 236、226）：通常依賴「當前節點 + 左右子問題」。
   * **涉及兩樹結構比較**（如 101 對稱、100 相同樹）：習慣開 `isMirror(t1, t2)` 雙指標同步比對。
2. **資訊流向**：
   * **由上往下做 (Top-Down / 前序)**：先改變當前節點狀態，再丟給小孩做（如 226 翻轉）。
   * **由下往上做 (Bottom-Up / 後序)**：小孩先算完回報給父節點做決定（如 236 LCA）。

---

> 📝 *後續新的 C++ 與 LeetCode 筆記將持續補充於此處。*


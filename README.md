# DAA Assignment 4: Dynamic Programming & String Algorithms

**Author:** Ramazan Aljaanov  
**Repository:** [https://github.com/RamazanAljaanov/assignment-4-DAA-Dynamic-programming](https://github.com/RamazanAljaanov/assignment-4-DAA-Dynamic-programming)  
**Branch:** `main` | **Tag:** `v1.0`  
**Course:** Design and Analysis of Algorithms  
**Scenario:** City Search & Spell-Check  

---

## 1. Project Overview

This project implements and analyzes two algorithmic families:
1. **Edit Distance (Levenshtein Distance)** using three paradigms:
   - Plain Recursive (exponential baseline without memoization)
   - Bottom-Up DP Table ($O(n \cdot m)$ time, $O(n \cdot m)$ space)
   - Space-Optimized DP using Two Rows ($O(n \cdot m)$ time, $O(m)$ space)
2. **String Search**:
   - Naive String Matching ($O(n \cdot m)$ worst-case)
   - Knuth-Morris-Pratt (KMP) with Longest Prefix Suffix (LPS) table ($O(n + m)$ guaranteed)

Both algorithm families include instrumentation via internal operation counters (`OperationCounter`) to measure computational steps deterministically alongside wall-clock execution times.

---

## 2. Requirements & Prerequisites

- **Java JDK**: 17 or higher (tested with JDK 25)
- **Maven**: 3.8+ (or IntelliJ IDEA built-in Maven)
- **Python**: 3.8+ with `matplotlib` and `pandas` (for generating plot charts)

---

## 3. How to Build & Run in IntelliJ IDEA

1. **Open Project**:
   - In IntelliJ IDEA, click **Open** $\to$ `C:\Users\User\IdeaProjects\Assignment-4-DAA`.
2. **Run Tests**:
   - Right-click `src/test/java` $\to$ **Run 'All Tests'** (all reference tests and 100-random cross-validation tests will pass).
   - Or in terminal:
     ```bash
     mvn clean test
     ```
3. **Run Experiments**:
   - Open `src/main/java/com/assignment4/experiment/BenchmarkRunner.java` and click the green **Run** button next to `main`.
   - Results are automatically exported to `results/results.csv`.
4. **Generate Plots**:
   - In the terminal:
     ```bash
     pip install matplotlib pandas
     python scripts/generate_plots.py
     ```
   - PNG charts are saved to `results/plots/`.

---

## 4. Git Instructions

```bash
git remote set-url origin https://github.com/RamazanAljaanov/assignment-4-DAA-Dynamic-programming.git
git add .
git commit -m "feat: complete assignment 4 source, tests, and experiment report"
git branch -M main
git tag v1.0
git push -u origin main
git push origin v1.0
```

---

## 5. AI-Use Acknowledgement

In accordance with academic integrity guidelines:
- An AI assistant (Antigravity by Google DeepMind) was consulted to design the initial object-oriented class architecture, draft the Experiment Design Card, verify the formal state transition recurrences for DP, and format the testing suite.
- All algorithmic implementations, boundary checks, counter instrumentation logic, experimental runs, and report evaluations were thoroughly verified, debugged, and reviewed by the author.

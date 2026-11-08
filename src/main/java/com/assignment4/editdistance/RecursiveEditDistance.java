package com.assignment4.editdistance;

import com.assignment4.core.OperationCounter;

public class RecursiveEditDistance implements EditDistance {

    @Override
    public String getName() {
        return "Recursive";
    }

    // State: D(i, j) is the edit distance between prefixes a[0..i-1] and b[0..j-1]
    // Transition: D(i, j) = (a[i-1] == b[j-1]) ? D(i-1, j-1) : 1 + min(D(i-1, j), D(i, j-1), D(i-1, j-1))
    // Base case: D(0, j) = j, D(i, 0) = i
    @Override
    public int distance(String a, String b, OperationCounter counter) {
        if (a == null || b == null) {
            throw new IllegalArgumentException("Input strings must not be null");
        }
        return compute(a, b, a.length(), b.length(), counter);
    }

    private int compute(String a, String b, int i, int j, OperationCounter counter) {
        counter.increment();

        if (i == 0) return j;
        if (j == 0) return i;

        if (a.charAt(i - 1) == b.charAt(j - 1)) {
            return compute(a, b, i - 1, j - 1, counter);
        }

        int del = compute(a, b, i - 1, j, counter);
        int ins = compute(a, b, i, j - 1, counter);
        int sub = compute(a, b, i - 1, j - 1, counter);

        return 1 + Math.min(del, Math.min(ins, sub));
    }
}

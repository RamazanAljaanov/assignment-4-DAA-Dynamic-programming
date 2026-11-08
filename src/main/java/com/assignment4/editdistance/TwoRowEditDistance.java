package com.assignment4.editdistance;

import com.assignment4.core.OperationCounter;

public class TwoRowEditDistance implements EditDistance {

    @Override
    public String getName() {
        return "Two-Rows";
    }

    // State: curr[j] is the edit distance for row i, prev[j] is the edit distance for row i-1
    // Transition: curr[j] = (a[i-1] == b[j-1]) ? prev[j-1] : 1 + min(prev[j], curr[j-1], prev[j-1])
    // Base case: prev[j] = j for 0 <= j <= m; curr[0] = i at each iteration i
    @Override
    public int distance(String a, String b, OperationCounter counter) {
        if (a == null || b == null) {
            throw new IllegalArgumentException("Input strings must not be null");
        }
        int n = a.length();
        int m = b.length();

        int[] prev = new int[m + 1];
        int[] curr = new int[m + 1];

        for (int j = 0; j <= m; j++) {
            prev[j] = j;
        }

        for (int i = 1; i <= n; i++) {
            curr[0] = i;
            for (int j = 1; j <= m; j++) {
                counter.increment();
                if (a.charAt(i - 1) == b.charAt(j - 1)) {
                    curr[j] = prev[j - 1];
                } else {
                    int del = prev[j];
                    int ins = curr[j - 1];
                    int sub = prev[j - 1];
                    curr[j] = 1 + Math.min(del, Math.min(ins, sub));
                }
            }
            System.arraycopy(curr, 0, prev, 0, m + 1);
        }

        return prev[m];
    }
}

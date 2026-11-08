package com.assignment4.editdistance;

import com.assignment4.core.OperationCounter;

public class TableEditDistance implements EditDistance {

    @Override
    public String getName() {
        return "Table-DP";
    }

    // State: dp[i][j] is the edit distance between prefixes a[0..i-1] and b[0..j-1]
    // Transition: dp[i][j] = (a[i-1] == b[j-1]) ? dp[i-1][j-1] : 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    // Base case: dp[i][0] = i for all 0 <= i <= n; dp[0][j] = j for all 0 <= j <= m
    @Override
    public int distance(String a, String b, OperationCounter counter) {
        if (a == null || b == null) {
            throw new IllegalArgumentException("Input strings must not be null");
        }
        int n = a.length();
        int m = b.length();

        int[][] dp = new int[n + 1][m + 1];

        for (int i = 0; i <= n; i++) {
            dp[i][0] = i;
        }
        for (int j = 0; j <= m; j++) {
            dp[0][j] = j;
        }

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                counter.increment();
                if (a.charAt(i - 1) == b.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    int del = dp[i - 1][j];
                    int ins = dp[i][j - 1];
                    int sub = dp[i - 1][j - 1];
                    dp[i][j] = 1 + Math.min(del, Math.min(ins, sub));
                }
            }
        }

        return dp[n][m];
    }
}

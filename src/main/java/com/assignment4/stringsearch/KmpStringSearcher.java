package com.assignment4.stringsearch;

import com.assignment4.core.OperationCounter;
import java.util.ArrayList;
import java.util.List;

public class KmpStringSearcher implements StringSearcher {

    @Override
    public String getName() {
        return "KMP";
    }

    public static int[] lps(String p) {
        if (p == null) {
            throw new IllegalArgumentException("Pattern must not be null");
        }
        int m = p.length();
        int[] lps = new int[m];
        if (m == 0) return lps;

        int len = 0;
        int i = 1;
        lps[0] = 0;

        while (i < m) {
            if (p.charAt(i) == p.charAt(len)) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

    @Override
    public List<Integer> search(String text, String pattern, OperationCounter counter) {
        if (text == null || pattern == null) {
            throw new IllegalArgumentException("Text and pattern must not be null");
        }
        if (pattern.isEmpty()) {
            throw new IllegalArgumentException("Pattern must not be empty");
        }

        List<Integer> occurrences = new ArrayList<>();
        int n = text.length();
        int m = pattern.length();

        if (m > n) {
            return occurrences;
        }

        int[] lps = lps(pattern);

        int i = 0;
        int j = 0;

        while (i < n) {
            counter.increment();
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
                if (j == m) {
                    occurrences.add(i - j);
                    j = lps[j - 1];
                }
            } else {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }

        return occurrences;
    }
}

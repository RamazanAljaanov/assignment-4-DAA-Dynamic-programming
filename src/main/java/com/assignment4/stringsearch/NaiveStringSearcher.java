package com.assignment4.stringsearch;

import com.assignment4.core.OperationCounter;
import java.util.ArrayList;
import java.util.List;

public class NaiveStringSearcher implements StringSearcher {

    @Override
    public String getName() {
        return "Naive";
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

        for (int i = 0; i <= n - m; i++) {
            int j = 0;
            while (j < m) {
                counter.increment();
                if (text.charAt(i + j) != pattern.charAt(j)) {
                    break;
                }
                j++;
            }
            if (j == m) {
                occurrences.add(i);
            }
        }

        return occurrences;
    }
}

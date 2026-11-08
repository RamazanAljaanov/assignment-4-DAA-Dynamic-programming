package com.assignment4.editdistance;

import com.assignment4.core.OperationCounter;

public interface EditDistance {

    default int distance(String a, String b) {
        return distance(a, b, new OperationCounter());
    }

    int distance(String a, String b, OperationCounter counter);

    String getName();
}

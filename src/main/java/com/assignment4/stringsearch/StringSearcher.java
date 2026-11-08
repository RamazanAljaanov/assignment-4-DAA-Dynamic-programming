package com.assignment4.stringsearch;

import com.assignment4.core.OperationCounter;
import java.util.List;

public interface StringSearcher {

    default List<Integer> search(String text, String pattern) {
        return search(text, pattern, new OperationCounter());
    }

    List<Integer> search(String text, String pattern, OperationCounter counter);

    String getName();
}

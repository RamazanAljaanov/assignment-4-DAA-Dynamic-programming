package com.assignment4.core;

public class OperationCounter {
    private long count = 0;

    public void increment() {
        count++;
    }

    public void add(long delta) {
        count += delta;
    }

    public long get() {
        return count;
    }

    public void reset() {
        count = 0;
    }
}

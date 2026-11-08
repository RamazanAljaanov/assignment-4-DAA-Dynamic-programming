package com.assignment4.experiment;

import java.util.Random;

public class DataGenerator {

    private final Random random;

    public DataGenerator(long seed) {
        this.random = new Random(seed);
    }

    public String randomString(int length, String alphabet) {
        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            sb.append(alphabet.charAt(random.nextInt(alphabet.length())));
        }
        return sb.toString();
    }

    public String[] generateRandomEditDistancePair(int n, int m) {
        String alphabet = "ACGT";
        return new String[]{
                randomString(n, alphabet),
                randomString(m, alphabet)
        };
    }

    public String[] generateWorstCaseEditDistancePair(int n, int m) {
        String a = "A".repeat(n);
        String b = "B".repeat(m);
        return new String[]{a, b};
    }

    public String[] generateRandomSearchPair(int textLen, int patternLen) {
        String alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        String text = randomString(textLen, alphabet);
        String pattern = randomString(patternLen, alphabet);
        return new String[]{text, pattern};
    }

    public String[] generateWorstCaseSearchPair(int textLen, int patternLen) {
        if (patternLen <= 0) patternLen = 1;
        String text = "A".repeat(textLen);
        String pattern = "A".repeat(patternLen - 1) + "B";
        return new String[]{text, pattern};
    }
}

package com.assignment4;

import com.assignment4.stringsearch.*;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.List;
import java.util.Random;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

public class StringSearchTest {

    static Stream<StringSearcher> implementations() {
        return Stream.of(
                new NaiveStringSearcher(),
                new KmpStringSearcher()
        );
    }

    @Test
    @DisplayName("Reference LPS arrays from Section 7")
    void testLpsReferenceArrays() {
        assertArrayEquals(new int[]{0, 1, 2, 0, 1, 2, 3, 3}, KmpStringSearcher.lps("AAACAAAA"));
        assertArrayEquals(new int[]{0, 0, 1, 2, 0, 1, 2, 3, 4}, KmpStringSearcher.lps("ABABCABAB"));
    }

    @ParameterizedTest
    @MethodSource("implementations")
    @DisplayName("Reference search matches from Section 7")
    void testReferenceMatches(StringSearcher searcher) {
        assertEquals(List.of(10), searcher.search("ABABDABACDABABCABAB", "ABABCABAB"));
        assertEquals(List.of(0, 1, 2, 3), searcher.search("AAAAA", "AA"));
        assertEquals(List.of(0, 2, 4), searcher.search("ABABABA", "ABA"));
    }

    @ParameterizedTest
    @MethodSource("implementations")
    @DisplayName("Edge cases")
    void testEdgeCases(StringSearcher searcher) {
        assertThrows(IllegalArgumentException.class, () -> searcher.search("HELLO", ""));
        assertTrue(searcher.search("ABC", "ABCDEF").isEmpty());
        assertTrue(searcher.search("", "A").isEmpty());
    }

    @Test
    @DisplayName("Cross-check: 100 random texts and patterns")
    void testRandom100MatchesCrossCheck() {
        StringSearcher naive = new NaiveStringSearcher();
        StringSearcher kmp = new KmpStringSearcher();

        Random rng = new Random(1337);
        String alphabet = "AB";

        for (int step = 0; step < 100; step++) {
            int textLen = 50 + rng.nextInt(100);
            int patLen = 2 + rng.nextInt(6);

            String text = generateString(rng, alphabet, textLen);
            String pat = generateString(rng, alphabet, patLen);

            List<Integer> naiveMatches = naive.search(text, pat);
            List<Integer> kmpMatches = kmp.search(text, pat);

            assertEquals(naiveMatches, kmpMatches);
        }
    }

    private String generateString(Random rng, String alphabet, int length) {
        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            sb.append(alphabet.charAt(rng.nextInt(alphabet.length())));
        }
        return sb.toString();
    }
}

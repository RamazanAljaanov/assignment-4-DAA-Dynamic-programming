package com.assignment4;

import com.assignment4.editdistance.*;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.Random;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class EditDistanceTest {

    static Stream<EditDistance> implementations() {
        return Stream.of(
                new RecursiveEditDistance(),
                new TableEditDistance(),
                new TwoRowEditDistance()
        );
    }

    @ParameterizedTest
    @MethodSource("implementations")
    @DisplayName("Reference values from Section 7")
    void testReferenceValues(EditDistance algorithm) {
        assertEquals(3, algorithm.distance("kitten", "sitting"));
        assertEquals(2, algorithm.distance("flaw", "lawn"));
        assertEquals(5, algorithm.distance("intention", "execution"));
        assertEquals(3, algorithm.distance("", "abc"));
        assertEquals(3, algorithm.distance("abc", ""));
        assertEquals(0, algorithm.distance("abc", "abc"));
        assertEquals(0, algorithm.distance("", ""));
    }

    @Test
    @DisplayName("Cross-check: 100 random short strings must produce identical results across all 3 versions")
    void testRandomStringsAgreement() {
        EditDistance rec = new RecursiveEditDistance();
        EditDistance tab = new TableEditDistance();
        EditDistance two = new TwoRowEditDistance();

        Random rng = new Random(42);
        String chars = "ABCDEFGHIJ";

        for (int step = 0; step < 100; step++) {
            int lenA = rng.nextInt(9);
            int lenB = rng.nextInt(9);

            String a = generateRandomString(rng, chars, lenA);
            String b = generateRandomString(rng, chars, lenB);

            int resRec = rec.distance(a, b);
            int resTab = tab.distance(a, b);
            int resTwo = two.distance(a, b);

            assertEquals(resTab, resRec);
            assertEquals(resTab, resTwo);
        }
    }

    private String generateRandomString(Random rng, String alphabet, int length) {
        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            sb.append(alphabet.charAt(rng.nextInt(alphabet.length())));
        }
        return sb.toString();
    }
}

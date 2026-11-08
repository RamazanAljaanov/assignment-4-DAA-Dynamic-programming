package com.assignment4.experiment;

import com.assignment4.core.OperationCounter;
import com.assignment4.editdistance.*;
import com.assignment4.stringsearch.*;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.List;

public class BenchmarkRunner {

    private static final long SEED = 42L;
    private static final int TRIALS = 5;

    public static void main(String[] args) {
        File resultsDir = new File("results");
        if (!resultsDir.exists()) {
            resultsDir.mkdirs();
        }

        File csvFile = new File(resultsDir, "results.csv");

        try (PrintWriter writer = new PrintWriter(new FileWriter(csvFile))) {
            writer.println("algorithm,input,n,m,time_ms,operations_count");

            benchmarkEditDistanceRecursive(writer);
            benchmarkEditDistanceDP(writer);
            benchmarkStringSearch(writer);

            System.out.println("Benchmarks completed. Results saved to: " + csvFile.getAbsolutePath());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void benchmarkEditDistanceRecursive(PrintWriter writer) {
        EditDistance rec = new RecursiveEditDistance();
        int[] sizes = {3, 6, 9, 12, 14};

        for (String inputType : List.of("random", "worst_case")) {
            for (int n : sizes) {
                DataGenerator gen = new DataGenerator(SEED);
                String[] pair = inputType.equals("random") 
                        ? gen.generateRandomEditDistancePair(n, n) 
                        : gen.generateWorstCaseEditDistancePair(n, n);

                rec.distance(pair[0], pair[1], new OperationCounter());

                double[] times = new double[TRIALS];
                long ops = 0;

                for (int t = 0; t < TRIALS; t++) {
                    OperationCounter counter = new OperationCounter();
                    long start = System.nanoTime();
                    rec.distance(pair[0], pair[1], counter);
                    long elapsed = System.nanoTime() - start;
                    times[t] = elapsed / 1_000_000.0;
                    ops = counter.get();
                }

                Arrays.sort(times);
                double medianTime = times[TRIALS / 2];

                System.out.printf("[%s] %-10s n=%-2d | time: %8.4f ms | ops: %d%n",
                        rec.getName(), inputType, n, medianTime, ops);
                writer.printf("%s,%s,%d,%d,%.4f,%d%n",
                        rec.getName(), inputType, n, n, medianTime, ops);
            }
        }
    }

    private static void benchmarkEditDistanceDP(PrintWriter writer) {
        List<EditDistance> algorithms = List.of(new TableEditDistance(), new TwoRowEditDistance());
        int[] sizes = {500, 1000, 2000, 4000};

        for (EditDistance algo : algorithms) {
            for (String inputType : List.of("random", "worst_case")) {
                for (int n : sizes) {
                    DataGenerator gen = new DataGenerator(SEED);
                    String[] pair = inputType.equals("random") 
                            ? gen.generateRandomEditDistancePair(n, n) 
                            : gen.generateWorstCaseEditDistancePair(n, n);

                    algo.distance(pair[0], pair[1], new OperationCounter());

                    double[] times = new double[TRIALS];
                    long ops = 0;

                    for (int t = 0; t < TRIALS; t++) {
                        OperationCounter counter = new OperationCounter();
                        long start = System.nanoTime();
                        algo.distance(pair[0], pair[1], counter);
                        long elapsed = System.nanoTime() - start;
                        times[t] = elapsed / 1_000_000.0;
                        ops = counter.get();
                    }

                    Arrays.sort(times);
                    double medianTime = times[TRIALS / 2];

                    System.out.printf("[%s] %-10s n=%-4d | time: %8.4f ms | ops: %d%n",
                            algo.getName(), inputType, n, medianTime, ops);
                    writer.printf("%s,%s,%d,%d,%.4f,%d%n",
                            algo.getName(), inputType, n, n, medianTime, ops);
                }
            }
        }
    }

    private static void benchmarkStringSearch(PrintWriter writer) {
        List<StringSearcher> algorithms = List.of(new NaiveStringSearcher(), new KmpStringSearcher());
        int[] textSizes = {10000, 50000, 100000, 200000};
        int patternSize = 500;

        for (StringSearcher algo : algorithms) {
            for (String inputType : List.of("random", "worst_case")) {
                for (int n : textSizes) {
                    DataGenerator gen = new DataGenerator(SEED);
                    String[] pair = inputType.equals("random") 
                            ? gen.generateRandomSearchPair(n, patternSize) 
                            : gen.generateWorstCaseSearchPair(n, patternSize);

                    algo.search(pair[0], pair[1], new OperationCounter());

                    double[] times = new double[TRIALS];
                    long ops = 0;

                    for (int t = 0; t < TRIALS; t++) {
                        OperationCounter counter = new OperationCounter();
                        long start = System.nanoTime();
                        algo.search(pair[0], pair[1], counter);
                        long elapsed = System.nanoTime() - start;
                        times[t] = elapsed / 1_000_000.0;
                        ops = counter.get();
                    }

                    Arrays.sort(times);
                    double medianTime = times[TRIALS / 2];

                    System.out.printf("[%s] %-10s N=%-6d M=%-3d | time: %8.4f ms | comparisons: %d%n",
                            algo.getName(), inputType, n, patternSize, medianTime, ops);
                    writer.printf("%s,%s,%d,%d,%.4f,%d%n",
                            algo.getName(), inputType, n, patternSize, medianTime, ops);
                }
            }
        }
    }
}

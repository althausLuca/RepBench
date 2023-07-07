package code.test;

import code.DP;
import code.entity.TimePoint;
import code.entity.TimeSeries;
import code.util.Assist;

import java.io.FileWriter;
import java.io.IOException;

/**
 * Created by Stoke on 2017/10/8.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class DPTest {

    public static void main(String[] args) {
        String inputFileName = "stock1.2k.data";
//    String inputFileName = "stock10k.data"; may be out of memory under 10G

        Assist assist = new Assist();
        String splitOp = ",";

        TimeSeries dirtySeries = assist.readData(inputFileName, 1, splitOp);
        TimeSeries truthSeries = assist.readData(inputFileName, 2, splitOp);

        double rmsDirty = assist.calcRMS(truthSeries, dirtySeries);
        System.out.println("Dirty RMS error is " + rmsDirty);

        double RES = 0.1;     // the resolution of the data
        int PARAM = (int) (1/RES);       // RES * PARAM = 1, the normalized parameter
        double THETA = 5;     // after normalized
        double delta = 1500;
        System.out.println("delta: " + delta);

        assist.buildVModel();
        DP dp = new DP(dirtySeries, THETA, delta);
        dp.normalizeParams(RES, PARAM);
        dp.normalizeProbability(assist);
        TimeSeries resultSeries = dp.mainDP();

        double rms = assist.calcRMS(truthSeries, resultSeries);

        System.out.println("Repair RMS error is " + rms);

//        for (TimePoint tp : resultSeries.getTimeseries()) {
//            System.out.println(tp.getValue());
//        }

        String filePath = "../data/stat_data_"+THETA+"_"+delta+"_"+RES;
        TimeSeries truthSeriesNew = assist.readData(inputFileName, 2, splitOp);
        TimeSeries dirtySeriesNew = assist.readData(inputFileName, 1, splitOp);

        System.out.println(truthSeriesNew.getTimeseries().get(1).getValue());
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.append("Truth,Injected,Repair\n"); // Write the header row

            // Assuming all series have the same length
            for (int i = 0; i < truthSeriesNew.getTimeseries().size(); i++) {
                writer.append(String.valueOf(truthSeriesNew.getTimeseries().get(i).getValue())).append(",");
                writer.append(String.valueOf(dirtySeriesNew.getTimeseries().get(i).getValue())).append(",");
                writer.append(String.valueOf(resultSeries.getTimeseries().get(i).getValue())).append("\n");
            }
            System.out.println("Data has been written to " + filePath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


//        for (double THETA = 1; THETA <= 1; THETA += 1) {
//            Assist assist = new Assist();
//            String splitOp = ",";
//
//            TimeSeries dirtySeries = assist.readData(inputFileName, 1, splitOp);
//            TimeSeries truthSeries = assist.readData(inputFileName, 2, splitOp);
//
//            System.out.println("theta: " + THETA);
//            assist.buildVModel();
//            DP dp = new DP(dirtySeries, THETA, delta);
//            dp.normalizeParams(RES, PARAM);
//            dp.normalizeProbability(assist);
//            TimeSeries resultSeries = dp.mainDP();
//
//            double rms = assist.calcRMS(truthSeries, resultSeries);
//
//            System.out.println("Repair RMS error is " + rms);
//        }
}


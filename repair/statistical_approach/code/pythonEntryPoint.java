package code;

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
public class pythonEntryPoint {

    public static void main(String[] args) {
        System.out.println("main called");
    }

    public TimeSeries init_time_series(double[] values) {
        TimeSeries timeSeries = new TimeSeries();
        try {
            long timestamp;
            double value;
            TimePoint tp;
            for (int i = 0; i < values.length; i++) {
                timestamp = i;
                value = values[i];

                tp = new TimePoint(timestamp, value);
                timeSeries.addTimePoint(tp);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return timeSeries;
    }

    public double[] start(double theta, double delta_ , double[] injectedValues , double[] trueValues) { //String[] args

        Assist assist = new Assist();

        TimeSeries dirtySeries = this.init_time_series(injectedValues);
        TimeSeries truthSeries = this.init_time_series(trueValues);

        double rmsDirty = assist.calcRMS(truthSeries, dirtySeries);
        System.out.println("Dirty RMS error is " + rmsDirty);

        double RES = 0.1;     // the resolution of the data
        int PARAM = (int) (1 / RES);       // RES * PARAM = 1, the normalized parameter

        //theta is the first
        double THETA = theta;     // after normalized
        double delta = delta_;
        System.out.println("delta: " + delta);

        assist.buildVModel();
        DP dp = new DP(dirtySeries, THETA, delta);
        dp.normalizeParams(RES, PARAM);
        dp.normalizeProbability(assist);
        TimeSeries resultSeries = dp.mainDP();

        double rms = assist.calcRMS(truthSeries, resultSeries);

//        System.out.println("Repair RMS error is " + rms);

        for (TimePoint tp : resultSeries.getTimeseries()) {
            System.out.println(tp.getValue());
        }

        double[] retval = new double[resultSeries.getTimeseries().size()];
        for (int i = 0; i < retval.length; i++) {
            retval[i] = resultSeries.getTimeseries().get(i).getValue();
        }

        return retval;
    }

}


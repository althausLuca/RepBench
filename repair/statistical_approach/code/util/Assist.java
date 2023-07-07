package code.util;

import code.entity.TimePoint;
import code.entity.TimeSeries;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

/**
 * Created by Stoke on 2017/10/8.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class Assist {
  public static String PATH = "../data/";

  /**
   * Basic attributes: timestamp, dirty, truth
   *
   * @param filename filename
   * @param index which column besides timestamp should be read
   * @param splitOp to split up the lines
   * @return data in timeseries form
   */
  public TimeSeries readData(String filename, int index, String splitOp) {
    TimeSeries timeSeries = new TimeSeries();

    try {
      FileReader fr = new FileReader(PATH + filename);
      BufferedReader br = new BufferedReader(fr);

      String line;
      long timestamp;
      double value;
      TimePoint tp;

      while ((line = br.readLine()) != null) {
        String[] vals = line.split(splitOp);
        timestamp = Long.parseLong(vals[0]);
        value = Double.parseDouble(vals[index]);

        tp = new TimePoint(timestamp, value);
        timeSeries.addTimePoint(tp);
      }

      br.close();
      fr.close();
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }

    return timeSeries;
  }

  /**
   * RMS sqrt(|modify - truth|^2 / len)
   *
   * @param truthSeries truth
   * @param resultSeries after repair
   * @return RMS error
   */
  public double calcRMS(TimeSeries truthSeries, TimeSeries resultSeries) {
    double cost = 0;
    double delta;
    int len = truthSeries.getLength();

    for (int i = 0; i < len; ++i) {
      delta = resultSeries.getTimeseries().get(i).getModify()
          - truthSeries.getTimeseries().get(i).getValue();

      cost += delta * delta;
    }
    cost /= len;

    return Math.sqrt(cost);
  }

  /**
   * build the normalized disV model
   */
  public void buildVModel() {
    double minV = Constants.MINV;
    double maxV = Constants.MAXV;
    double interval = Constants.INTERV;

    int size = (int) (Math.ceil((maxV - minV) / interval) + 1);

    Constants.SPEEDPAT = new double[size];
    for (int i = 0; i < size; ++i) {
      Constants.SPEEDPAT[i] = minV + i * interval;
    }

    Constants.SPEEDOUT = new double[size];
    Constants.SPEEDOUT[0] = minV;
    for (int i = 1; i < size; ++i) {
      Constants.SPEEDOUT[i] = (Constants.SPEEDPAT[i - 1] + Constants.SPEEDPAT[i]) / 2;
    }
  }

  /**
   * compute the normalized disV
   * @param v2 the latter v
   * @param v1 the former v
   * @return the normalized disV of (v2-v1)
   */
  public static double calcDisV(double v2, double v1) {
    double disV;

    int index;
    double tmpV = v2 - v1;
    if (tmpV > Constants.MAXV || tmpV < Constants.MINV) {
      disV = Double.MAX_VALUE;
      return disV;
    }

    index = (int) Math.ceil((tmpV - Constants.MINV) / Constants.INTERV);
    disV = Constants.SPEEDOUT[index];
    return disV;
  }

  /**
   * calculate the ln of probability
   *
   * @param conMap the hit number map
   * @param LAMBDA the likelihood map
   * @param size the size
   * @return the max and min probability
   */
  public double[] calcLnProbability(HashMap<Double, Integer> conMap,
      HashMap<Double, Double> LAMBDA, int size) {
    int maxHit = 0, minHit = size;
    double value;

    Iterator<Entry<Double, Integer>> iterator = conMap.entrySet()
        .iterator();
    while (iterator.hasNext()) {
      Map.Entry<Double, Integer> entry = iterator.next();
      if (entry.getValue() > maxHit) {
        maxHit = entry.getValue();
      }
      if (entry.getValue() < minHit) {
        minHit = entry.getValue();
      }
    }

    double maxP = maxHit * 1.0 / size;
    double minP = minHit * 1.0 / size;

    iterator = conMap.entrySet().iterator();
    while (iterator.hasNext()) {
      Map.Entry<Double, Integer> entry = iterator.next();
      value = entry.getValue();
      value = value * 1.0 / size;

      LAMBDA.put(entry.getKey(), Math.log(value));
    }

    double[] maxMinP = { maxP, minP };
    return maxMinP;
  }

  /**
   * build the normalized hit number model
   *
   * @param timeseries timeseries
   * @return disV -> hit number
   */
  public HashMap<Double, Integer> convolution(TimeSeries timeseries) {
    // conMap Double: speed distance; Integer: hitnum
    HashMap<Double, Integer> conMap = new HashMap<>();

    ArrayList<TimePoint> tpList = timeseries.getTimeseries();
    ArrayList<Double> vList = new ArrayList<>();

    double preVal = 0, curVal;
    long preTime = 0, curTime;
    boolean isFirst = true;

    double deltaVal;
    long deltaTime;

    for (TimePoint tp : tpList) {
      if (isFirst) {
        preVal = tp.getValue();
        preTime = tp.getTimestamp();
        isFirst = false;
        continue;
      }

      curVal = tp.getValue();
      curTime = tp.getTimestamp();
      deltaVal = curVal - preVal;
      deltaTime = curTime - preTime;

      vList.add(deltaVal / deltaTime);
      preVal = curVal;
      preTime = curTime;
    }

    double preV = 0, curV, deltaV;

    isFirst = true;
    for (Double v : vList) {
      if (isFirst) {
        preV = v;
        isFirst = false;
        continue;
      }

      curV = v;
      deltaV = calcDisV(curV, preV);
      // in case there is a big gap between time points
      if (deltaV == Double.MAX_VALUE) {
        preV = curV;
        continue;
      }

      if (conMap.containsKey(deltaV)) {
        conMap.put(deltaV, conMap.get(deltaV) + 1);
      } else {
        conMap.put(deltaV, 1);
      }
      preV = curV;
    }

    return conMap;
  }

}

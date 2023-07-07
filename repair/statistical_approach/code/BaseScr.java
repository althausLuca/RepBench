package code;

import code.entity.TimePoint;
import code.entity.TimeSeries;
import code.util.Assist;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by Stoke on 2017/10/8.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class BaseScr {

  protected TimeSeries timeseries;
  protected ArrayList<TimePoint> tpList;
  protected double delta;
  protected double THETA;

  protected double RES;     // normalized to 1?
  protected double ORGRES;  // the original resolution
  protected int PARAM;
  protected HashMap<Double, Double> LAMBDA; // the lnProbability

  protected int sizeLBase;
  protected int[] sizeLs;
  protected double maxP;
  protected double minP;

  public BaseScr(TimeSeries timeseries, double theta, double delta) {
    setTimeSeries(timeseries);
    tpList = timeseries.getTimeseries();
    setTHETA(theta);
    setDelta(delta);
  }

  public void setTimeSeries(TimeSeries timeSeries) {
    this.timeseries = timeSeries;
  }

  public void setDelta(double delta) {
    this.delta = delta;
  }

  public void setTHETA(double THETA) {
    this.THETA = THETA;
  }

  public void normalizeParams(double RES, int PARAM) {
    this.ORGRES = RES;
    this.PARAM = PARAM;
    this.RES = RES * PARAM;

    normalizeTuples();
  }

  /**
   * normalize the values by PARAM
   * [val-THETA, val+THETA]
   */
  protected void normalizeTuples() {
    double value;
    double minVal = Double.MAX_VALUE;
    double maxVal = -Double.MAX_VALUE;

    for (TimePoint tp : tpList) {
      value = Math.round(tp.getValue() * PARAM);

      if (value > maxVal) {
        maxVal = value;
      }
      if (value < minVal) {
        minVal = value;
      }

      tp.setValue(value);
      tp.setModify(value);
    }

    // MIN and MAX
    for (TimePoint tp : tpList) {
      value = tp.getValue();
      tp.setRange(value - THETA, value + THETA);
    }
  }

  /**
   * normalize probability
   */
  public void normalizeProbability(Assist assist) {
    int size = tpList.size();

    LAMBDA = new HashMap<>();
    HashMap<Double, Integer> conMap;

    conMap = assist.convolution(timeseries);

    double[] maxMinP = assist.calcLnProbability(conMap, LAMBDA, size);
    maxP = maxMinP[0];
    minP = maxMinP[1];

    // based on weight, Algorithm 1
    sizeLBase = (int) Math.round(THETA / RES);  // the maximum cost for single tuple
    sizeLs = new int[tpList.size()];
    // allowed budget may be smaller than n * sizeLBase
    int budgetMax = (int) Math.ceil(delta / RES) + 1;
    int tmpSize;
    for (int i = 0; i < size; ++i) {
      tmpSize = sizeLBase * (i + 1) + 1;
      sizeLs[i] = tmpSize > budgetMax ? budgetMax : tmpSize;
    }
  }

  /**
   * calculate the likelihood of original timeseries
   *
   * @return likelihood
   */
  protected double calcIncumbent() {
    double valK, valP, valQ;
    double incumbent = 0, tmpPr;

    valQ = tpList.get(0).getValue();
    valP = tpList.get(1).getValue();
    long timeK, timeQ = tpList.get(0).getTimestamp(),
        timeP = tpList.get(1).getTimestamp();

    for (int i = 1; i < tpList.size() - 1; ++i) {
      valK = tpList.get(i + 1).getValue();
      timeK = tpList.get(i + 1).getTimestamp();

      tmpPr = getLikelihood(timeK, timeP, timeQ, valK, valP, valQ);
      // if one point has no likelihood, then return 1
      if (tmpPr > 0) {
        return 1;
      }
      incumbent += tmpPr;

      valQ = valP;
      valP = valK;
      timeQ = timeP;
      timeP = timeK;
    }

    return incumbent;
  }

  /**
   * get likelihood from learned V model
   * If no hit, then return 1
   */
  protected double getLikelihood(long timeK, long timeP, long timeQ,
      double valK, double valP, double valQ) {

    double vKP = (valK - valP) / (timeK - timeP);
    double vPQ = (valP - valQ) / (timeP - timeQ);

    double deltaV = Assist.calcDisV(vKP, vPQ);

    double likelihood = LAMBDA.containsKey(deltaV) ? LAMBDA.get(deltaV) : 1;
    return likelihood;
  }

  protected int getIndexW(double cost) {
    int index = (int) Math.round(cost / RES);

    return index;
  }

  /**
   * @return the max likelihood
   */
  protected double getTraceW(double[][][][] D, double[][][][] record) {
    int size = tpList.size();
    int targetK = -1, targetP = -1, targetW = 0;
    int theta = (int) Math.round(THETA * 2 / RES) + 1;

    double lambda = -Double.MAX_VALUE, tmpW;

    TimePoint tpK, tpP, tpQ;
    double valK, valP, valQ;

    tpK = tpList.get(size - 1);
    double minValk = tpK.getMinVal();

    // The probability should be below zero
    for (int k = 0; k < theta; ++k) {
      for (int p = 0; p < theta; ++p) {
        for (int w = 0; w < sizeLs[size - 1]; ++w) {
          if (D[0][p][k][w] < 0 && D[0][p][k][w] > lambda) {
            lambda = D[0][p][k][w];
            targetW = w;
            targetK = k;
            targetP = p;
          }
        }
      }
    }
    //    System.out.println("max likelihood = " + lambda);

    // find the trace and do the repair
    valK = minValk + targetK * RES;
    tpK.setModify(valK);
    if (size == 1) {
      return lambda;
    }

    tpP = tpList.get(size - 2);
    valP = tpP.getMinVal() + targetP * RES;
    tpP.setModify(valP);
    if (size == 2) {
      return lambda;
    }

    int j = size - 2;

    valQ = record[size - 1][targetP][targetK][targetW];

    // j >= 1
    while (j > 1) {
      tpQ = tpList.get(j - 1);
      tpQ.setModify(valQ);

      tmpW = Math.round(Math.abs(valK - tpK.getValue()));
      targetW -= getIndexW(tmpW);

      tpK = tpP;
      valK = valP;
      targetK = targetP;

      tpP = tpQ;
      valP = valQ;
      targetP = (int) Math.round((valP - tpP.getMinVal()) / RES);

      valQ = record[j][targetP][targetK][targetW];
      j = j - 1;
    }
    tpQ = tpList.get(0);
    tpQ.setModify(valQ);

    return lambda;
  }
}

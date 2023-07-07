package code;

import code.entity.TimePoint;
import code.entity.TimeSeries;
import code.util.Constants;
import java.util.ArrayList;

/**
 * Created by Stoke on 2017/10/8.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class DP extends BaseScr {

  public DP(TimeSeries timeseries, double THETA, double delta) {
    super(timeseries, THETA, delta);
  }

  /**
   *
   * @return timeseries after repair
   */
  public TimeSeries mainDP() {
    int size = tpList.size();
    int theta = (int) Math.round(THETA * 2) + 1;

    ArrayList<Integer> indexList = new ArrayList<>();
    for (int i = 0; i < theta; ++i) {
      indexList.add(i);
    }

    double[][][][] D = new double[2][theta][theta][];
    double[][][][] record = new double[size][theta][theta][];

    double minValk, minValp, minValq;
    double valK, valP, valQ;
    long timeK, timeP, timeQ;
    TimePoint tpK;

    double lambda, cost;
    double tmpL;
    // weight的index
    int indexW;

    // for middle store, save space
    for (int i = 0; i < 2; ++i) {
      D[i] = new double[theta][theta][sizeLs[size - 1]];
      initialize(D[i]);
    }

    // initial likelihood, lower bound
    double incumbent = calcIncumbent();
    if (incumbent == 1) {
      incumbent = -Double.MAX_VALUE;
    }

    // The first one, record[0] is null
    tpK = tpList.get(0);
    minValq = tpK.getMinVal();
    timeQ = tpK.getTimestamp();

    // The second one, record[1] is null
    tpK = tpList.get(1);
    minValp = tpK.getMinVal();
    timeP = tpK.getTimestamp();

    // initialize D(1), the first two points
    for (int p : indexList) {
      valP = minValp + RES * p;
      for (int q : indexList) {
        valQ = minValq + RES * q;

        cost = Math.abs(valP - tpList.get(1).getValue());
        cost += Math.abs(valQ - tpList.get(0).getValue());
        if (cost > delta)
          continue;

        indexW = getIndexW(cost);

        D[0][q][p][indexW] = 0;
      }
    }

    int startIndexW, targetIndexW;
    // others
    for (int i = 2; i < size; ++i) {
//      if (i % 100 == 0)
//        System.out.println(i);

      tpK = tpList.get(i);
      minValk = tpK.getMinVal();
      timeK = tpK.getTimestamp();
      record[i] = new double[theta][theta][sizeLs[i]];

      for (int k : indexList) {
        valK = minValk + RES * k;
        cost = Math.abs(valK - tpK.getValue());
        startIndexW = getIndexW(cost);

        for (int p : indexList) {
          valP = minValp + RES * p;

          for (int w = startIndexW; w < sizeLs[i]; w += 1) {
            // the former point
            targetIndexW = w - startIndexW;

            for (int q : indexList) {
              valQ = minValq + RES * q;

              if (D[0][q][p][targetIndexW] > 0)
                continue;

              // compute the likelihood for point P
              tmpL = getLikelihood(timeK, timeP, timeQ, valK, valP, valQ);
              if (tmpL > 0) {
                // continue;
                tmpL = Constants.ZEROP;
              }
              lambda = tmpL + D[0][q][p][targetIndexW];
              // prune
              if (lambda + (size - 1 - i) * Math.log(maxP) < incumbent)
                continue;

              if (D[1][p][k][w] > 0 || D[1][p][k][w] < lambda) {
                D[1][p][k][w] = lambda;
                record[i][p][k][w] = valQ;
              }
            }
          }
        }
      } // end of k

      for (int k = 0; k < theta; ++k) {
        for (int p = 0; p < theta; ++p) {
          for (int w = 0; w < sizeLs[i]; ++w) {
            D[0][p][k][w] = D[1][p][k][w];
          }
        }
      }
      initialize(D[1]);

      minValq = minValp;
      timeQ = timeP;

      minValp = minValk;
      timeP = timeK;
    }

    double targetLikelihood = getTraceW(D, record);
//    System.out.println("The final likelihood is " + targetLikelihood);

    // form resultSeries
    TimeSeries resultSeries = new TimeSeries();
    long timestamp;
    double modify;
    TimePoint tp;

    for (TimePoint timePoint : timeseries.getTimeseries()) {
      timestamp = timePoint.getTimestamp();
      modify = timePoint.getModify();
      tp = new TimePoint(timestamp, modify * ORGRES);
      resultSeries.addTimePoint(tp);
    }

    return resultSeries;
  }

  /**
   * initialize the likelihood vector
   *
   * @param D recurrence matrix
   */
  private void initialize(double[][][] D) {
    int dim1 = D.length;
    int dim2 = D[0].length;
    int dim3 = D[0][0].length;

    for (int i = 0; i < dim1; ++i) {
      for (int j = 0; j < dim2; ++j) {
        for (int k = 0; k < dim3; ++k) {
          D[i][j][k] = 1;
        }
      }
    }
  }

}

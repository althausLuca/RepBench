package code.entity;

import java.util.ArrayList;

/**
 * Created by Stoke on 2017/10/8.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class TimeSeries {

  private ArrayList<TimePoint> timeseries;

  public TimeSeries(ArrayList<TimePoint> timeseries) {
    setTimeseries(timeseries);
  }

  public TimeSeries() {
    setTimeseries(new ArrayList<TimePoint>());
  }

  public ArrayList<TimePoint> getTimeseries() {
    return timeseries;
  }

  public void setTimeseries(ArrayList<TimePoint> timeseries) {
    this.timeseries = timeseries;
  }

  public void addTimePoint(TimePoint tp) {
    this.timeseries.add(tp);
  }

  public int getLength() {
    return this.timeseries.size();
  }
}

package code.entity;

/**
 * Created by Stoke on 2017/10/8.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class TimePoint {

  private long timestamp;
  private double value; // the observe value
  private double modify; // modify is in [minVal, maxVal]

  private double minVal; // the minimum/maximum value of candidates
  private double maxVal;


  public TimePoint(long timestamp, double val) {
    setTimestamp(timestamp);

    setValue(val);
    setModify(val);

    setRange(-Double.MAX_VALUE, Double.MAX_VALUE);
  }

  public long getTimestamp() {
    return timestamp;
  }

  public void setTimestamp(long timestamp) {
    this.timestamp = timestamp;
  }

  public double getValue() {
    return value;
  }

  public void setValue(double observeval) {
    this.value = observeval;
  }

  public double getModify() {
    return modify;
  }

  public void setModify(double modify) {
    this.modify = modify;
  }

  public double getMinVal() {
    return this.minVal;
  }

  public double getMaxVal() {
    return this.maxVal;
  }

  public void setRange(double minVal, double maxVal) {
    this.minVal = minVal;
    this.maxVal = maxVal;
  }

}

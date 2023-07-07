package code.util;

/**
 * Created by Stoke on 2017/10/8.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class Constants {
  public static double EPSILON = 1.0e-5;

  // use this value to replace the probability of 0, since there is no ln
  public static double ZEROP = -10000;

  // Currently, it is from background knowledge
  // TODO: how to determine these values automatically
  public static double MINV = -101;
  public static double MAXV = 99;
  public static double INTERV = 1;

  public static double[] SPEEDPAT;
  public static double[] SPEEDOUT;
}

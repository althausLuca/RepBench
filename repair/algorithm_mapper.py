import repair as algs
import repair.algorithms_config as ac
import functools

algo_mapper = {
    ac.RPCA: algs.Robust_PCA_estimator,
    ac.SCREEN: algs.SCREENEstimator,
    ac.IMR: algs.IMR_estimator,
    ac.CDREP: algs.CDRecEstimator,
    ac.SPEEDandAcceleration: algs.SpeedAndAccelerationEstimator,
    ac.SCR: algs.SCREstimator,
}



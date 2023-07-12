import repair as algs
import repair.algorithms_config as ac

"""
Mapping of algorithm names to the actual estimator classes (used when ever we need to create an estimator object)
make sure to include the estimator in the repair.__init__.py file 
"""
algo_mapper = {
    ac.RPCA: algs.Robust_PCA_estimator,
    ac.SCREEN: algs.SCREENEstimator,
    ac.IMR: algs.IMR_estimator,
    ac.CDREP: algs.CDRecEstimator,
    ac.SPEEDandAcceleration: algs.SpeedAndAccelerationEstimator,
    ac.SCR: algs.SCREstimator,
    ac.KalmanFilter : algs.KalmanFilterEstimator,
}



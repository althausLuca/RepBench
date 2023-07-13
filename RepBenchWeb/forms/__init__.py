from RepBenchWeb.forms.alg_param_forms import SCREENparamForm, RPCAparamForm, CDparamForm, IMRparamField, \
    SpeedAndAccelerationField , SRCFForm , KalmanFilterFilterForm
from repair import algorithms_config as ac

ParamForms = {ac.SCREEN: SCREENparamForm(),
              ac.RPCA: RPCAparamForm(),
              ac.CDREP : CDparamForm(),
              ac.IMR : IMRparamField(),
              ac.SPEEDandAcceleration : SpeedAndAccelerationField(),
              ac.SCR : SRCFForm(),
              ac.KalmanFilter : KalmanFilterFilterForm()}



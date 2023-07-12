from RepBenchWeb.forms.alg_param_forms import SCREENparamForm, RPCAparamForm, CDparamForm, IMRparamField, \
    SpeedAndAccelerationField , SRCFForm , KalmanFilterFilterForm

ParamForms = {"SCREEN": SCREENparamForm(),
              "RPCA": RPCAparamForm(),
              "CDrec": CDparamForm(),
              "IMR": IMRparamField(),
              "SPEEDandAcceleration": SpeedAndAccelerationField(),
              "SCR" : SRCFForm(),
              "KFilter" : KalmanFilterFilterForm()}
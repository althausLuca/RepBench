from RepBenchWeb.forms.optimization_forms import BayesianOptForm, optimization_param_forms_inputs
from RepBenchWeb.models import InjectedContainer
from RepBenchWeb.views.config import OPTIMIZATION_TEMPLATE
from RepBenchWeb.views.dataset_views import DatasetView


class OptimizationView(DatasetView):
    template = OPTIMIZATION_TEMPLATE

    def create_opt_context(self, df):
        opt_context = {"bayesian_opt_form": BayesianOptForm(),
                       "b_opt_param_forms": optimization_param_forms_inputs(df),
                       # "injection_form": InjectionForm(list(df.columns))
                       }
        return opt_context

    def data_set_info_context(self, setname):
        injected_container = InjectedContainer.objects.get(title=setname)
        df = injected_container.df
        context = {"data_info": injected_container.get_info()}
        context.update(self.create_opt_context(df))
        return context


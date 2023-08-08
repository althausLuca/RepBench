from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from RepBenchWeb.views.recommendation import recommendation_view, file_upload_view , recommendation_example_view
from RepBenchWeb.views.optimization import optimizationview

from RepBenchWeb.views import (
    index_view,
    dataset_views,
    injection_view,
    datasets_display,
    data_upload_view,
)
from RepBenchWeb.views.repair import repair_view

from RepBenchWeb.views import dimensionality_reduction_view, synthetic_dataset_view, data_loader
from RepBenchWeb.views.recommendation.recommendation_tasks import FlamlTask, RayTuneTask
from RepBenchWeb.views.optimization.optimization_tasks import SuccesiveHalvingTask, BayesianOptimisationTask
from RepBenchWeb.views.repair.repair_comparison import RepairAndCompare
from RepBenchWeb.config import WEB_SIDE_NAME

app_name = WEB_SIDE_NAME

urlpatterns = [
    path('', index_view.index, name='index'),
    path(app_name, index_view.index, name='index'),
    path(app_name+'/', index_view.index, name='index'),
    path("about/", index_view.about, name='about'),

    path('display_datasets/', dataset_views.display_datasets, name='display_datasets'),
    path('display_datasets/<str:option>', dataset_views.display_datasets, name='display_datasets'),
    path('display_datasets/<str:option>/<str:synthetic>', dataset_views.display_datasets, name='display_datasets'),

    path('display_dataset/<str:setname>', dataset_views.DatasetView.as_view(), name='display_dataset'),
    path('display_dataset_synthetic/<str:setname>', synthetic_dataset_view.SyntheticDatasetView.as_view(),
         name='synthetic_dataset_view'),

    path('repairDatasets', repair_view.RepairView.repair_datasets, name='repair_datasets'),
    path('repairDataset/<str:type>', repair_view.RepairView.repair_datasets, name='repair_datasets'),

    ## repair view
    # path('repair', repair_view.RepairView.as_view(), name='repair'),
    path('repair/<str:setname>', repair_view.RepairView.as_view(), name='repair'),
    path('inject-compare', RepairAndCompare.as_view(), name='inject_and_compare'),

    path('injection/<str:setname>', injection_view.InjectionView.as_view(), name='injectAndRepair'),

    # store and inject data
    path('inject_data/<str:setname>', injection_view.inject_data, name='inject_data'),
    path('store_data/<str:setname>', injection_view.store_data, name='store_data'),

    ##  repair data
    path('repair_data/<str:setname>', repair_view.RepairView.repair_data, name='repair_data'),

    # optimization
    path('optimization_datasets',datasets_display.display_optimization_datasets,name="optimization_datasets"),
    path('opt', optimizationview.OptimizationView.as_view(), name="opt"),
    path('opt/<str:setname>', optimizationview.OptimizationView.as_view(), name="opt"),

    path('start_bayesian_opt', BayesianOptimisationTask.init_task, name='start_bayesian_opt'),
    path('start_succesive_halving', SuccesiveHalvingTask.init_task, name='start_successive_halving'),

    path('fetch_optresults', SuccesiveHalvingTask.fetch_data, name='fetch_optresults'),


    # alg inspection
    path('dim_reduction_datasets', dimensionality_reduction_view.display_dim_reduction_datasets, name="dim_reduction_datasets"),
    path('alg_inspection', dimensionality_reduction_view.DimensionalityReductionView.as_view(),
         name="dimensionality_reduction"),
    path('alg_inspection/<str:setname>', dimensionality_reduction_view.DimensionalityReductionView.as_view(),
         name="dimensionality_reduction"),
    path('alg_inspection_repair/<str:setname>', dimensionality_reduction_view.DimensionalityReductionView().repair_data,
         name="alg_inspection_repair"),

    # data getter
    path('get_data/<str:setname>', data_loader.get_data, name='get_data'),

    # catch22 sliders getter
    # path('sliders_view/<str:setname>', dataset_views.sliders_view, name='get_catch22_data'),





    ## recommendation
    path('recommendation_datasets', recommendation_view.RecommendationView().recommendation_datasets,
         name='recommendation_datasets'),
    path('recommendation/<str:type>', recommendation_view.RecommendationView.as_view(), name='recommendation'),



    path('flaml_example',FlamlTask.init_task, name='start_flaml'),
    path('raytunes_example',RayTuneTask.init_task, name='start_raytunes'),

    path('recommendation_retrieve', FlamlTask.fetch_data,name='retrieve_recommendation_results'),
    path('get_recommendation/<str:setname>' , recommendation_example_view.flaml_prediction , name='get_recommendation'),




    #delete dataset
    path('delete/<str:setname>', dataset_views.delete_dataset, name='delete_dataset'),

    #save dataset
    path('userData/', file_upload_view.upload_files, name='upload_files'),
    path('upload', data_upload_view.UploadView.as_view(), name='upload'),
]



urlpatterns += [
                   # path('RepBenchWeb/', include("RepBenchWeb.urls")),
                   path('admin/', admin.site.urls),
                   # path('', RedirectView.as_view(url='/RepBenchWeb/', permanent=True)),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

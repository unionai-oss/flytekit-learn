from tests.integration.bentoml_integration.digits_classifier_app import service

service.load_model("latest")
service.configure(
    enable_async=True,
    supported_resources=("cpu",),
    supports_cpu_multi_threading=False,
    runnable_method_kwargs={"batchable": False},
)

from . import ECSService


def destroy_workers(
    number_of_workers: int = 0,
    ecs_cluster_name: str = None
):
    # list number of workers
    esc_service = ECSService(
        ecs_cluster_name=ecs_cluster_name
    )
    list_of_ecs_services = esc_service.list()
    print("destroy workers")
    return

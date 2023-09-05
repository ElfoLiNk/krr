from robusta_krr.core.models.objects import K8sObjectData

from .base import BatchedRequestMixin, FilterJobsMixin, QueryMetric, QueryRangeMetric


class MemoryLoader(QueryRangeMetric, FilterJobsMixin, BatchedRequestMixin):
    def get_query(self, object: K8sObjectData, duration: str, step: str) -> str:
        pods_selector = "|".join(pod.name for pod in object.pods)
        cluster_label = self.get_prometheus_cluster_label()
        return f"""
            max(
                container_memory_working_set_bytes{{
                    namespace="{object.namespace}",
                    pod=~"{pods_selector}",
                    container="{object.container}"
                    {cluster_label}
                }}
            ) by (container, pod, job)
        """


class MaxMemoryLoader(QueryMetric, FilterJobsMixin, BatchedRequestMixin):
    def get_query(self, object: K8sObjectData, duration: str, step: str) -> str:
        pods_selector = "|".join(pod.name for pod in object.pods)
        cluster_label = self.get_prometheus_cluster_label()
        return f"""
            max_over_time(
                max(
                    container_memory_working_set_bytes{{
                        namespace="{object.namespace}",
                        pod=~"{pods_selector}",
                        container="{object.container}"
                        {cluster_label}
                    }}
                ) by (container, pod, job)
                [{duration}:{step}]
            )
        """


class MemoryAmountLoader(QueryMetric, FilterJobsMixin, BatchedRequestMixin):
    def get_query(self, object: K8sObjectData, duration: str, step: str) -> str:
        pods_selector = "|".join(pod.name for pod in object.pods)
        cluster_label = self.get_prometheus_cluster_label()
        return f"""
            count_over_time(
                max(
                    container_memory_working_set_bytes{{
                        namespace="{object.namespace}",
                        pod=~"{pods_selector}",
                        container="{object.container}"
                        {cluster_label}
                    }}
                ) by (container, pod, job)
                [{duration}:{step}]
            )
        """

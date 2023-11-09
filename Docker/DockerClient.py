import docker

class DockerClient:
    """Encapsulates common Docker operations"""
    
    client = docker.from_env()

    @staticmethod
    def ensure_image(image_name: str):
        if not any([img for img in DockerClient.client.images.list() if image_name in img.tags]):
            DockerClient.client.images.pull(image_name)

    @staticmethod
    def remove_container(container):
        if container:
            container.remove()

    @staticmethod
    def execute_in_container(image_name: str, command: str) -> (int, str):
        container = None
        try:
            container = DockerClient.client.containers.create(
                image=image_name,
                command=command,
                detach=True
            )

            container.start()
            result = container.wait()
            exit_code = result['StatusCode']

            if exit_code == 0:
                return exit_code, container.logs(stdout=True, stderr=False).decode('utf-8').strip()
            else:
                return exit_code, container.logs(stdout=False, stderr=True).decode('utf-8').strip()

        finally:
            DockerClient.remove_container(container)

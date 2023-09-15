import docker
from Functionary.PromptEngineering import prompts
from Functionary.Generation.Completions import get_gpt4_completion




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


class DockerFunctions:
    def __init__(self, language="python"):
        self.image_name = f"{language}:latest"

    def install_packages(self, install_cmd: str):
        DockerClient.ensure_image(self.image_name)

        container = None
        try:
            container = DockerClient.client.containers.create(
                image=self.image_name,
                command=install_cmd,
                detach=True
            )

            container.start()
            container.wait()

            self.image_name = f"{self.image_name}_with_packages"
            container.commit(repository=self.image_name)

        except Exception as e:
            print(f"Failed to install packages. Error: {str(e)}")

        finally:
            DockerClient.remove_container(container)

    def run_code_in_docker(self, code: str) -> dict:
        DockerClient.ensure_image(self.image_name)

        command = self._get_execution_command(code)

        try:
            exit_code, output = DockerClient.execute_in_container(self.image_name, command)

            if exit_code == 0:
                return {
                    "code": code,
                    "info": output if output else "No output produced.",
                    "status": "success"
                }
            else:
                return {
                    "code": code,
                    "info": output,
                    "status": "failure"
                }
        except Exception as e:
            return {
                "code": code,
                "info": str(e),
                "status": "failure"
            }

    def _get_execution_command(self, code: str) -> str:
        # You can add more logic here or replace with another function to determine the command
        return get_gpt4_completion(prompts.execution_command(code))


if __name__ == "__main__":
    # Example of using it for Python
    docker_func = DockerFunctions(language="python")
    docker_func.install_packages("pip install requests")
    result = docker_func.run_code_in_docker("import requests; print(requests.__version__)")
    print(result)

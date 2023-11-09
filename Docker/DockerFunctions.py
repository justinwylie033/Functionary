from Generation.Generate import Generate
from Docker.DockerClient import DockerClient
from Utils.utils import Utils


class DockerFunctions:
    def __init__(self, language="python"):
        self.image_name = f"{language}:latest"
        self.generation = Generate()

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
        if not command:
            return {
                "code": code,
                "info": "No command generated to execute the code.",
                "status": "failure"
            }

        print(f"Command to be executed: {command}")

        container = None
        try:
            container = DockerClient.client.containers.run(
                image=self.image_name,
                command=command,
                detach=True,
                stderr=True
            )
            exit_code = container.wait()['StatusCode']
            print(f"Exit code: {exit_code}")
            output = container.logs(stdout=True, stderr=True).decode('utf-8')

            if exit_code == 0:
                return {
                    "code": code,
                    "info": output,
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
        finally:
            if container:
                DockerClient.remove_container(container)



    def _get_execution_command(self, code: str) -> str:
        # You can add more logic here or replace with another function to determine the command
        return Utils.code_extractor(self.generation.generate_execution_commmand(code))


if __name__ == "__main__":
    # Example of using it for Python
    docker_func = DockerFunctions(language="python")
    docker_func.install_packages("pip install requests")
    result = docker_func.run_code_in_docker("import requests; print(requests.get('https://www.google.com'))")
    print(result)

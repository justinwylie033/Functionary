import docker

class DockerFunctions:
    client = docker.from_env()
    
    # Initialize with a default language, e.g., Python
    def __init__(self, language="python"):
        self.image_name = f"{language}:latest"
    
    def ensure_image(self):
        if not any([img for img in self.client.images.list() if self.image_name in img.tags]):
            self.client.images.pull(self.image_name)

    def install_packages(self, install_cmd: str):
        self.ensure_image()

        container = None

        try:
            container = self.client.containers.create(
                image=self.image_name,
                command=install_cmd,
                detach=True
            )

            container.start()
            container.wait()

            new_image_name = f"{self.image_name}_with_packages"
            new_image = container.commit(repository=new_image_name)

            self.image_name = new_image_name

        except Exception as e:
            print(f"Failed to install packages. Error: {str(e)}")

        finally:
            if container:
                container.remove()

    def run_code_in_docker(self, code: str, command_format: str) -> dict:
        self.ensure_image()

        try:
            command = command_format.format(code.replace('"', '\\"'))

            container = self.client.containers.create(
                image=self.image_name,
                command=command,
                detach=True
            )

            container.start()
            result = container.wait()
            exit_code = result['StatusCode']

            if exit_code == 0:
                output = container.logs(stdout=True, stderr=False).decode('utf-8').strip()
                return {
                    "code": code,
                    "info": output if output else "No output produced.",
                    "status": "success"
                }
            else:
                error = container.logs(stdout=False, stderr=True).decode('utf-8').strip()
                return {
                    "code": code,
                    "info": error,
                    "status": "failure"
                }
        except Exception as e:
            return {
                "code": code,
                "info": str(e),
                "status": "failure"
            }
        finally:
            if 'container' in locals():
                container.remove()

if __name__ == "__main__":
    # Example of using it for Python
    docker_func = DockerFunctions(language="python")
    docker_func.install_packages("pip install requests")
    result = docker_func.run_code_in_docker("import requests; print(requests.__version__)", command_format='python -c "{}"')
    print(result)

import docker

class DockerFunctions:
    client = docker.from_env()
    image_name = "python:latest"

    @staticmethod
    def ensure_image():
        if not any([img for img in DockerFunctions.client.images.list() if DockerFunctions.image_name in img.tags]):
            DockerFunctions.client.images.pull(DockerFunctions.image_name)

    @staticmethod
    def install_packages(install_cmd: str):
        DockerFunctions.ensure_image()

        container = None

        try:
            container = DockerFunctions.client.containers.create(
                image=DockerFunctions.image_name,
                command=install_cmd,
                detach=True
            )

            container.start()
            container.wait()

            new_image_name = f"{DockerFunctions.image_name}_with_packages"
            new_image = container.commit(repository=new_image_name)

            DockerFunctions.image_name = new_image_name

        except Exception as e:
            print(f"Failed to install packages. Error: {str(e)}")

        finally:
            if container:
                container.remove()

    @staticmethod
    def run_python_in_docker(python_code: str) -> dict:
        DockerFunctions.ensure_image()

        try:
            command = 'python -c "{}"'.format(python_code.replace('"', '\\"'))

            container = DockerFunctions.client.containers.create(
                image=DockerFunctions.image_name,
                command=command,
                detach=True
            )

            container.start()
            result = container.wait()
            exit_code = result['StatusCode']

            if exit_code == 0:
                output = container.logs(stdout=True, stderr=False).decode('utf-8').strip()
                return {
                    "code": python_code,
                    "info": output if output else "No output produced.",
                    "status": "success"
                }
            else:
                error = container.logs(stdout=False, stderr=True).decode('utf-8').strip()
                return {
                    "code": python_code,
                    "info": error,
                    "status": "failure"
                }
        except Exception as e:
            return {
                "code": python_code,
                "info": str(e),
                "status": "failure"
            }
        finally:
            if 'container' in locals():
                container.remove()

if __name__ == "__main__":
    # Install required packages
    DockerFunctions.install_packages("pip install requests")

    # Test the method with a Python code snippet
    python_code = "import requests; print(requests.__version__)"
    result = DockerFunctions.run_python_in_docker(python_code)
    print(result)

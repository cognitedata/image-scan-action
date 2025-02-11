# OCI image scanner action

GitHub action for scanning OCI container images and uploading the results to GitHub Advanced Security. The action wraps the [Trivy action](https://github.com/aquasecurity/trivy-action) for scanning images and the [CodeQL action](https://github.com/github/codeql-action/blob/main/upload-sarif/action.yml) for uploading the SARIF result to the GitHub repository security tab. A python script is used to tailor how GHAS will categorize the findings. The action is tested on GitHub Ubuntu runners.

------------

## Usage

### Inputs

| Name           | Required | Default value                 |
|----------------|----------|-------------------------------|
| image          | `true`   |                               |
| exit-code      | `true`   | `1`                           |
| vuln-type      | `true`   | `os`                          |
| severity       | `true`   | `LOW,MEDIUM,HIGH,CRITICAL`    |
| trivy-output   | `true`   | `trivy-results.sarif`         |
| trivyignores   | `false`  |                               |
| python-version | `true`   | `3.12`                        |

### Scanning an image

The image input requires a fully qualified image name (FQIN). This means that it must include both the image repository and the tag. Here are two examples of the fully qualified image name of the DockerHub hello-world image:

- `docker.io/library/hello-world:latest`
- `docker.io/library/hello-world@sha256:d7...07`

```yaml
on:
  push:
    branches:
      - main
  pull_request:

jobs:
  image-scan:
    runs-on: ubuntu-latest
    name: Scan container image
    steps:
      - uses: actions/checkout@v4
      - uses: cognitedata/image-scan-action@v1
        with:
          image: <fully_qualified_image_name>
```

You can reference an image you have built in a previous step or from a remote registry. You will have to provide credentials for private registries. Refer to the Trivy action documentation for details.  For descriptions of the other possible inputs, refer to the inputs section in `action.yml`.

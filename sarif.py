import json
import sys
from typing import Any, Dict


def get_image_repository(image_full_name: str) -> str:
    return image_full_name.split("@")[0].split(":")[0]


def get_image_registry(image_full_name: str) -> str:
    registy = image_full_name.split("/")[0]

    if "." not in registy:
        raise ValueError(f"Registry not found in image name: {image_full_name}")

    return registy


def prepare_sarif(sarif: Dict[str, Any], image_name: str) -> Dict[str, Any]:
    """Prepare SARIF file for upload to GHAS.

    Set automationDetail.id to the desired category. We use the image
    repository as the category.

    Prefix all artifactLocation.uri fields with the registry URI. This will
    make GitHub show the absolute path to the artifact.

    Remove originalUriBaseIds and all artifactLocation.uriBaseId because we are
    making the artifactLocation.uri absolute.

    Args:
        sarif (Dict[str, Any]): The parsed SARIF data.
        image_name (str): Name of the image that was scanned.

    Returns:
        Dict[str, Any]: The modified SARIF data.
    """

    category = get_image_repository(image_full_name=image_name)
    registry = get_image_registry(image_full_name=image_name)

    for run in sarif["runs"]:
        # Set the automation details field to the category we want.
        run["automationDetails"] = {"id": f"{category}/"}
        # Remove the original uri base ids
        run.pop("originalUriBaseIds", None)

        for result in run["results"]:
            for location in result["locations"]:
                # Prefix the registry to the artifact location
                artifact_uri = location["physicalLocation"]["artifactLocation"]["uri"]
                location["physicalLocation"]["artifactLocation"]["uri"] = f"{registry}/{artifact_uri}"

                # Remove the uri base id
                location["physicalLocation"]["artifactLocation"].pop("uriBaseId", None)

    return sarif


if __name__ == "__main__":
    with open(sys.argv[2], "r+") as fp:
        sarif = prepare_sarif(sarif=json.load(fp), image_name=sys.argv[1])

        fp.seek(0)
        json.dump(obj=sarif, fp=fp)
        fp.truncate()

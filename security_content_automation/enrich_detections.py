import base64
import csv
import io
import json
import logging
import os
import shutil
import sys
import time
from pathlib import Path

import git
import yaml
from github import Github

TIMESTAMP_FORMAT = "%(asctime)s %(levelname)s - %(message)s"


def fetch_ta_cim_mapping_report(file_name):
    try:
        with open(file_name) as file_content:
            cim_field_report = json.load(file_content)
            return cim_field_report
    except Exception as error:
        error_message = f"Unexpected error occurred while reading file. {error}"
        logging.error(error_message)


def load_file(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as stream:
            file = list(yaml.safe_load_all(stream))[0]
            return file
    except yaml.YAMLError as exc:
        sys.exit("ERROR: reading {0}".format(file_path))


def map_required_fields(cim_summary, datamodel, required_fields):
    datasets_fields = {}
    add_addon = False
    time_fields = ["_time", "_times"]
    if len(required_fields) > 0:
        for required_field in required_fields:
            dataset_field = required_field.split(".")
            length = len(dataset_field)

            if length == 1 and required_field in time_fields:
                continue

            elif length == 2:
                detection_datamodel = datamodel[0]
                detection_dataset, detection_field = dataset_field

            elif length == 3:
                detection_datamodel, detection_dataset, detection_field = dataset_field

            else:
                with open("unsupported_fields.txt", "a") as file_obj:
                    file_obj.write(str(required_field))
                    file_obj.write("\n")
                    continue

            datamodel_dataset = f"{detection_datamodel}:{detection_dataset}"
            if not datasets_fields.get(datamodel_dataset):
                datasets_fields[datamodel_dataset] = list()

            datasets_fields[datamodel_dataset].append(detection_field)

        for mapping_set, fields in datasets_fields.items():
            if mapping_set in cim_summary.keys():
                for fields_list in cim_summary[mapping_set].values():
                    for field_set in fields_list:
                        if set(fields).issubset(set(field_set.get("fields", []))):
                            add_addon = True

            if not add_addon:
                return False

        return add_addon


def is_valid_detection_file(filepath):

    detection_analytic_type = ["ttp", "anomaly"]
    detection_with_valid_analytic_type = False
    detection_with_valid_datamodel = False
    detection_file_path = load_file(filepath)

    if detection_file_path.get("type", "").lower() in detection_analytic_type:
        detection_with_valid_analytic_type = True

    if detection_file_path.get("datamodel", []):
        detection_with_valid_datamodel = True

    return detection_with_valid_analytic_type & detection_with_valid_datamodel


def enrich_detection_file(file, ta_list, keyname):
    detection_obj = load_file(file)
    detection_obj["tags"][keyname] = ta_list

    with open(file, "w") as f:
        yaml.dump(detection_obj, f, sort_keys=False, allow_unicode=True)


def main():

    security_content_repo = "splunk/security_content"
    security_content_branch = "FixDatamodelFormat"

    ta_cim_field_reports_repo = "splunk/ta-cim-field-reports"
    ta_cim_field_reports_branch = "test/custom-ms-sysmon-report"

    # Decodin GITHUB_ACCESS_TOKEN from base64
    git_token_base64_bytes = os.environ.get("GITHUB_ACCESS_TOKEN").encode("ascii")
    git_token_bytes = base64.b64decode(git_token_base64_bytes)
    github_token = git_token_bytes.decode("ascii")

    git_token = Github(github_token)
    detection_types = ["cloud", "endpoint", "network"]
    cim_report_path = (
        "ta_cim_mapping_reports/ta_cim_mapping/cim_mapping_reports/latest/"
    )
    detection_ta_mapping = {}

    try:
        # clone security content repository
        security_content_repo_obj = git.Repo.clone_from(
            "https://"
            + github_token
            + ":x-oauth-basic@github.com/"
            + security_content_repo,
            "security_content",
            branch=security_content_branch,
        )
        message = "Successfully cloned security_content."
        logging.info(message)
    except Exception as error:
        error_message = (
            f"Unexpected error occurred while Cloning security_content, {error}"
        )
        logging.error(error_message)

    try:
        # clone ta cim field reports repository
        ta_cim_field_reports_obj = git.Repo.clone_from(
            "https://"
            + github_token
            + ":x-oauth-basic@github.com/"
            + ta_cim_field_reports_repo,
            "ta_cim_mapping_reports",
            branch=ta_cim_field_reports_branch,
        )
        message = "Successfully cloned ta_cim_mapping_reports."
        logging.info(message)
    except Exception as error:
        error_message = f"Unexpected error occurred while Cloning ta-cim-field-reports repo, {error}"
        logging.error(error_message)

    # iterate for every detection types

    for detection_type in detection_types:

        for subdir, _, files in os.walk(f"security_content/tests/{detection_type}"):

            for file in files:
                filepath = subdir + os.sep + file
                tas_with_cim_mapping_list = []
                supported_tas_list = []
                detection_obj = load_file(filepath)
                source_types = []
                for data in detection_obj.get("tests")[0].get("attack_data"):
                    source_types.append(data.get("sourcetype"))

                detection_file_name_path = (
                    detection_obj.get("tests")[0].get("file").rsplit("/", 1)[1]
                )
                detection_file_name = Path(detection_file_name_path).stem
                filepath = "security_content/detections/" + detection_obj.get("tests")[
                    0
                ].get("file")
                if not os.path.isfile(filepath):
                    continue

                if is_valid_detection_file(filepath):
                    for ta_cim_mapping_file in os.listdir(cim_report_path):
                        ta_cim_map = fetch_ta_cim_mapping_report(
                            cim_report_path + ta_cim_mapping_file
                        )

                        detection_obj = load_file(filepath)
                        required_fields = detection_obj.get("tags", {}).get(
                            "required_fields"
                        )
                        datamodel = detection_obj.get("datamodel", [])
                        result = map_required_fields(
                            ta_cim_map["cimsummary"], datamodel, required_fields
                        )
                        cim_version = ta_cim_map["cim_version"]

                        if result:
                            tas_with_cim_mapping_list.append(
                                ta_cim_map.get("ta_name").get("name")
                            )
                            ta_sourcetype = ta_cim_map["sourcetypes"]
                            for source_type in source_types:

                                if (
                                    source_type in ta_sourcetype
                                    and ta_cim_map.get("ta_name").get("name")
                                    not in supported_tas_list
                                ):
                                    supported_tas_list.append(
                                        ta_cim_map.get("ta_name").get("name")
                                    )
                            detection_ta_mapping[detection_file_name] = {}

                    if tas_with_cim_mapping_list:
                        keyname = "tas_with_cim_mapping"
                        detection_ta_mapping[detection_file_name][
                            "cim_version"
                        ] = cim_version
                        detection_ta_mapping[detection_file_name][
                            keyname
                        ] = tas_with_cim_mapping_list

                    if supported_tas_list:
                        keyname = "supported_tas"
                        enrich_detection_file(filepath, supported_tas_list, keyname)
                        detection_ta_mapping[detection_file_name][
                            keyname
                        ] = supported_tas_list

                        logging.info(
                            f"Enriched {detection_file_name} with supported TAs : {supported_tas_list}"
                        )

                    security_content_repo_obj.index.add(
                        [filepath.strip("security_content/")]
                    )

    # Generating detection_ta_mapping yml file
    try:
        with io.open(
            r"./security_content/security_content_automation/detection_ta_mapping.yml",
            "w",
            encoding="utf8",
        ) as outfile:
            yaml.safe_dump(
                detection_ta_mapping,
                outfile,
                default_flow_style=False,
                allow_unicode=True,
            )

        security_content_repo_obj.index.add(
            ["security_content_automation/detection_ta_mapping.yml"]
        )
        message = "Created detection_ta_mapping.yml file"
        logging.info(message)

    except Exception as error:
        error_message = f"Unexpected error occurred while generating detection_ta_mapping.yml file, {error}"
        logging.error(error_message)

    # Generating detection_ta_mapping CSV report
    try:
        with open(
            r"./security_content/security_content_automation/detection_ta_mapping.csv",
            "w+",
            newline="",
        ) as csv_file:
            fieldnames = [
                "detection_name",
                "cim_version",
                "supported_tas",
                "tas_with_cim_mapping",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for detection_name, detection_content in detection_ta_mapping.items():
                detection_content.update(
                    {
                        "tas_with_cim_mapping": ", ".join(
                            detection_content["tas_with_cim_mapping"]
                        )
                        if detection_content.get("tas_with_cim_mapping")
                        else "",
                        "supported_tas": ", ".join(detection_content["supported_tas"])
                        if detection_content.get("supported_tas")
                        else "",
                        "detection_name": detection_name,
                    }
                )
                writer.writerow(detection_content)
        security_content_repo_obj.index.add(
            ["security_content_automation/detection_ta_mapping.csv"]
        )
        message = "Created detection_ta_mapping.csv file"
        logging.info(message)

    except Exception as error:
        error_message = f"Unexpected error occurred while generating detection_ta_mapping CSV report, {error}"
        logging.error(error_message)

    try:
        security_content_repo_obj.index.commit(
            "Updated detection files with recommended TA list."
        )

        epoch_time = str(int(time.time()))
        branch_name = f"enrich_detection_{security_content_branch}"
        security_content_repo_obj.git.checkout("-b", branch_name)
        security_content_repo_obj.git.push("--set-upstream", "origin", branch_name)
        repo = git_token.get_repo("splunk/security_content")

        # pr = repo.create_pull(
        #     title="Enrich Detection PR " + branch_name,
        #     body="Enriched the detections with supported TAs",
        #     head=branch_name,
        #     base="develop",
        # )
        # message = "Created pull request"
        # logging.info(message)
    except Exception as error:
        error_message = (
            f"Unexpected error occurred while creating pull request, {error}"
        )
        logging.error(error_message)

    try:
        shutil.rmtree("./security_content")
        shutil.rmtree("./ta_cim_mapping_reports")
        message = "Cleaned up the environment"
        logging.info(message)
    except OSError as e:
        error_message = f"Unexpected error occurred while deleting files, {error}"
        logging.error(error_message)


if __name__ == "__main__":
    log_level = logging.INFO
    handlers = [logging.StreamHandler()]
    logging.basicConfig(level=log_level, format=TIMESTAMP_FORMAT, handlers=handlers)
    main()

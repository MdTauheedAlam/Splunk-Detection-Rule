---
title: "Windows Log Manipulation"
last_modified_at: 2017-09-12
toc: true
toc_label: ""
tags:
  - Splunk Enterprise
  - Splunk Enterprise Security
  - Splunk Cloud
  - Endpoint
  - Actions on Objectives
---

[Try in Splunk Security Cloud](https://www.splunk.com/en_us/cyber-security.html){: .btn .btn--success}

#### Description

Adversaries often try to cover their tracks by manipulating Windows logs. Use these searches to help you monitor for suspicious activity surrounding log files--an essential component of an effective defense.

- **Product**: Splunk Enterprise, Splunk Enterprise Security, Splunk Cloud
- **Datamodel**: [Endpoint](https://docs.splunk.com/Documentation/CIM/latest/User/Endpoint)
- **Last Updated**: 2017-09-12
- **Author**: Rico Valdez, Splunk
- **ID**: b6db2c60-a281-48b4-95f1-2cd99ed56835

#### Narrative

Because attackers often modify system logs to cover their tracks and/or to thwart the investigative process, log monitoring is an industry-recognized best practice. While there are legitimate reasons to manipulate system logs, it is still worthwhile to keep track of who manipulated the logs, when they manipulated them, and in what way they manipulated them (determining which accesses, tools, or utilities were employed). Even if no malicious activity is detected, the knowledge of an attempt to manipulate system logs may be indicative of a broader security risk that should be thoroughly investigated.\
The Analytic Story gives users two different ways to detect manipulation of Windows Event Logs and one way to detect deletion of the Update Sequence Number (USN) Change Journal. The story helps determine the history of the host and the users who have accessed it. Finally, the story aides in investigation by retrieving all the information on the process that caused these events (if the process has been identified).

#### Detections

| Name        | Technique   | Type         |
| ----------- | ----------- |--------------|
| [Deleting Shadow Copies](/endpoint/deleting_shadow_copies/) | None| TTP |
| [Suspicious Event Log Service Behavior](/endpoint/suspicious_event_log_service_behavior/) | None| TTP |
| [Suspicious wevtutil Usage](/endpoint/suspicious_wevtutil_usage/) | None| TTP |
| [USN Journal Deletion](/endpoint/usn_journal_deletion/) | None| TTP |
| [Windows Event Log Cleared](/endpoint/windows_event_log_cleared/) | None| TTP |

#### Reference

* [https://www.crowdstrike.com/blog/bears-midst-intrusion-democratic-national-committee/](https://www.crowdstrike.com/blog/bears-midst-intrusion-democratic-national-committee/)
* [https://zeltser.com/security-incident-log-review-checklist/](https://zeltser.com/security-incident-log-review-checklist/)
* [http://journeyintoir.blogspot.com/2013/01/re-introducing-usnjrnl.html](http://journeyintoir.blogspot.com/2013/01/re-introducing-usnjrnl.html)



[*source*](https://github.com/splunk/security_content/tree/develop/stories/windows_log_manipulation.yml) \| *version*: **2**
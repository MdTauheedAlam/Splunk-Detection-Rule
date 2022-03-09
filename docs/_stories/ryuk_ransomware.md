---
title: "Ryuk Ransomware"
last_modified_at: 2020-11-06
toc: true
toc_label: ""
tags:
  - Splunk Enterprise
  - Splunk Enterprise Security
  - Splunk Cloud
  - Endpoint
  - Network_Traffic
  - Actions on Objectives
  - Delivery
  - Exploitation
  - Reconnaissance
---

[Try in Splunk Security Cloud](https://www.splunk.com/en_us/cyber-security.html){: .btn .btn--success}

#### Description

Leverage searches that allow you to detect and investigate unusual activities that might relate to the Ryuk ransomware, including looking for file writes associated with Ryuk, Stopping Security Access Manager, DisableAntiSpyware registry key modification, suspicious psexec use, and more.

- **Product**: Splunk Enterprise, Splunk Enterprise Security, Splunk Cloud
- **Datamodel**: [Endpoint](https://docs.splunk.com/Documentation/CIM/latest/User/Endpoint), [Network_Traffic](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkTraffic)
- **Last Updated**: 2020-11-06
- **Author**: Jose Hernandez, Splunk
- **ID**: 507edc74-13d5-4339-878e-b9744ded1f35

#### Narrative

Cybersecurity Infrastructure Security Agency (CISA) released Alert (AA20-302A) on October 28th called Ransomware Activity Targeting the Healthcare and Public Health Sector. This alert details TTPs associated with ongoing and possible imminent attacks against the Healthcare sector, and is a joint advisory in coordination with other U.S. Government agencies. The objective of these malicious campaigns is to infiltrate targets in named sectors and to drop ransomware payloads, which will likely cause disruption of service and increase risk of actual harm to the health and safety of patients at hospitals, even with the aggravant of an ongoing COVID-19 pandemic. This document specifically refers to several crimeware exploitation frameworks, emphasizing the use of Ryuk ransomware as payload. The Ryuk ransomware payload is not new. It has been well documented and identified in multiple variants. Payloads need a carrier, and for Ryuk it has often been exploitation frameworks such as Cobalt Strike, or popular crimeware frameworks such as Emotet or Trickbot.

#### Detections

| Name        | Technique   | Type         |
| ----------- | ----------- |--------------|
| [Windows connhost exe started forcefully](/deprecated/windows_connhost_exe_started_forcefully/) | None| TTP |
| [BCDEdit Failure Recovery Modification](/endpoint/bcdedit_failure_recovery_modification/) | None| TTP |
| [Common Ransomware Extensions](/endpoint/common_ransomware_extensions/) | None| Hunting |
| [Common Ransomware Notes](/endpoint/common_ransomware_notes/) | None| Hunting |
| [NLTest Domain Trust Discovery](/endpoint/nltest_domain_trust_discovery/) | None| TTP |
| [Ryuk Test Files Detected](/endpoint/ryuk_test_files_detected/) | None| TTP |
| [Ryuk Wake on LAN Command](/endpoint/ryuk_wake_on_lan_command/) | None| TTP |
| [Suspicious Scheduled Task from Public Directory](/endpoint/suspicious_scheduled_task_from_public_directory/) | None| Anomaly |
| [WBAdmin Delete System Backups](/endpoint/wbadmin_delete_system_backups/) | None| TTP |
| [Windows DisableAntiSpyware Registry](/endpoint/windows_disableantispyware_registry/) | None| TTP |
| [Windows Security Account Manager Stopped](/endpoint/windows_security_account_manager_stopped/) | None| TTP |
| [WinEvent Scheduled Task Created to Spawn Shell](/endpoint/winevent_scheduled_task_created_to_spawn_shell/) | None| TTP |
| [WinEvent Scheduled Task Created Within Public Path](/endpoint/winevent_scheduled_task_created_within_public_path/) | None| TTP |
| [Spike in File Writes](/endpoint/spike_in_file_writes/) | None| Anomaly |
| [Remote Desktop Network Bruteforce](/network/remote_desktop_network_bruteforce/) | None| TTP |
| [Remote Desktop Network Traffic](/network/remote_desktop_network_traffic/) | None| Anomaly |

#### Reference

* [https://www.splunk.com/en_us/blog/security/detecting-ryuk-using-splunk-attack-range.html](https://www.splunk.com/en_us/blog/security/detecting-ryuk-using-splunk-attack-range.html)
* [https://www.crowdstrike.com/blog/big-game-hunting-with-ryuk-another-lucrative-targeted-ransomware/](https://www.crowdstrike.com/blog/big-game-hunting-with-ryuk-another-lucrative-targeted-ransomware/)
* [https://us-cert.cisa.gov/ncas/alerts/aa20-302a](https://us-cert.cisa.gov/ncas/alerts/aa20-302a)



[*source*](https://github.com/splunk/security_content/tree/develop/stories/ryuk_ransomware.yml) \| *version*: **1**
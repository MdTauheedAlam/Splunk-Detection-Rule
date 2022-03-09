---
title: "IcedID"
last_modified_at: 2021-07-29
toc: true
toc_label: ""
tags:
  - Splunk Enterprise
  - Splunk Enterprise Security
  - Splunk Cloud
  - Endpoint
  - Actions on Objectives
  - Exploitation
  - Reconnaissance
---

[Try in Splunk Security Cloud](https://www.splunk.com/en_us/cyber-security.html){: .btn .btn--success}

#### Description

Leverage searches that allow you to detect and investigate unusual activities that might relate to the IcedID banking trojan, including looking for file writes associated with its payload, process injection, shellcode execution and data collection.

- **Product**: Splunk Enterprise, Splunk Enterprise Security, Splunk Cloud
- **Datamodel**: [Endpoint](https://docs.splunk.com/Documentation/CIM/latest/User/Endpoint)
- **Last Updated**: 2021-07-29
- **Author**: Teoderick Contreras, Splunk
- **ID**: 1d2cc747-63d7-49a9-abb8-93aa36305603

#### Narrative

IcedId banking trojan campaigns targeting banks and other vertical sectors.This malware is known in Microsoft Windows OS targetting browser such as firefox and chrom to steal banking information. It is also known to its unique payload downloaded in C2 where it can be a .png file that hides the core shellcode bot using steganography technique or gzip dat file that contains "license.dat" which is the actual core icedid bot.

#### Detections

| Name        | Technique   | Type         |
| ----------- | ----------- |--------------|
| [Account Discovery With Net App](/endpoint/account_discovery_with_net_app/) | None| TTP |
| [CHCP Command Execution](/endpoint/chcp_command_execution/) | None| TTP |
| [CMD Carry Out String Command Parameter](/endpoint/cmd_carry_out_string_command_parameter/) | None| Hunting |
| [Create Remote Thread In Shell Application](/endpoint/create_remote_thread_in_shell_application/) | None| TTP |
| [Disable Schedule Task](/endpoint/disable_schedule_task/) | None| TTP |
| [Drop IcedID License dat](/endpoint/drop_icedid_license_dat/) | None| Hunting |
| [Eventvwr UAC Bypass](/endpoint/eventvwr_uac_bypass/) | None| TTP |
| [FodHelper UAC Bypass](/endpoint/fodhelper_uac_bypass/) | None| TTP |
| [IcedID Exfiltrated Archived File Creation](/endpoint/icedid_exfiltrated_archived_file_creation/) | None| Hunting |
| [Mshta spawning Rundll32 OR Regsvr32 Process](/endpoint/mshta_spawning_rundll32_or_regsvr32_process/) | None| TTP |
| [NLTest Domain Trust Discovery](/endpoint/nltest_domain_trust_discovery/) | None| TTP |
| [Office Application Spawn Regsvr32 process](/endpoint/office_application_spawn_regsvr32_process/) | None| TTP |
| [Office Application Spawn rundll32 process](/endpoint/office_application_spawn_rundll32_process/) | None| TTP |
| [Office Document Executing Macro Code](/endpoint/office_document_executing_macro_code/) | None| TTP |
| [Office Product Spawning MSHTA](/endpoint/office_product_spawning_mshta/) | None| TTP |
| [Registry Keys Used For Persistence](/endpoint/registry_keys_used_for_persistence/) | None| TTP |
| [Regsvr32 with Known Silent Switch Cmdline](/endpoint/regsvr32_with_known_silent_switch_cmdline/) | None| Anomaly |
| [Rundll32 Create Remote Thread To A Process](/endpoint/rundll32_create_remote_thread_to_a_process/) | None| TTP |
| [Rundll32 CreateRemoteThread In Browser](/endpoint/rundll32_createremotethread_in_browser/) | None| TTP |
| [Rundll32 DNSQuery](/endpoint/rundll32_dnsquery/) | None| TTP |
| [Rundll32 Process Creating Exe Dll Files](/endpoint/rundll32_process_creating_exe_dll_files/) | None| TTP |
| [Schedule Task with Rundll32 Command Trigger](/endpoint/schedule_task_with_rundll32_command_trigger/) | None| TTP |
| [Sqlite Module In Temp Folder](/endpoint/sqlite_module_in_temp_folder/) | None| TTP |
| [Suspicious IcedID Rundll32 Cmdline](/endpoint/suspicious_icedid_rundll32_cmdline/) | None| TTP |
| [Suspicious Rundll32 PluginInit](/endpoint/suspicious_rundll32_plugininit/) | None| TTP |
| [WinEvent Scheduled Task Created Within Public Path](/endpoint/winevent_scheduled_task_created_within_public_path/) | None| TTP |
| [WinEvent Windows Task Scheduler Event Action Started](/endpoint/winevent_windows_task_scheduler_event_action_started/) | None| Hunting |

#### Reference

* [https://threatpost.com/icedid-banking-trojan-surges-emotet/165314/](https://threatpost.com/icedid-banking-trojan-surges-emotet/165314/)
* [https://app.any.run/tasks/48414a33-3d66-4a46-afe5-c2003bb55ccf/](https://app.any.run/tasks/48414a33-3d66-4a46-afe5-c2003bb55ccf/)



[*source*](https://github.com/splunk/security_content/tree/develop/stories/icedid.yml) \| *version*: **1**
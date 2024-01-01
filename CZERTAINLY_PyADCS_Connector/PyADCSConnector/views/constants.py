"""
Script contains the constants for the attributes used int the project
"""
# Property Name of the attributes

NAME_ATTRIBUTE_PROPERTY = "name"
UUID_ATTRIBUTE_PROPERTY = "uuid"
TYPE_ATTRIBUTE_PROPERTY = "type"
CONTENT_TYPE_ATTRIBUTE_PROPERTY = "contentType"
LABEL_ATTRIBUTE_PROPERTY = "label"
DESCRIPTION_ATTRIBUTE_PROPERTY = "description"
READ_ONLY_ATTRIBUTE_PROPERTY = "readOnly"
REQUIRED_ATTRIBUTE_PROPERTY = "required"
VISIBLE_ATTRIBUTE_PROPERTY = "visible"
MUTLISELECT_ATTRIBUTE_PROPERTY = "multiSelect"
GROUP_ATTRIBUTE_PROPERTY = "group"
GLOBAL_ATTRIBUTE_PROPERTY = "global"
LIST_ATTRIBUTE_PROPERTY = "list"
CONTENT_ATTRIBUTE_PROPERTY = "content"
PROPERTY_ATTRIBUTE_PROPERTY = "properties"
PROPERTY_ATTRIBUTE_CALLBACK = "attributeCallback"
CONSTRAINTS_ATTRIBUTE_PROPERTY = "constraints"

# Attribute
# Authority related attributes

# ADCS Info Attribute
ADCS_INFO_ATTRIBUTE_NAME = "adcs_info"
ADCS_INFO_ATTRIBUTE_UUID = "870b612e-fd82-446f-bb5e-e9078ca117cc"
ADCS_INFO_ATTRIBUTE_LABEL = "ADCS Information"
ADCS_INFO_ATTRIBUTE_DESCRIPTION = "How to use ADCS Attributes"

# WinRM Transport Attribute
WINRM_TRANSPORT_ATTRIBUTE_NAME = "winrm_transport"
WINRM_TRANSPORT_ATTRIBUTE_UUID = "06cf66eb-5c1e-4edf-8308-617565a5d6b4"
WINRM_TRANSPORT_ATTRIBUTE_LABEL = "WinRM Transport"
WINRM_TRANSPORT_ATTRIBUTE_DESCRIPTION = "Choose the transport type to use for communication with ADCS"

# WinRM Transport Config Attribute
WINRM_TRANSPORT_CONFIG_ATTRIBUTE_NAME = "winrm_transport_config"
WINRM_TRANSPORT_CONFIG_ATTRIBUTE_UUID = "dd12711e-2daa-4b82-b167-0c2ee5f71df6"
WINRM_TRANSPORT_CONFIG_ATTRIBUTE_LABEL = "WinRM Transport Configuration"
WINRM_TRANSPORT_CONFIG_ATTRIBUTE_DESCRIPTION = "Configure transport specific attributes"

# Server Attribute
SERVER_ADDRESS_ATTRIBUTE_NAME = "server_address"
SERVER_ADDRESS_ATTRIBUTE_UUID = "f2ee713a-c7cf-4b27-ae91-a84606b4877a"
SERVER_ADDRESS_ATTRIBUTE_LABEL = "ADCS server address"
SERVER_ADDRESS_ATTRIBUTE_DESCRIPTION = "Server hostname where ADCS is running"

# Use HTTPS Attribute
USE_HTTPS_ATTRIBUTE_NAME = "use_https"
USE_HTTPS_ATTRIBUTE_UUID = "645d3690-b460-43e7-94c9-9374cf5f14b3"
USE_HTTPS_ATTRIBUTE_LABEL = "Use HTTPS"
USE_HTTPS_ATTRIBUTE_DESCRIPTION = "Use HTTPS to connect to ADCS"

# WinRM Port Attribute
WINRM_PORT_ATTRIBUTE_NAME = "winrm_port"
WINRM_PORT_ATTRIBUTE_UUID = "079f9f93-adc0-48bd-96f1-095991295cb9"
WINRM_PORT_ATTRIBUTE_LABEL = "WinRM Port"
WINRM_PORT_ATTRIBUTE_DESCRIPTION = "WinRM port, default port for http is 5985 and for https 5986"

# SSH Port Attribute
SSH_PORT_ATTRIBUTE_NAME = "ssh_port"
SSH_PORT_ATTRIBUTE_UUID = "1731ad64-e986-4b0d-b1cd-48d59f33e56a"
SSH_PORT_ATTRIBUTE_LABEL = "SSH Port"
SSH_PORT_ATTRIBUTE_DESCRIPTION = "SSH port, default port is 22"

# Credential Type Attribute
CREDENTIAL_TYPE_ATTRIBUTE_NAME = "credential_type"
CREDENTIAL_TYPE_ATTRIBUTE_UUID = "e05beb6a-90fe-4f85-bd9f-2394d70a0a29"
CREDENTIAL_TYPE_ATTRIBUTE_LABEL = "Credential Type"
CREDENTIAL_TYPE_ATTRIBUTE_DESCRIPTION = ("Choose the credential type to use for authentication, it should be "
                                         "compatible with selected protocol")

# Credential Attribute
CREDENTIAL_ATTRIBUTE_NAME = "credential"
CREDENTIAL_ATTRIBUTE_UUID = "93d77f65-d9c4-497c-bdee-f3330eb0f209"
CREDENTIAL_ATTRIBUTE_LABEL = "Credential"
CREDENTIAL_ATTRIBUTE_DESCRIPTION = "Credential to authenticate with ADCS"

# Discovery Info Attribute
DISCOVERY_INFO_ATTRIBUTE_NAME = "discovery_info"
DISCOVERY_INFO_ATTRIBUTE_UUID = "6daef143-0c76-46db-a162-bc38cf70951f"
DISCOVERY_INFO_ATTRIBUTE_LABEL = "Discovery Information"
DISCOVERY_INFO_ATTRIBUTE_DESCRIPTION = "How to use Discovery Attributes"

# Authority Instance Attribute
AUTHORITY_INSTANCE_ATTRIBUTE_NAME = "authority_instance"
AUTHORITY_INSTANCE_ATTRIBUTE_UUID = "b0026fc5-cbee-447b-9e6c-1b1a20f183e4"
AUTHORITY_INSTANCE_ATTRIBUTE_LABEL = "Authority Instance"
AUTHORITY_INSTANCE_ATTRIBUTE_DESCRIPTION = "Choose the authority instance to use"

# CA Name Attribute
CA_NAME_ATTRIBUTE_NAME = "ca_name"
CA_NAME_ATTRIBUTE_UUID = "c725fa53-a3f2-4d24-909d-c40a52a93c01"
CA_NAME_ATTRIBUTE_LABEL = "CA Name"
CA_NAME_ATTRIBUTE_DESCRIPTION = "Identification of the certification authority"

# Issued After Attribute
ISSUED_AFTER_ATTRIBUTE_NAME = "issued_after"
ISSUED_AFTER_ATTRIBUTE_UUID = "f1b49091-de61-4806-95de-02ed94f8f954"
ISSUED_AFTER_ATTRIBUTE_LABEL = "Issued After"
ISSUED_AFTER_ATTRIBUTE_DESCRIPTION = "Select certificates issued after this date (notBefore)"

# Issued Days Before Attribute
ISSUED_DAYS_BEFORE_ATTRIBUTE_NAME = "issued_days_before"
ISSUED_DAYS_BEFORE_ATTRIBUTE_UUID = "bccd95b2-c580-4311-baff-7099aeb57b48"
ISSUED_DAYS_BEFORE_ATTRIBUTE_LABEL = "Number of days before discovery"
ISSUED_DAYS_BEFORE_ATTRIBUTE_DESCRIPTION = ("Maximum number of days before the certificate was issued, from running "
                                            "the discovery")

# Template Name Attribute
TEMPLATE_NAME_ATTRIBUTE_NAME = "template_name"
TEMPLATE_NAME_ATTRIBUTE_UUID = "53286673-be2a-453f-9998-cab67dbb4620"
TEMPLATE_NAME_ATTRIBUTE_LABEL = "Certificate Template Name"
TEMPLATE_NAME_ATTRIBUTE_DESCRIPTION = "Select certificate templates to use"

# CA Name for RA Profile Attribute
CA_NAME_RA_PROFILE_ATTRIBUTE_NAME = "ca_name_ra_profile"
CA_NAME_RA_PROFILE_ATTRIBUTE_UUID = "bf800101-0a20-43b8-9f7a-084c8c2efdc3"
CA_NAME_RA_PROFILE_ATTRIBUTE_LABEL = "CA Name"
CA_NAME_RA_PROFILE_ATTRIBUTE_DESCRIPTION = "Identification of the certification authority"

# Template Name for RA Profile Attribute
TEMPLATE_NAME_RA_PROFILE_ATTRIBUTE_NAME = "template_name_ra_profile"
TEMPLATE_NAME_RA_PROFILE_ATTRIBUTE_UUID = "4a8b5c27-9dc6-447f-b2fc-5f1334d7239f"
TEMPLATE_NAME_RA_PROFILE_ATTRIBUTE_LABEL = "Certificate Template Name"
TEMPLATE_NAME_RA_PROFILE_ATTRIBUTE_DESCRIPTION = "Select certificate templates to use"

# CA Name Metadata Attribute
CA_NAME_METADATA_ATTRIBUTE_NAME = "ca_name_metadata"
CA_NAME_METADATA_ATTRIBUTE_UUID = "8dbc74f1-32e7-427a-9764-046b6400c054"
CA_NAME_METADATA_ATTRIBUTE_LABEL = "CA Name"
CA_NAME_METADATA_ATTRIBUTE_DESCRIPTION = "CA name"

# Template Name Metadata Attribute
TEMPLATE_NAME_METADATA_ATTRIBUTE_NAME = "template_name_metadata"
TEMPLATE_NAME_METADATA_ATTRIBUTE_UUID = "a1a9946c-190e-4e6d-9090-718ec9c99625"
TEMPLATE_NAME_METADATA_ATTRIBUTE_LABEL = "Certificate Template Name"
TEMPLATE_NAME_METADATA_ATTRIBUTE_DESCRIPTION = "Certificate template name"

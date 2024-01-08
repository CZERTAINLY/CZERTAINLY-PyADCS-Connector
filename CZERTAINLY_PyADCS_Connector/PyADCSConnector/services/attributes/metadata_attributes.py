from PyADCSConnector.services.attributes import *


########################################################################################################################
# Attributes definitions
########################################################################################################################

def get_ca_name_metadata_attribute(ca_name):
    properties = get_metadata_attribute_properties(
        METADATA_CA_NAME_ATTRIBUTE_LABEL,
        is_visible=True)
    content = [
        {"reference": ca_name, "data": ca_name}
    ]

    return build_attribute(METADATA_CA_NAME_ATTRIBUTE_NAME,
                           METADATA_CA_NAME_ATTRIBUTE_UUID,
                           "meta",
                           "string",
                           METADATA_CA_NAME_ATTRIBUTE_DESCRIPTION,
                           properties,
                           content,
                           None,
                           None)


def get_template_name_metadata_attribute(template_name):
    properties = get_metadata_attribute_properties(
        METADATA_TEMPLATE_NAME_ATTRIBUTE_LABEL,
        is_visible=True)
    content = [
        {"reference": template_name, "data": template_name}
    ]

    return build_attribute(METADATA_TEMPLATE_NAME_ATTRIBUTE_NAME,
                           METADATA_TEMPLATE_NAME_ATTRIBUTE_UUID,
                           "meta",
                           "string",
                           METADATA_TEMPLATE_NAME_ATTRIBUTE_DESCRIPTION,
                           properties,
                           content,
                           None,
                           None)


########################################################################################################################
# Constants
########################################################################################################################


# CA Name Metadata Attribute
METADATA_CA_NAME_ATTRIBUTE_NAME = "metadata_ca_name"
METADATA_CA_NAME_ATTRIBUTE_UUID = "8dbc74f1-32e7-427a-9764-046b6400c054"
METADATA_CA_NAME_ATTRIBUTE_LABEL = "CA Name"
METADATA_CA_NAME_ATTRIBUTE_DESCRIPTION = "CA name"

# Template Name Metadata Attribute
METADATA_TEMPLATE_NAME_ATTRIBUTE_NAME = "metadata_template_name"
METADATA_TEMPLATE_NAME_ATTRIBUTE_UUID = "a1a9946c-190e-4e6d-9090-718ec9c99625"
METADATA_TEMPLATE_NAME_ATTRIBUTE_LABEL = "Certificate Template Name"
METADATA_TEMPLATE_NAME_ATTRIBUTE_DESCRIPTION = "Certificate template name"

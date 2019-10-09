import xmltodict
import os

from json import loads
from collections import OrderedDict


# \brief Convert current metadata.xml to json
#
# \param[in] rods_zone  Zone name
# \param[in] vault_collection  Collection name of metadata XML
# \param[in] xml_data_name  Data name of metadata XML that requires transformation
# \param[in] data_name_json  Name of data object to be created containing the 
##
def transformPublishedMetadataXmlToJson(callback, rods_zone, publish_collection, xml_data_name, data_name_json):
    # This function simply transforms given data_name to a Json data object. 
	# No further intelligence required further. 
	# Perhaps handling within vault??
	
	ofFlags = ''
	json_file = publish_collection + '/' + data_name_json

	ret_val = callback.msiDataObjCreate(json_file, ofFlags, 0)
	
	#copyACLsFromParent(callback, json_file, "default")

        xmlDataDict = getMetadataXmlAsDict(callback, publish_collection + "/" + xml_data_name)
        
	# take category incuding version from declared namespace in xml
	category_version = xmlDataDict['metadata']['@xmlns'].split('/')[-1]

	dictSchema = getActiveJsonSchemaAsDict(callback,rods_zone, category_version)

	newJsonDataString = transformYodaXmlDataToJson(callback, dictSchema, xmlDataDict)
	
	fileHandle = ret_val['arguments'][2]
	callback.msiDataObjWrite(fileHandle, newJsonDataString, 0)
	callback.msiDataObjClose(fileHandle, 0)

	callback.writeString("serverLog", "[ADDED METADATA.JSON AFTER TRANSFORMATION] %s" % (json_file))



# \brief Loop through all metadata xml data objects within '/tempZone/yoda/publication'.
#        If NO corresponding json is found in that collection, the corresponding yoda-metadata.xml must be converted to json as an extra file - yoda-metadata.json.
#        The resulting file must be copied to moai collection as well
#
# \param[in] rods_zone Zone name
# \param[in] data_id   data id to start searching from
# \param[in] batch     Batch size, <= 256
# \param[in] pause     Pause between checks (float)
# \param[in] publicHost, yodaInstance, yodaPrefix are required for secure copy from /publication area to MOAI
#
# \return data_id to continue with in next batch.
# If data_id =0, no more data objects were found. 
# Batch is finished
#
def iiCheckPublishedMetadataXmlForTransformationToJsonBatch(callback, rods_zone, data_id, batch, pause, publicHost, yodaInstance, yodaPrefix):

    publication_collection = '/' + rods_zone + '/yoda/publication'
    iter = genquery.row_iterator(
        "ORDER(DATA_ID), DATA_NAME, COLL_ID",
        "COLL_NAME = '%s' AND DATA_NAME like '%%.xml' AND DATA_ID >= '%d'" % (publication_collection, data_id),
        genquery.AS_LIST, callback
    )

    # Check each collection in batch.
    for row in iter:
	data_id = int(row[0])
        data_name_xml = row[1]
        coll_id = int(row[2])
        pathParts = coll_name.split('/')
        data_name_no_extension = os.path.splitext(data_name)[0] # the base name of the data object without extension
        data_name_json = data_name_no_extension + '.json'

        try:
	    # First make sure that no metadata json file exists already in the published collection .
	    # If so, no transformation is required and the json file needs not be copied into the MOAI area.

	    jsonFound = False
	    iter2 = genquery.row_iterator(
		 "ORDER(COLL_ID), COLL_NAME",
		 "DATA_NAME = '%s' AND COLL_ID = '%d'" % (data_name_json, coll_id),
		 genquery.AS_LIST, callback
	    )
	    for row2 in iter2:
		jsonFound = True
		break

	    if jsonFound == False:
                # At this moment only default schema is used. So not required to figure out which schema is necessary
	        transformPublishedMetadataXmlToJson(callback, rods_zone, publication_collection, data_name_xml, data_name_json)

                callback.iiCopyTransformedPublicationToMOAI(data_name_json, publication_collection, publicHost, yodaInstance, yodaPrefix)
        except:
            pass

        # Sleep briefly between checks.
        time.sleep(pause)

        # The next data_id to check must have a higher DATA_ID
        data_id = data_id + 1
    else:
        # All done.
        data_id = 0

    return data_id


# \brief Convert published metadata XML that residedes in 'published' collection to JSON - batchwise
#
# \param[in] data_id  first data to check - initial =0
# \param[in] batch    batch size, <= 256
# \param[in] pause    pause between checks (float)
# \param[in] delay    delay between batches in seconds
# \param[in] publicHost,yodaInstance,yodaPrefix are required for secure copy from /publication area to MOAI
#
def iiCheckPublishedMetadataXmlForTransformationToJson(rule_args, callback, rei):
    coll_id = int(rule_args[0])
    batch = int(rule_args[1])
    pause = float(rule_args[2])
    delay = int(rule_args[3])
    publicHost = rule_args[4] 
    yodaInstance = rule_args[5] 
    yodaPrefix = rule_args[6]
    rods_zone = session_vars.get_map(rei)["client_user"]["irods_zone"]

    # Check one	batch of metadata schemas.
    # If no more data_ids are found in the main/single publication folder, the function returns 0
    data_id = iiCheckPublishedMetadataXmlForTransformationToJsonBatch(callback, rods_zone, data_id, batch, pause, publicHost, yodaInstance, yodaPrefix)

    if coll_id != 0:
        # Check the next batch after a delay.
        callback.delayExec(
            "<PLUSET>%ds</PLUSET>" % delay,
            "iiCheckPublishedMetadataXmlForTransformationToJson('%d', '%d', '%f', '%d')" % (data_id, batch, pause, delay, publicHost, yodaInstance, yodaPrefix),
            "")




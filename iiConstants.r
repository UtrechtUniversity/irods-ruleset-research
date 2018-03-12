# \file
# \brief Constants for the ii rules. If architecture changes, only
# 			this file needs be adapted
#
# \author    Paul Frederiks
# \copyright Copyright (c) 2016-2017, Utrecht University. All rights reserved.
# \license   GPLv3, see LICENSE.

# \constant GENQMAXROWS Maximum number of rows returned by an iRODS GenQuery or msiGetMoreRows call
GENQMAXROWS = 256

#\brief the length of the search string should be below 1075, as this hits the MAX_SQL_SIZE limit in iRODS.
#       The search field is limited to 255 characters to be consistent with the metadata text field maxLength
#       255 * 4 = 1020 bytes when all characters are 4 byte utf-8 encoded, like in chinese.
#\constant IIMAXSEARCHSTRINGLENGTH
IIMAXSEARCHSTRINGLENGTH = 1020;

# \constant IIGROUPPREFIX
IIGROUPPREFIX = "research-"

# \constant IIVAULTPREFIX
IIVAULTPREFIX = "vault-"

# \constant IIXSDCOLLECTION
IIXSDCOLLECTION = UUSYSTEMCOLLECTION ++ "/xsd"

# \constant IIXSLCOLLECTION
IIXSLCOLLECTION = UUSYSTEMCOLLECTION ++ "/xsl"

# \constant IIFORMELEMENTSCOLLECTION
IIFORMELEMENTSCOLLECTION = UUSYSTEMCOLLECTION ++ "/formelements"

# \constant IILICENSECOLLECTION
IILICENSECOLLECTION = UUSYSTEMCOLLECTION ++ "/licenses"

# \constant IITERMSCOLLECTION
IITERMSCOLLECTION = UUSYSTEMCOLLECTION ++ "/terms"

# \constant IIXSDDEFAULTNAME Name of the fallback default xsd for ilab
IIXSDDEFAULTNAME = "default.xsd"

# \constant IIFORMELEMENTSDEFAULTNAME
IIFORMELEMENTSDEFAULTNAME = "default.xml"

# \constant IIMETADATAXMLNAME
IIMETADATAXMLNAME = "yoda-metadata.xml"

# \constant IIXSLDEFAULTNAME
IIXSLDEFAULTNAME = "default.xsl"

# \constant IIDATACITEDEFAULTNAME
IIDATACITEXSLDEFAULTNAME = "default2datacite.xsl"

# \constant IILANDINGPAGEXSLDEFAULTNAME
IILANDINGPAGEXSLDEFAULTNAME = "default2landingpage.xsl"

# \constant IIPUBLICATIONCOLLECTION
IIPUBLICATIONCOLLECTION = UUSYSTEMCOLLECTION ++ "/publication"

# \constant IILOCKATTRNAME
IILOCKATTRNAME = UUORGMETADATAPREFIX ++ "lock"

# \constant IISTATUSATTRNAME
IISTATUSATTRNAME = UUORGMETADATAPREFIX ++ "status"

# \constant IIVAULTSTATUSATTRNAME
IIVAULTSTATUSATTRNAME = UUORGMETADATAPREFIX ++ "vault_status"

# \brief All research folder states.
FOLDER = "";
LOCKED = "LOCKED";
SUBMITTED = "SUBMITTED";
ACCEPTED = "ACCEPTED";
REJECTED = "REJECTED";
SECURED = "SECURED";

# \constant IIFOLDERTRANSITIONS
IIFOLDERTRANSITIONS = list((FOLDER, LOCKED),
			   (FOLDER, SUBMITTED),
			   (LOCKED, FOLDER),
			   (LOCKED, SUBMITTED),
			   (SUBMITTED, LOCKED),
			   (SUBMITTED, ACCEPTED),
			   (SUBMITTED, REJECTED),
			   (REJECTED, FOLDER),
			   (ACCEPTED, SECURED),
			   (SECURED, FOLDER))

# \brief All vault package states.
INCOMPLETE = "INCOMPLETE"
COMPLETE = "COMPLETE"
UNPUBLISHED = "UNPUBLISHED";
SUBMITTED_FOR_PUBLICATION = "SUBMITTED_FOR_PUBLICATION";
APPROVED_FOR_PUBLICATION = "APPROVED_FOR_PUBLICATION";
PUBLISHED = "PUBLISHED";
REQUESTED_FOR_DEPUBLICATION = "REQUESTED_FOR_DEPUBLICATION";
DEPUBLISHED = "DEPUBLISHED";

# \constant IIVAULTTRANSITIONS
IIVAULTTRANSITIONS = list((UNPUBLISHED, SUBMITTED_FOR_PUBLICATION),
			  (COMPLETE, SUBMITTED_FOR_PUBLICATION),
			  (SUBMITTED_FOR_PUBLICATION, APPROVED_FOR_PUBLICATION),
			  (SUBMITTED_FOR_PUBLICATION, UNPUBLISHED),
			  (APPROVED_FOR_PUBLICATION, PUBLISHED),
			  (PUBLISHED, REQUESTED_FOR_DEPUBLICATION),
			  (REQUESTED_FOR_DEPUBLICATION, DEPUBLISHED))

# \brief All cronjob states.
CRONJOB_PENDING = "CRONJOB_PENDING"
CRONJOB_PROCESSING = "CRONJOB_PROCESSING"
CRONJOB_RETRY = "CRONJOB_RETRY"
CRONJOB_UNRECOVERABLE = "CRONJOB_UNRECOVERABLE"
CRONJOB_OK = "CRONJOB_OK"

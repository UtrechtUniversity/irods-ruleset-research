# \file
# \brief job to copy collections that are snapshot locked to vault.
#                       adapted from job_movetovault.re
# \author Jan de Mooij
# \copyright Copyright (c) 2015, Utrecht university. All rights reserved
# \license GPLv3, see LICENSE
#
#  This file should be executed as part of a recurring crontab job
#  as the irods admin user (i.e. irods user type rodsadmin)
#  e.g. run every minute
#
#  if another instance of the job is running then the vault will be
#  locked and silently ignored
#

uuIiRunCreateSnapshots {
        *user = "$userNameClient#$rodsZoneClient";
        uuGetUserAndZone(*user, *userName, *userZone);
        uuGroupMemberships(*user, *grouplist);
        foreach(*grp in *grouplist) {
                writeLine("stdout", "Found group '*grp'");
                *intakeRoot = "/*zone/home/grp-intake-*grp";
                *vaultRoot = "/*zone/home/grp-vault-*grp";

                uuIi2Vault(*intakeRoot, *vaultRoot, *status);
                if (*status == 0 ) then *result = "ok" else *result = "ERROR (*status)";
                writeLine("serverLog","RunIntake2Vault for *intakeRoot result = *result");
        }
}


input *intakeRoot='dummy'
output ruleExecOut
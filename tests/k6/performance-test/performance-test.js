import {variables} from "./common/config/common.js";
import {issueCertificate} from "./common/helper/http.js"

const payload = open(variables.pyadcs.payloadPath);

export function setup () {
  return {
     runId: Date.now().toString(),
  };
}

export default function (data) {

    // Issue the certificate
    issueCertificate(
       variables.pyadcs.baseUrl,
       variables.pyadcs.authorityUuid,
       payload,
       variables.pyadcs.logging.enabled
    );

}

import { check, fail } from 'k6';
import http from 'k6/http';

export const issueCertificate = (baseUrl, uuid, payload, log) => {
  const url = baseUrl + '/v2/authorityProvider/authorities/' + uuid + '/certificates/issue';

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  };

  const res = http.post(
    url,
    payload,
    params
  );

  if (res.status !== 200) {
    if (log === 'true') {
      console.log(JSON.stringify(res));
    }
  }

  if (
    !check(res, {
      'issueCertificate response status is 200': (r) => r.status === 200,
    })
  ) {
    fail(`Failed to issue certificate: ${res.status} - ${res.body}`);
  } else {
    return res.json();
  }

}

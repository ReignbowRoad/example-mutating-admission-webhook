import os
import logging

from Responses.AdmissionReview import AdmissionReview
from Responses.AdmissionReview import AdmissionResponse

from flask import Flask, request, jsonify

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/mutate', methods=['POST'])
def mutate_admission_request():
    admission_review = request.json

    # Implement your mutating logic here
    mutated_object = admission_review['request']['object']
    mutated_object['metadata']['annotations']['mutated-by'] = 'PythonWebhook'

    # Instantiate the AdmissionResponse class
    admission_response_instance = AdmissionResponse(
        uid=admission_review["request"]["uid"],
        allowed=True, 
        patchType="JSONPatch", 
        patch="W3sib3AiOiAiYWRkIiwgInBhdGgiOiAiL21ldGFkYXRhL2Fubm90YXRpb25zL2lvLmRpZ2l0YWx3YW5kZXJsdXN0fjFtdXRhdGVkIiwgInZhbHVlIjogInRydWUifV0K"
    )

    admission_review = AdmissionReview(admissionResponse=admission_response_instance)

    return admission_review.response()

if __name__ == '__main__':

    tlsKey = os.environ.get('TLS_KEY', "/app/tls.key")
    tlsCert = os.environ.get('TLS_CRT', "/app/tls.crt")

    app.run(host='0.0.0.0', port=8443, ssl_context=(tlsCert, tlsKey))

from Responses.AdmissionReview import AdmissionReview
from Responses.AdmissionReview import AdmissionResponse

# Instantiate the Response class
response_instance = AdmissionResponse(
   uid="<value from request.uid>", 
   allowed=True, 
   patchType="JSONPatch", 
   patch="W3sib3AiOiAiYWRkIiwgInBhdGgiOiAiL3NwZWMvcmVwbGljYXMiLCAidmFsdWUiOiAzfV0="
)

# Instantiate the AdmissionReview class with the response instance
admission_review_instance = AdmissionReview(admissionResponse=response_instance)

print(admission_review_instance.response())
from dataclasses import dataclass
import json
from typing import Optional

@dataclass
class AdmissionResponse:

    # Must match the uid found in the request
    uid: str

    # Is the admission of the object allowed (true) or not (false)
    allowed: bool

    # Only JSONPatch is supported at the moment
    # https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response
    patchType: Optional[str] = None

    # Contains a base64-encoded array of JSON patch operations
    # See https://jsonpatch.com/ for info on how to patch
    patch: Optional[str] = None

    # Ensure that patchType and patch are either both set or both None
    def __post_init__(self):
        if (self.patchType is not None and self.patch is None) or (self.patchType is None and self.patch is not None):
            raise ValueError("Both patchType and patch must be set together.")
        

@dataclass
class AdmissionReview:

    admissionResponse: AdmissionResponse

    apiVersion: str = "admission.k8s.io/v1"

    kind: str = "AdmissionReview"

    def response(self) -> str:

        return json.dumps({
            "apiVersion": self.apiVersion,
            "kind": self.kind,
            "response": self.admissionResponse.__dict__
        }, indent=2)

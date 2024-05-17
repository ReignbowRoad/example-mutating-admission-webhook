# Example Mutating Webhook Demo

An example (rough and ready) Mutatiing Webhook written in Python. Does nothing fancy other than add an annotation to an ingress resource. Created with the express purpose of gaining more insight into how they work for the benefit of the CKS exam in which these are covered as a topic.

## Building

Build with Docker:

```shell
$ docker build -t dpluser/example-mutating-webhook:1.0.2-beta .
```

Push the image:

```shell
docker push dpluser/example-mutating-webhook:1.0.3-beta 
```

## Generating Certifcates

The Webhook requires certificates and the cert of the CA used to sign them. Use this script to generate some self-signed ones.

```
$ ./generate-demo-certs.sh --host <hostname> --password <ca-password>
```

Then create a secret in Kubernetes that can be used by both your application and the Webhook configuration (Root CA cert only)

```shell
$ kubectl create secret generic example-mutating-webhook-tls \
    --from-file=rootCA.crt=rootCA.crt \
    --from-file=tls.crt=tls.crt \
    --from-file=tls.key=tls.key
```

## Deployment

Run the following command to deploy all of the components: `Deployment`, `Service` and `MutatingWebhookConfiguration`. 

```shell
$ kubectl create -f deploy/deployment.yaml
$ kubectl create -f deploy/service.yaml
$ kubectl create -f deploy/mutatingwebhookconfig.yaml
```

## Testing

Create and basic Ingress resource and fire it at Kubernetes:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80
```

Check the ingress resource once it's been created. You should see a new annotation has been added:

```shell
$ kubectl get ing minimal-ingress -o jsonpath='{.metadata.annotations}' | jq .
{
  "io.digitalwanderlust/mutated": "true",     # <<<--------- We added this
  "nginx.ingress.kubernetes.io/rewrite-target": "/"
}

```
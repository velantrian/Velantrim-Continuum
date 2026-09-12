# Raw GET /models (Field 5 identity)

- captured_at_utc: `2026-09-12T16:22:28Z`
- endpoint: `https://api.deepseek.com/models`
- method: `GET`
- request_body: none
- Authorization: **REDACTED / not stored**
- response_body_sha256: `0c5d2ba6ebb791e893b0e7efed32c64415a633ed774e8d89dad8e33c4d69ae77`
- returned_model_ids: ['deepseek-flash', 'deepseek-v4-pro']

## Response headers (sanitized)

```
HTTP/2 200 
content-type: application/json
content-length: 153
date: Sat, 12 Sep 2026 16:22:28 GMT
server: elb
vary: origin, access-control-request-method, access-control-request-headers
access-control-allow-credentials: true
x-ds-trace-id: 3269e1f4012aaec7f5fe1792188eb74d
strict-transport-security: max-age=31536000; includeSubDomains; preload
x-content-type-options: nosniff
x-cache: Miss from cloudfront
via: 1.1 9485615792f5f5ecef76608e38635192.cloudfront.net (CloudFront)
x-amz-cf-pop: DFW59-P7
x-amz-cf-id: JCJgnnlbW3E47YyjmuZBwwzjk9_t5SmiospTdB3OM7SJ_RBz80tijQ==

```

## Response body

```json
{
  "object": "list",
  "data": [
    {
      "id": "deepseek-flash",
      "object": "model",
      "owned_by": "deepseek"
    },
    {
      "id": "deepseek-v4-pro",
      "object": "model",
      "owned_by": "deepseek"
    }
  ]
}
```


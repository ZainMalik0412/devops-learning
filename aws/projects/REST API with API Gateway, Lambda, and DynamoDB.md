# Project: REST API with API Gateway → Lambda → DynamoDB (POST /submit + CORS)

## Objective

Build a serverless REST API from scratch:
- DynamoDB table to store submissions
- Lambda function that validates JSON and writes to DynamoDB
- API Gateway (REST API) with `POST /submit` integrated to Lambda (proxy)
- CORS enabled so browsers can call it
- Tested with `curl` and verified in DynamoDB

---

## Step 1 — Create the DynamoDB Table

1. AWS Console → **DynamoDB**
2. Tables → **Create table**
3. Table name: `submissions`
4. Partition key: `submissionID` (String)
5. Capacity mode: **On-demand**
6. Click **Create table**

> **Important:** The partition key must be exactly `submissionID` (capital ID) — this must match the Lambda code.

![DynamoDB Create table showing name submissions and partition key submissionID (String)](screenshots/api-step1-create-dynamodb-table.png)

![DynamoDB table overview showing submissions table with partition key submissionID, On-demand capacity, Active status](screenshots/api-step1-dynamodb-table-overview.png)

---

## Step 2 — Create the Lambda Execution Role (IAM)

### Create the role

1. AWS Console → **IAM** → Roles → **Create role**
2. Trusted entity: **AWS service** → **Lambda**

![IAM Create role showing AWS service trusted entity with Lambda selected](screenshots/api-step2-iam-trusted-entity.png)

3. Permissions: attach **AWSLambdaExecute**

![IAM Add permissions showing AWSLambdaExecute policy selected](screenshots/api-step2-iam-add-permissions.png)

4. Role name: `lambda-dynamodb-submissions-role`
5. Click **Create role**

![IAM role details showing name lambda-dynamodb-submissions-role and trust policy for lambda.amazonaws.com](screenshots/api-step2-iam-role-details.png)

### 2.1 — Add DynamoDB Permission (PutItem)

1. Open the role → Permissions tab
2. **Add permissions** → **Create inline policy**
3. JSON tab, paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowWriteToSubmissionsTable",
      "Effect": "Allow",
      "Action": "dynamodb:PutItem",
      "Resource": "arn:aws:dynamodb:eu-west-2:YOUR_ACCOUNT_ID:table/submissions"
    }
  ]
}
```

4. Name it: `AllowWriteToSubmissionsTable`
5. Click **Create policy**

![IAM inline policy editor showing AllowWriteToSubmissionsTable with dynamodb:PutItem on submissions table](screenshots/api-step2-iam-inline-policy-putitem.png)

> Do not change the trust relationship — it should remain `lambda.amazonaws.com`.

Final role permissions:

![Permissions summary showing AmazonDynamoDBFullAccess and AWSLambdaExecute attached](screenshots/api-step2-iam-permissions-summary.png)

---

## Step 3 — Create the Lambda Function

1. AWS Console → **Lambda** → **Create function**
2. **Author from scratch**
3. Function name: `submitHandler`
4. Runtime: **Node.js**
5. Execution role: **Use existing role** → select `lambda-dynamodb-submissions-role`
6. Click **Create function**

![Lambda function submitHandler successfully created showing function overview and ARN](screenshots/api-step3-lambda-function-created.png)

### 3.1 — Verify Execution Role

Lambda → **Configuration** → Permissions tab — confirm the role is attached:

![Lambda Configuration tab showing execution role and permissions for submitHandler](screenshots/api-step3-lambda-execution-role.png)

### 3.2 — Add Environment Variable

Lambda → Configuration → **Environment variables**

Add:

| Key | Value |
|---|---|
| `TABLE_NAME` | `submissions` |

Save.

### 3.3 — Paste the Lambda Code and Deploy

Lambda → **Code** tab → paste the following code and click **Deploy**:

```javascript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand } from "@aws-sdk/lib-dynamodb";
import crypto from "crypto";

const ddb = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(ddb);

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Allow-Methods": "POST,OPTIONS",
};

export const handler = async (event) => {
  if (event?.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers: corsHeaders, body: "" };
  }

  try {
    let body = {};
    if (event?.body) {
      body = typeof event.body === "string" ? JSON.parse(event.body) : event.body;
    }

    const { name, email, message } = body;

    if (!name || !email || !message) {
      return {
        statusCode: 400,
        headers: corsHeaders,
        body: JSON.stringify({ error: "name, email, and message are required" }),
      };
    }

    const submissionID = crypto.randomUUID();
    const createdAt = new Date().toISOString();

    await docClient.send(
      new PutCommand({
        TableName: process.env.TABLE_NAME,
        Item: { submissionID, createdAt, name, email, message },
      })
    );

    return {
      statusCode: 200,
      headers: corsHeaders,
      body: JSON.stringify({ ok: true, submissionID, createdAt }),
    };
  } catch (err) {
    console.error("Handler error:", err);
    return {
      statusCode: 500,
      headers: corsHeaders,
      body: JSON.stringify({ error: "Internal Server Error" }),
    };
  }
};
```

![Lambda code source showing the deployed submitHandler function with CORS headers and DynamoDB PutCommand](screenshots/api-step3-lambda-code-deployed.png)

---

## Step 4 — Create the REST API in API Gateway

1. AWS Console → **API Gateway**
2. **Create API** → Choose **REST API** → **Build**
3. API name: `submissions-api`
4. Endpoint type: **Regional**
5. Click **Create API**

![API Gateway Create REST API page showing name submissions api and Regional endpoint type](screenshots/api-step4-create-rest-api.png)

---

## Step 5 — Create /submit Resource + POST Method (Lambda Proxy)

### Create the resource

1. API Gateway → your API → Resources
2. **Create resource**
3. Resource name: `submit`
4. Resource path: `/submit`
5. Click **Create resource**

![API Gateway Create resource showing resource name submit and path /submit](screenshots/api-step5-create-resource-submit.png)

### Create the POST method

1. Select `/submit`
2. **Create method** → Method type: **POST**
3. Integration type: **Lambda Function**
4. Toggle **Lambda proxy integration** ON
5. Lambda function: `submitHandler` (eu-west-2)
6. Click **Create method** and allow permission prompt

![API Gateway POST method showing Lambda function integration with proxy integration enabled and submitHandler selected](screenshots/api-step5-post-method-lambda-proxy.png)

---

## Step 6 — Enable CORS (for Browsers)

1. Select `/submit`
2. **Enable CORS**
3. Access-Control-Allow-Methods: tick **POST** (OPTIONS is included automatically)
4. Access-Control-Allow-Origin: `*`
5. Click **Save**

![API Gateway Enable CORS settings showing POST ticked, OPTIONS included, and Allow-Origin set to *](screenshots/api-step6-enable-cors.png)

---

## Step 7 — Deploy to a Stage (prod)

1. **Deploy API**
2. Stage: **New stage**
3. Stage name: `prod`
4. Click **Deploy**

![API Gateway Deploy API dialog showing new stage prod with /submit resource and POST + OPTIONS methods](screenshots/api-step7-deploy-api-prod.png)

Your invoke URL will be:

```
https://<api-id>.execute-api.eu-west-2.amazonaws.com/prod/submit
```

---

## Step 8 — Test the Endpoint

Test with `curl`:

```bash
curl -i -X POST "https://YOUR_API_ID.execute-api.eu-west-2.amazonaws.com/prod/submit" \
  -H "Content-Type: application/json" \
  -d '{"name":"Zain","email":"zain@zainecs.com","message":"Hello from API Gateway"}'
```

**Result:** HTTP/2 200 with JSON containing `ok: true`, `submissionID`, and `createdAt`

![Terminal showing curl POST request returning HTTP/2 200 with ok:true, submissionID, and createdAt in response](screenshots/api-step8-curl-test-response.png)

---

## Step 9 — Verify It Saved into DynamoDB

1. DynamoDB → Tables → `submissions`
2. **Explore table items**
3. Click **Run** (Scan)
4. Confirm the item exists with the same `submissionID` from the API response

![DynamoDB Explore items scan showing 1 item returned with submissionID, createdAt, email, message, and name](screenshots/api-step9-dynamodb-items-scan.png)

![DynamoDB item detail showing all attributes: submissionID, createdAt, email (zain@zainecs.com), message, and name (Zain)](screenshots/api-step9-dynamodb-item-detail.png)
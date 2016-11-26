# demon

## Instructions from the boilerplate

This function handles a Slack slash command and echoes the details back to the user.

Follow these steps to configure the slash command in Slack:

1. Navigate to https://<your-team-domain>.slack.com/services/new
1. Search for and select "Slash Commands".
1. Enter a name for your command and click "Add Slash Command Integration".
1. Copy the token string from the integration settings and use it in the next section.
1. After you complete this blueprint, enter the provided API endpoint URL in the URL field.

Follow these steps to encrypt your Slack token for use in this function:

1. Create a KMS key — http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html.
1. Encrypt the token using the AWS CLI: `$ aws kms encrypt --key-id alias/<KMS key name> --plaintext "<COMMAND_TOKEN>"`
1. Copy the base-64 encoded, encrypted key (CiphertextBlob) to the kmsEncryptedToken environment variable.

Follow these steps to complete the configuration of your command API endpoint

1. When completing the blueprint configuration select "Open" for security on the "Configure triggers" page.
1. Enter a name for your execution role in the "Role name" field. Your function's execution role needs kms:Decrypt permissions. We have pre-selected the "KMS decryption permissions" policy template that will automatically add these permissions.
1. Update the URL for your Slack slash command with the invocation URL for the created API resource in the prod stage.

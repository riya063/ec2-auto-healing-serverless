name: Deploy EC2 Auto Healing Infra

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-south-1

      - name: Install SAM CLI
        run: |
          pip install aws-sam-cli

      - name: Deploy using SAM
        run: |
          sam build
          sam deploy --no-confirm-changeset \
                     --stack-name ec2-auto-healing \
                     --capabilities CAPABILITY_IAM \
                     --parameter-overrides \
                       VpcId=${{ secrets.VPC_ID }} \
                       SubnetIds='${{ secrets.SUBNET_IDS }}' \
                       KeyName=${{ secrets.KEY_NAME }} \
                       ImageId=${{ secrets.IMAGE_ID }}


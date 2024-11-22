## Policy document for lambda assume role permission (a way of portraying the JSON)
data "aws_iam_policy_document" "assume_role_policy" {
    statement {
        effect = "Allow"
        actions = ["sts:AssumeRole"]
        principals {
            type = "Service"
            identifiers = ["lambda.amazonaws.com"]
        }
    }
}

## Policy document to log to Cloudwatch
data "aws_iam_policy_document" "Cloudwatch_log_document" {
    statement {
        effect = "Allow"
        actions = [
            "logs:CreateLogStream",
            "logs:PutLogEvents"
            ]
        resources = ["arn:aws:logs:*:*:*"]
    }
}

## Policy document for Secrets Manager get secret value permission (a way of portraying the JSON)
data "aws_iam_policy_document" "get_secret_value_policy" {
    statement {
        effect = "Allow"
        actions = ["secretsmanager:GetSecretValue"]
        resources = [ "arn:aws:secretsmanager:eu-west-2:796973515606:secret:totesys-conn-430tOE" ]
    }
}


#############################################################################
#############################################################################
#######################  EventBridge & StepFunction  ########################
#############################################################################
#############################################################################


## StepFunction State Machine IAM Policy
data "aws_iam_policy_document" "state_machine_assume_role_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole",
    ]
  }
}

## StepFunction State Machine Role
resource "aws_iam_role" "StateMachineRole" {
  name               = "NC-StepFunctions-Terraform-Role"
  assume_role_policy = data.aws_iam_policy_document.state_machine_assume_role_policy.json
}


## StepFunction State Machine Role Policy
data "aws_iam_policy_document" "state_machine_role_policy" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups"
    ]

    resources = ["${aws_cloudwatch_log_group.MySFNLogGroup.arn}:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "cloudwatch:PutMetricData",
      "logs:CreateLogDelivery",
      "logs:GetLogDelivery",
      "logs:UpdateLogDelivery",
      "logs:DeleteLogDelivery",
      "logs:ListLogDeliveries",
      "logs:PutResourcePolicy",
      "logs:DescribeResourcePolicies",
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction"
    ]

    resources = ["arn:aws:lambda:eu-west-2:796973515606:function:lambda1:$LATEST", "arn:aws:lambda:eu-west-2:796973515606:function:lambda2:$LATEST", "arn:aws:lambda:eu-west-2:796973515606:function:lambda3:$LATEST"]
  }

}

# Create an IAM policy for the Step Functions state machine (converts above to JSON)
resource "aws_iam_role_policy" "StateMachinePolicy" {
  role   = aws_iam_role.StateMachineRole.id
  policy = data.aws_iam_policy_document.state_machine_role_policy.json
}

# Create a Log group for the state machine
resource "aws_cloudwatch_log_group" "MySFNLogGroup" {
  name_prefix       = "/aws/vendedlogs/states/MyStateMachine-"
  retention_in_days = 1
#   kms_key_id        = aws_kms_key.log_group_key.arn
}
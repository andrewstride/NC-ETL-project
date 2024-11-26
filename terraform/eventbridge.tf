## EventBridge to trigger Step Function every 25 minutes
module "eventbridge" {
  source = "terraform-aws-modules/eventbridge/aws"

  create_bus = false
  
  rules = {
    crons = {
      description         = "Trigger for StepFunction every 25 minutes"
      schedule_expression = "rate(25 minutes)"
    }
  }

  targets = {
    crons = [
      {
        name            = "nc-state-machine" ## replace
        # arn             = "${aws_sfn_state_machine.sfn_state_machine.arn}"
        arn = "arn:aws:states:eu-west-2:796973515606:stateMachine:nc-state-machine" ## replace
        attach_role_arn = true
      }
    ]
  }
    sfn_target_arns = ["arn:aws:states:eu-west-2:796973515606:stateMachine:nc-state-machine"]
#   sfn_target_arns   = [aws_sfn_state_machine.sfn_state_machine.arn] ## step-function target
    attach_sfn_policy = true
}

## StepFunction to trigger Lambda1 (two and three?)
resource "aws_sfn_state_machine" "sfn_state_machine" {
  name     = "nc-state-machine"
  role_arn = aws_iam_role.StateMachineRole.arn ## Check / replace

  definition = <<EOF
{
  "Comment": "Terraformers State Machine",
  "StartAt": "Invoke Lambda1",
  "States": {
    "Invoke Lambda1": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:eu-west-2:796973515606:function:lambda1:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Choice"
    },
    "Choice": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.triggerLambda2",
          "BooleanEquals": false,
          "Next": "Success"
        }
      ],
      "Default": "Invoke Lambda2"
    },
    "Success": {
      "Type": "Succeed"
    },
    "Invoke Lambda2": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:eu-west-2:796973515606:function:lambda2:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Invoke Lambda3"
    },
    "Invoke Lambda3": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:eu-west-2:796973515606:function:lambda3:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "End": true
    }
  },
  "TimeoutSeconds": 300
}
EOF  
} ## Code from console. Parameterize Lambda1 ARN ? 

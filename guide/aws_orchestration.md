#

||
|---|
|![Banner](../assets/banner-guide-aws-orchestration.png)|
||

## ESTADOS | *STATES*

A state machine is a workflow. A task is a state in a workflow that represents a single unit of work that another AWS service performs. Each step in a workflow is a state.

States are elements in your state machine. A state is referred to by its name, which can be any string but it must be unique within the scope of the entire state machine. Individual states can make decisions based on their input, perform actions, and pass output to other states.

States can provide a variety of functions in your state machine:

- Perform some work in your state machine.
- Make a choice between branches of activity.
- Stop an activity with a failure or success.
- Simply pass its input to its output or inject some fixed data.
- Provide a delay for a certain amount of time or until a specified time or date.
- Begin parallel branches of activity.
- Dynamically iterate steps.

## STEP FUNCTIONS

Step Functions is based on state machines and tasks. Step Functions provides serverless orchestration for modern applications. Orchestration centrally manages a workflow by breaking it into multiple steps, adding flow logic, and tracking the inputs and outputs between the steps. As your applications run, Step Functions maintains the application state, tracking exactly which workflow step your application is in, and stores an event log of data that is passed between application components. That means if the workflow is interrupted for any reason, your application can pick up right where it left off.

AWS Step Functions helps with any computational problem or business process that can be subdivided into a series of steps. Application development is faster and more intuitive with Step Functions, because you can define and manage the workflow of your application independently from its business logic. Making changes to one does not affect the other. You can easily update and modify workflows in one place, without having to struggle with managing, monitoring, and maintaining multiple point-to-point integrations. Step Functions frees your functions and containers from excess code, so you can write your applications faster and make them more resilient and easier to maintain.

### CARACTERÍSTICAS

- **Escalabilidade Automática | *Automatic Scaling***
  AWS Step Functions automatically scales the operations and underlying compute to run the steps of your application for you in response to changing workloads. Step Functions scales automatically to help ensure the performance of your application workflow remains consistent as the frequency of requests increases.
- **Alta Disponibilidade | *High Availability***
  AWS Step Functions has built-in fault tolerance and maintains service capacity across multiple Availability Zones in each region to protect applications against individual machine or data center failures. This helps ensure high availability for both the service itself and for the application workflow it operates.
- **Pagamento por Utilização | *Pay-Per-Use***
  With AWS Step Functions, you pay for each transition from one state to the next. Billing is metered by state transition, and you do not pay for idle time, regardless of how long each state persists (up to one year). This keeps Step Functions cost-effective as you scale from a few executions to tens of millions.
- **Segurança e Compliance | *Security and Compliance***
  AWS Step Functions is integrated with AWS Identity and Access Management (IAM), and recommends a least-privileged IAM policy for all of the resources used in your workflow. You can access AWS Step Functions from VPC-enabled AWS Lambda functions and other AWS services without traversing the public internet using AWS PrivateLink. 
  AWS Step Functions  is a HIPAA eligible service, and can be used with applications containing healthcare-related information such as personal health information (PHI). Step Functions is also compliant with SOC (System & Organization Control) measures, and the results of these third-party audits are available on the AWS SOC Compliance site(opens in a new tab).

### RECURSOS

- **Primitivas de Serviço *Built-In***
  AWS Step Functions provides ready-made steps for your workflow, called states. States can pass data to other states and microservices, handle exceptions, add timeouts, make decisions, run multiple paths in parallel, and more. Using this feature, you can remove that logic from your application.

- **Integração com Serviços AWS**
  You can configure your Step Functions workflow to call other AWS services such as:
  - Compute services, such as AWS Lambda, Amazon Elastic Container Service (Amazon ECS), Amazon Elastic Kubernetes Service (Amazon EKS), and AWS Fargate
  - Database services (Amazon DynamoDB)
  - Messaging services, such as Amazon Simple Notification Service (Amazon SNS) and Amazon Simple Queue Service (Amazon SQS)
  - Data processing and analytics services, such as Amazon Athena, AWS Batch, AWS Glue, Amazon EMR, and AWS Glue DataBrew
  - Machine learning services (Amazon SageMaker)
  - APIs created by Amazon API Gateway
  - AWS SDK integrations to call over two hundred AWS services

- **Tratamento de Erros *Built-In***
  AWS Step Functions automatically handles errors and exceptions with built-in try/catch and retry, whether the task takes seconds or months to complete. You can automatically retry failed or timed-out tasks, respond differently to different types of errors, and recover gracefully by falling back to designated cleanup and recovery code.

- **Histórico de Execuções**
  AWS Step Functions delivers real-time diagnostics and dashboards, integrates with Amazon CloudWatch and AWS CloudTrail, and logs every execution, including overall state, failed steps, inputs, and outputs. If things go wrong, you can quickly identify not only where, but why, and quickly troubleshoot and remediate failures.

- **Monitoramento Visual**
  Launching an application is as simple as pressing a button, then watching the invocation of the steps visually lets you quickly verify that everything is operating in order, and as expected. The console clearly highlights errors, so you can quickly pinpoint their root-cause, and troubleshoot issues.

- **Orquestração de Alto Volume**
  AWS Step Functions has Express Workflows to support event rates greater than 100,000 per second, so you can build high volume, short duration workflows. Express Workflows can coordinate AWS Lambda function invocations, AWS IoT Rules Engine actions, and Amazon EventBridge events.

AWS Step Functions coordinates your existing Lambda functions and microservices into robust applications so you can quickly rewire them into new compositions. The tasks in your workflow can run anywhere, including on instances, containers, functions, and mobile devices. Using Step Functions, you can quickly create distributed applications that leverage AWS services in addition to your own microservices.

AWS Step Functions keeps your application logic strictly separated from the implementation of your application. You can add, move, swap, and reorder steps without having to make changes to your business logic. Through this separation, your workflows gain modularity, simplified maintenance, scalability, and reuse of code.

In AWS Step Functions, you define your workflows in the Amazon States Language.

### TIPOS DE ESTADO

#### PASS STATE

A Pass state passes its input to its output, without performing work. Pass states are useful when constructing and debugging state machines.

#### TASK STATE

A Task state represents a single unit of work performed by a state machine. Tasks perform all work in your state machine. A task performs work by using an activity or an AWS Lambda function, or by passing parameters to the API actions of other services.

#### CHOICE STATE

A Choice state adds branching logic to a state machine.

#### WAIT STATE

A Wait state delays the state machine from continuing for a specified time. You can choose either a relative time, specified in seconds from when the state begins, or an absolute end time, specified as a timestamp.

#### SUCCEED STATE

A Succeed state stops an activity successfully. The Succeed state is a useful target for Choice state branches that don't do anything except stop the activity. Because Succeed states are terminal states, they have no Next field, and don't need an End field.

#### FAIL STATE

A Fail state stops the activity of the state machine and marks it as a failure, unless it is caught by a Catch block.

#### PARALLEL STATE

The Parallel state can be used to create parallel branches of activity in your state machine.

#### MAP STATE

The Map state can be used to run a set of steps for each element of an input array. While the Parallel state invokes multiple branches of steps using the same input, a Map state will invoke the same steps for multiple entries of an array in the state input.

## AMAZON STATES LANGUAGE

The Amazon States Language is a JSON-based, structured language used to define your state machine. Using Amazon States Language, you create workflows. Workflows are a collection of states that can do work (Task states), determine which states to transition to next (Choice states), or stop an activity with an error (Fail states), and so on. The Step Functions console provides a graphical representation of that state machine to help visualize your application logic.

```json
{
    "Comment": "An example of the Amazon States Language using a choice state.",
    "StartAt": "FirstState",
    "States": {
        "FirstState": {
        "Type": "Task",
        "Resource": "arn:aws:lambda:us-east-1:123456789012:function:FUNCTION_NAME",
        "Next": "ChoiceState"
        },
        "ChoiceState": {
        "Type" : "Choice",
        "Choices": [
            {
            "Variable": "$.foo",
            "NumericEquals": 1,
            "Next": "FirstMatchState"
            },
            {
            "Variable": "$.foo",
            "NumericEquals": 2,
            "Next": "SecondMatchState"
            }
        ],
        "Default": "DefaultState"
        },

        "FirstMatchState": {
        "Type" : "Task",
        "Resource": "arn:aws:lambda:us-east-1:123456789012:function:OnFirstMatch",
        "Next": "NextState"
        },

        "SecondMatchState": {
        "Type" : "Task",
        "Resource": "arn:aws:lambda:us-east-1:123456789012:function:OnSecondMatch",
        "Next": "NextState"
        },

        "DefaultState": {
        "Type": "Fail",
        "Error": "DefaultStateError",
        "Cause": "No Matches!"
        },

        "NextState": {
        "Type": "Task",
        "Resource": "arn:aws:lambda:us-east-1:123456789012:function:FUNCTION_NAME",
        "End": true
        }
    }
}
```

### TRANSIÇÕES | *TRANSITIONS*

Transitions link states together, defining the control flow for the state machine. When a state machine is invoked, the system begins with the state referenced in the top-level "StartAt" field. This field is a string value that must match the name of one of the states exactly. It is case sensitive. 

All non-terminal states must have a Next field, except for the Choice state. After initiating a state, AWS Step Functions uses the value of the Next field to determine the next state. Next fields also specify state names as strings, and must match the name of a state specified in the state machine description exactly.

States can have multiple incoming transitions from other states. The process repeats itself until it reaches a terminal state, a Success or Fail state, or until a runtime error occurs.

### CHAVES MAIS COMUNS

- `StartAt` (Obrigatória)
  This is a case-sensitive string that must match the name of one of the state objects exactly. This field value indicates the task or the state where the workflow starts.

- `States` (Obrigatória)
  This is an object containing a comma-delimited set of states.

- `Type` (Obrigatória)
  This is the state's type.

- `OutputPath` (Opcional)
  This is a path that selects a portion of the state's input to be passed to the state's output. If omitted, it has the value $, which designates the entire input.

- `Next` (Opcional)
  This is the name of the next state to be run when the current state finishes. Some state types, such as Choice, allow multiple transition states.

- `TimeoutSeconds` (Opcional)
  This is the maximum number of seconds an activity of the state machine can run. If it runs longer than the specified time, the activity fails with a States.Timeout error.

- `InputPath` (Opcional)
  This is a path that selects a portion of the state's input to be passed to the state's task for processing. If omitted, it has the value $, which designates the entire input.

- End (Obrigatória)
  This designates this state as a terminal state and ends the activity if set to true. There can be any number of terminal states per state machine. Next and End can only be used once each in a state.

### SUPORTE ÀS EXPRESSÕES DE CAMINHO JSON

Step Functions, when invoked, receives a JSON text as input and passes that input to the first state in the workflow. Individual states receive JSON as input and usually pass JSON as output to the next state. Step Functions can be effectively designed not only by understanding the flow of data from one state to another but also by  knowing how to manipulate and filter the data. The fields that filter and control the flow from state to state in the Amazon States Language are:

- InputPath
- ResultPath
- OutputPath
- Parameters
- ResultSelector

### FUNÇÕES INTRÍNSECAS | *INTRINSIC FUNCTIONS*

The Amazon States Language provides several intrinsic functions to allow basic operations without Task states. Intrinsic functions are constructs that look like functions in programming languages and can be used to help Payload Builders process the data going to and from Task Resources. An intrinsic function must be a string and must begin with an intrinsic function name.

- `States.Format`
  This intrinsic function takes one or more arguments. The value of the first must be a string, which may include zero or more instances of the character sequence.

- ``

## REFERÊNCIAS

AMAZON. **Amazon States Language**. Amazon.com Inc., 2016. Disponível em: <[states-language.net](https://states-language.net/)>.

AMAZON. **Step Functions** in: Developer Guide. Amazon Web Services, Inc., 2024. Disponível em: <[docs.aws.amazon.com/pdfs/step-functions](https://docs.aws.amazon.com/pdfs/step-functions/latest/dg/step-functions-dg.pdf#welcome)>.
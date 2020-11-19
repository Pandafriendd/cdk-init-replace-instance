import json
import pytest

from aws_cdk import core
from cdk-instance.cdk_instance_stack import CdkInstanceStack


def get_template():
    app = core.App()
    CdkInstanceStack(app, "cdk-instance")
    return json.dumps(app.synth().get_stack("cdk-instance").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())

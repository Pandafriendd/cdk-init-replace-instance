#!/usr/bin/env python3

from aws_cdk import core

from cdk_instance.cdk_instance_stack import CdkInstanceStack


import os

app = core.App()
CdkInstanceStack(app, "cdk-instance", env=core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"]))

app.synth()

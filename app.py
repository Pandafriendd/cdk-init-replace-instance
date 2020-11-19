#!/usr/bin/env python3

from aws_cdk import core

from cdk_instance.cdk_instance_stack import CdkInstanceStack


app = core.App()
CdkInstanceStack(app, "cdk-instance", env={'region': 'us-west-2'})

app.synth()

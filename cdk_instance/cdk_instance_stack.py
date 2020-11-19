from aws_cdk import (
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    core
)


class CdkInstanceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        all_ec2_instances = []
        
        vpc = ec2.Vpc.from_lookup(self,"test",is_default=True) 

        cfn_init_config_sets = {
            "default": ["ssm-agent"]
        }

        cfn_init_configs = {
                    "ssm-agent": ec2.InitConfig([
                        # ec2.InitPackage.yum(f'https://s3.{self.region}.amazonaws.com/amazon-ssm-{self.region}/latest/linux_amd64/amazon-ssm-agent.rpm'),
                        ec2.InitService.enable(service_name="amazon-ssm-agent"),
                        ec2.InitCommand.shell_command("sudo systemctl start amazon-ssm-agent")
                    ])
                    
                }

        cfninit_user_data = ec2.UserData.custom('\n'.join([
            "#!/bin/bash",
            "sudo ln -s /usr/local/lib/python2.7/site-packages/cfnbootstrap /usr/lib/python2.7/site-packages/cfnbootstrap"
        ]))
        
        
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation     = ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition        = ec2.AmazonLinuxEdition.STANDARD,
            virtualization = ec2.AmazonLinuxVirt.HVM,
            storage        = ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        oem_rhel_server_name = "OEM-RHEL Server CDK"
        oem_rhel_server = ec2.Instance(self, oem_rhel_server_name,
                                  instance_type=ec2.InstanceType("t3.large"),
                                  machine_image=amzn_linux,
                                  vpc=vpc,
                                  instance_name=oem_rhel_server_name,
                                  user_data_causes_replacement=True,
                                  user_data=cfninit_user_data,
                                  init=ec2.CloudFormationInit.from_config_sets(
                                      config_sets=cfn_init_config_sets,
                                      configs=cfn_init_configs
                                  )
                                  )
                                  
        all_ec2_instances.append(oem_rhel_server)
        
        cfn_init_config_sets2 = {
            "default": ["ssm-agent"]
        }

        cfn_init_configs2 = {
                    "ssm-agent": ec2.InitConfig([
                        ec2.InitService.enable(service_name="amazon-ssm-agent"),
                        ec2.InitCommand.shell_command("sudo systemctl start amazon-ssm-agent")
                    ])
                    
                }

        cfninit_user_data2 = ec2.UserData.custom('\n'.join([
            "#!/bin/bash",
            "sudo ln -s /usr/local/lib/python2.7/site-packages/cfnbootstrap /usr/lib/python2.7/site-packages/cfnbootstrap"
        ]))
        
        syslog_server_name = "Syslog Server CDK"
        syslog_server = ec2.Instance(
            self, syslog_server_name,
            instance_type=ec2.InstanceType("t3.large"),
            machine_image=amzn_linux,
            vpc=vpc,
            instance_name=syslog_server_name,
            user_data_causes_replacement=True,
                                  user_data=cfninit_user_data2,
                                  init=ec2.CloudFormationInit.from_config_sets(
                                      config_sets=cfn_init_config_sets2,
                                      configs=cfn_init_configs2
                                  )
                                  )
                                  
        all_ec2_instances.append(syslog_server)

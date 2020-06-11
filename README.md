# snapshotalyzer-30000
Demo project to manage AWS EC2 instance snapshots

## About

This project is a demo from AcloudGuru and uses boto to manage AWS EC2 instances

## Configuring

Shotty uses the configuration created by the AWS CLI  e.g.

'aws configure --profile shotty'

##running

'Pipenv run python shotty/shotty.py <command> <subcommand>
 <--project="TAG FOR PROJECT"''

*command* is instances, volumes or snapshots
*subcommand depends upon command
*project* is optional

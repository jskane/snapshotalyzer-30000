import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
	if project:
		filters=[{'Name':'tag:Project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)

	#	print("in filtered case")
	else:
		instances = ec2.instances.all()
	#	print("else case")
	return instances

@click.group()
def instances():
	"""Commands for instances"""
@instances.command('list')

@click.option('--project', default=None,
	help="only instances for project (tag project:<name>)")
def list_instances(project):
	"List EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		tags = { t['Key']: t['Value'] for t in i.tags or [] }
		print(', '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
			tags.get('Project', '<no project>')
			)))
	return


@instances.command('stop')
@click.option('--project',default="Valkyrie_jskane",
	help = 'only instance for project')
def stop_instances(project):
	"Stop EC2 instances"
	instances = filter_instances(project)
	for i in instances:
		print("Stopping {0}...".format(i.id))	
		i.stop()
	return
		
@instances.command('start')
@click.option('--project',default="Valkyrie_jskane",
	help = 'only instance for project')
def start_instances(project):
	"Start EC2 instances"
	instances = filter_instances(project)
	for i in instances:
		print("Starting {0}...".format(i.id))	
		i.start()
	return		

if __name__ == '__main__':
	instances()



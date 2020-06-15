import boto3
import botocore
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
def cli():
	"""Shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
	"""Commands for Snapshots"""

@snapshots.command('list')

@click.option('--project', default='Valkyrie_jskane',
	help="only snapshots for project (tag project:<name>)")

@click.option('--all', 'list_all', default=False, is_flag=True,
	help="list all snapshots, not just current ones")

def list_snapshots(project, list_all):
	"List EC2 snapshots"

	instances = filter_instances(project)

	for i in instances:
		for v  in i.volumes.all():
			for s in v.snapshots.all():
				print(", ".join((
	    			s.id,
	    			v.id,
	    			i.id,
	    			s.state,
	    			s.progress,
	    			s.start_time.strftime("%c")
	    		)))
				if s.state == 'completed' and not list_all: break
	return



@cli.group('volumes')
def volumes():
	"""Commands for volumes"""

@volumes.command('list')

@click.option('--project', default='Valkyrie_jskane',
	help="only volumes for project (tag project:<name>)")

def list_volumes(project):
	"List EC2 volumes"

	instances = filter_instances(project)

	for i in instances:
	    for v  in i.volumes.all():
	    	print(", ".join((
	    		v.id,
	    		i.id,
	    		v.state,
        		str(v.size) + "GiB",
        		v.encrypted and "Encrypted" or "Not Encrypted"
        	)))
	return    	

@cli.group('instances')
def instances():
	"""Commands for instances"""


@instances.command('snapshot',
	help="Create snapshots of all Volumes")
@click.option('--project', default='Valkyrie_jskane',
	help="only instances for project (tag project:<name>)")
def create_snapshots(project):
	"Create snapshots for EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		
		print("Stopping...{0}".format(i.id))
		i.stop()
		i.wait_until_stopped()

		for v in i.volumes.all():
			print("   Creating Snapshot of {0}".format(v.id))
			v.create_snapshot(Description="create by SnapshotAlyzer 30000")
		
		print("Starting...{0}".format(i.id))
		i.start()
		i.wait_until_running()
		print("Job's done!!!")
	return






@instances.command('list')

@click.option('--project', default='Valkyrie_jskane',
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
		try:
			i.stop()
		except botocore.exceptions.ClientError as e:
			print("Could not stop {0}.".format(i.id) + str(e))
			continue
	return
		
@instances.command('start')
@click.option('--project',default="Valkyrie_jskane",
	help = 'only instance for project')
def start_instances(project):
	"Start EC2 instances"
	instances = filter_instances(project)
	for i in instances:
		print("Starting {0}...".format(i.id))
		try:
			i.start()
		except botocore.exceptions.ClientError as e:
			print("Could not start {0}.".format(i.id) + str(e))
			continue	
	
	return		

if __name__ == '__main__':
	cli()




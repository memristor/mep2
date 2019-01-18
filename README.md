# Mep2 - Eurobot 2017+ competition platform

# Getting Started

## folder structure:
- ![][folder] core
- ![][folder] modules
	- ![][folder] drivers
	- ![][folder] sensors
	- ![][folder] processors
	- ![][folder] services
	- ![][folder] schedulers
- ![][folder] robots
	- ![][folder] robot1
		- config.py
		- ![][folder] strategies
			- ![][folder] strategy1
				- init.py
				- task1.py
				- task2.py
	- ![][folder] robot2
		- config.py
		- ![][folder] strategies
			- ![][folder] strategy1
				- init.py
				- task1.py
				- task2.py
- main.py

[folder]: https://i.imgur.com/ntYUoBK.png "folder"


### ![][folder] core
Contains minimal code for running platform, by itself doesn't contain any robot configuration or behavior.
This part should never be changed as part of programing robot.

### ![][folder] modules
This folder contains modules which are used by robot configuration script ```config.py```.
Put here only robot independent modules, and modules should be standalone, not depending on each other 
(try to stick to this principle for modular and easy to understand code).

### ![][folder] robots
This folder contains robot specific code, configuration and strategies.
Each robot has its own folder.
If there is need for special driver which only specific robot will ever use, for example actuator code,
it should be put in same place as config.py is, but creating additional folders is also fine.

- robot configuration is always in file "config.py"
	```python
	# hello world code for driving robot
	from core.network.Can import *
	from modules.drivers.motion.Motion import *
	# use can0 CAN device for communicating with motion board (virtual or physical)
	can = Can('can0')
	# make motion driver instance and give can channel with address 0x80000258 
	#	0x80000258 is default motion board address
	motion = Motion(packet_stream=can.get_packet_stream(0x80000258))
	motion.export_cmds('r') # exports commands with namespace 'r' (r.goto, r.conf_set, ...)
	# add modules to core 
	# 	(they will have their `def run(self):` functions executed prior to task execution, 
	#	but not before config.py execution ends)
	_core.add_module([can, motion])
	```
	or just
	```python
	# hello world code for driving robot
	from modules.default_config import motion
	```
- strategies are located in folder called, well "strategies" and in its own folder. Just put here folders with strategy names.
- each strategy consists of: tasks
	- init.py - if created, will be used as initial task, use it to prepare strategy execution (setup strategy shared states or so.)
		```python
		# define states here (any other state defined other way won't be tracked and is not simulator friendly)
		State.shared_state = _State('initial value') # shared state
		a=_State(0, 'name') # task local state
		# define task execution here
		def run():
			print(a.get()) # <==> print(a.val)
			a.set('new value') # <==> a.val = 'new value'
			...
		```
		_State should only use [immutable](https://en.wikibooks.org/wiki/Python_Programming/Data_Types#Mutable_vs_Immutable_Objects) types
	- task_name.py - tasks are inserted just by putting files, only .py files are used. 
		When they are executed is entirely dependent on scheduler used and parameters given in this file.
		```python
		# define task local states here (they will be preserved if task is suspended and restarted later)
		a=_State(0, 'name')
		
		# define task local constants which are not to be changed during task execution
		points = {
			'entry_point', (0,200),
			'point1': (100,200),
			'point2': (500,200)
		}

		# define task generation here 
		#	(note: task is first generated and then executed as explained later)
		def run():
			# define task preconditions here
			if cannot_do_task():
				# by returning false, scheduler will not consider this task
				return False
			
			# for example
			path = pathfind(points['entry_point'])
			if not path:
				return False
			
			a.val = 6
			r.goto(points['point1'])
			r.goto(points['point2'])
			...

		# this part is optional
		# when task is suspended or finished, it allows cleaning up half finished task
		#	for example: 
		#		robot tried to pick something, but scheduler changed task
		#		or some event caused task suspend
		def leave():
			...
		```
		
		hello world example (used with hello world config.py), put this in init.py or some_task.py
		```python
		weight=1
		def run():
			# not necessary but useful for visualising on gui
			r.conf_set('send_status_interval', 100)
			
			# natural mathematic coordinate system
			# x - when robot orientation == 0, robot is looking at positive x axis
			# y - when robot orientation == 90, robot is looking at positive y axis
			# setting robot starting position (x,y,o), o - orientation (in degrees)
			r.setpos(0,0,0)

			# 200 mm forward
			r.forward(200)

			# 200 mm backward
			r.forward(-200)

			# move to point 200,200
			r.goto(200,200)

			# wait 1 second
			sleep(1)

			# go back to 0,0
			r.goto(0,0)

			# go to 200,0
			r.goto(200,0)

			# go back to 0,0 in reverse
			r.goto(0,0,-1)
		```

### main.py
This file as its name explains, is used as platform main function (entry point). 
Use:
```
$ ROBOT=robot1 python3 main.py strategy1
```
or
```
$ ROBOT=robot1 ./main.py strategy1
```
to launch robot named "robot1" and its strategy "strategy1"

You can try helloworld robot with helloworld strategy:
```
$ ROBOT=helloworld python3 main.py helloworld
```

# Command exporting and task execution
By default tasks don't have any commands to use, except builtin commands which are denoted by _ (underscore) prefix.
Commands have to be exported by robot configuration script (config.py) and modules included by config.py.

task builtin commands are:
- _print
- _do, _spawn
- _on, _listen, _unlisten
- _if, _else, _end_if
- _this, _label, _sync, _goto
- _task_suspend, _task_done

global builtins:
- _core - access to core instance
- _e - access to task exported stuff (everything that is available to task is available to config.py by this variable)
- _State - class available for instancing in tasks and config.py
- State - used for plugging in any global variables shared between tasks
	```python
	State.robot_loaded = _State(False, name='robot_loaded')
	```
## Task execution

Task code is executed asynchronously within state machine which is generated transparently by exported commands.

Every task must have `def run():` function defined:


for example:
```python
def run():
	print(1)
	print(2)
	print(3)
	print(4)
```
will output:
```
1
2
3
4
```
which is ok, but still isn't part of task.
Because in task asynchronous execution is used, so code here generates task, in other words it appends commands to task's own command list
to be executed later as state machine.
For example:

```python
def run():
	sleep(1)
	_print(1)
	_print(2)
	print(3)
	print(4)
```
will output:
```
3
4
(waits 1 second)
1
2
```
order of execution is wrong because there are task generation commands and immediate commands (regular python) used for printing.
`_print()` here only generates command to print something as part of task execution, while normal `print()` command prints immediately.

to fix this (by still using normal `print` command):

```python
def run():
	_print('1')
	_print('2')
	_do(print, 3) # or: _do(lambda: print(3))
	_do(print, 4) # or: _do(lambda: print(4))
```
output:
```
1
2
3
4
```
`_do()` command is used to continue generating task while task is running, in other words function given to it
	will run just like `def run():` was ran and will be able to append more commands to task.

```python
def run():
	def run_this_in_parallel():
		sleep(1)
		_print('1')
		sleep(1)
		_print('2')
		
	_spawn(run_this_in_parallel)
	
	sleep(1.1) # for stable output adding 100ms
	_do(print, 3) # or: _do(lambda: print(3))
	sleep(1)
	_do(print, 4) # or: _do(lambda: print(4))
```
output:
```
(waits 1 sec)
1
3
(waits 1 sec)
2
4
```
`_spawn()` command does just like `_do()` command but starts new command list branch and executes it in parallel (as new thread)


another way to write this is:
```python
def run():

	@_spawn
	def run_this_in_parallel():
		sleep(1)
		_print('1')
		sleep(1)
		_print('2')
	
	sleep(1.1) # for stable output adding 100ms
	
	@_do
	def _():
		print(3)
		
	sleep(1)
	
	@_do
	def _():
		print(4)
```
output (is same):
```python
(waits 1 sec)
1
3
(waits 1 sec)
2
4
```

# Exporting commands to tasks

### Regular python command, executed outside of task

```python
@_core.export_cmd
def command_name():
	print('this is sync command')
```

task:

```python
def run():
	_print('1')
	_print('2')
	print('3')
	command_name()
```
output:
```
3
this is sync command
1
2
```

to put them in correct order we have to use _do task builtin function:

```python
def run():
	_print('1')
	_print('2')
	_do(print, '3') # or: _do(lambda: print('3'))
	_do(command_name) # or: _do(lambda: command_name())
```
output:
```
1
2
3
this is sync command
```


## normal export

for example to export command "command_name" to task:
```python
def command_name():
	print('this is sync command')
_core.export_cmd(command_name)
```
is same as:

```python
@_core.export_cmd
def command_name():
	print('this is sync command')
```

```python
def run():
	command_name()
	# should output: this is sync command
```

### using command as part of task command

```python
def command_name():
	_e._do(print,'this will be part of task')
_core.export_cmd(command_name)
```
is same as:

```python
@_core.do
def command_name():
	print('this will be part of task')
_core.export_cmd(command_name)
```
or same as:
```python
@_core.export_cmd
@_core.do
def command_name():
	print('this will be part of task')
```

## renamed export

```python
def command_name():
	print('this is sync command')
_core.export_cmd('other_name', command_name)
```

or like this with decorator:

```python
@_core.export_cmd('other_name')
def command_name():
	print('this is sync command')
```

in task:

```python
def run():
	other_name()
```

## asynchronous commands
If we add parameter _future to command being exported (we can also assign it some default value to it), then function becomes asynchronous, 
it will block thread execution until _future.set_result(1) is called anywhere. Argument _future may be saved somewhere else
and finished some time later (for example when physical action is done, servo movement is done or robot reached destination or .set_exception('some message') if command failed).
This asynchronous type of command is to be used in drivers.

```python
saved_future=None
def command_name(_future):
	global saved_future
	print('this is async command')
	print('it will block until _future.set_result(1) is given')
	saved_future=_future

# lets say this function is called when response is received from hardware
def on_command_finished():
	# this will finish command and continue thread execution
	saved_future.set_result(1)
_core.export_cmd(command_name)
```

```python
def run():
	command_name()
```
output:
```
this is async command
it will block until _future.set_result(1) is given
(waits until on_command_finished is called)
```

Or:
```python
def command_name(_future):
	print('do something, but don't block execution')
	_future.set_result(1)
_core.export_cmd(command_name)
```
A reminder that decorator export style can also be used like shown in previous sections:
```python
@_core.export_cmd
def command_name(_future):
	print('do something, but don't block execution')
	_future.set_result(1)
```

From inside task result can be checked this way:
```python
def run():
	res = command_name()
	_do(lambda: print('result is:', res.val))
	# or
	_do(lambda: print('result is:', res.get()))
	# or
	_do(lambda: print('result is:', res.get_result()))
```

### simulation interface
Asynchronous commands supports simulation interface which allows it to provide information about its
execution without actually executing it. If we add _sim parameter to asynchronous command, we can define its
behavior in simulation mode. By default if simulation interface is not used, it is assumed that command does not
block (lasts 0 seconds). 

- one step simulation
```python
@_core.export_cmd
def load_robot(point, _future, _sim):
	# always put first
	if _sim:
		print('this is being executed in simulation mode')
		# do some state changes
		some_arrived_new_position = point
		_core.set_position(some_arrived_new_position)
		
		# lets say if robot is already loaded, we can return False
		#	which means that if running simulation scheduler, it won't consider executing this task
		if State.robot_loaded.val:
			return False
		
		State.robot_loaded.set(True)
		
		# must always return (to not start actually executing command)
		# 	returns how much seconds it takes to execute
		return 1
		
	# do actual command outside of simulation
	...
```

- timestep simulation:
```python
@_core.export_cmd
def load_robot(point, _future, _sim):
	# always put first
	if _sim:
		print('this is being executed in simulation mode')
		# do some state changes
		...
		
		# lets say if robot is already loaded, we can return False
		#	which means that if running simulation scheduler, it won't consider executing this task
		if State.robot_loaded.val:
			return False
		
		State.robot_loaded.set(True)
		
		start_point = _core.get_position()
		
		def next_step(t,dt):
			# do some state changes (which will be visible across task simulation, if parallel threads are present)
			some_closer_point = interpolate(start_point, point, t)
			_core.set_position( some_closer_point )
			
			if distance(point, _core.get_position()) < 1:
				# returning 0 means it is finished
				return 0
			
			# returns how much seconds to next step
			return 1
		
		# now we use tuple
		# returns how much seconds to next step
		return 1, next_step
		
	# do actual command outside of simulation
	...
```


## using namespaces for command exports:
in some cases names will clash, for example if using multiple instances of same driver, as it was case for big robot
which used 2 motion drivers (it had 2 physical motion cards, one using CAN bus, other using UART which was also in linear mode, functioning as actuator)

```python
_core.export_ns('t')
```

now anything which goes after export_ns will be located in given namespace (in this case 't')

now if we used this command before exporting other_name command, it would be accessed this way:
```python
def run():
	t.other_name()
```

## task instances
Multiple similar tasks can be created from single task, where each instance differs by few constants.
This can reduce amount of code needed to make strategy, and will make it more manageable. In case of errors, they can be
fixed in one place (in single file) and not in all separate task files. Having little code also encourages experimentation.

For example, if robot has to pick multiple objects of same type and similar way.

```python
_instances=2
points=[ (100,200), (400,500) ]
def run():
	# use _i as task number and use it for generating different task based on number
	_print('this is task number: ', _i)
	
	# operator * is parameter expansion operator
	r.goto(*points[_i]) # <=> r.goto(points[_i][0], points[_i][1])
	pick()
	
	# do something only for instance #1
	if _i == 1:
		_print('doing this only on instance: ', _i)
```

This will create 2 tasks:
- 1. task will go to point (100,200) and pick something
- 2. task will go to point (400,500) and pick something

In theory all tasks can be made from single task, but idea is to use task instancing only when minimal changes exist between instances.


# How to visualise

__Requirements: blender__

You have to install blender either from ubuntu repository or https://www.blender.org

For Ubuntu:
```bash
sudo apt-get update
sudo apt-get install blender
```

You need 3 terminals:

Open 1st terminal and type (STEP 1):
```bash
# clone pic-motion-driver repository (do this only once)
git clone https://github.com/memristor/pic-motion-driver
cd pic-motion-driver
# compile simulator (need gcc compiler)
make sim
# make virtual can0 device for communication of motion driver with mep2
sudo make dev dev=can0
# start motion driver
./sim can0
```

Open 2nd terminal and type (STEP 2):
```bash
# clone this repository (do this only once)
git clone https://github.com/memristor/mep2.git
cd mep2
./run_blender
```

Finally 3rd terminal (same directory - mep2), run this (each time you run strategy) (STEP 3):
```bash
# run helloworld strategy
ROBOT=helloworld ./main.py helloworld
# or
ROBOT=helloworld python3 main.py helloworld
```

Useful shortcuts for blender are:
- numpad 7 (top view)
- numpad 5 (toggle orthogonal projection and back to perspective projection)
- numpad 0 (jump to camera view and back)
- rotate with by holding middle mouse button and moving mouse
- strafe by holding shift + middle mouse button and moving mouse

Read coordinates:
- to read coordinates, use 3D cursor by clicking left mouse button anywhere on playing field.
- coordinates are scaled to match those that we use in mep2 (in millimeters)

### Multiple Robots (3 robots example)

You can simulate like this up to 10 robots.

We need 3 robots in robots dir. Lets name them robot1, robot2, robot3
```
├── core
├── modules
├── robots
│   ├── robot1
│   │   ├── config.py
│   │   └── strategies
│   │       └── simple
│   │           ├── 1_task.py
│   │           └── init.py
│   ├── robot2
│   │   ├── config.py
│   │   └── strategies
│   │       └── simple
│   │           ├── 1_task.py
│   │           └── init.py
│   ├── robot3
│   │   ├── config.py
│   │   └── strategies
│   │       └── simple
│   │           ├── 1_task.py
│   │           └── init.py
```

```
from modules.default_config import motion, pathfind
motion.can.iface='can0'
```
```
from modules.default_config import motion, pathfind
motion.can.iface='can1'
```
```
from modules.default_config import motion, pathfind
motion.can.iface='can2'
```

Do step #1 for each robot:
```bash
cd pic-motion-driver
sudo make dev dev=can0
sudo make dev dev=can1
sudo make dev dev=can2
./sim can0 & # with & runs in background
./sim can1 & # with & runs in background
./sim can2
pkill sim
```

Repeat step #2 here

Run 3 robots:
```bash
# 1st terminal
ROBOT=robot1 ./main.py simple
# 2nd terminal
ROBOT=robot2 ./main.py simple
# 3rd terminal
ROBOT=robot3 ./main.py simple
```


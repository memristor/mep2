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
		# which means that if running simulation scheduler, it won't consider executing this task
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

__Requirements: blender 2.79, Tkinter, libboost-python-dev, g++__

Blender:

You have to install blender 2.79 https://www.blender.org
This version is OK
https://download.blender.org/release/Blender2.79/latest/blender-2.79-e045fe53f1b0-linux-glibc217-x86_64.tar.bz2

And after that write the path to the Blender directory in the "run_blender" file.
For example: path="/home/milos/Documents/memra/blender/"

Tkinter and libboost:

	sudo apt-get update
	
	sudo apt-get install python3-tk
	
	sudo apt-get install libboost-python-dev

        sudo apt-get install g++
	



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

### Real robot in simulation with simulated ones
Also you can simulate robot with real robot in similar way. When you connect on wifi network
where robot is connected and is running mep2, when you run blender that robot will automatically
connect to it, and thus when you run additional mep2 on your machine, you will put them in same
virtual terrain that real robot will react to simulated robot.

# Going deeper

In previous section of this tutorial we have learned how to run basic task where robot
does some sequence of actions without actually caring much about what happens with robot in reality.
In this section we learn how to respond to outside influence, how to make module, how to
use simulation mode and simulation scheduler to automatically optimize strategy during its
execution and thus be able to avoid opponents interference.


## Task commands

### _goto
- this thread:
	- _goto('label') - jump to label
	- _goto(offset=2) - skip next command
- other thread:
	- _goto('label', ref='some_other_thread') - make some_other_thread jump to label
	- _goto(offset=0, ref='some_other_thread') - make some_other_thread repeat last command

This example is very simple and useless in practice (robot moves forward and backward forever):
```python
def run():
	_label('test')
	r.forward(100)
	r.forward(-100)
	_goto('test')
```
This one was useless because task never ends, no loop escape plan.

Now lets check useful case.
```python
def run():
	@_spawn
	def unload_something():
		unload()
		sleep(5)
		 # makes main thread jump to unload_done and leave loop
		_goto('unload_done', ref='main')
		
	_label('test')
	r.turn(10)
	r.turn(-10)
	_goto('test')
	
	_label('unload_done')
```

### naming thread
```python
def run():
	@_spawn(_name='some_name')
	def t():
		sleep(5)
		_label('skip_print')
		_print('some_name is done')
		
	# in previous thread jump to label 'skip_print'
	_goto('skip_print', _ref='some_name')
	
	sleep(1)
```

### _sync
Stops current or other thread (ref=some_thread) until some action wakes it up.

```python
_sync()         - wait forever (or until _wake)
_sync('str') 	- wait for anything to hit label
_sync(a)        - wait single thread to finish
_sync([a,b,c]) 	- wait for all given threads to finish
```


```python
def run():
	@_spawn(_name='some_name')
	def t():
		sleep(5)
		_print('hey')
	
	# pause thread named 'some_name'
	_sync(_ref='some_name')
	
	sleep(10)
	# wake thread 'some_name'
	_wake(ref='some_name')
	
```

_sync('str') - stops current thread until some thread enters label named 'str'
```python
def run():
	@_spawn
	def t():
		sleep(5)
		_print('hey')
		_label('some_label')
	
	# wait until some thread entered label 'some_label'
	_sync('some_label')
	_print('this will be printed after 5 secs')
```


## Block commands (with ...)

### with _pick_best()

This function uses simulator to evaluate which of the given paths should robot take (it will pick shortest)
```python
def run():
	r.goto(200,80)
	# simulate every choice, and pick one with shortest time 
	# or highest score if score function is used
	with _pick_best(): 
		r.goto(100,200) # choice 1
		r.goto(200,100) # choice 2
		r.turn(10) # choice 3
		@_do
		def choice4(): # choice 4
			r.goto(100,10)
			sleep(1)
			r.goto(50,100)
	r.look(0,0)
	r.forward(100)
```

### with disabled('event_name')

With this command we can block certain events from hitting _listen-ers that are listening to them.
Also listener can be named, so that not all handlers listening to same event are blocked but only one.

```python
with disabled('collision'):
	# this will let our robot crash into closest robot detected :)
	bot = _core.entities.get_closest_entity('robot')
	r.goto(*bot.point)
```

## Events

### Using events outside of task
#### _core.listen('event_name', function, params...)

Decorator style is also supported:
```python
@_core.listen('task:done')
def on_task_done(task):
	print('task', task, 'just finished')
```

*params...* - here are used only for listening (subscribing) to service, for example:
```python
def function():
	print('called every 5th second')
_core.listen('timer', function, 5)

# or decorator style
@_core.listen('timer', 5)
def function():
	print('called every 5th second')
```
So service handles each listener according to its parameters, they are listening to same event
but with certain "filters" or requests. And this event is no longer an event but service.

```python
@_core.listen('detection', ent='robot', area=[100,100,300,300])
def on_robot_detected_stealing_our_stuff():
	# disable task pick_stuff because we suspect that opponent robot has just stolen it
	_core.task_manager.get_task('pick_stuff').disable()
```

#### _core.emit('event_name', params...)
	
This calls all listeners listening to event_name

### Using events inside of task
#### _listen('event_name', function, params...)

usage same as _core.listen, but as part of task, and is automatically unlistened when task is finished or 
thread that created it is finished.

Event listener turns into thread when any asynchronous commands are used, for example:
```python3
def run():
	@_listen('motion:stuck')
	def on_stuck():
		# pause main thread
		_sync(ref='main')
		# go backward
		r.forward(-30)
		# resume main thread
		_wake('main')
	r.goto(200,600)
```

As way to control behavior of these threads (subtasks), there are 3 options:
- _repeat="block" - block any other events while current is still running
- _repeat="replace" - stop previously running thread and start new one
- _repeat="duplicate" - start new one also (use this if you know what you are doing, because if this event occurs often, it could generate a lot of threads
	and potentially cause unwanted chaos)
	
	
#### _emit('event_name', params...)

This is mostly useless because it doesn't make sense and shouldn't be used :).

### List of events currently emited
- task:new task-name
- task:done task-name
- collision msg => msg is either 'danger' or 'safe'
- entity:new entity
- entity:refresh entity
- entity:remove entity
- sensor:new_pt sensor-point
- config:done
- strategy:done
- motion:idle
- motion:stuck
- share:state_change <old-state> <new-state>

## Schedulers

### Basic scheduler
	
This scheduler relies on parameter *weight* given in each task for determining order of their execution.
Just like with any scheduler parameter, weight doesn't have to be constant (it can be function which is then
evaluated each time new task is being scheduled). 
This parameter is set as global variable in each task:
```python
weight = 1
def run():
	...
```
Or as function like this:
```python
def weight():
	ent = _core.entity.get_closest_entity('pack')
	dist=_core.distance_to(ent.point)
	return dist
def run():
	...
```
### Simulation scheduler

Within config.py it is possible to set scheduler to be used for task choosing (default is BasicScheduler):
```python
from modules.default_config import sim_sched
```
or equivalently
```python
from core.schedulers.SimulationScheduler import *
_core.task_manager.set_scheduler( SimulationScheduler() )
```
Now with this activated, task will be chosen based on how much points will it take and based on amount
of time it takes to do it. Score = points / time.
Each time new task is picked, all ready tasks are simulated and evaluated by commands simulation interface,
to determine whick task to be used next. This is very useful because it makes writing strategy more elegant,
with less code, without needing to worry much about its priority constants and functions.

### Writing new scheduler

In case you want to write your own scheduler consider how BasicScheduler is made:
```python
from core.Util import get_task_param
class BasicScheduler:
	def __init__(self, mode='weight'):
		self.mode=mode
	
	def score_func(self, task):
		return get_task_param(task, self.mode)
		
	def pick_task(self, tasks):
		tasks = [task for task in tasks if hasattr(task.module, self.mode)]
		if tasks:
			tasks=sorted(tasks, key=self.score_func, reverse=(self.mode == 'weight'))
			for task in tasks:
				if _core.task_manager.set_task(task.name):
					# successfully picked task
					return True
		return False
```
Task scheduler is class with at least pick_task function.
Only requirement for task scheduler is *pick_task(self, tasks)* function which takes tasks as argument, it should use 
*_core.task_manager.set_task('task_name')* function to try pick task 
(it will return False if task returned False because of unmet preconditions) and then
returns True when task was successfully picked, or returns False when not task was picked in which case
next scheduling will take place after some determined time (in task manager). It is also possible to return
name of task to be picked, but this way preconditions are not checked, and have to be checked other way, 
by precondition parameter for example.

In task scheduler feel free to use event listeners to control task execution any time, while task is running. For example to
stop execution of tasks which are taking too long to execute, or to stop execution based on prediction
that task will execute too long after simulating task from this very moment.
you may use _core.task_manager.run_simulator() at any time when task is set or even running.
if task is already running then simulator will run from current task state to finish (it will not start from
beginning of it). Place scheduler as module in modules/schedulers directory or if scheduler is dependent on
specific robot, place it in *robot/robot-name* directory.




## Finishing task

- task is stopped (finished or suspended) when:
	1. its execution is finished
	2. _task_done() is called
	3. _task_suspend() is called
	4. scheduler switches task at some point in time
	
_task_done and _task_suspend may take parameter name of next task that is suggested, and that next task
will be forced over other tasks no matter which scheduler is used (unless that task is already finished or 
preconditions are not satisfied). Of course task scheduler may export its own function for suggesting next task.

```python
def run():
	...
	@_do
	def pick_next_pack():
		ent = _core.entity.get_closest_entity('pack')
		if not ent:
			# no more things to pick
			_task_done()
		else:
			pick_entity(ent)
```

## Robot configuration (config.py)
#### Default_config
	
It is easier to use default configuration and not care much
```python
from modules.default_config import motion, lidar, collision_wait_suspend
```
List of configs that may be used is: motion, pathfind, collision_wait_suspend, timer, share, lidar, chinch, sim_sched.
	
#### How to set scheduler

```python
from modules.default_config import sim_sched
```
or
```python
from core.schedulers.SimulationScheduler import *
_core.task_manager.set_scheduler( SimulationScheduler() )
# or some scheduler from modules directory
from motion.schedulers.SomeScheduler import *
_core.task_manager.set_scheduler( SomeScheduler() )
```
	
#### Adding Infrared sensors
BinaryInfrared(name, local_point, local_vector, packet_stream)
```python
from modules.sensors.BinaryInfrared import *
_core.add_module([
BinaryInfrared('back middle', (0,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d12)),
BinaryInfrared('back left', (0,0), (-500,0), packet_stream=can.get_packet_stream(0x80008d16)),
BinaryInfrared('front1', (0,0), (500,0), packet_stream=can.get_packet_stream(0x80008d14)),
BinaryInfrared('front2', (0,0), (500,0), packet_stream=can.get_packet_stream(0x80008d13))])
```

#### Adding default init task
This default init task is always executed on start of any strategy, 
if init.py exists in strategy it will be executed after this function.

```python
@_core.init_task
def init_task():
	_e.r.conf_set('pid_d_p', 3.7)
	_e.r.conf_set('pid_d_d', 100)
	_e.r.conf_set('pid_r_p', 4.0)
	_e.r.conf_set('pid_r_d', 150)
	_e.r.conf_set('pid_r_i', 0.013)
```

#### Task setup function
Here we can place any shared task configuration.
This is going to be start of any task except init task.

```python
@_core.task_setup_func
def on_start_of_each_task():
	@_e._listen('collision')
	def handle_collision(status):
		...
```


## Writing modules

Example of module:
```python
class ModuleName:
	def __init__(self, params):
		...
	def export_cmds(self, namespace):
		with _core.export_ns(namespace):
			_core.export_cmd('command', self.command1)
			_core.export_cmd('subtask', self.subtask)
	@_core.module_cmd
	def command1(self, params): # Note: we didn't use _future here 
		...                 # (but it is still async because of _core.module_cmd)
	@_core.do
	def subtask(self, params):
		...
	def command2(self, params, _future):
		...
	def command3(self, params, _future, _sim=0):
		if _sim:
			# eval simulation
			return done_in_secs
		
	def run(self):
		...
```

In module all functions are optional, and are used when defined.

But:
- def run(self) - is called after config is fully executed.
- def export_cmds(self, namespace)

	This is to be defined like this by convention, as module may be instanced multiple times.
	Also commands may not be directly exported to task, but rather with temporary namespace
	and redefined here, for example:
	```python
	# in config.py
	...
	motion.export_cmds('tmp_ns1')
	_core.add_module(motion)
	t=_e.tmp_ns1
	with _core.export_ns('r'):
		@_core.export_cmd
		def goto(point):
			t.goto(point[0],point[1])
		@_core.export_cmd
		def goto2(point):
			_e.sleep(1)
			t.goto(point[0],point[1])
	```
	We have just redefined our goto from motion driver as new functions r.goto and r.goto2

_core.module_cmd - saves _future to self.future and then calls this function without _future

#### Using c++ as module

**Requirement: c++ boost library (boost::python)**

File structure
```
module/service/
├── pathfinder_cpp
│   ├── Binder.cpp
│   ├── Geometry.cpp
│   ├── Geometry.hpp
│   ├── __init__.py
│   ├── Makefile
│   ├── Pathfinder.cpp
│   └── Pathfinder.hpp
└── Pathfinder.py
```

File ```pathfinder_cpp/__init__.py```:
```python
from core.Util import load_boost_cpp_module
pathfinder = load_boost_cpp_module('Pathfinder')
```

File ```Pathfinder.py```:
```python
from .pathfinder_cpp import pathfinder
class PathfinderService:
	def __init__(self):
		...
		# make instance of c++ PathfinderBinder class
		self.pathfinder = pathfinder.Pathfinder()
	def run(self):
		...
```

In Makefile use this example as template and change only *module* and *src* variables.

File ```pathfinder_cpp/Makefile```
```Makefile
module := Pathfinder

src := Binder.cpp Pathfinder.cpp

############################################

machine := $(shell uname -m)
bin/$(machine)/$(module).so: $(src)
	mkdir -p bin/$(machine)
	g++ $^ -shared -fpic $(shell python3-config --includes) -lboost_python3 -O2 -o $@

clean:
	rm -rf bin
```

Example binder (taken from actual implementation of PathfinderBinder), it
shows list and tuple usage:

File ```pathfinder_cpp/Binder.cpp```:
```c++
...
#include <boost/python.hpp>
namespace py = boost::python;
class PathfinderBinder {
	private:
		Pathfinder pf; // actual implementation of module in pure c++
	public:
		PathfinderBinder() {}
		int AddPolygon(py::list& lt, double offset) {
			// iterate list lt
			for (int i = 0; i < py::len(lt); ++i) {
				py::tuple t = py::extract<py::tuple>(lt[i]);
				int x = py::extract<int>(t[0]);
				int y = py::extract<int>(t[1]);
			}
		}
		
		void RemovePolygon(int poly_id) {
		}
		
		py::list GetPolygon(int poly_id) {
		}
		
		py::list Search(py::tuple start, py::tuple end) {
			int x1 = py::extract<int>(start[0]);
			int y1 = py::extract<int>(start[1]);
			int x2 = py::extract<int>(end[0]);
			int y2 = py::extract<int>(end[1]);
			Point pt_start = Point(x1,y1);
			Point pt_end = Point(x2,y2);
			my::Path path = pf.Search(pt_start, pt_end);
			
			py::list l;
			for(auto &pt : path) {
				l.append(py::make_tuple(pt.x, pt.y));
			}
			return l;
		}
		void Clear() {
		}
};
BOOST_PYTHON_MODULE(Pathfinder)
{
    class_<PathfinderBinder>("Pathfinder")
		.def("AddPolygon", &PathfinderBinder::AddPolygon)
		.def("RemovePolygon", &PathfinderBinder::RemovePolygon)
		.def("GetPolygon", &PathfinderBinder::GetPolygon)
		.def("Search", &PathfinderBinder::Search)
		.def("Clear", &PathfinderBinder::Clear)
		;
}
```
Of course it is possible to export bare c++ function without class (from SimpleExample link below)
```c++
#include <boost/python.hpp>
namespace py = boost::python;

std::string greet() { return "hello, world"; }
int square(int number) { return number * number; }
BOOST_PYTHON_MODULE(getting_started1)
{
    py::def("greet", greet);
    py::def("square", square);
}
```
Some links to documentation
- [boost.python](https://wiki.python.org/moin/boost.python)
- [SimpleExample](https://wiki.python.org/moin/boost.python/SimpleExample)
- [Another example](https://www.boost.org/doc/libs/1_61_0/libs/python/doc/html/tutorial/tutorial/exposing.html)

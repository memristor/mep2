# task states
RUNNING = 'running'
WAITING = 'waiting'
SUSPENDED = 'suspended'
DENIED = 'denied'
DONE = 'done'
PENDING = 'pending'
LEAVING = 'leaving'
DISABLED = 'disabled'

# future states
PENDING='pending'
FINISHED='finished'
CANCELLED='cancelled'
PAUSED='paused'

# sync flags
SYNC_UNCOND = 1 # pause/continue
SYNC_DO = 2 # none
SYNC_FUTURE = 4 # none
SYNC_THREAD = 8 # will pause/continue
SYNC_EVENT = 16 # will pause and continue
SYNC_FORCE = 32 # no pause, no cancel just block/unblock thread
SYNC_LABEL = 64 # no pause, no cancel just block/unblock thread

NEW = 0
PAUSE = 1
RESUME = 2
CANCEL = 4

# meta commands
CMD_DO = '_do'
CMD_IF = '_if'
CMD_ELIF = '_elif'
CMD_ELSE = '_else'
CMD_END_IF = '_end_if'
CMD_WHILE = '_while'
CMD_LABEL = '_label'
CMD_SYNC = '_sync'
CMD_SPAWN = '_spawn'
CMD_TASK_DONE = '_task_done'
CMD_TASK_STOP = '_task_stop'
CMD_TASK_SUSPEND = '_task_suspend'
CMD_RETURN = '_return'
CMD_ON = '_on'
CMD_LISTEN = '_listen'
CMD_UNLISTEN = '_unlisten'
CMD_WAIT = '_wait'
CMD_GOTO = '_goto'
CMD_REF = '_ref'
CMD_THIS = '_this'
CMD_WAKE = '_wake'
CMD_EMIT = '_emit'
CMD_WHILE = '_while'
CMD_PICK_BEST = '_pick_best'
CMD_WAKE = '_wake'
CMD_REDO = '_redo'
CMD_PARALLEL = '_parallel'
CMD_REPEAT = '_repeat'
CMD_RESET_LABEL = '_reset_label'

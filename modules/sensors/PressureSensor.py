from core.Convert import *
class PressureSensor:
	def __init__(self, name, id, packet_stream=None):
		self.ps = None
		self.id = id
		self.name = name
		self.future = None
		if packet_stream:
			self.set_packet_stream(packet_stream)
	
	
	def on_recv(self, pkt):
		if len(pkt) >= 4:
			self.value = lu16l(pkt,0)
			self.future.set_result( self.value < 0x0400 )
			#self.future.set_result( self.value  )

	def export_cmds(self, ns=''):
		with _core.export_ns(ns):
			_core.export_cmd('picked', self.picked)
		
	@_core.module_cmd
	def picked(self):
		self.ps.send(bytes([self.id]))
		if State.sensor_sim:
			from tkinter import Tk, Label, Button
 
			window = Tk()
			window.title("Did the pump catch something?")
			window.geometry('400x150')

			self.is_yes_clicked = False

			def clicked_yes():
				self.is_yes_clicked = True
				window.destroy()

			def clicked_no():
				window.destroy()

			btn_yes = Button(window, text="Yes", command=clicked_yes)
			btn_no = Button(window, text="No", command=clicked_no)

			btn_yes.grid(column=1, row=0)
			btn_no.grid(column=2, row=0)
			
			window.mainloop()

			result = 1 if self.is_yes_clicked else 0

			self.future.set_result(result)


		elif State.sim:
			self.future.set_result(1)

	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps

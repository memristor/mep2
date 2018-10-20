from core.convert import l16
from core.Util import AABB, point_distance, add_pt, point_int
import math
class Lidar:
	
	def __init__(self, tolerance=300, tune_angle=0, packet_stream=None):
		self.name = 'lidar'
		self.set_packet_stream(packet_stream)
		self.tune_angle = tune_angle
		self.points = 0
		self.sensor_position = [0,0]
		self.prevPoint = None
		self.tolerance = tolerance
		self.aabb = AABB()
		
	def on_recv(self,pkt):
		angle = l16(pkt, 0)
		dist = l16(pkt, 2)
		deg_angle = angle + self.tune_angle
		#  if dist < 300:
			#  print('lidar:', dist, deg_angle)
		rad_angle = math.radians(deg_angle)
		vector = [math.cos(rad_angle) * dist, math.sin(rad_angle) * dist]
			
		self.processPoint(vector)
	
	def processPoint(self, vec):
		
		pt = vec
		if self.points == 0:
			# minx, maxx, miny, maxy
			self.aabb = AABB(pt[0], pt[1])
			self.points += 1
			self.prevPoint = pt
		elif point_distance(pt, self.prevPoint) < self.tolerance:
			self.aabb.put(pt[0], pt[1])
		else:
			if all((i < 300 for i in self.aabb.get_size())):
				pt = point_int( self.aabb.get_midpoint() )
				
				#  print('new detection: ', pt)
				self.sensor_map.add_sensor_point('lidar', self.name, self.sensor_position, add_pt(self.sensor_position, vec))
			self.points = 0
		
		
			
	def set_packet_stream(self, ps):
		if not ps:
			return
		ps.recv = self.on_recv
		self.ps = ps
		
	def run(self):
		self.sensor_map = self.core.sensors



'''
_addPointToPolyGenerator(angle, distance) {
        let point = new Point(0, distance);
        point.rotateAroundZero(angle);

        if (this._poly.polyPointsCount === 0) {
            if (distance < 2000) {
                this._poly.maxX = point.getX();
                this._poly.minX = point.getX();
                this._poly.maxY = point.getY();
                this._poly.minY = point.getY();
                this._poly.polyPointsCount++;
            }
        }
        else if (point.getDistance(this._poly.previousPoint) < this.config.tolerance) {
            if (point.getX() > this._poly.maxX) this._poly.maxX = point.getX();
            if (point.getX() < this._poly.minX) this._poly.minX = point.getX();
            if (point.getY() > this._poly.maxY) this._poly.maxY = point.getY();
            if (point.getY() < this._poly.minY) this._poly.minY = point.getY();
            this._poly.polyPointsCount++;
        }
        else {
            if (this._poly.maxY - this._poly.minY < 400 && this._poly.maxX - this._poly.minX < 400) {
                let offsetX = (this.config.volume - (this._poly.maxX - this._poly.minX) / 2);
                let offsetY = (this.config.volume - (this._poly.maxY - this._poly.minY) / 2);
                let polyPoints = [
                    new Point(this._poly.minX - offsetX, this._poly.minY - offsetY),
                    new Point(this._poly.maxX + offsetX, this._poly.minY - offsetY),
                    new Point(this._poly.maxX + offsetX, this._poly.maxY + offsetY),
                    new Point(this._poly.minX - offsetX, this._poly.maxY + offsetY),
                ];
                let polygon = new Polygon(this.name, Mep.Config.get('obstacleMaxPeriod'), polyPoints);
                let poi = new Point((this._poly.minX + this._poly.maxX) / 2, (this._poly.minY + this._poly.maxY) / 2);

                /**
                 * Position changed event.
                 * @event drivers.lidar.LidarDriver#obstacleDetected
                 * @property {String} driverName Unique name of a driver
                 * @property {misc.Point} poi Point which is part of obstacle
                 * @property {misc.Polygon} polygon Approximation of the obstacle
                 * @property {Boolean} detected True if obstacle is detected
                 */
                this.emit('obstacleDetected',
                    this.name,
                    poi,
                    polygon,
                    true
                );
            }
            this._poly.polyPointsCount = 0;
        }

        this._poly.previousPoint = point;
    }
'''

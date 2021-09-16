from shapely.geometry import LineString
from altprint.printable import BasePrint
from altprint.flow import extrude, calculate

class GcodeExporter:

    def __init__(self):
        self.gcode_content: list[str] = []
        self.head_x: float = 0.0
        self.head_y: float = 0.0
        self.min_jump: float = 1

    def segment(self, x, y, z, e, v) -> str:
        segment = []
        segment.append('; segment\n')
        segment.append('G92 E0.0000\n')
        segment.append('G1 Z{0:.3f} F{1:.3f}\n'.format(z, v))
        segment.append('G1 X{0:.3f} Y{1:.3f}\n'.format(x[0], y[0]))
        for i in range(len(x)-1):
            segment.append('G1 X{0:.3f} Y{1:.3f} E{2:.4f}\n'.format(x[i+1], y[i+1], e[i+1]))
        segment = "".join(segment)
        return segment

    def jump(self, x, y, v=12000) -> str:
        jump = []
        jump.append('; jumping\n')
        jump.append('G92 E3.0000\n')
        jump.append('G1 E0 F2400\n')
        jump.append('G1 X{0:.3f} Y{1:.3f} F{2:.3f}\n'.format(x, y, v))
        jump.append('G1 E3 F2400\n')
        jump.append('G92 E0.0000\n')
        jump = "".join(jump)
        return jump

    def make_gcode(self, printable: BasePrint):
        for z, layer in printable.layers.items():
            for line in layer.perimeter:
                x, y = line.xy
                if LineString([(self.head_x, self.head_y), (x[0], y[0])]).length > self.min_jump:
                    self.gcode_content.append(self.jump(x[0], y[0]))
                self.head_x, self.head_y = x[-1], y[-1]
                e = extrude(x, y, calculate())
                self.gcode_content.append(self.segment(x, y, z, e, 3000))
            for line in layer.infill:
                x, y = line.xy
                if LineString([(self.head_x, self.head_y), (x[0], y[0])]).length > self.min_jump:
                    self.gcode_content.append(self.jump(x[0], y[0]))
                self.head_x, self.head_y = x[-1], y[-1]
                e = extrude(x, y, calculate())
                self.gcode_content.append(self.segment(x, y, z, e, 3000))

    def export_gcode(self, filename):
        with open(filename, 'w') as f:
            for gcode_block in self.gcode_content:
                f.write(gcode_block)

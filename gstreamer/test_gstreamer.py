import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from common.FPS import PERF_DATA

Gst.init(None)

global perf_data
perf_data = PERF_DATA()

def on_pad_added(decodebin, pad, data):
    sink_pad = data.get_static_pad("sink")
    if not sink_pad.is_linked():
        pad.link(sink_pad)

pipeline = Gst.Pipeline.new("pipeline")

# Create uridecodebin element
uri_decode_bin = Gst.ElementFactory.make("uridecodebin", "uri-decode-bin")
uri_decode_bin.set_property("uri", "rtsp://127.0.0.1")

# Create a sink element
sink = Gst.ElementFactory.make("fakesink", "fake_display")

# Add elements to the pipeline
pipeline.add(uri_decode_bin)
pipeline.add(sink)

# Connect the pad-added signal
uri_decode_bin.connect("pad-added", on_pad_added, sink)

# Start playing the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Run the main loop
loop = GLib.MainLoop()
GLib.timeout_add(5000, perf_data.perf_print_callback)

try:
    loop.run()
except KeyboardInterrupt:
    pass

# Clean up
pipeline.set_state(Gst.State.NULL)

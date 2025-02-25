import logging
from napari_live_recording import NapariLiveRecording

logger = logging.getLogger(__name__)

def test_mmcore_live_recording(recording_widget, qtbot):
    widget : NapariLiveRecording = recording_widget

    qtbot.addWidget(widget)

    widget.anchor.selectionWidget.camerasComboBox.combobox.setCurrentIndex(1) # MicroManager
    widget.anchor.selectionWidget.adapterComboBox.combobox.setCurrentIndex(8) # DemoCamera
    widget.anchor.selectionWidget.deviceComboBox.combobox.setCurrentIndex(0) # DCam

    widget.anchor.selectionWidget.addButton.click()
    
    # live acquisition is timed via a local timer;
    # we monitor a single timeout event to ensure that
    # we have a new layer added
    events = [widget.anchor.recordingWidget.live.toggled, widget.anchor.liveTimer.timeout]

    with qtbot.waitSignals(events, timeout=3000):
        widget.anchor.recordingWidget.live.toggle()
        assert widget.mainController.isLive == True

    widget.anchor.recordingWidget.live.toggle()
    assert widget.mainController.isLive == False    

    # the plugin when acquiring live produces a layer with the ID of the camera;
    # we can check if the layer is present or not
    layer = widget.anchor.viewer.layers["Live MyCamera:MicroManager:DemoCamera DCam"]
    assert layer is not None
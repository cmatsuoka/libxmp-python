#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
A simple modplayer in python (callback version)
Based on player_skeleton2.py by Mike Driscoll
"""

import unicodedata
import sys
import os
import wx
import wx.lib.buttons as buttons
import pyaudio
from threading import Lock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import *
 
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')
 
CHANNELS = 2
WORD_SIZE = 2
SAMPLE_RATE = 44100

class MediaPanel(wx.Panel):
    """"""
 
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
 
        self.frame = parent
        self.currentVolume = 50
        self.createMenu()
        self.layoutControls()
 
        self.currentFolder = os.getcwd()
 
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(100)
 
    def layoutControls(self):
        """
        Create and layout the widgets
        """
 
        self.player = Player()
        self.lock = Lock()
 
        # create playback slider
        self.playbackSlider = wx.Slider(self, size=wx.DefaultSize)
        self.Bind(wx.EVT_SLIDER, self.onSeek, self.playbackSlider)
 
        self.volumeCtrl = wx.Slider(self, style=wx.SL_VERTICAL|wx.SL_INVERSE)
        self.volumeCtrl.SetRange(0, 100)
        self.volumeCtrl.SetValue(self.currentVolume)
        self.volumeCtrl.Bind(wx.EVT_SLIDER, self.onSetVolume)
 
        # Create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        audioSizer = self.buildAudioBar()
 
        # layout widgets
        mainSizer.Add(self.playbackSlider, 1, wx.ALL|wx.EXPAND, 5)
        hSizer.Add(audioSizer, 0, wx.ALL|wx.CENTER, 5)
        hSizer.Add(self.volumeCtrl, 0, wx.ALL, 5)
        mainSizer.Add(hSizer)
 
        self.SetSizer(mainSizer)
        self.Layout()
 
    def buildAudioBar(self):
        """
        Builds the audio bar controls
        """
        audioBarSizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.buildBtn({'bitmap':'player_prev.png', 'handler':self.onPrev,
                       'name':'prev'},
                      audioBarSizer)
 
        # create play/pause toggle button
        img = wx.Bitmap(os.path.join(bitmapDir, "player_play.png"))
        self.playPauseBtn = buttons.GenBitmapToggleButton(self, bitmap=img, name="play")
        self.playPauseBtn.Enable(False)
 
        img = wx.Bitmap(os.path.join(bitmapDir, "player_pause.png"))
        self.playPauseBtn.SetBitmapSelected(img)
        self.playPauseBtn.SetInitialSize()
 
        self.playPauseBtn.Bind(wx.EVT_BUTTON, self.onPlay)
        audioBarSizer.Add(self.playPauseBtn, 0, wx.LEFT, 3)
 
        btnData = [{'bitmap':'player_stop.png',
                    'handler':self.onStop, 'name':'stop'},
                    {'bitmap':'player_next.png',
                     'handler':self.onNext, 'name':'next'}]
        for btn in btnData:
            self.buildBtn(btn, audioBarSizer)
 
        return audioBarSizer
 
    def buildBtn(self, btnDict, sizer):
        """"""
        bmp = btnDict['bitmap']
        handler = btnDict['handler']
 
        img = wx.Bitmap(os.path.join(bitmapDir, bmp))
        btn = buttons.GenBitmapButton(self, bitmap=img, name=btnDict['name'])
        btn.SetInitialSize()
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.LEFT, 3)
 
    def createMenu(self):
        """
        Creates a menu
        """
        menubar = wx.MenuBar()
 
        fileMenu = wx.Menu()
        open_file_menu_item = fileMenu.Append(wx.NewId(), "&Open", "Open a File")
        menubar.Append(fileMenu, '&File')
        self.frame.SetMenuBar(menubar)
        self.frame.Bind(wx.EVT_MENU, self.onBrowse, open_file_menu_item)
 
    def loadMusic(self, musicFile):
        """
        Load the music into the MediaCtrl or display an error dialog
        if the user tries to load an unsupported file type
        """

        try:
            self.mod = Module(musicFile, self.player)
        except IOError, error:
            wx.MessageBox('Unable to load {0}: {1}'.format(filename, error.strerror),
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            #self.player.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mod.len)
            self.playPauseBtn.Enable(True)
 
    def onBrowse(self, event):
        """
        Opens file dialog to browse for music
        """
        dlg = wx.FileDialog(self, message="Choose a file",
                            defaultDir=self.currentFolder, 
                            defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            path = unicodedata.normalize('NFKD', path).encode('ascii','ignore')
            self.currentFolder = os.path.dirname(path)
            self.loadMusic(path)
        dlg.Destroy()
 
    def onNext(self, event):
        """
        Not implemented!
        """
        pass
 
    def onPause(self):
        """
        Pauses the music
        """
        if self.stream.is_active():
            self.stream.stop_stream()
        else:
            self.stream.start_stream()
 
    def callback(self, in_data, frame_count, time_info, status):
        """Pyaudio callback function."""
        size = frame_count * CHANNELS * WORD_SIZE
        self.lock.acquire()
        data = self.player.play_buffer(size)
        self.lock.release()
        return (data, pyaudio.paContinue)
        data = Xmp.create_buffer(size)


    def onPlay(self, event):
        """
        Plays the music
        """
        if not event.GetIsDown():
            self.onPause()
            return
 
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
                 format = self.audio.get_format_from_width(WORD_SIZE),
                 channels = CHANNELS, rate = SAMPLE_RATE,
                 output = True, stream_callback = self.callback)

        self.player.start(SAMPLE_RATE)
        self.stream.start_stream()


        #if not self.player.Play():
        #    wx.MessageBox("Unable to Play media : Unsupported format?",
        #                  "ERROR",
        #                  wx.ICON_ERROR | wx.OK)
        #else:
        #    self.player.SetInitialSize()
        #    self.GetSizer().Layout()
        #    self.playbackSlider.SetRange(0, self.mod.len)
 
        event.Skip()
 
    def onPrev(self, event):
        """
        Not implemented!
        """
        pass
 
    def onSeek(self, event):
        """
        Seeks the media file according to the amount the slider has
        been adjusted.
        """
        offset = self.playbackSlider.GetValue()
        self.player.Seek(offset)
 
    def onSetVolume(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume = self.volumeCtrl.GetValue()
        print "setting volume to: %s" % int(self.currentVolume)
        self.player.SetVolume(self.currentVolume)
 
    def onStop(self, event):
        """
        Stops the music and resets the play button
        """
        self.playPauseBtn.SetToggle(False)
        self.stream.stop_stream()
        self.player.stop()
        self.player.end()
        self.stream.close()
        self.audio.terminate()

    def onTimer(self, event):
        """
        Keeps the player slider updated
        """
        offset = 0 #self.player.Tell()
        self.playbackSlider.SetValue(offset)
 

class MediaFrame(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Python Music Player")
        panel = MediaPanel(self)
 

if __name__ == "__main__":
    app = wx.App(False)
    frame = MediaFrame()
    frame.Show()
    app.MainLoop()

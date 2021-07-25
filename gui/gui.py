#GUI built on the Kivy framework

# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')
Config.set('postproc', 'double_tap_time', '800')

# Enables referencing to packages in parent directory  #
#   Discovered this method online at codeolives.com    #
########################################################
import os, sys
import subprocess
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
########################################################
DIVISOR = 0
from sys import platform
if platform == "linux" or platform == "linux2":
    DIVISOR = 4
elif platform == "darwin":
    DIVISOR = 8
elif platform == "win32":
    DIVISOR = 8

import kivy

import numpy as np

from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics import Rotate
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import PopMatrix, PushMatrix
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import NoTransition
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider


from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

# used for triggering events
from kivy.clock import Clock

from main import Omni
OmniSynth = Omni()

from kivy.core.window import Window
Window.fullscreen = 'auto'
#Window.show_cursor = False

knobCoords = dict()
patchList = []
patternList = []

updateSliderOn = True



slotOne = Label(size_hint = [1,0.33], color = [1,1,50,1])
slotTwo = Label(size_hint = [1,0.33], color = [0, 85, 255, 1])
slotThree = Label(size_hint = [1,0.33], color = [1,1,50,1])



#Creating very simple plot
plt.plot([1, 23, 2, 4])
plt.title('WaveForm')
plt.ylabel('yLabel')
plt.xlabel('xLabel')

# Extending FigureCanvasKivyAgg for MatPlotLib
class WaveForm(FigureCanvasKivyAgg):
    def __init__(self, **kwargs):
        super(WaveForm, self).__init__(plt.gcf(), **kwargs)

# Creating the parent class for the screens and
# defining the functions they will need to share
class MyScreens(Screen):
    def screenSel(self, screenName):
        sm.current = screenName
    def toneSel(self, tone):
        OmniSynth.synth_sel(tone, parentdir)
    def exitSel(self, *args):
        OmniSynth.exit_sel()
        exit()

# Extending the Button class for Tone Buttons
class ToneButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            OmniSynth.synth_sel(self.text, parentdir)
            OmniSynth.patchIndex = OmniSynth.patchListIndex[self.text]
            self.background_color = [0, 85, 255, 1]
            if touch.is_double_tap:
                if self.text == 'tone5':
                    sm.current = 'Tone5Page'
                else:
                    sm.current = 'KnobValPage'
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = [1, 1, 1, 1]


# Extending the Button class for LED Buttons
class LedButton(Button):
    def __init__(self, **kwargs):
        super(LedButton, self).__init__(**kwargs)
        self.active = False
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = [0, 85, 255, 1]
            if self.active:
                OmniSynth.pattern_sel(self.text, 'stop', parentdir)
                self.active = False
            else:
                OmniSynth.pattern_sel(self.text, 'start', parentdir)
                self.active = True
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = [1, 1, 1, 1]

class Page2Button(Button):
    def on_release(self, *kwargs):
        sm.current = 'PatchPage2'

class Page3Button(Button):
    def on_release(self, *kwargs):
        sm.current = 'PatchPage3'
        
class Page4Button(Button):
    def on_release(self, *kwargs):
        sm.current = 'PatchPage4'

class PatternPage2Button(Button):
    def on_release(self, *kwargs):
        sm.current = 'LedPage2'

class PatternPage3Button(Button):
    def on_release(self, *kwargs):
        sm.current = 'LedPage3'
        
class PatternPage4Button(Button):
    def on_release(self, *kwargs):
        sm.current = 'LedPage4'

class UpButton(Button):
    def on_release(self, *kwargs):
        self.moveUp()
    def moveUp(self):
        if OmniSynth.patchIndex != 0:
            if OmniSynth.patchIndex == 1:
                slotOne.text = ''
                slotTwo.text = str(patchList[0])
                slotThree.text = str(patchList[1])
                OmniSynth.patchIndex = 0
                OmniSynth.synth_sel(slotTwo.text, parentdir)
            else:
                slotThree.text = str(patchList[OmniSynth.patchIndex])
                OmniSynth.patchIndex -= 1
                slotTwo.text = str(patchList[OmniSynth.patchIndex])
                slotOne.text = str(patchList[OmniSynth.patchIndex - 1])
                OmniSynth.synth_sel(slotTwo.text, parentdir)
class DownButton(Button):
    def on_release(self, *kwargs):
        self.moveDown()
    def moveDown(self):
        if OmniSynth.patchIndex != (OmniSynth.numPatch-1):
            slotOne.text = str(patchList[OmniSynth.patchIndex])
            OmniSynth.patchIndex += 1
            slotTwo.text = str(patchList[OmniSynth.patchIndex])
            if OmniSynth.patchIndex+1 != OmniSynth.numPatch:
                slotThree.text = str(patchList[OmniSynth.patchIndex + 1])
            else:
                slotThree.text = ''
            OmniSynth.synth_sel(slotTwo.text, parentdir)


class BootScreen(MyScreens):
    def on_enter(self, **kwargs):
        Clock.schedule_once(self.changeToMain,0.5)
    def changeToMain(self, *args):
        sm.current = 'MainGUI'

# Defining all the screens for ScreenManager
class MainGUI(MyScreens):
    def __init__(self, **kwargs):
        super(MainGUI, self).__init__(**kwargs)
        self.topRightCorner = AnchorLayout(anchor_x = 'right', anchor_y = 'top')
        self.patchSelectLayout = BoxLayout(orientation = 'horizontal', size_hint = [0.499,0.395])
        self.patchSelectListLayout = BoxLayout(orientation = 'vertical', size_hint = [0.67,1])
        self.patchSelectInterfaceLayout = BoxLayout(orientation = 'vertical', size_hint = [0.23,1])
        self.firstTime = True
        
        selectUpButton = UpButton(text = 'Up')
        selectDownButton = DownButton(text = 'Down')

        self.patchSelectInterfaceLayout.add_widget(selectUpButton)
        self.patchSelectInterfaceLayout.add_widget(selectDownButton)

        self.patchSelectLayout.add_widget(self.patchSelectListLayout)
        self.patchSelectLayout.add_widget(self.patchSelectInterfaceLayout)
        self.topRightCorner.add_widget(self.patchSelectLayout)
        self.add_widget(self.topRightCorner)

    def on_pre_enter(self, **kwargs):
        OmniSynth.numPatch = len(patchList)
        if self.firstTime:
            OmniSynth.patchIndex = 0
            if OmniSynth.numPatch > 1:
                slotTwo.text = str(patch1to12[0])
                slotThree.text = str(patch1to12[1])
            else:
                if OmniSynth.numPatch == 1:
                    slotTwo.text = str(patch1to12[0])
            self.patchSelectListLayout.add_widget(slotOne)
            self.patchSelectListLayout.add_widget(slotTwo)
            self.patchSelectListLayout.add_widget(slotThree)
            self.firstTime = False
            OmniSynth.synth_sel(slotTwo.text, parentdir)
        else:
            if OmniSynth.patchIndex == 0:
                slotOne.text = ''
                slotTwo.text = patchList[0]
                slotThree.text = patchList[1]
                OmniSynth.synth_sel(slotTwo.text, parentdir)
            else:
                if OmniSynth.patchIndex == OmniSynth.numPatch-1:
                    slotOne.text = patchList[OmniSynth.patchIndex - 1]
                    slotTwo.text = patchList[OmniSynth.patchIndex]
                    slotThree.text = ''
                    OmniSynth.synth_sel(slotTwo.text, parentdir)
                else:
                    slotOne.text = patchList[OmniSynth.patchIndex - 1]
                    slotTwo.text = patchList[OmniSynth.patchIndex]
                    slotThree.text = patchList[OmniSynth.patchIndex + 1]
                    OmniSynth.synth_sel(slotTwo.text, parentdir)

class PatchPage1(MyScreens):
    def on_pre_enter(self):
        self.grid = GridLayout(size_hint = [0.8,0.87], pos_hint = {'x':0.1, 'y':0},
                                rows = 3, cols = 4, spacing = [2,2], padding = [0,0,0,30])
        for pName in patch1to12:
            self.grid.add_widget(ToneButton(text=pName, size_hint = [1,0.25]))
        if len(patch13to24) > 0:
            self.add_widget(Page2Button(text = '>', size_hint = [0.08,0.7], pos_hint = {'x':0.91, 'y':0.15}))
        self.add_widget(self.grid)

class PatchPage2(MyScreens):
    def on_pre_enter(self):
        self.grid = GridLayout(size_hint = [0.8,0.87], pos_hint = {'x':0.1, 'y':0},
                                rows = 3, cols = 4, spacing = [2,2], padding = [0,0,0,30])
        for pName in patch13to24:
            self.grid.add_widget(ToneButton(text=pName, size_hint = [1,0.25]))
        if len(patch25to36) > 0:
            self.add_widget(Page3Button(text = '>', size_hint = [0.08,0.7], pos_hint = {'x':0.91, 'y':0.15}))
        self.add_widget(self.grid)

class PatchPage3(MyScreens):
    def on_pre_enter(self):
        self.grid = GridLayout(size_hint = [0.8,0.87], pos_hint = {'x':0.1, 'y':0},
                                rows = 3, cols = 4, spacing = [2,2], padding = [0,0,0,30])
        for pName in patch25to36:
            self.grid.add_widget(ToneButton(text=pName, size_hint = [1,0.25]))
        if len(patch37to48) > 0:
            self.add_widget(Page4Button(text = '>', size_hint = [0.08,0.7], pos_hint = {'x':0.91, 'y':0.15}))
        self.add_widget(self.grid)

class PatchPage4(MyScreens):
    def on_pre_enter(self):
        self.grid = GridLayout(size_hint = [0.8,0.87], pos_hint = {'x':0.1, 'y':0},
                                rows = 3, cols = 4, spacing = [2,2], padding = [0,0,0,30])
        for pName in patch37to48:
            self.grid.add_widget(ToneButton(text=pName, size_hint = [1,0.25]))
        self.add_widget(self.grid)

class LedPage1(MyScreens):
    def on_pre_enter(self):
        self.grid = GridLayout(size_hint = [0.8,0.87], pos_hint = {'x':0.1, 'y':0},
                                rows = 3, cols = 4, spacing = [2,2], padding = [0,0,0,30])
        for pName in pattern1to12:
            self.grid.add_widget(LedButton(text=pName, size_hint = [1,0.25]))
        if len(pattern13to24) > 0:
            self.add_widget(PatternPage2Button(text = '>', size_hint = [0.08,0.7], pos_hint = {'x':0.91, 'y':0.15}))
        self.add_widget(self.grid)
class LedPage2(MyScreens):
    def on_pre_enter(self):
        self.grid = GridLayout(size_hint = [0.8,0.87], pos_hint = {'x':0.1, 'y':0},
                                rows = 3, cols = 4, spacing = [2,2], padding = [0,0,0,30])
        for pName in pattern13to24:
            self.grid.add_widget(LedButton(text=pName, size_hint = [1,0.25]))
        if len(pattern25to36) > 0:
            self.add_widget(PatternPage3Button(text = '>', size_hint = [0.08,0.7], pos_hint = {'x':0.91, 'y':0.15}))
        self.add_widget(self.grid)
class LedPage3(MyScreens):
    def on_pre_enter(self):
        self.grid = GridLayout(size_hint = [0.8,0.87], pos_hint = {'x':0.1, 'y':0},
                                rows = 3, cols = 4, spacing = [2,2], padding = [0,0,0,30])
        for pName in pattern25to36:
            self.grid.add_widget(LedButton(text=pName, size_hint = [1,0.25]))
        if len(pattern37to48) > 0:
            self.add_widget(PatternPage4Button(text = '>', size_hint = [0.08,0.7], pos_hint = {'x':0.91, 'y':0.15}))
        self.add_widget(self.grid)
class LedPage4(MyScreens):
    def on_pre_enter(self):
        self.grid = GridLayout(size_hint = [0.8,0.87], pos_hint = {'x':0.1, 'y':0},
                                rows = 3, cols = 4, spacing = [2,2], padding = [0,0,0,30])
        for pName in patch37to48:
            self.grid.add_widget(LedButton(text=pName, size_hint = [1,0.25]))
        self.add_widget(self.grid)
class WaveFormPage(MyScreens):
    pass
class MidiLearnPage(MyScreens):
    pass

class KnobImage(Image):
    def __init__(self, name, **kwargs):
        self.knob_name = name
        super(KnobImage, self).__init__(**kwargs)
#        with self.canvas:
#            self.opacity = 0.5
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if OmniSynth.mapMode:
                if len(OmniSynth.knob_table) != 0:
                    with self.canvas:
                        self.opacity = 1
                    src = OmniSynth.control_evnt[2]
                    chan = OmniSynth.control_evnt[3]
                    knobCoords[self.knob_name] = (src, chan)
                    OmniSynth.map_knob((src,chan), self.knob_name)

class IndicatorImage(Image):
    def __init__(self, name, **kwargs):
        self.knob_name = name
        super(IndicatorImage, self).__init__(**kwargs)
        # When user touches a knob and drags, that one should be updated
        self.updateMe = False
        self.hold_value = 0
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            self.rot.origin = self.center
            self.rot.angle = 0
            self.rot.axis = (0, 0, 1)
        with self.canvas.after:
            PopMatrix()
#        with self.canvas:
#            self.opacity = 0.5
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.updateMe = True
    # When the user releases from the screen, none of the knobs should update
    def on_touch_up(self, touch):
        self.updateMe = False
    def on_touch_move(self, touch):
        if self.updateMe:
            self.rot.origin = self.center
            self.hold_value -= touch.dx + touch.dy
            if self.hold_value > 155:
                self.rot.angle = 155
            else:
                if self.hold_value < -155:
                    self.rot.angle = -155
                else:
                    self.rot.angle = self.hold_value

class mySlider(Slider):
    def __init__(self, name, **kwargs):
        self.slider_name = name
        self.hold_value = 0
        super(mySlider, self).__init__(**kwargs)
# Had to "disable" the sliders to avoid touch interference
        self.disabled = True
        self.updateSliderOn = True
        self.prev_val = 0
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.updateSliderOn = False
            self.value_pos = touch.pos
            #self.hold_value = self.value + int(touch.dy/DIVISOR)
            self.hold_value = self.value
# Prevents the slider from going negative or over max (127)
            if self.hold_value < 0:
                self.hold_value = 0
            if self.hold_value > 127:
                self.hold_value = 127
            self.value = self.hold_value
            if self.slider_name in knobCoords:
                self.prev_val = OmniSynth.knob_table[knobCoords[self.slider_name]]
                OmniSynth.filter_sel( self.slider_name, self.value )

class slideButton(Button):
    def __init__(self, name, **kwargs):
        self.button_name = name
        super(slideButton, self).__init__(**kwargs)
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = [0, 85, 255, 1]
            if OmniSynth.mapMode:
                if len(OmniSynth.knob_table) != 0:
                    with self.canvas:
                        self.opacity = 1
                    src = OmniSynth.control_evnt[2]
                    chan = OmniSynth.control_evnt[3]
                    knobCoords[self.button_name] = (src, chan)
                    OmniSynth.map_knob((src,chan), self.button_name)
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = [1, 1, 1, 1]


class KnobValPage(MyScreens):
    def __init__(self, **kwargs):
        super(KnobValPage, self).__init__(**kwargs)
        self.slideList = []
        self.buttonList = []

        # "Master" layout of patch screen, will likely change to grid later
        self.layout = BoxLayout(orientation='horizontal', size_hint_y = 0.75, pos_hint = {'x':0, 'y':0.25})

        # Columns to group a knob or slider with associated control
        lpf_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        hpf_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        attack_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        decay_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        sustain_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        release_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)

        # Knob setup
        # Each knob set is a layout to allow the indicator image to be placed on top of the knob image
        lpf_knob_set = RelativeLayout(size_hint_y = 0.85)
        hpf_knob_set = RelativeLayout(size_hint_y = 0.85)
        attack_knob_set = RelativeLayout(size_hint_y = 0.85)
        decay_knob_set = RelativeLayout(size_hint_y = 0.85)
        sustain_knob_set = RelativeLayout(size_hint_y = 0.85)
        release_knob_set = RelativeLayout(size_hint_y = 0.85)

        lpf_knob = KnobImage('lpf', source = 'knobV1.png')
        lpf_indicator = IndicatorImage('lpf', source = 'indicator.png')
        lpf_label = Label(text='lpf', size_hint = [1,0.15])

        hpf_knob = KnobImage('hpf', source = 'knobV1.png')
        hpf_indicator = IndicatorImage('hpf', source = 'indicator.png')
        hpf_label = Label(text='hpf', size_hint = [1,0.15])

        attack_knob = KnobImage('attack', source = 'knobV1.png')
        attack_indicator = IndicatorImage('attack', source = 'indicator.png')
        attack_label = Label(text='attack', size_hint = [1,0.15])

        decay_knob = KnobImage('decay', source = 'knobV1.png')
        decay_indicator = IndicatorImage('decay', source = 'indicator.png')
        decay_label = Label(text='decay', size_hint = [1,0.15])

        sustain_knob = KnobImage('sustain', source = 'knobV1.png')
        sustain_indicator = IndicatorImage('sustain', source = 'indicator.png')
        sustain_label = Label(text='sustain', size_hint = [1,0.15])

        release_knob = KnobImage('release', source = 'knobV1.png')
        release_indicator = IndicatorImage('release', source = 'indicator.png')
        release_label = Label(text='release', size_hint = [1,0.15])

        # Filling the knob sets
        lpf_knob_set.add_widget(lpf_knob)
        lpf_knob_set.add_widget(lpf_indicator)
        hpf_knob_set.add_widget(hpf_knob)
        hpf_knob_set.add_widget(hpf_indicator)
        attack_knob_set.add_widget(attack_knob)
        attack_knob_set.add_widget(attack_indicator)
        decay_knob_set.add_widget(decay_knob)
        decay_knob_set.add_widget(decay_indicator)
        sustain_knob_set.add_widget(sustain_knob)
        sustain_knob_set.add_widget(sustain_indicator)
        release_knob_set.add_widget(release_knob)
        release_knob_set.add_widget(release_indicator)

        # Slider setup
        lpf_slider = mySlider('lpf', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        lpf_button = slideButton('lpf', text = 'lpf', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        
        hpf_slider = mySlider('hpf', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        hpf_button = slideButton('hpf', text = 'hpf', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        
        attack_slider = mySlider('attack', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                               size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        attack_button = slideButton('attack', text = 'attack', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        
        decay_slider = mySlider('decay', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        decay_button = slideButton('decay', text = 'decay', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        
        sustain_slider = mySlider('sustain', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        sustain_button = slideButton('sustain', text = 'sustain', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        
        release_slider = mySlider('release', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        release_button = slideButton('release', text = 'release', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        

        # Slider implementation
        lpf_layout.add_widget(lpf_slider)
        lpf_layout.add_widget(lpf_button)
        hpf_layout.add_widget(hpf_slider)
        hpf_layout.add_widget(hpf_button)
        attack_layout.add_widget(attack_slider)
        attack_layout.add_widget(attack_button)
        decay_layout.add_widget(decay_slider)
        decay_layout.add_widget(decay_button)
        sustain_layout.add_widget(sustain_slider)
        sustain_layout.add_widget(sustain_button)
        release_layout.add_widget(release_slider)
        release_layout.add_widget(release_button)

        # Knob implementation
        # lpf_layout.add_widget(lpf_knob_set)
        # lpf_layout.add_widget(lpf_label)
        # hpf_layout.add_widget(hpf_knob_set)
        # hpf_layout.add_widget(hpf_label)
        # attack_layout.add_widget(attack_knob_set)
        # attack_layout.add_widget(attack_label)
        # decay_layout.add_widget(decay_knob_set)
        # decay_layout.add_widget(decay_label)
        # sustain_layout.add_widget(sustain_knob_set)
        # sustain_layout.add_widget(sustain_label)
        # release_layout.add_widget(release_knob_set)
        # release_layout.add_widget(release_label)


        self.layout.add_widget(lpf_layout)
        self.layout.add_widget(hpf_layout)
        self.layout.add_widget(attack_layout)
        self.layout.add_widget(decay_layout)
        self.layout.add_widget(sustain_layout)
        self.layout.add_widget(release_layout)

        self.slideList.append(lpf_slider)
        self.slideList.append(hpf_slider)
        self.slideList.append(attack_slider)
        self.slideList.append(decay_slider)
        self.slideList.append(sustain_slider)
        self.slideList.append(release_slider)

        self.buttonList.append(lpf_button)
        self.buttonList.append(hpf_button)
        self.buttonList.append(attack_button)
        self.buttonList.append(decay_button)
        self.buttonList.append(sustain_button)
        self.buttonList.append(release_button)

        self.add_widget(self.layout)
        OmniSynth.firstTime = False

    def slideUpdate(self, *kwargs):
        for x in self.slideList:
            if x.slider_name in knobCoords:
                current_val = OmniSynth.knob_table[knobCoords[x.slider_name]]
    # If the last value recorded by the gui slider movement event is different from the current value, 
    # x.value should be set to current_val.
    # However, if the user moves the physical slider/knob and then attempts to set it back to that exact 
    # value once again, the value would not be accurately depicted on the GUI.
    # This is why the "and not x.updateSliderOn" must be added
    #            if x.prev_val != current_val:
    #                x.value = current_val
                if x.prev_val != current_val and not x.updateSliderOn:
                    x.updateSliderOn = True
                if x.updateSliderOn:
                    x.value = current_val
                        
    def on_enter(self):
        self.slideEvent = Clock.schedule_interval(self.slideUpdate, 1/60)
        OmniSynth.midi_learn_on = True
        OmniSynth.mapMode = False
    def on_pre_leave(self):
        self.slideEvent.cancel()
        OmniSynth.midi_learn_on = False
        OmniSynth.mapMode = False
    def learnMidi(self):
        if OmniSynth.mapMode:
            OmniSynth.mapMode = False
        else:
            OmniSynth.mapMode = True
    
class Tone5Page(MyScreens):
    def __init__(self, **kwargs):
        super(Tone5Page, self).__init__(**kwargs)
        self.slideList = []
        self.buttonList = []

        self.layout = BoxLayout(orientation='horizontal', size_hint_y = 0.75, pos_hint = {'x':0, 'y':0.25})

        lpf_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        lpf_slider = mySlider('lpf', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        lpf_button = slideButton('lpf', text = 'lpf', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        lpf_layout.add_widget(lpf_slider)
        lpf_layout.add_widget(lpf_button)

        hpf_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        hpf_slider = mySlider('hpf', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        hpf_button = slideButton('hpf', text = 'hpf', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        hpf_layout.add_widget(hpf_slider)
        hpf_layout.add_widget(hpf_button)

        attack_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        attack_slider = mySlider('attack', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        attack_button = slideButton('attack', text = 'attack', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        attack_layout.add_widget(attack_slider)
        attack_layout.add_widget(attack_button)

        decay_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        decay_slider = mySlider('decay', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        decay_button = slideButton('decay', text = 'decay', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        decay_layout.add_widget(decay_slider)
        decay_layout.add_widget(decay_button)

        sustain_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        sustain_slider = mySlider('sustain', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        sustain_button = slideButton('sustain', text = 'sustain', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        sustain_layout.add_widget(sustain_slider)
        sustain_layout.add_widget(sustain_button)

        release_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        release_slider = mySlider('release', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        release_button = slideButton('release', text = 'release', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        release_layout.add_widget(release_slider)
        release_layout.add_widget(release_button)

        mod_freq_layout = BoxLayout(orientation='vertical', size_hint_x = 0.15, spacing = 25, padding = 25)
        mod_freq_slider = mySlider('mod_freq', background_disabled_vertical = 'atlas://data/images/defaulttheme/sliderv_background',
                                cursor_disabled_image = 'sliderV3.png', orientation = 'vertical', size_hint_y = 0.75,
                                size_hint_x = 0.25, pos_hint = {'x':0.5, 'y': 0.25}, range = [0,127], step = 1)
        mod_freq_button = slideButton('mod_freq', text = 'mod_freq', size_hint_x = 0.75, size_hint_y = 0.1, pos_hint = {'x':0.17, 'y':0})
        mod_freq_layout.add_widget(mod_freq_slider)
        mod_freq_layout.add_widget(mod_freq_button)

        self.layout.add_widget(lpf_layout)
        self.layout.add_widget(hpf_layout)
        self.layout.add_widget(attack_layout)
        self.layout.add_widget(decay_layout)
        self.layout.add_widget(sustain_layout)
        self.layout.add_widget(release_layout)
        self.layout.add_widget(mod_freq_layout)

        self.slideList.append(lpf_slider)
        self.slideList.append(hpf_slider)
        self.slideList.append(attack_slider)
        self.slideList.append(decay_slider)
        self.slideList.append(sustain_slider)
        self.slideList.append(release_slider)
        self.slideList.append(mod_freq_slider)

        self.buttonList.append(lpf_button)
        self.buttonList.append(hpf_button)
        self.buttonList.append(attack_button)
        self.buttonList.append(decay_button)
        self.buttonList.append(sustain_button)
        self.buttonList.append(release_button)
        self.buttonList.append(mod_freq_slider)

        self.add_widget(self.layout)

    def slideUpdate(self, *kwargs):
        for x in self.slideList:
            if x.slider_name in knobCoords:
                current_val = OmniSynth.knob_table[knobCoords[x.slider_name]]
    # If the last value recorded by the gui slider movement event is different from the current value, 
    # x.value should be set to current_val.
    # However, if the user moves the physical slider/knob and then attempts to set it back to that exact 
    # value once again, the value would not be accurately depicted on the GUI.
    # This is why the "and not x.updateSliderOn" must be added
    #            if x.prev_val != current_val:
    #                x.value = current_val
                if x.prev_val != current_val and not x.updateSliderOn:
                    x.updateSliderOn = True
                if x.updateSliderOn:
                    x.value = current_val
                        
    def on_enter(self):
        self.slideEvent = Clock.schedule_interval(self.slideUpdate, 1/60)
        OmniSynth.midi_learn_on = True
        OmniSynth.mapMode = False
    def on_pre_leave(self):
        self.slideEvent.cancel()
        OmniSynth.midi_learn_on = False
        OmniSynth.mapMode = False
    def learnMidi(self):
        if OmniSynth.mapMode:
            OmniSynth.mapMode = False
        else:
            OmniSynth.mapMode = True
        

class OmniGui(ScreenManager):
    def __init__(self, **kwargs):
        super(OmniGui, self).__init__(**kwargs)
        #selecting the Main GUI screen for startup
        self.current = 'BootScreen'
        



class OmniApp(App):
    def build(self):
        global sm, patch1to12, patch13to24, patch25to36, patch37to48, pattern1to12, pattern13to24, pattern25to36, pattern37to48
        patch1to12 = []
        patch13to24 = []
        patch25to36 = []
        patch37to48 = []

        pattern1to12 = []
        pattern13to24 = []
        pattern25to36 = []
        pattern37to48 = []
   
     #   self.use_kivy_settings = False
        sc_main = parentdir + "/dsp/main.scd"
        subprocess.Popen(["sclang", sc_main])
        
        OmniSynth.sc_compile("patches", parentdir) # compiles all synthDefs.
        OmniSynth.synth_sel("tone1", parentdir) # selects first patch.

        sm = OmniGui(transition=NoTransition())
        event = Clock.schedule_interval(OmniSynth.open_stream, .001)
        # Iterate through patches to initialize patch selection screens
        iterator = 0
        for patch_name in os.listdir(parentdir + '/dsp/patches'):
            if patch_name.endswith('.scd'):
                patchList.append(patch_name.strip('.scd'))
                OmniSynth.patchListIndex[patch_name.strip('.scd')] = iterator
                iterator += 1
        tempPatchList = patchList
        tempPatchList = np.sort(np.array(patchList)).tolist()
        num_patches = len(patchList)
        if num_patches > 36:
            patch1to12 = tempPatchList[0:12]
            patch13to24 = tempPatchList[12:24]
            patch25to36 = tempPatchList[24:36]
            patch37to48 = tempPatchList[36:]
        else:
            if num_patches > 24:
                patch1to12 = tempPatchList[0:12]
                patch13to24 = tempPatchList[12:24]
                patch25to36 = tempPatchList[24:]
            else:
                if num_patches > 12:
                    patch1to12 = tempPatchList[0:12]
                    patch13to24 = tempPatchList[12:]
                else:
                    patch1to12 = tempPatchList
        # Same thing for patterns
        iterator = 0
        for pattern_name in os.listdir(parentdir + '/dsp/patterns/songs/song1'):
            if pattern_name.endswith('.scd'):
                patternList.append(pattern_name.strip('.scd'))
                OmniSynth.patternListIndex[pattern_name.strip('.scd')] = iterator
                iterator += 1
        tempPatternList = patternList
        tempPatternList = np.sort(np.array(patternList)).tolist()

        num_patterns = len(patternList)
        if num_patterns > 36:
            pattern1to12 = tempPatternList[0:12]
            pattern13to24 = tempPatternList[12:24]
            pattern25to36 = tempPatternList[24:36]
            pattern37to48 = tempPatternList[36:]
        else:
            if num_patterns > 24:
                pattern1to12 = tempPatternList[0:12]
                pattern13to24 = tempPatternList[12:24]
                pattern25to36 = tempPatternList[24:]
            else:
                if num_patterns > 12:
                    pattern1to12 = tempPatternList[0:12]
                    pattern13to24 = tempPatternList[12:]
                else:
                    pattern1to12 = tempPatternList
        return sm

    def build_config(self, config):
        config.setdefaults('example', {
            'boolexample': True,
            'numericexample': 10,
            'optionsexample': 'option2',
            'stringexample': 'some_string',
            'pathexample': '/some/path'})
    def build_settings(self, settings):
        settings.add_json_panel('Settings Template', self.config, filename = parentdir + '/gui/settings.json')

    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)

if __name__ == "__main__":
    OmniApp().run()
    

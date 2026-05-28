import os, sys
os.chdir(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(os.path.dirname(os.getcwd()), "libs"))
print(os.path.join(os.path.dirname(os.getcwd()), "libs"))
import psutil
isOpen = None
import ctypes
from ctypes import wintypes
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
IsWindowVisible = user32.IsWindowVisible
def get_hwnds_by_pid(pid):
	hwnds = []

	@EnumWindowsProc
	def foreach_window(hwnd, lParam):
		if IsWindowVisible(hwnd):
			lpdw_process_id = wintypes.DWORD()
			GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw_process_id))
			if lpdw_process_id.value == pid:
				hwnds.append(hwnd)
		return True

	EnumWindows(foreach_window, 0)
	return hwnds
for proc in psutil.process_iter(['pid', 'name','cmdline','exe']):
	if proc.info['name'] in ["pythonw.exe","python.exe","py","pyw"]:
		for i in ["XumoPlayApp.py"]:
			if i in proc.info['cmdline'][1]:
				if proc.pid != os.getpid():
					isOpen = proc.pid
if isOpen != None:
	print("App is open")
	hwnd = get_hwnds_by_pid(isOpen)[0]
	from win32more.Windows.Win32.UI.WindowsAndMessaging import (
	GetForegroundWindow,
	SetForegroundWindow,
	FindWindowW,
	ShowWindow,
	IsIconic,
	SW_RESTORE,
	)
	ShowWindow(hwnd, SW_RESTORE)
	# Bring to front
	SetForegroundWindow(hwnd)
	exit(0)
try:
	os.remove("../update.zip")
except:
	pass
from win32more.Windows.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Controls import ContentControl
from win32more.Windows.UI.Xaml.Hosting import WindowsXamlManager
from win32more.Windows.UI.Xaml.Interop import TypeName
from win32more.Windows.UI.Xaml import UIElement
from win32more.Windows.Win32.System.Threading import Sleep
from win32more import Windows
from win32more.winui3 import XamlApplication
from win32more.Microsoft.UI.Xaml import Window, FrameworkElement
from win32more.Microsoft.UI.Xaml.Media import MicaBackdrop,Imaging,FontFamily,CompositionTarget,VisualTreeHelper
from win32more.Microsoft.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Interop import TypeKind
from win32more.Windows.UI.Xaml import GridLength, GridLengthHelper, GridUnitType,DependencyObject,Thickness,Visibility
from win32more.Microsoft.UI.Xaml.Controls import InfoBar,Primitives,ToggleSplitButton,Border,ToggleSwitch,Page,HyperlinkButton,Button,CheckBox,ComboBox,NumberBox, ProgressRing,Image,PasswordBox,TextBlock,TextBlock, Slider, StackPanel, NavigationView, Frame, NavigationViewItem, RowDefinition, Grid, GridView, GroupStyle, Canvas, ToolTip
from win32more.Windows.Foundation import PropertyValue,IPropertyValue,Uri
from win32more.Windows.Win32.System.WinRT import IInspectable
from win32more.Microsoft.UI.Windowing import AppWindow
from win32more.Microsoft.UI import WindowId
from win32more.Microsoft.UI.Xaml import DispatcherTimer
from win32more.Windows.Foundation import TimeSpan,MemoryBuffer
from win32more.Windows.UI import Colors
from win32more.Windows.UI.Xaml.Media import SolidColorBrush,TranslateTransform,ImageBrush,ImageSource, Stretch
from win32more.Microsoft.UI.Xaml.Media.Animation import Storyboard, DoubleAnimation
from win32more.Windows.UI.Xaml import Duration, DurationHelper
from win32more.Microsoft.UI.Xaml.Media.Animation import NavigationThemeTransition, TransitionCollection
from win32more.Windows.Win32.System.Registry import *
from win32more.Microsoft.UI.Xaml.Controls import WebView2
import threading,json,requests
from time import sleep

from win32more.Windows.Win32.UI.WindowsAndMessaging import (
	GetWindowLongW, SetWindowLongW,
	GetWindowLongPtrW, SetWindowLongPtrW,
	GWL_STYLE,
	WS_OVERLAPPEDWINDOW, WS_CAPTION, WS_THICKFRAME, WS_SYSMENU, WS_MINIMIZEBOX, WS_MAXIMIZEBOX
)
from win32more.Windows.Win32.Foundation import HWND

def remove_titlebar(hwnd: HWND):
	"""Removes title bar and window borders using Win32 style flags."""
	style = GetWindowLongW(hwnd, GWL_STYLE)
	# Remove caption, thickframe, minimize/maximize boxes, and system menu
	style &= ~(WS_CAPTION | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_SYSMENU)
	SetWindowLongW(hwnd, GWL_STYLE, style)
from win32more.Microsoft.UI.Windowing import (
	FullScreenPresenter,
	OverlappedPresenter
)
cfuStatus = -1
cfuProgress = 0
def checkForUpdate():
	import urllib.request as request,io
	global cfuStatus,cfuProgress
	cfuStatus = 0
	try:
		resp = requests.get("https://raw.githubusercontent.com/Github73840134/XumoPlay-Windows/refs/heads/main/version",timeout=5)
		cfuStatus = 1
		if resp.text == open("version").read():
			cfuStatus = 5
			return 
	except requests.exceptions.Timeout:
		cfuStatus = 4
	except Exception as e:
		cfuStatus = 6
	exe = "../core/pythonw.exe update.py"
	if "bigscreen" in sys.argv:
		exe += " -launchBigScreen"
	if "wait" in sys.argv:
		exe += " -launchWait"
	try:
		cfuStatus = 2
		resp = request.urlopen("https://raw.githubusercontent.com/Github73840134/XumoPlay-Windows/refs/heads/main/update.zip")
		file = open("../update.zip","wb+")
		length = int(resp.headers.get("Content-Length"))
		while True:
			x = resp.read(io.DEFAULT_BUFFER_SIZE)
			file.write(x)
			cfuProgress = round((file.tell()/length)*100)
			
		file.close()
		cfuStatus = 3
		import psutil,subprocess
		
		#subprocess.Popen(exe,start_new_session=True)
		#x = psutil.Process(os.getpid())
		#x.kill()
	except:
		cfuStatus = 4


	
class SplashApp(XamlApplication):
	def __init__(self):
		super().__init__()
		self.xaml_manager = None
		self.splash_window = None
		self.main_window = None
		self.status = 0
	
	def OnLaunched(self, args):
		# Initialize XAML runtime
		self.page = "cfu"
		
		# Load splash screen XAML
		xaml = open("main.xaml", encoding="utf-8").read()
		self.splash_window = XamlReader.Load(xaml).as_(Window)
		self.document = self.splash_window.Content.as_(FrameworkElement).FindName("ContentFrame").as_(Frame)
		self.document.Loaded += self.on_document_loaded
		self.splash_window.SystemBackdrop = MicaBackdrop()
		self.splash_window.Closed += self.onClosed
		hwnd = self.splash_window.AppWindow.Id.Value
		self.document.Content = XamlReader().Load(open("loading.xaml", "r", encoding='utf-8').read())
		self.checkOnlineStatus()
		self.splash_window.Activate()
		self.timer = DispatcherTimer()
		self.timer.Interval = TimeSpan(10_000_000*5) # 100ms
		self.timer.Tick += lambda s, e: self.checkOnlineStatus()
		self.timer.Start()
		self.timer2 = DispatcherTimer()
		self.timer2.Interval = TimeSpan(1_000_000) # 100ms
		self.timer2.Tick += lambda s, e: self.updateUI()
		self.timer2.Start()
		self.splash_window.Title = "Xumo Play"
		icon_path = os.path.abspath(os.path.join(os.getcwd(),'logo.ico'))
		# Weird windows thing
		from win32more.Windows.Win32.UI.WindowsAndMessaging import SendMessageW,LoadImageW,IMAGE_ICON,LR_LOADFROMFILE, WM_SETICON, ICON_SMALL, ICON_BIG
		hicon = LoadImageW(
			None,
			icon_path,
			IMAGE_ICON,
			0,
			0,
			LR_LOADFROMFILE
		)
		
		# Set the window icon
		SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
		SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
		skipcfu = False
		self.steam = False
		if len(sys.argv) > 1:
			if "nocfu" in sys.argv:
				self.page = "loading"
				self.document.Content.as_(FrameworkElement).FindName("Loading.Status").as_(TextBlock).Text = "Connecting to Xumo Play"
				skipcfu = True
			if "bigscreen" in sys.argv:
				self.apply_display_mode()
				self.steam = True
			
		if not skipcfu:
			import _thread
			_thread.start_new_thread(checkForUpdate,())
	def apply_display_mode(self):
		self.splash_window.AppWindow.SetPresenter(
			FullScreenPresenter.Create()
		)
		
	def on_document_loaded(self,*args):
		if self.page == "main":
			if self.steam == False:
				self.setup_webview_hook()
	def setup_webview_hook(self):

		root = self.document.Content.as_(FrameworkElement)
		self.webview = root.FindName("WebView").as_(WebView2)
		
		from win32more.Microsoft.Web.WebView2.Core import CoreWebView2Environment
		
		if self.webview is None:
			print("WebView not found")
			return

		try:
			print("Initializing WebView2 Core...")

			# 🔥 THIS IS THE MISSING PIECE
			self.webview.EnsureCoreWebView2Async()

			# event fallback
			self.webview.CoreWebView2Initialized += self.on_webview_ready

		except Exception as e:
			print("ERROR:", e)
			self.webview.CoreWebView2Initialized += self.on_webview_ready

	def on_webview_ready(self, sender, args):
		self.launched = True
		

		self.attach_fullscreen_hook(sender.CoreWebView2)

	# -----------------------------
	# FULLSCREEN HOOK
	# -----------------------------
	def attach_fullscreen_hook(self, core):

		core.ContainsFullScreenElementChanged += (
			self.on_fullscreen_changed
		)

	def on_fullscreen_changed(self, sender, args):
		if self.steam == False:
			if sender.ContainsFullScreenElement:
				self.enter_fullscreen()
			else:
				self.exit_fullscreen()

	def enter_fullscreen(self):
		self.splash_window.AppWindow.SetPresenter(
			FullScreenPresenter.Create()
		)

	def exit_fullscreen(self):
		self.splash_window.AppWindow.SetPresenter(
			OverlappedPresenter.Create()
		)
	def checkOnlineStatus(self):
		import requests
		try:
			self.status = 0
			resp = requests.get("https://play.xumo.com")
			if resp.status_code == 200:
				self.status = 1
			else:
				print("C",resp.status_code)
				self.status = 2
		except Exception as e:
			print("E",str(e))

			self.status = 2
		print(self.status)
	def updateUI(self):
		if self.page == "cfu":
			#print(cfuStatus)
			if cfuStatus == 0:
				self.document.Content.as_(FrameworkElement).FindName("Loading.Status").as_(TextBlock).Text = "Checking for update"

			elif cfuStatus == 2:
				self.document.Content.as_(FrameworkElement).FindName("Loading.Status").as_(TextBlock).Text = f"Downloading update ({cfuProgress}%)"


			elif cfuStatus == 4:
				self.document.Content.as_(FrameworkElement).FindName("Loading.Status").as_(TextBlock).Text = "Connecting to Xumo Play"

				self.page = "loading"
			elif cfuStatus == 5:
				self.document.Content.as_(FrameworkElement).FindName("Loading.Status").as_(TextBlock).Text = "Connecting to Xumo Play"

				self.page = "loading"
			elif cfuStatus == 6:
				self.page = "error"
				self.document.Content = XamlReader().Load(open("error.xaml", "r", encoding='utf-8').read())
			return
		if self.page == "loading" and self.status == 1:
			self.page = "main"
			self.document.Content = XamlReader().Load(open("view.xaml", "r", encoding='utf-8').read())
			#self.document.Content.as_(FrameworkElement).FindName("WebView").as_(WebView2).CoreWebView2.Navigate("https://play.xumo.com")
			self.splash_window.DispatcherQueue.TryEnqueue(
				lambda: self.setup_webview_hook()
			)
		if self.page == "error" and self.status == 1:
			self.page = "main"
			
			self.document.Content = XamlReader().Load(open("view.xaml", "r", encoding='utf-8').read())
			
			self.splash_window.DispatcherQueue.TryEnqueue(
				lambda: self.setup_webview_hook()
			)
		if self.page == "main" and self.status == 0:
			self.page = "loading"
			self.document.Content = XamlReader().Load(open("loading.xaml", "r", encoding='utf-8').read())
			self.document.Content.as_(FrameworkElement).FindName("Loading.Status").as_(TextBlock).Text = "Connecting to Xumo Play"

		if self.page == "loading" and self.status == 0:
			self.document.Content.as_(FrameworkElement).FindName("Loading.Status").as_(TextBlock).Text = "Connecting to Xumo Play"

		if self.page != "error" and self.status == 2:
			self.page = "error"
			self.document.Content = XamlReader().Load(open("error.xaml", "r", encoding='utf-8').read())
	def onClosed(self,sender,args):
		import psutil
		x = psutil.Process(os.getpid())
		x.kill()

	def _check_thread(self, thread):
		

		if not thread.is_alive() and not self.launched:
			self.splash_window.Close()
			self.launched = True
		else:
			if self.loadState == 0:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "Starting service"
			elif self.loadState == 1:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "Starting app"
			elif self.loadState == 2:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "Preparing updates"
			elif self.loadState == 3:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "Installing updates"
			elif self.loadState == 4:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "One Moment"
	def _set_window_properties(self, hwnd):
		# You can use win32 APIs to set size, position, etc.
		from win32more.Windows.Win32.UI.WindowsAndMessaging import (
			GetWindowRect, MoveWindow
		)

		# Example: center on screen
		from win32more.Windows.Win32.UI.WindowsAndMessaging import GetSystemMetrics
		from win32more.Windows.Win32.UI.WindowsAndMessaging import SM_CXSCREEN, SM_CYSCREEN

		screen_w = GetSystemMetrics(SM_CXSCREEN)
		screen_h = GetSystemMetrics(SM_CYSCREEN)
		win_w, win_h = 400, 250
		x = (screen_w - win_w) // 2
		y = (screen_h - win_h) // 2

		MoveWindow(hwnd, x, y, win_w, win_h, True)
		

	def OnSuspending(self, args):
		print("App suspending...")

	def OnResuming(self, args):
		print("App resuming...")

XamlApplication.Start(SplashApp)


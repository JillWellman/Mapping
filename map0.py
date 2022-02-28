"""zbox0  zbox/transform/reference frame stuff with illustrative
diagrams.  Taken out of main program.  Want this clean and testable
Transform relates window and box, screen and world (order?)
task: make two windows.show xbox and zbox ane zooming """

"""objects
- image of current state in state window
- xbox  region for next state
- zbox  image of xbox in z window, image of calcs for next state
- transforms:
  - trxx xbox to state window
  - trzz zbox to z window
  - trxz xbox to z window
  - trzx zbox to x window
- transition  xbox to xwindow, zbox to zwindow, xbox defines zbox"""



import sys

from matplotlib.pyplot import draw


# from sacred.sacredCopyFeb22_6 import box_from_center
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/myImports')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')

from PIL import Image, ImageDraw, ImageFont
# import PIL.Image
import PIL.ImageDraw
import numpy as np
import datetime
import graphics
from graphics import *
from mygraphics import *
import colorsys

import inspect
myself = lambda: inspect.stack()[1][3]


global win, GraphWin,TR,winA,winB
global imgx,imgy,maxIt,mgn,sp
global gzbox,gscreen,depth


n=0
imgx,imgy=500,500
X = Y = imgx
side2x,side2y = imgx/16,imgy/16  #33,24   #(5.5 x 4)

maxIt = 255 # should be imgx / adjusted for debugging, non imgy # changes color palette
mgn=20
side2 = 40

gzbox=[-2,-1.5,1,1.5]    # z/complex/scale
gscreen = [0,0,imgx,imgy]   # plot size
sp = 3


def rec_draw(box,win):
	# print('\n-',myself())
	xa,ya,xb,yb = box
	return Rectangle(Point(xa,ya),Point(xb,yb)).draw(win)

def int_round_all(num,n):
	if n==0:
		return int(round(num,0))
	else:
		return round(num,0)

def round_all(lst,n):
	return list(map(lambda l : round(l,n) , lst))

class Window:

	def __init__(self,name,dtpl,coords,unit) -> None:
		self.name = name
		self.dtpl = dtpl 
		self.coords = coords 
		self.unit	= unit # pixels defined unit
	
	def transform(self,sbox,mapping):
		self.sbox = sbox   #selected box
		self.mapping = transform  #box to window


	def create(self,title,dtpl,coords,lctpl):
		win = GraphWin(self.title,*self.dtpl)
		win.setCoords(*self.coords)

	def grid(self,coords,unit):
		pass

	def clk_select(self,win,sz):
		clk = win.getMouse()
		cx,cy = clk.x,clk.y
		Circle(Point(cx,cy),w).draw(win)
		return ((cx,cy),w)

	# make and use Transforms

	

class Mapping:
	"""Zbox is transition.  Leave state space with clk_select"""
	def __init__(self) -> None:
		self.zbox = [-2,-1.5,1,1.5]
		# self.xbox,self.zbox = xbox,zbox
		# self.n = n
		# self.side2 = 15

	def z_window(self):
		self.window = GraphWin('Transition(zbox)',X,Y)
		window_location(self.window,X,Y,1.3*X,45)
		self.window.setCoords(-2,-1.5,1,1.5)

		for i in range(-2,2):
			for j in range(-2,2):
				Rectangle(Point(i,j),Point(i+1,j+1)).draw(self.window)
		# self.window.getMouse()

	def x_window(self):
		self.window = GraphWin('State(xbox)',X,Y)
		self.window.setCoords(0,Y,X,0)

		in_window(X/2,Y/2,'./sacred/bin0.png',self.window)

		



		# self.xbox,self.zbox = [0,0,X,Y],[-2,-1.5,1,1.5]

		# self.xbox_transform(win)
		# self.zbox_transform(win)
		# self.transform_printout(win)

	

	# def transition_window('zbox/transition',(X,Y),(-2.-1.5,1,1.5)):
	# 	pass
	
	def clk_select(self,win):
		clk = win.getMouse()
		cx,cy = clk.x,clk.y
		self.xbox = box_from_center(cx,cy,side2)
		rec_draw( self.xbox,win)   # this is new xbox
		self.xbox_transform(win)   ## annotate sel box with origin
		self.calculate_transforms(win)
		self.pseudo_button(win)

	def calculate_transforms(self,win):
		win = GraphWin('Transition(zbox)',X,Y)
		window_location(win,X,Y,1.3*X,35)
		win.setCoords(-2,-1.5,1,1.5)
		
		print()
		# these are for monitoring and dubugging zoom calcs
		self.zbox_transform(win)
		self.zbox_compare_xbox(win)
		self.transform_printout(win)

	def pseudo_button(self,win):
		"""in lower left of image window"""
		ps = Rectangle(Point(0,Y),Point(75,Y-50)).draw(win)
		ps.setWidth(3)
		Text(Point(-1.25,-1.25),'ZOOM').draw(win)

		win.getMouse()   #pseudo continue button

	def xbox_transform(self,win):
		# already have xbox.  want origin/  need main window
		print('\nself.xbox',round_all(self.xbox,0))
		self.trxx = Transform(X,Y,*self.xbox)
		ox,oy = self.trxx.xbase,self.trxx.ybase
		Circle(Point(ox,oy),5).draw(win).setFill('magenta')  		# xsel box already drawn
	
	def zbox_transformx(self,win):
		self.trxz = Transform(X,Y,*self.zbox)
		print('\ntrxz',self.trxz)
		
		xa,ya,xb,yb = self.xbox
		trxx_zbox = self.trxz.world(xa,ya) + self.trxz.world(xb,yb)
		print('zbox',round_all(trxx_zbox,4))
		rec_draw(trxx_zbox,win)
		zxa,zya,zxb,zyb = trxx_zbox
		Circle(Point(zxa,zya),0.04).draw(win).setFill('magenta')

		win.setCoords(-2,-1.5,1,1.5)
		u = 1
		for i in range(-2,1):
			for j in range(-2,2):
				Rectangle(Point(i*u,j*u),Point((i+1)*u,(j+1)*u)).draw(win)
				Text(Point(i-0.08,j+0.07),str(i)+','+str(j)).draw(win).setSize(18)
		# self.zbox = self.world.trxx(3,3,*self.xbox)
		# print(self.zbox)

	def zbox_transform(self,win):
		"""unclear how y coords work and where the origin is"""
		zxa,zya,zxb,zyb = self.zbox   #old zbox

		trxx_zbox = self.trxx.world(zxa,zya) + self.trxx.world(zxb,zyb)
		print('\nzbox after applying trxx from old xbox',round_all(trxx_zbox,0),' equals xsel, or new xbox ORIGIN twice')  # corresponds to xseel
		print('apply trxz to xsel')
		
		xa,ya,xb,yb = self.xbox
		new_zbox = self.trxz.world(xa,ya) + self.trxz.world(xb,yb)
		# new_zbox = round_all(new_zbox,4)
		self.zbox = new_zbox
		print('self.zbox',round_all(self.zbox,4))

		# rec_draw(self.zbox,win)

		self.trzz = Transform(3,3,*self.zbox)
		self.trzx = Transform(3,3,*self.xbox)

	def transform_printout(self,win):
		print()
		print('trxx',self.trxx)
		print('trxz',self.trzx)
		print('trzx',self.trzx)
		print('trzz',self.trzz)

	def zbox_compare_xbox(self,win):
		# calculation space
		win.setCoords(-2,-1.5,1,1.5)
		# draw grid
		u = 1
		for i in range(-2,1):
			for j in range(-2,2):
				Rectangle(Point(i*u,j*u),Point((i+1)*u,(j+1)*u)).draw(win)
				Text(Point(i-0.08,j+0.07),str(i)+','+str(j)).draw(win).setSize(18)

		# zbox on z coords in winZ
		zxa,zya,zxb,zyb = self.zbox
		Rectangle(Point(zxa,zya,), Point(zxb,zyb)).draw(win)
		Circle(Point(zxa,zyb),0.02).draw(win).setFill('magenta')

# zbox drivers   separate from OO code
def zbox_init():
	"""shows initial state with selection box"""
	win = GraphWin('',X,Y)   # shouldn't be in zbox~~state
	xbox,zbox = [0,0,X,Y], [-2,1.5,1,-1.5]
	zb = Zbox(xbox,zbox,0)
	
	
	# existing (state0) file in window
	file = './sacred/sacred0.png'
	in_window(X/2,Y/2,file,win)

	print('original zbox',zb.zbox,'\n')

	# selection box drawn
	print('sel box in center/width and corners format')
	cx,cy,w = 50,Y/2,30
	zb.sel_xbox(cx,cy,w)
	rec_draw(zb.xbox,win)
	# origin
	Circle(Point(cx-w,cy-w),5).draw(win).setFill('magenta')

	return zb

def zbox_image():
	"""exploration/explanation of zbox transition process"""
	zb = zbox_init()
	zxa,zya,zxb,zyb = zb.zbox

	zb.xbox_transform()
	trxx = zb.trxx
	trxz = zb.trxz

	# image under trxx and trxz
	print('\n ---Transforms on Original zbox--- ')
	trxx_zbox = trxx.world(zxa,zya) + trxx.world(zxb,zyb)
	print('zbox after trxx from xsel',round_all(trxx_zbox,0),' equals xsel')  # corresponds to xseel
	zxa,zya,zxb,zyb = trxx_zbox

	# image after trxz
	trxz_zbox = trxz.world(zxa,zya) + trxz.world(zxb,zyb)
	print('apply trxz to above xsel',round_all(trxz_zbox,2))
	zxa,zya,zxb,zyb = trxz_zbox

	 #selection box, corner format
	xsel = 20, 270, 80, 330    
	trxsel_zbox = trxz.world(20,270)+ trxz.world(80,330)
	print('apply trxz to xsel directly',round_all(trxsel_zbox,2))

	

	# calculation space
	winZ = GraphWin('winZ',X,Y)
	winZ.setCoords(-2,-1.5,1,1.5)
	window_location(winZ,X,Y,1.3*X,35)
	# draw grid
	u = 1
	for i in range(-2,1):
		for j in range(-2,2):
			Rectangle(Point(i*u,j*u),Point((i+1)*u,(j+1)*u)).draw(winZ)
			Text(Point(i-0.08,j+0.07),str(i)+','+str(j)).draw(winZ).setSize(18)

	# zbox on z coords in winZ
	Rectangle(Point(-1.9, 0.15), Point(-1.6, -0.15)).draw(winZ)
	Circle(Point(zxa,zya),0.02).draw(winZ).setFill('magenta')

	

	

	winZ.getMouse()
	
def driver():
	
	
	mpx = Mapping()
	mpx.x_window()
	# mpx.window.getMouse()
	mpz = Mapping() 
	mpz.z_window()
	# mpz.window.getMouse()

	# bx = Point(0,0).draw(mpx.window)
	# while True:

	clk = mpx.window.getMouse()
	cx,cy = clk.x,clk.y
	# bx.undraw()
	rec_draw( box_from_center(cx,cy,side2),mpx.window )
	mpx.xbox = box_from_center(cx,cy,side2)
	mpx.xbox_transform(mpx.window)
	mpx.zbox_transformx(mpz.window)
	# mpx.zbox_compare_xbox(mpz.window)

	mpx.window.getMouse()

driver()

	

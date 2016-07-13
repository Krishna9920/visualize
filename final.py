# 
# Authors: Sri Harsha Arangi
#          Venkata Krishna Annam
#          Abinash Patra
#
# It shows the AVL tree operations graphically.
#

import wx
import wx.xrc
import random
import time
from graphviz import Digraph as dg
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

os.system('rm Digraph.gv.svg')
os.system('cp temp.svg Digraph.gv.svg')
browser = webdriver.Firefox()
url = 'file://'+os.getcwd()+'/avltree.html'
browser.get(url)
s=0
i=0
d=0


class Node():
    def __init__(self, key):
        self.key = key
        self.left = None 
        self.right = None 
    def __unicode__(self):
        return "Node object"

class AVLTree():
    def __init__(self, *args):
        self.node = None 
        self.height = -1  
        self.balance = 0;
        
        if len(args) == 1: 
            for i in args[0]: 
                self.insert(i)
                
    def height(self):
        if self.node: 
            return self.node.height 
        else: 
            return 0 
    
    def is_leaf(self):
        return (self.height == 0) 
   
   
######################################################################################################## 
    def insert(self, key, root):
        tree = self.node
        
        newnode = Node(key)
        
        if tree == None:
            self.node = newnode
            self.node.left = AVLTree() 
            self.node.right = AVLTree()
            edges = []
            nodes = [(self.node.key, 'blue')]
            show_graph(nodes, getEdges(root.node if root.node != None else self.node, edges))
        
        elif key < tree.key:
            edges = []
            nodes = [(self.node.key, 'red'), (key, 'blue')]
            show_graph(nodes, getEdges(root.node, edges))
            self.node.left.insert(key, root)
            
        elif key > tree.key:
            edges = []
            nodes = [(self.node.key, 'green'), (key, 'blue')]
            show_graph(nodes, getEdges(root.node, edges))
            self.node.right.insert(key, root)
            
        else:
            edges = []
            nodes = [(self.node.key, '#333333'), ("Key already exists!!", 'red')]
            show_graph(nodes, getEdges(root.node, edges))
            return

        if root.node != None:
            self.rebalance(root) 
    ###############################################################################################    
    
    
    def rebalance(self, root):
        ''' 
        Rebalance a particular (sub)tree
        ''' 
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        if self.node:
        	edges = []
        	nodes = [(self.node.key, 'DarkMagenta')]
        	getEdges(root.node, edges)
        	if not len(edges) and root.node:
        	    nodes = [(self.node.key, '#333333')]
        	show_graph(nodes, edges)
        
        while self.balance < -1 or self.balance > 1: 
            if self.balance > 1:
                if self.node.left.balance < 0:  
                    self.node.left.lrotate(root) # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate(root)
                self.update_heights()
                self.update_balances()
                
            if self.balance < -1:
                if self.node.right.balance > 0:  
                    self.node.right.rrotate(root) # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate(root)
                self.update_heights()
                self.update_balances()


            
    def rrotate(self, root):
        # Rotate right pivoting on self
        A = self.node 
        B = self.node.left.node 
        T = B.right.node 
        
        self.node = B 
        B.right.node = A 
        A.left.node = T
        
        edges = []
        nodes = [(self.node.key, 'DarkMagenta')]
        show_graph(nodes, getEdges(root.node, edges))

    
    def lrotate(self, root):
        # Rotate left pivoting on self 
        A = self.node 
        B = self.node.right.node 
        T = B.left.node 
        
        self.node = B 
        B.left.node = A 
        A.right.node = T 
        
        edges = []
        nodes = [(self.node.key, 'DarkMagenta')]
        show_graph(nodes, getEdges(root.node, edges))
            
    def update_heights(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()
            
            self.height = max(self.node.left.height,
                              self.node.right.height) + 1 
        else: 
            self.height = -1 
            
    def update_balances(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height 
        else: 
            self.balance = 0 
    
    def search(self,number):
        node=self.node
        nodes = [(node.key, '#ff7700'), (number, 'blue')]
        edges = []
        show_graph(nodes, getEdges(self.node, edges))
        while node != None:

            if number == node.key:
                nodes = [(node.key, 'blue')]
                edges = []
                show_graph(nodes, getEdges(self.node, edges))
                break

            elif number < node.key:
                if node.left.node == None:
                    nodes = [(node.key, '#333333'), ("Not Found", 'red')]
                    edges = []
                    show_graph(nodes, getEdges(self.node, edges))
                    break 
                else:
                    node = node.left.node
                    nodes = [(node.key, 'green'), (number, 'blue')]
                    edges = []
                    show_graph(nodes, getEdges(self.node, edges))

            elif number > node.key:
                if node.right.node == None: 
                    nodes = [(node.key, '#333333'), ("Not Found", 'red')]     
                    edges = []
                    show_graph(nodes, getEdges(self.node, edges))
                    break 
                else:
                    node = node.right.node
                    nodes = [(node.key, 'red'), (number, 'blue')]
                    edges = []
                    show_graph(nodes, getEdges(self.node, edges))
            
    
    def delete(self, key, root):
        if self.node != None: 
            if self.node.key == key: 
                #edges = []
                #nodes = [(self.node.key, 'blue')]
                #show_graph(nodes, getEdges(root.node, edges))
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None # leaves can be killed at will
                    edges = []
                    getEdges(root.node, edges)
                    if not len(edges) and root.node:
                        nodes = [(root.node.key, '#333333')]
                    else:
                        nodes = []
                    show_graph(nodes, edges)
                # if only one subtree, take that 
                elif self.node.left.node == None:
                    self.node = self.node.right.node
                    edges = []
                    nodes = [(self.node.key, 'blue')]
                    show_graph(nodes, getEdges(root.node, edges))
                elif self.node.right.node == None:
                    self.node = self.node.left.node
                    edges = []
                    nodes = [(self.node.key, 'blue')]
                    show_graph(nodes, getEdges(root.node, edges))
                
                # worst-case: both children present. Find logical successor
                else:  
                    replacement = self.logical_successor(self.node, root, key)
                    if replacement != None: # sanity check 
                        self.node.key = replacement.key
                        #edges = []
                        #nodes = [(self.node.key, '#333333'), (key, 'blue')]
                        #show_graph(nodes, getEdges(root.node, edges))
                        # replaced. Now delete the key from right child 
                        self.node.right.delete(replacement.key, root)
                self.rebalance(root)
                return
            elif key < self.node.key: 
                self.node.left.delete(key, root)  
            elif key > self.node.key: 
                self.node.right.delete(key, root)
                
            self.rebalance(root)
        else: 
            return 

    def logical_predecessor(self, node):
        ''' 
        Find the biggest valued node in LEFT child
        ''' 
        node = node.left.node 
        if node != None: 
            while node.right != None:
                if node.right.node == None: 
                    return node 
                else: 
                    node = node.right.node  
        return node 
    
    def logical_successor(self, node, root, key):
        ''' 
        Find the smallest valued node in RIGHT child
        ''' 
        node = node.right.node
        if node != None: # just a sanity check  
            
            while node.left != None:                
                edges = []
                nodes = [(node.key, '#ff7700'), (key, 'blue')]
                show_graph(nodes, getEdges(root.node, edges))
                if node.left.node == None: 
                    return node
                else: 
                    node = node.left.node  
        return node 

    def check_balanced(self):
        if self == None or self.node == None: 
            return True
        
        # We always need to make sure we are balanced 
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())  
        
    def inorder_traverse(self):
        if self.node == None:
            return [] 
        
        inlist = [] 
        l = self.node.left.inorder_traverse()
        for i in l: 
            inlist.append(i) 

        inlist.append(self.node.key)

        l = self.node.right.inorder_traverse()
        for i in l: 
            inlist.append(i) 
    
        return inlist 

    def display(self, level=0, pref=''):
        self.update_heights()  # Must update heights before balances 
        self.update_balances()
        if(self.node != None): 
            if self.node.left != None: 
                self.node.left.display(level + 1, '<')
            if self.node.left != None:
                self.node.right.display(level + 1, '>')

def getEdges(curr, edges):
        if curr:
            if curr.left.node:
                edges.append((curr.key, curr.left.node.key, 'L'))
            else:
                edges.append((curr.key, None, 'L'))
            if curr.right.node:
                edges.append((curr.key, curr.right.node.key, 'R'))
            else:
                edges.append((curr.key, None, 'R'))
            if curr.left.node:
                getEdges(curr.left.node, edges)
            if curr.right.node:
                getEdges(curr.right.node, edges)
        return edges


a = AVLTree()

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"AVL Tree", pos = wx.DefaultPosition, size = wx.Size( 280,140 ) , style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_scrolledWindow4 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow4.SetScrollRate( 5, 5 )
		#bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText2 = wx.StaticText( self.m_scrolledWindow4, wx.ID_ANY, u"Search:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer2.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self.m_scrolledWindow4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
		
		self.m_button2 = wx.Button( self.m_scrolledWindow4, 1, u"Search", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_scrolledWindow4, wx.ID_ANY, u"Insert:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer2.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl3 = wx.TextCtrl( self.m_scrolledWindow4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_textCtrl3, 0, wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self.m_scrolledWindow4, 2, u"Insert", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button3, 0, wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_scrolledWindow4, wx.ID_ANY, u"Delete:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer2.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl4 = wx.TextCtrl( self.m_scrolledWindow4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_textCtrl4, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self.m_scrolledWindow4, 3, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button4, 0, wx.ALL, 5 )
		
		
		self.m_scrolledWindow4.SetSizer( fgSizer2 )
		self.m_scrolledWindow4.Layout()
		fgSizer2.Fit( self.m_scrolledWindow4 )
		bSizer4.Add( self.m_scrolledWindow4, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		self.Centre( wx.BOTH )
		self.Bind(wx.EVT_BUTTON, self.S, id = 1)
		self.Bind(wx.EVT_BUTTON, self.I, id = 2)
		self.Bind(wx.EVT_BUTTON, self.D, id = 3)#when 'done' button is pressed execute the function mentioned
	def S(self, event):
		s=self.m_textCtrl2.GetValue()
		self.m_textCtrl2.SetValue('')
		a.search(int(s))
		
	def I(self, event):
		i=self.m_textCtrl3.GetValue()
		fl=0
		self.m_textCtrl3.SetValue('')
		if a.node==None:
		    fl=1
		a.insert(int(i), a)
		edges = []
		if fl!=1:
			nodes = [(a.node.key, '#333333')]
			show_graph(nodes, getEdges(a.node, edges))
		
	def D(self, event):
		d=self.m_textCtrl4.GetValue()
		self.m_textCtrl4.SetValue('')
		a.search(int(d))
		a.delete(int(d), a)
		if a.node:
			nodes = [(a.node.key, '#333333')]
		else:
			nodes = []
		edges = []
		show_graph(nodes, getEdges(a.node, edges))
		
	def __del__( self ):
		pass
	
def add_nodes(graph, nodes):
    for n in nodes:
        graph.node(str(n))
    return graph

def add_edges(graph, edges):
    i = 0
    l = len(edges)
    while(i < l):
        left = edges[i]
        i += 1
        right = edges[i]
        i += 1
        if left[1] or right[1]:
            if left[1]:
                graph.edge(str(left[0]), str(left[1]))
            else:
                if left[2] == 'L':
                    graph.node(str(left[0])+'L', style='invis')
                    graph.edge(str(left[0]), str(left[0])+'L', style='invis')
                else:
                    graph.node(str(left[0])+'R', style='invis')
                    graph.edge(str(left[0]), str(left[0])+'R', style='invis')
            if right[1]:
                graph.edge(str(right[0]), str(right[1]))
            else:
                if right[2] == 'L':
                    graph.node(str(right[0])+'L', style='invis')
                    graph.edge(str(right[0]), str(right[0])+'L', style='invis')
                else:
                    graph.node(str(right[0])+'R', style='invis')
                    graph.edge(str(right[0]), str(right[0])+'R', style='invis')
    return graph

def show_graph(nodes, edges):
    graph = dg(format='svg', strict=True)
    sub = dg()
    sub.attr('graph', rank='same')
    if nodes:
        if len(nodes) == 1:
            sub.node(str(nodes[0][0]), color=nodes[0][1], shape='circle', style='bold')
        if len(nodes) > 1:
            if nodes[1][0] == "Key already exists!!":
                sub.node(str(nodes[0][0]), color=nodes[0][1], shape='circle', style='bold')
                sub.node(str(nodes[1][0]), color=nodes[1][1],style='bold')
            if nodes[1][0] == "Not Found":
                sub.node(str(nodes[0][0]), color=nodes[0][1], shape='circle')
                sub.node(str(nodes[1][0]), color=nodes[1][1],style='bold')
            if nodes[1][0] != "Not Found" and nodes[1][0] != "Key already exists!!":
                sub.node(str(nodes[0][0]), color=nodes[0][1], shape='circle', style='bold')
                sub.node(str(nodes[1][0])+" ", color=nodes[1][1], shape='circle', style='bold')
        graph.subgraph(sub)

    graph.attr('graph', ordering='out')
    graph.attr('edge', color='DarkCyan')
    graph.attr('node', shape='circle', color='#333333')
    add_edges(graph, edges)
    graph.render()
    time.sleep(1)
    browser.refresh()

app2=wx.App(False)
frame=MyFrame1(None)
frame.Show(True)
app2.MainLoop()


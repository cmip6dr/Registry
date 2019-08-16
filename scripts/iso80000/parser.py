
import xml
import xml.dom.minidom as md




class Parse(object):
  k1 = {'ch5':'THERMODYNAMICS', 'ch3':'SPACE AND TIME', 'ch4':'MECHANICS',
        'ch8':'ACOUSTICS','ch9':'PHYSICAL CHEMISTRY AND MOLECULAR PHYSICS',
        'ch6':'ELECTROMAGNETISM', 'ch7':'LIGHT' }
  def __init__(self,base='ch5',ofile=None):
    doc = md.parse( '%s/word/document.xml' % base )
    tabs = doc.getElementsByTagName( 'w:tbl' )
    print (len(tabs))
    self.tp = []
    for i in range( len(tabs) -1 ):
      tr=tabs[i].getElementsByTagName( 'w:tr' )
      v = tr[0].getElementsByTagName( 'w:t')[0].firstChild.data
      if v == self.k1[base]:
        v1 = tabs[i+1].getElementsByTagName( 'w:tr' )[0].getElementsByTagName( 'w:t')[0].firstChild.data
        if v1 == 'UNITS':
          self.tp.append(i)
    print ( self.tp )
    self.tabs = tabs
    if ofile != None:
      self.oo = open( ofile, 'w' )

  def _scantab(self,i):
    tr=self.tabs[i].getElementsByTagName( 'w:tr' )
    tab = []
    for this in tr:
      t = this.getElementsByTagName( 'w:tc' )
      tab.append( [' '.join( [x.firstChild.data for x in thisthis.getElementsByTagName( 'w:t') ] ) for thisthis in t ] )

    return tab

  def _tab2compress(self,tab2):
    xx = [x[0].split('.')[0].strip() for x in tab2[2:]]
    print ('xx: %s' % xx )
    if '' not in xx:
      return tab2
    idx = []
    for i in range(len(xx)):
      if xx[i] != '' and (i == 0 or xx[i] != xx[i-1]):
        idx.append(i)
    idx.append( len(xx) )
    return self._compress_tab_on_idx(tab2,idx)

  def _compress_tab_on_idx(self,tabi,idx):
    tab = tabi[:2]
    for i in range( len(idx)-1 ):
           i0 = idx[i]
           i9 = idx[i+1]
           rr = []
           for j in range(len(tabi[i0+2])):
             s = ''
             for x in range(i0,i9):
               if j < len( tabi[x+2] ):
                 xx = tabi[x+2][j].strip()
                 if xx != '':
                   if s != '':
                     s += '; '
                   s += xx
             rr.append( s )
           tab.append(rr)
    return tab

  def _tabalign01(self,tab1,tab2):
    """Attempt to align tables, based on matching first word in tab1 with first word before '.' in tab2"""

    xx = [x[0].split('.')[0] for x in tab2[2:]]
    yy = []
    for x in tab1[2:]:
      this = x[0].split()
      if len(this) > 0:
        yy.append( this[0].strip().split('.')[0] )
      else:
        yy.append( '' )
    print( xx )
    print( yy )

    if not all( [x in yy for x in xx] ):
      return (-1,None)
    if len(set(xx)) < len(xx):
      return (-2,None)
    oo = []
    for x in xx:
      oo.append( yy.index(x) )
    return (1,oo)

  def _scanpair(self,i,isFirst):
    tab1 = self._scantab(i)
    tab2 = self._scantab(i+1)
    tab2 =  self._tab2compress(tab2)
    if len(tab1) != len(tab2):
      print ( 'Mismatch in table lengths: %s - %s' % (len(tab1), len(tab2)) )
      if len(tab1) > len(tab2):
        rc,idx = self._tabalign01(tab1,tab2)
        print ('%s:%s' % (rc,idx))
        if rc <0:
          match = False
        else:
         tab3 = tab1[:2]
         idx.append( len(tab1)-2 )
         for i in range( len(tab2)-2 ):
           i0 = idx[i]
           i9 = idx[i+1]
           rr = []
           for j in range(len(tab1[i0+2])):
             s = ''
             for x in range(i0,i9):
               if j < len( tab1[x+2] ):
                 xx = tab1[x+2][j].strip()
                 if xx != '':
                   if s != '':
                     s += '; '
                   s += xx
             rr.append( s )
           tab3.append(rr)
         tab1 = tab3
         match = True
         print ('Adjused match 01')
      else:
        match = False
    else:
      match = True
    ll = min( [len( tab1 ) ,  len(tab2) ] )
    for i in range( ll ):
      if isFirst or i > 1:
        self.oo.write( '\t'.join( tab1[i] ) + '\t' )
        self.oo.write( '\t'.join( tab2[i] ) )
        self.oo.write( '\n' )
      ##print( '%12s;%s\n' % (tab1[i][0], tab2[i][0] ) )

  def run(self):
    for i in self.tp:
      print ( 'STARTING %s' % i )
      self._scanpair(i,i==self.tp[0])

for k in [8,9]:
  this = 'ch%s' % k
  p = Parse( base=this,ofile = 'ISO8000_parsed_%s.csv' % this )
  p.run()
  p.oo.close()

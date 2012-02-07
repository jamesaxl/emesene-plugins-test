import pygtk
pygtk.require('2.0')
import gtk
import webkit
import gobject
import pango
import subprocess
#[one_half] [contact_form] [/one_half]
#[one_half_last] [contact_map] [/one_half_last]
class WatchVideo():
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        self.window.hide()
    def init_info(self):
        self.images=[]
        self.videos=[]
        self.titles=[]
        self.users=[]

    def __init__(self):
        print "run"
        self.bl=0
        self.pointer=0
        self.init_info()
        gobject.threads_init()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.resize(425,150)
        self.window.set_resizable(True)
        self.window.set_title("title")
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.window.move(30, 30)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.win_hide)
        self.vbox = gtk.VBox()
        # hbox with image, pages, and main text
        self.hbox = gtk.HBox()
        self.hbox.set_spacing(4)
        self.hbox.set_border_width(4)

        # the contents of the hbox (image+vboxtext)
        self.image = webkit.WebView()
        #self.image.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
        self.imagebox = gtk.HBox()
        self.imagebox.set_border_width(4)
        #self.image.set_alignment(0.0, 0.5)

        # the vboxtext (pages+text)
        self.vboxtext = gtk.VBox()
        self.pages = self._buildpages()
        self.text = gtk.Label()
        self.text.set_selectable(True)
        self.text.set_ellipsize(3) #pango.ELLIPSIZE_END
        self.text.set_alignment(0.0, 0.0) # top left
        self.text.set_width_chars(60)

        # hboxbuttons + button box
        self.hboxbuttons = gtk.HBox()
        self.hboxbuttons.set_spacing(4)
        self.hboxbuttons.set_border_width(4)
        self.buttonbox = gtk.HButtonBox()
        self.buttonbox.set_layout(gtk.BUTTONBOX_END)

        # the contents of the buttonbox
        self.later = gtk.Button()
        self.later.add(gtk.Label('Watch Video'))
        self.later.connect('clicked', self.watch_video)
        self.reject = gtk.Button(stock=gtk.STOCK_REMOVE)
        self.reject.connect('clicked', self.remove)
        #self.addbutton = gtk.Button(stock=gtk.STOCK_ADD)
        #self.addbutton.connect('clicked', self.cb_add)

        ## packing
        self.window.add(self.vbox)
        self.vbox.pack_start(self.hbox, True, True)
        self.vbox.pack_start(self.hboxbuttons, False, False)

        self.imagebox.pack_start(self.image)
        self.hbox.pack_start(self.imagebox, False, False)
        self.hbox.pack_start(self.vboxtext, True, True)
        self.vboxtext.pack_start(self.pages, False, False)
        self.vboxtext.pack_start(self.text, True, True)

        self.hboxbuttons.pack_start(self.later, False, False)
        self.hboxbuttons.pack_start(self.reject, False, False)
        self.hboxbuttons.pack_start(self.buttonbox)
        #self.buttonbox.pack_start(self.addbutton)
        #self.window.show_all()
        if not self.pointer:
            self.update()
    def _buildpages(self):
        '''Builds hboxpages, that is a bit complex to include in __init__'''
        hboxpages = gtk.HBox()

        arrowleft = TinyArrow(gtk.ARROW_LEFT)
        self.buttonleft = gtk.Button()
        self.buttonleft.set_relief(gtk.RELIEF_NONE)
        self.buttonleft.add(arrowleft)
        self.buttonleft.connect('clicked', self.switchmail, -1)

        arrowright = TinyArrow(gtk.ARROW_RIGHT)
        self.buttonright = gtk.Button()
        self.buttonright.set_relief(gtk.RELIEF_NONE)
        self.buttonright.add(arrowright)
        self.buttonright.connect('clicked', self.switchmail, 1)

        self.currentpage = gtk.Label()

        hboxpages.pack_start(gtk.Label(), True, True) # align to right
        hboxpages.pack_start(self.buttonleft, False, False)
        hboxpages.pack_start(self.currentpage, False, False)
        hboxpages.pack_start(self.buttonright, False, False)

        return hboxpages
    def switchmail(self, button, order):
        '''Moves the mail pointer +1 or -1'''
        if (self.pointer + order) >= 0:
            if (self.pointer + order) < len(self.titles):
                self.pointer += order
            else:
                self.pointer = 0
        else:
            self.pointer = len(self.titles) - 1

        self.update()
        
    def update(self):
        '''Update the GUI, including labels, arrow buttons, etc'''
        try:
            #mail, nick = self.mails[self.pointer]
            title=self.titles[self.pointer]
            user=self.users[self.pointer]
            image=self.images[self.pointer]
        except IndexError:
            self.win_hide(self)
            
            return

        #if nick != mail:
         #   mailstring = "<b>%s</b>\n<b>(%s)</b>" % (nick, mail)
        #else:
        titlestring = '<b>%s</b>' % title
        userstring= '<b>%s</b>' % user
        imagestring='<center><img src="%s" width="100" height="100" /></center>' % image
        self.text.set_markup(userstring + (' sent you ')+titlestring+('\nDo you want to watch this video? '))
        self.image.load_html_string(imagestring,'file:///')
        self.buttonleft.set_sensitive(True)
        self.buttonright.set_sensitive(True)
        if self.pointer == 0:
            self.buttonleft.set_sensitive(False)
        if self.pointer == len(self.titles) - 1:
            self.buttonright.set_sensitive(False)

        self.currentpage.set_markup('<b>(%s/%s)</b>' % \
            (self.pointer + 1, len(self.titles)))        


    def set_video(self,title,video,image,user):
        self.images.append(image)
        self.videos.append(video)
        self.titles.append(title)
        self.users.append(user)
        self.update()
    
    def watch_video(self,button):
        subprocess.Popen(['python', os.getcwd()+'/E_youtube.py','--title',self.titles[self.pointer],'--video',self.videos[self.pointer]])
        self.remove(None)
        
    def remove(self,button):
        self.titles.pop(self.pointer)
        self.videos.pop(self.pointer)
        self.users.pop(self.pointer)
        self.switchmail(None, -1)
 
    def win_hide(self,button):
        self.window.hide() 
        self.bl=0
        
    def win_show(self):
        self.window.show_all()
        self.bl=1
    
    def main(self):
        gtk.main()
        
        
class TinyArrow(gtk.DrawingArea):
    LENGTH = 8
    WIDTH = 5

    def __init__(self, arrow_type, shadow=gtk.SHADOW_NONE):
        gtk.DrawingArea.__init__(self)
        self.arrow_type = arrow_type
        self.shadow = shadow
        self.margin = 0

        self.set_size_request(*self.get_size())
        self.connect("expose_event", self.expose)

    def get_size(self):
        if self.arrow_type in (gtk.ARROW_LEFT, gtk.ARROW_RIGHT):
            return (TinyArrow.WIDTH + self.margin*2, \
                    TinyArrow.LENGTH + self.margin*2)
        else:
            return (TinyArrow.LENGTH + self.margin*2, \
                    TinyArrow.WIDTH + self.margin*2)

    def expose(self, widget=None, event=None):
        if self.window is None:
            return
        self.window.clear()
        width, height = self.get_size()
        self.get_style().paint_arrow(self.window, self.state, \
            self.shadow, None, self, '', self.arrow_type, True, \
            0, 0, width, height)

        return False

    def set(self, arrow_type, shadow=gtk.SHADOW_NONE, margin=None):
        self.arrow_type = arrow_type
        self.shadow = shadow
        if margin is not None:
            self.margin = margin
        self.set_size_request(*self.get_size())
        self.expose() 
               
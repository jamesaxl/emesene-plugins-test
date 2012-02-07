import pygtk
pygtk.require('2.0')
import gtk

#you need to import webkit and gobject, gobject is needed for threads
import webkit
import gobject

class Browser:
         #"http://www.youtube.com/v/AhBJwaUzrfY"
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self,default_site,title):
        self.default_site=default_site
        
        gobject.threads_init()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.resize(350,300)
        self.window.set_resizable(True)
        self.window.set_title(title)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        #webkit.WebView allows us to embed a webkit browser
        #it takes care of going backwards/fowards/reloading
        #it even handles flash
        self.web_view = webkit.WebView()
        self.web_view.open(self.default_site)


        scroll_window = gtk.ScrolledWindow(None, None)
        scroll_window.add(self.web_view)
        

        vbox = gtk.VBox(False, 0)
        vbox.add(scroll_window)

        self.window.add(vbox)
        self.window.show_all()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--title')
    parser.add_argument('--video')

    parsed_args = parser.parse_args()
    title=parsed_args.title
    video=parsed_args.video
    
    browser = Browser(video,title)
    browser.main()

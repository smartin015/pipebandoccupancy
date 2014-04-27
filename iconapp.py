import wx
import threading
import subprocess
import urllib2
import sys, traceback
import time

TRAY_TOOLTIP = 'Pipe Band Room Occupancy'
TRAY_ICON = 'icon.jpg'

run_loop = True

def ping_thread():
    global run_loop
    URL = "http://aretherepipers.appspot.com/update?v=%s"
    #URL = "http://localhost:8080/update?v=%s"
    while run_loop:
        time.sleep(15.0)
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(
                     ['receive.exe'],
                     startupinfo=startupinfo,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     stdin=subprocess.PIPE
            )
            result, err = process.communicate()
            if result:
                print(result)
                req = urllib2.Request(url = URL % result)
                print urllib2.urlopen(req).read()
        except:
            print "Exception:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        
    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_exit(self, event):
        run_loop = False
        wx.CallAfter(self.Destroy)


def main():
    t = threading.Thread(target=ping_thread)
    t.daemon = True
    t.start()
    app = wx.PySimpleApp()
    TaskBarIcon()
    app.MainLoop()


if __name__ == '__main__':
    main()
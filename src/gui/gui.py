from kivy.app import App
from kivy.uix.widget import Widget


class RegionWidget(Widget):
	pass

class RegionApp(App):
	def build(self):
		return RegionWidget()

if __name__=='__main__':
	RegionApp().run()

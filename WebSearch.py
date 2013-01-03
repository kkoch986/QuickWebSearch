import sublime, sublime_plugin
import webbrowser
import urllib

class WebSearchCommand(sublime_plugin.TextCommand):
	defaultUrl = "http://google.com/search?"

	def run(self, edit):
		settings = sublime.load_settings("WebSearch.sublime-settings")
		self.search = settings.get("com.kenkoch.websearch.search_engine", self.defaultUrl)

		self.edit = edit
		initial = ""
		for r in self.view.sel(): 
			if not r.empty():
				initial = self.view.substr(r)	
				break

		self.view.window().show_input_panel("Search", initial, self.on_done, None, None)	


	def on_done(self, string):
		url = str(''.join((self.search, urllib.urlencode({"q":string}))))
		webbrowser.open(url,new=2)
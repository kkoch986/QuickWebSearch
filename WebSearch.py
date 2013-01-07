'''
' by Ken Koch 2013 [kkoch986@gmail.com]
' Sublime Web Search Plugin
'''
import sublime, sublime_plugin
import webbrowser
import urllib

'''
	The Quick Web Search Command ("quick_web_search") takes the first search engine in the settings list
	and opens an input for a query. Upon entering the query, a browser window is opened up displaying
	search results for the given query.
'''
class QuickWebSearchCommand(sublime_plugin.TextCommand):
	# this is a fallback url in case there isnt any found
	defaultUrl = "http://google.com/search?"
	defaultVar = "q"
	defaultName = "Google"

	def run(self, edit):
		settings = sublime.load_settings("WebSearch.sublime-settings")
		search_engines = settings.get("com.kenkoch.websearch.search_engines")
		if(search_engines is None):
			self._search = defaultUrl
			self._var = defaultVar
			self._name = defaultName
		else:
			index = settings.get("com.kenkoch.websearch.default_search_engine",0);
			self._search = search_engines[index]["url"];
			self._var = search_engines[index]["var"];
			self._name = search_engines[index]["name"];


		self._edit = edit
		initial = ""
		for r in self.view.sel(): 
			if not r.empty():
				initial = self.view.substr(r)	
				break

		self.view.window().show_input_panel(self._name + " Search", initial, self.on_done, None, None)	


	def on_done(self, string):
		url = str(''.join((self._search, urllib.urlencode({self._var:string}))))
		webbrowser.open(url,new=2)

'''
	The Web Search Command ("web_search") opens a choice dialog of search engines defined in the WebSearch.sublime-settings file.
	Once you choose one, it gives you a dialog to enter your query into. Upon entering that info, a browser window is opened
	displaying search results on the given search engine.
'''
class WebSearchCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		# load the settings and the list of search engines
		self._edit = edit
		settings = sublime.load_settings("WebSearch.sublime-settings")
		self._search_engines = settings.get("com.kenkoch.websearch.search_engines")

		# ensure there are engines to choose from
		if(self._search_engines is None):
			sublime.message_dialog("No Engines Loaded.")
			return

		# show a dialog to select from those choices
		self.view.window().show_quick_panel([ [s["name"], s["desc"] ] for s in self._search_engines], self.on_choice)

	# After a choice has been made:
	# set the choice and show the input dialog
	def on_choice(self, index):	
		# ensure that a selection was in fact made
		if(index == -1): 
			return 

		# load the info about that engine
		self._search     = self._search_engines[index]["url"];
		self._var        = self._search_engines[index]["var"];
		self._name       = self._search_engines[index]["name"];

		# grab the selected text
		initial = ""
		for r in self.view.sel(): 
			if not r.empty():
				initial = str(self.view.substr(r))	
				break

		# open the niput dialog
		self.view.window().show_input_panel(self._name + " Search", initial, self.on_done, None, None)	

	# After text has been entered
	# Open the browser window.
	def on_done(self, string):
		# build the url
		url = str(''.join((self._search, urllib.urlencode({self._var:string}))))

		# open the browser
		webbrowser.open(url,new=2)



import sublime
import sublime_plugin

class UnwrapSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		pairs = {"'": "'", '"': '"', "(": ")", "[": "]", "{": "}", "`": "`", "#": "#"}

		for index, region in enumerate(self.view.sel()):
			if len(region) == 0:
				if len(self.view.sel()) == 1:
					self.view.run_command("expand_selection", {"to": "scope"})
					region = self.view.sel()[0]
				else:
					text = None
					region_begin = region.begin()
					while region_begin:
						next_char = self.view.substr(sublime.Region(region_begin - 1, region_begin))
						if next_char in pairs:
							text = next_char
							break
						region_begin -= 1
					if text:
						region_end = region.end()
						while region_end < self.view.size():
							next_char = self.view.substr(sublime.Region(region_end, region_end + 1))
							if next_char == pairs.get(text):
								text = "successfully paired"
								break
							region_end += 1
						if text == "successfully paired":
							self.view.sel().subtract(region)
							region = sublime.Region(region_begin, region_end)
							self.view.sel().add(region)
			text = self.view.substr(region)
			if len(text) >= 2 and text[0] in pairs and text[-1] == pairs.get(text[0]):
				self.view.replace(edit, region, text[1:-1])  # Trim safely
			else:
				region_length = len(region)
				ext_region_begin = region.begin()
				if ext_region_begin > 0:
					ext_region_begin -= 1
				ext_region_end = region.end()
				if ext_region_end < self.view.size():
					ext_region_end += 1
				ext_region = sublime.Region(ext_region_begin, ext_region_end)
				text = self.view.substr(ext_region)
				if text[0] in pairs and text[-1] == pairs.get(text[0]):
					self.view.replace(edit, ext_region, text[1:-1])
					if len(self.view.sel()[index]) != region_length:
						self.view.sel().subtract(region)
						self.view.sel().add(sublime.Region(ext_region_begin, ext_region_begin + region_length))

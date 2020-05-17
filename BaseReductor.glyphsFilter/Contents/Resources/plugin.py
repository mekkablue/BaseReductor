# encoding: utf-8
from __future__ import division, print_function, unicode_literals

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

excludeDict = {
	"idotless": "i",
	"jdotless": "j",
}

specialDict = {
	"AE": ("A", "E",),
	"OE": ("O", "E",),
	"ae": ("a", "e",),
	"oe": ("o", "e",),
	"Eng": ("N",),
	"eng": ("n",),
	"napostrophe": ("n",),
	"kgreenlandic": ("k",),
	"thorn": ("p",),
	"Thorn": ("P",),
	"IJ": ("I", "J",),
	"ij": ("i", "j",),
	"idotless": ("i",),
	"jdotless": ("j",),
	"dotlessi": ("i",),
	"dotlessj": ("j",),
}

class BaseReductor(FilterWithoutDialog):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Base Reductor',
			'de': 'Basis-Reduktor',
			'fr': 'Réducteur à base',
			'es': 'Reductor a la base',
		})
		
		self.keyboardShortcut = None # With Cmd+Shift
	
	@objc.python_method
	def nameWithoutSuffix(self, glyphName):
		if "." in glyphName:
			dotOffset = glyphName.find(".")
			return glyphName[:dotOffset]
		else:
			return glyphName
	
	@objc.python_method
	def filter(self, Layer, inEditView, customParameters):
		glyph = Layer.parent
		font = glyph.parent
		
		# check for specials
		specialNamesToCheck = [glyph.name,]
		if "." in glyph.name:
			specialNamesToCheck.append( self.nameWithoutSuffix(glyph.name) )
		for specialName in specialNamesToCheck:
			if specialName in specialDict:
				allSpecialComponentsInFont = True
				for specialComponent in specialDict[specialName]:
					if not font[specialComponent]:
						allSpecialComponentsInFont = False
				if not allSpecialComponentsInFont:
					print("🔥 Base Reductor: Not all parts available for: %s" % specialName)
				else:
					Layer.clear()
					for basename in specialDict[specialName]:
						base = GSComponent(basename)
						try:
							# GLYPHS 3
							Layer.shapes.append(base)
						except:
							# GLYPHS 2
							Layer.components.append(base)
					return None
			
		if glyph.category =="Letter" and glyph.subCategory != "Ligature":
			glyphInfo = glyph.glyphInfo
			if not glyphInfo:
				print("🔥 Base Reductor: no glyph info: %s" % glyph.name)
			elif glyphInfo.components:
				basename = glyphInfo.components[0].name
				
				# i -> idotless, j -> jdotless
				if basename in excludeDict:
					oldBasename = basename
					basename = excludeDict[basename]
					
					# print("🔄 Base Reductor %s: Will use %s instead of %s." % (glyph.name, oldBasename, basename))
				
				# look if glyph exists:
				if not font.glyphs[basename] and font.glyphs[self.nameWithoutSuffix(basename)]:
					basename = self.nameWithoutSuffix(basename)
				if font.glyphs[basename]:
					if basename != glyph.name:
						Layer.clear()
						base = GSComponent(basename)
						try:
							# GLYPHS 3
							Layer.shapes.append(base)
						except:
							# GLYPHS 2
							Layer.components.append(base)
					else:
						Layer.decomposeComponents() # do not let i/j reference itself
				else:
					print("❌ Base Reductor: no base glyph (%s) in font for: %s" % (basename, glyph.name))
			else:
				pass
				# print("⚠️ Base Reductor: no components in glyph info: %s" % glyph.name)
		else:
			pass
			# print("💚 Base Reductor: %s left unchanged" % glyph.name)
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

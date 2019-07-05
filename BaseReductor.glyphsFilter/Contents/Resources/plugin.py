# encoding: utf-8

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
	
	def settings(self):
		self.menuName = u'BaseReductor'
		self.keyboardShortcut = None # With Cmd+Shift
	
	def nameWithoutSuffix(self, glyphName):
		if "." in glyphName:
			dotOffset = glyphName.find(".")
			return glyphName[:dotOffset]
		else:
			return glyphName
	
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
					print u"🔥 BaseReductor: Not all parts available for: %s" % specialName
				else:
					Layer.clear()
					for basename in specialDict[specialName]:
						base = GSComponent(basename)
						Layer.components.append(base)
					return None
			
		if glyph.category =="Letter" and glyph.subCategory != "Ligature":
			glyphInfo = glyph.glyphInfo
			if not glyphInfo:
				print u"🔥 BaseReductor: no glyph info: %s" % glyph.name
			elif glyphInfo.components:
				basename = glyphInfo.components[0].name
				
				# i -> idotless, j -> jdotless
				if basename in excludeDict:
					oldBasename = basename
					basename = excludeDict[basename]
					
					# print u"🔄 BaseReductor %s: Will use %s instead of %s." % (glyph.name, oldBasename, basename)
				
				# look if glyph exists:
				if not font.glyphs[basename] and font.glyphs[self.nameWithoutSuffix(basename)]:
					basename = self.nameWithoutSuffix(basename)
				if font.glyphs[basename]:
					if basename != glyph.name:
						Layer.clear()
						base = GSComponent(basename)
						Layer.components.append(base)
					else:
						Layer.decomposeComponents() # do not let i/j reference itself
				else:
					print u"❌ BaseReductor: no base glyph (%s) in font for: %s" % (basename, glyph.name)
			else:
				pass
				# print u"⚠️ BaseReductor: no components in glyph info: %s" % glyph.name
		else:
			pass
			# print u"💚 BaseReductor: %s left unchanged" % glyph.name
			
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
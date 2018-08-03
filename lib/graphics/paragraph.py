from kivy.properties import StringProperty, NumericProperty
from kivy.uix.scrollview import ScrollView


class Paragraph(ScrollView):
    text = StringProperty('')
    font_name = StringProperty('')
    halign = StringProperty('left')
    font_size = NumericProperty(10)
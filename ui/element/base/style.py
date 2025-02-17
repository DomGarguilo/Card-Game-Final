import pygame as pg

from .position import Position

class Style(Position):
    def __init__(
        self,

        fill_color=None,
        outline_color=None,
        outline_width=0,
        inner_outline_color=None,
        inner_outline_width=0,
        key_color=None,
        
        border_radius=0,
        border_top_left_radius=-1,
        border_top_right_radius=-1,
        border_bottom_left_radius=-1,
        border_bottom_right_radius=-1,

        pad=None,
        left_pad=0,
        right_pad=0,
        x_pad=None,
        top_pad=0,
        bottom_pad=0,
        y_pad=None,

        **kwargs
    ):
        super().__init__(**kwargs)

        self.fill_color = fill_color
        self.original_fill_color = fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.inner_outline_color = inner_outline_color
        self.inner_outline_width = inner_outline_width
        self.key_color = key_color
        
        self.border_radius = border_radius
        self.border = {
            'topleft': border_top_left_radius,
            'topright': border_top_right_radius,
            'bottomleft': border_bottom_left_radius,
            'bottomright': border_bottom_right_radius
        }

        if pad is not None:
            left_pad = right_pad = top_pad = bottom_pad = pad
        else:
            if x_pad is not None:
                left_pad = right_pad = x_pad
            if y_pad is not None:
                top_pad = bottom_pad = y_pad

        self.pad = {
            'left': left_pad,
            'right': right_pad,
            'top': top_pad,
            'bottom': bottom_pad
        }

    @property
    def padded_rect(self):
        w = self.rect.width + self.pad['left'] + self.pad['right']
        h = self.rect.height + self.pad['top'] + self.pad['bottom']
        x = self.rect.x - self.pad['left']
        y = self.rect.y - self.pad['top']
        return pg.Rect(x, y, w, h)
        
    @property
    def outline_rect(self):
        return self.padded_rect.inflate(self.outline_width * 2, self.outline_width * 2)

    @property
    def padding(self):
        return list(self.pad.values())
        
    @padding.setter
    def padding(self, padding):
        self.pad['left'], self.pad['right'], self.pad['top'], self.pad['bottom'] = padding
        
    @property
    def left_pad(self):
        return self.pad['left']
        
    @left_pad.setter
    def left_pad(self, left_pad):
        self.pad['left'] = left_pad
        
    @property
    def right_pad(self):
        return self.pad['right']
        
    @right_pad.setter
    def right_pad(self, right_pad):
        self.pad['right'] = right_pad
        
    @property
    def top_pad(self):
        return self.pad['top']
        
    @top_pad.setter
    def top_pad(self, top_pad):
        self.pad['top'] = top_pad
        
    @property
    def bottom_pad(self):
        return self.pad['bottom']
        
    @bottom_pad.setter
    def bottom_pad(self, bottom_pad):
        self.pad['bottom'] = bottom_pad
        
    @property
    def x_pad(self):
        return self.pad['left']
        
    @x_pad.setter
    def x_pad(self, x_pad):
        self.pad['left'] = self.pad['right'] = x_pad
        
    @property
    def y_pad(self):
        return self.pad['top']
        
    @y_pad.setter
    def y_pad(self, y_pad):
        self.pad['top'] = self.pad['bottom'] = y_pad
        
    @property
    def border_kwargs(self):
        return {
            'border_radius': self.border_radius,
            'border_top_left_radius': self.border['topleft'],
            'border_top_right_radius': self.border['topright'],
            'border_bottom_left_radius': self.border['bottomleft'],
            'border_bottom_right_radius': self.border['bottomright']
        }
        
    @property
    def hit_mouse(self):
        return self.padded_rect.collidepoint(pg.mouse.get_pos())

    def set_padding(
        self,
        pad=None,
        left_pad=None,
        right_pad=None,
        top_pad=None,
        bottom_pad=None
    ):
        if pad:
            left_pad = right_pad = top_pad = bottom_pad = pad
        self.pad['left'] = left
        self.pad['right'] = right
        self.pad['top'] = top
        self.pad['bottom'] = bottom

    def restore_fill(self):
        self.fill_color = self.original_fill_color

    def draw_rect(self, surf):
        fill = self.fill_color and self.fill_color != self.key_color
        bk = self.border_kwargs
        if self.outline_color and self.outline_width:
            pg.draw.rect(
                surf,
                self.outline_color,
                self.outline_rect,
                width=self.outline_width if not fill else self.outline_width * 2,
                **bk
            ) 
        if fill:
            pg.draw.rect(
                surf,
                self.fill_color,
                self.padded_rect,
                **bk
            )

        if self.inner_outline_color and self.inner_outline_width:
            pg.draw.rect(
                surf,
                self.inner_outline_color,
                self.padded_rect,
                width=self.inner_outline_width,
                **bk
            )
            
    def draw(self, surf):
        self.draw_rect(surf)
        super().draw(surf)
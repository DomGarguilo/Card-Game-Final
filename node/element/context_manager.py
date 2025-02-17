import pygame as pg

from data.constants import NODE_DATA

from ..compiler import Compiler

from ..screens.about_node import run as run_about
from ..screens.output import run as run_output

from ui.element.elements import Button, Live_Window

class Context_Manager(Live_Window):
    def __init__(
        self,
        menu,
        node=None
    ):
        self.separators = []

        button_kwargs = {
            'size': (100, 25),
            'fill_color': (255, 255, 255),
            'text_color': (0, 0, 0),
            'text_size': 15,
            'centery_aligned': True,
            'hover_color': (100, 100, 100),
            'left_pad': 5
        }
        buttons = []
        
        def add_sep():
            self.separators.append(len(buttons))
        
        if node:
            
            if not node.selected:
                node.select()

            selected = menu.get_selected()
            
            b = Button.Text_Button(
                text='Copy',
                func=menu.copy_nodes,
                **button_kwargs
            )
            buttons.append(b)
            
            b = Button.Text_Button(
                text='Delete',
                func=menu.delete_nodes,
                **button_kwargs
            )
            buttons.append(b)
            
            add_sep()
    
            if node.is_group:
                b = Button.Text_Button(
                    text='Ungroup',
                    func=menu.ungroup_node,
                    args=[node],
                    **button_kwargs
                )
                buttons.append(b)
                
            elif len(selected) > 1:
                b = Button.Text_Button(
                    text='Group',
                    func=menu.create_new_group_node,
                    **button_kwargs
                )
                buttons.append(b)
                
            add_sep()

            if node.name in NODE_DATA:
                b = Button.Text_Button(
                    text='About Node',
                    func=run_about,
                    args=[node.name],
                    **button_kwargs
                )
                buttons.append(b)
                
            if not node.is_group and node.ports:
                b = Button.Text_Button(
                    text='View Output',
                    func=run_output,
                    args=[node],
                    **button_kwargs
                )
                buttons.append(b)
                
            add_sep()
                
        elif menu.copy_data:
            b = Button.Text_Button(
                text='Paste',
                func=menu.paste_nodes,
                **button_kwargs
            )
            buttons.append(b)
            
            add_sep()
            
        if menu.get_required():
            b = Button.Text_Button(
                text='Get Required',
                func=menu.load_required_nodes,
                **button_kwargs
            )
            buttons.append(b)
            
            add_sep()
            
        def select_all(menu):
            menu.get_current_events().update({
                'ctrl': True,
                'kd': pg.event.Event(pg.KEYDOWN, key=pg.K_a)
            })
            
        b = Button.Text_Button(
            text='Select All',
            func=select_all,
            args=[menu],
            **button_kwargs
        )
        buttons.append(b)
        
        b = Button.Text_Button(
            text='Clean Up',
            func=menu.clean_up,
            **button_kwargs
        )
        buttons.append(b)
        
        for b in buttons:
            b.add_animation(
                [{
                    'attr': 'text_color',
                    'end': (255, 255, 255)
                }],
                tag='hover'
            )
            
        super().__init__(
            size=(105, sum([b.rect.height for b in buttons])),
            pos=pg.mouse.get_pos(),
            outline_color=(0, 0, 0),
            outline_width=3
        )
        
        if buttons:
            self.join_elements(
                buttons,
                borderx=5
            )
            
        if self.rect.bottom > menu.body.height:
            self.rect.bottom = menu.body.height - 10
        if self.rect.right > menu.body.width:
            self.rect.right = menu.body.width - 10
        
    def draw(self, surf):
        super().draw(surf)
        
        for i in self.separators:
            e = self.elements[i]
            pg.draw.line(
                surf,
                (150, 150, 150),
                (e.rect.left, e.rect.top - 1),
                (e.rect.right - 10, e.rect.top - 1),
                width=2
            )
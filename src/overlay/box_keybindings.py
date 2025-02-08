import pygame

from src.settings import OVERLAY_POSITIONS
from src.sprites.entities.player import Player
from src.support import get_translated_string as _
from src.support import import_font, import_image


class BoxKeybindingsLabel:
    def __init__(self, entity: Player):
        # setup
        self.display_surface = pygame.display.get_surface()
        self.player = entity

        # dimensions
        self.left = 20
        self.top = 20

        width, height = 330, 50
        self.font = import_font(26, "font/LycheeSoda.ttf")

        self.rect = pygame.Rect(self.left, self.top, width, height)

        self.rect.topleft = OVERLAY_POSITIONS["box_info_label"]

    def display(self):
        # colors connected to player state
        white = "White"
        gray = "Gray"
        foreground_color = gray if self.player.blocked else white

        # rects and surfs
        pad_y = 2

        box_keybindings_label_surf = self.font.render(
            f"{_('box info label')}", False, foreground_color
        )
        box_keybindings_label_rect = box_keybindings_label_surf.get_frect(
            midright=(self.rect.right - 20, self.rect.centery + pad_y)
        )

        # display
        self.display_surface.blit(
            box_keybindings_label_surf, box_keybindings_label_rect
        )


class BoxKeybindings:
    def __init__(self):
        self.font_size = 17
        self.key_image_size = (30, 30)
        self.key_images = {}
        self.info_order = []
        self.image = self.load_and_scale_image_by_factor(
            "images/ui/KeyBindUI_Placeholder.png"
        )
        self.width = self.image.get_width()
        self.info = []
        self.visible = False
        self.pos = OVERLAY_POSITIONS["box_info"]
        self.font = import_font(self.font_size, "font/LycheeSoda.ttf")
        self.box_keybindings_rect = pygame.Rect(
            self.pos[0],
            self.pos[1],
            self.image.get_width(),
            self.image.get_height(),
        )
        self.color = (255, 255, 255)
        self.padding = 8

        # prepare texts
        self.setup_text_list()

    def setup_text_list(self):
        self.info = [
            {
                "key": "",
                "descr": self.get_text("box info player task"),
                "pos": (122, 510),
            },
            {
                "key": "lclick",
                "descr": self.get_text("box info left mouse"),
                "pos": (172, 120),
            },
            {"key": "tab", "descr": self.get_text("box info tab"), "pos": (172, 168)},
            {
                "key": "rclick",
                "descr": self.get_text("box info right mouse"),
                "pos": (172, 215),
            },
            {
                "key": "lshift",
                "descr": self.get_text("box info left shift"),
                "pos": (172, 263),
            },
            {
                "key": "space",
                "descr": self.get_text("box info space"),
                "pos": (172, 310),
                "descr_vert_shift": -12,
            },
            {"key": "I", "descr": self.get_text("box info i"), "pos": (172, 357)},
            {"key": "E", "descr": self.get_text("box info e"), "pos": (172, 405)},
            {"key": "ESC", "descr": self.get_text("box info esc"), "pos": (172, 452)},
        ]
        self.info_order = [
            "lclick",
            "tab",
            "rclick",
            "lshift",
            "space",
            "I",
            "E",
            "ESC",
            "",
        ]
        self.key_images = {
            "lclick": self.load_and_scale_image(
                "images/ui/keys/lclick.png", self.key_image_size
            ),
            "tab": self.load_and_scale_image(
                "images/ui/keys/tab.png", self.key_image_size
            ),
            "rclick": self.load_and_scale_image(
                "images/ui/keys/rclick.png", self.key_image_size
            ),
            "lshift": self.load_and_scale_image(
                "images/ui/keys/lshift.png", self.key_image_size
            ),
            "space": self.load_and_scale_image(
                "images/ui/keys/space.png", self.key_image_size
            ),
            "generic": self.load_and_scale_image(
                "images/ui/keys/generic.png", self.key_image_size
            ),
        }

    def get_text(self, key):
        translation = _(key)
        return translation.split("|") if "|" in translation else [translation]

    def load_and_scale_image(self, img_name, target_size):
        return pygame.transform.scale(import_image(img_name), target_size)

    def load_and_scale_image_by_factor(self, img_name):
        return pygame.transform.scale_by(import_image(img_name), 1.08)

    def toggle_visibility(self):
        self.visible = not self.visible

    def draw(self, display_surface):
        if not self.visible:
            return

        # display box
        display_surface.blit(self.image, self.box_keybindings_rect)

        # iterate over text list
        for info_key in self.info_order:
            current_info = self.get_ordered_info(info_key)
            key = current_info["key"]
            current_key_topleft = current_info["pos"]
            description = current_info["descr"]
            vertical_shift = (
                current_info["descr_vert_shift"]
                if "descr_vert_shift" in current_info.keys()
                else 0
            )
            current_desc_topleft = (
                current_key_topleft[0] + 40,
                current_key_topleft[1] + vertical_shift,
            )

            # prepare key for draw
            if len(key) > 0:
                self.draw_key_surface(current_key_topleft, key, display_surface)

            # prepare description for draw
            if len(description) > 1:
                current_topleft = current_desc_topleft
                for description_item in description:
                    self.draw_description_item(
                        current_topleft, description_item, display_surface
                    )
                    current_topleft = (current_topleft[0], current_topleft[1] + 18)
            else:
                self.draw_description_item(
                    current_desc_topleft, description[0], display_surface
                )

    def draw_description_item(self, current_topleft, description_item, display_surface):
        text_surf = self.font.render(description_item, False, "Black")
        text_rect = text_surf.get_frect(topleft=current_topleft)
        display_surface.blit(text_surf, text_rect)

    def draw_key_surface(self, current_key_topleft, key, display_surface):
        if key in self.key_images.keys():
            key_img = self.key_images[key]
            generic = False
        else:
            key_img = self.key_images["generic"]
            generic = True
        key_rect = pygame.Rect(
            current_key_topleft[0],
            current_key_topleft[1],
            7,
            7,
        )

        display_surface.blit(key_img, key_rect)
        if generic:
            key_surf = self.font.render(key, False, "White")
            key_tmp_rect = key_surf.get_frect()
            key_surf.get_frect(left=key_tmp_rect.left + 10, top=key_rect.top + 10)
            display_surface.blit(key_surf, key_rect)

    def get_ordered_info(self, info_key) -> dict:
        result = {}
        for info in self.info:
            if info["key"] != info_key:
                continue
            result = info
            break
        return result

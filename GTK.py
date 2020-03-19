#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '0.0')
from gi.repository import Gtk, GdkPixbuf, Handy
import questionAPI
import html
import configparser


APP_VERSION = "0.1"
APP_NAME = "Quiz"
APP_ID = "org.airon.quiz"


class Program(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self, title=APP_NAME)
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        hb = Handy.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Quiz"
        self.set_titlebar(hb)

        button = Gtk.Button()
        button.add(Gtk.Image.new_from_icon_name(
            "document-new", Gtk.IconSize.BUTTON))
        button.connect("clicked", self.on_new_clicked)  # , args)
        hb.pack_start(button)

        button = Gtk.Button()
        button.add(Gtk.Image.new_from_icon_name(
            "open-menu-symbolic", Gtk.IconSize.BUTTON))
        button.connect("clicked", self.on_menu_clicked)
        hb.pack_end(button)

        self.popover = Gtk.PopoverMenu()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        button = Gtk.Button()
        button.set_label("Information")
        button.connect("clicked", self.on_about)
        vbox.pack_start(button, True, True, 0)
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)

        self.vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        # Gtk.StyleContext.add_class(self.vbox.get_style_context(), "linked")
        self.add(self.vbox)

        label = "Test"
        TestLabel = Gtk.Label()
        TestLabel.set_text(label)
        self.vbox.add(TestLabel)

        # This should be filled when clicking New game button
        # There would be n lists for each player
        # Each sub-list would have k dictionaries for each question
        # Each dictionary would be composed by following keys:
        # ['category', 'type', 'difficulty', 'question', 'correct_answer', 'incorrect_answers']
        # 'type' is just 'multple' (4 answers, 1 correct and 3 wrong) or 'boolean' (True, False)
        
        self.questions = []
        
        if (len(self.questions) != 0):
            pl = 0
            for i in range(len(self.questions)):
                number = i
                quest = self.questions[pl]["results"][i]
                QuestionType = quest["type"]
                if TOPIC != "":
                    cat = quest["category"]
                if DIFFICULTY != "":
                    diff = quest["difficulty"]
                label = html.unescape(quest["question"])
                QuestionLabel = Gtk.Label()
                QuestionLabel.set_text(label)
                print(label)
                answers = questionAPI.generate_answers(quest, QuestionType)
                for k in range(len(answers)):
                    print(str(k + 1) + ". " + html.unescape(answers[k]))
                
                self.vbox.add(QuestionLabel)
                if (self.questions[pl]["results"][i]["type"] == "boolean"):
                    
                    button = Gtk.Button()
                    button.set_label("True")
                    button.connect("clicked", self.do_clicked)
                    self.vbox.add(button)
                    button = Gtk.Button()
                    button.set_label("False")
                    button.connect("clicked", self.do_clicked)
                    self.vbox.add(button)

        self.show_all()

    def do_clicked(self, button):
        print("You clicked Button!")

    def on_menu_clicked(self, button):
        self.popover.set_relative_to(button)
        self.popover.show_all()
        self.popover.popup()

    def on_new_clicked(self, args):
        n = 1  # 10
        players = 1  # FIXME More players
        TOKEN = questionAPI.get_token()
        TOPIC = ""
        DIFFICULTY = ""

        for pl in range(players):
            self.questions.append(questionAPI.generate_questions(
                n, TOKEN, TOPIC, DIFFICULTY))
        print("You clicked New!")

    def on_about(self, action):
        aboutdialog = Gtk.AboutDialog(modal=True, transient_for=self)
        aboutdialog.set_program_name(APP_NAME)
        aboutdialog.set_version(APP_VERSION)
        aboutdialog.set_license_type(Gtk.License.GPL_3_0)
        aboutdialog.set_copyright("Copyright \xa9 2020 Michael Moroni")
        aboutdialog.add_credit_section("Questions and logo",
            ["Questions are obtained via OpenTDB APIs,\navailable under CC-BY-SA 4.0 license", "Logo temporary taken from Wikimedia Commons"])
        aboutdialog.set_comments("Test your skills with questions and have fun with friends!")
        aboutdialog.set_authors(["Michael Moroni"])
        aboutdialog.set_documenters(["Michael Moroni"])
        aboutdialog.set_website("http://github.com/airon90/quiz")
        aboutdialog.set_website_label("GitHub repository")
        aboutdialog.set_translator_credits("Michael Moroni")
        aboutdialog.set_logo(
            GdkPixbuf.Pixbuf.new_from_file_at_size(
                "Documenti/Progetti/Quiz/logo.png", 64, 64))
        aboutdialog.connect('response', lambda dialog, data: dialog.destroy())
        aboutdialog.show_all()


def quit_app(undefined_arg1, undefined_arg2):
    Gtk.main_quit()


def main():
    app = Program()
    app.connect("delete-event", quit_app)
    app.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
################################################################
#                                                              #
#                Tokenizer by Andalik Industries               #
#                                                              #
################################################################
# Project       : Tokenizer                                    #
#   Author      : Renato Andalik                               #
#   Description : Calculate the number of tokens for a text    #
#                 or a text file                               #
#                                                              #
# Script        : tokenizer.py                                 #
#   Version     : 0.1                                          #
#   Created     : 2024-08-01                                   #
#   Last Update : 2024-08-11                                   #
################################################################
"""
import wx
import os
import PyPDF2
import tiktoken
import re

class TokenizerFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Tokenizer')
        self.SetBackgroundColour(wx.Colour(28, 28, 28))  # Fundo escuro
        self.InitUI()
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # Tokenizador GPT-4
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(28, 28, 28))  # Fundo escuro
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Menu bar
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)

        # Título
        title = wx.StaticText(panel, label="Tokenizer")
        title.SetForegroundColour(wx.WHITE)
        title.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(title, 0, wx.ALL, 10)

        # Descrição
        description = wx.StaticText(panel, label="Contador de Tokens")
        description.SetForegroundColour(wx.WHITE)
        description.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        main_sizer.Add(description, 0, wx.ALL, 10)

        # Área para arrastar e soltar arquivos
        self.drop_target = wx.Panel(panel)
        self.drop_target.SetBackgroundColour(wx.Colour(45, 45, 45))
        self.drop_target.SetMinSize((760, 100))
        file_drop = FileDrop(self)
        self.drop_target.SetDropTarget(file_drop)
        
        self.file_text = wx.StaticText(self.drop_target, label="Arraste e solte um arquivo de texto aqui (TXT, MD ou PDF)")
        self.file_text.SetForegroundColour(wx.Colour(200, 200, 200))
        font = self.file_text.GetFont()
        font.SetPointSize(12)
        self.file_text.SetFont(font)
        
        self.drop_target.Bind(wx.EVT_SIZE, self.OnDropTargetSize)
        
        main_sizer.Add(self.drop_target, 0, wx.EXPAND | wx.ALL, 10)

        # Área de entrada de texto
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.text_ctrl.SetBackgroundColour(wx.Colour(45, 45, 45))  # Um pouco mais claro que o fundo
        self.text_ctrl.SetForegroundColour(wx.WHITE)
        self.text_ctrl.SetHint("Digite algum texto")
        main_sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        # Botões
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        clear_button = wx.Button(panel, label="Limpar")
        show_example_button = wx.Button(panel, label="Mostrar exemplo")
        button_sizer.Add(clear_button, 0, wx.RIGHT, 10)
        button_sizer.Add(show_example_button, 0)
        main_sizer.Add(button_sizer, 0, wx.ALL, 10)

        # Contagem de Tokens, Palavras e Caracteres
        count_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.token_count = wx.StaticText(panel, label="Tokens\n0")
        self.token_count.SetForegroundColour(wx.WHITE)
        self.token_count.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        count_sizer.Add(self.token_count, 0, wx.RIGHT, 35)
        
        self.word_count = wx.StaticText(panel, label="Palavras\n0")
        self.word_count.SetForegroundColour(wx.WHITE)
        self.word_count.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        count_sizer.Add(self.word_count, 0, wx.RIGHT, 35)
        
        self.char_count = wx.StaticText(panel, label="Caracteres\n0")
        self.char_count.SetForegroundColour(wx.WHITE)
        self.char_count.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        count_sizer.Add(self.char_count, 0)
        
        main_sizer.Add(count_sizer, 0, wx.ALL, 10)

        panel.SetSizer(main_sizer)
        
        # Vinculações
        self.text_ctrl.Bind(wx.EVT_TEXT, self.OnTextChange)
        clear_button.Bind(wx.EVT_BUTTON, self.OnClear)
        show_example_button.Bind(wx.EVT_BUTTON, self.OnShowExample)

        # Definir tamanho do frame
        self.SetSize((800, 600))
        self.SetSizeHints(400,400)
        self.Centre()

    def OnDropTargetSize(self, event):
        size = event.GetSize()
        self.file_text.SetPosition(((size.width - self.file_text.GetSize().width) // 2,
                                    (size.height - self.file_text.GetSize().height) // 2))
        event.Skip()

    def OnTextChange(self, event):
        text = self.text_ctrl.GetValue()
        self.UpdateCounts(text)

    def UpdateCounts(self, text):
        tokens = self.tokenizer.encode(text)
        token_count = len(tokens)
        word_count = len(re.findall(r'\w+', text))
        char_count = len(text)
        self.token_count.SetLabel(f"Tokens\n{token_count}")
        self.word_count.SetLabel(f"Palavras\n{word_count}")
        self.char_count.SetLabel(f"Caracteres\n{char_count}")

    def OnClear(self, event):
        self.text_ctrl.Clear()
        self.UpdateCounts("")

    def OnShowExample(self, event):
        example_text = "Os modelos de linguagem (LLMs) processam textos utilizando tokens, que são sequências comuns de caracteres encontradas em um conjunto de dados. Em resumo, os modelos aprendem a entender as relações estatísticas entre esses tokens, tornando-se altamente eficazes na previsão do próximo token em uma sequência.\n\nO Tokenizer é responsável por determinar como uma parte do texto é dividida em tokens por um modelo de linguagem, além de calcular a quantidade de tokens gerados.\n\nÉ importante destacar que o processo de tokenização varia entre os modelos. Modelos mais recentes utilizam tokenizadores diferentes dos mais antigos, o que resulta em tokens distintos para o mesmo texto de entrada."
        self.text_ctrl.SetValue(example_text)
        self.UpdateCounts(example_text)

    def ShowErrorDialog(self, message):
        wx.MessageBox(message, "Erro", wx.OK | wx.ICON_ERROR)

    def OnClose(self, event):
        self.Destroy()

class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        if filenames:
            try:
                content = self.read_file(filenames[0])
                self.window.text_ctrl.SetValue(content)
                self.window.UpdateCounts(content)
            except Exception as e:
                self.window.ShowErrorDialog(f"Erro ao ler o arquivo: {str(e)}")
        return True

    def read_file(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        
        if file_extension.lower() == '.pdf':
            return self.read_pdf(file_path)
        else:
            return self.read_text_file(file_path)

    def read_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def read_text_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

class TokenizerApp(wx.App):
    def OnInit(self):
        frame = TokenizerFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return True

    def OnExit(self):
        return 0

if __name__ == '__main__':
    app = TokenizerApp()
    app.MainLoop()

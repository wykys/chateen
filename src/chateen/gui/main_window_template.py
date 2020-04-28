# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chateen.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(858, 544)
        icon = QIcon()
        icon.addFile(u"img/chateen.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.menu_help_help = QAction(MainWindow)
        self.menu_help_help.setObjectName(u"menu_help_help")
        self.menu_help_about = QAction(MainWindow)
        self.menu_help_about.setObjectName(u"menu_help_about")
        self.menu_tools_reduce = QAction(MainWindow)
        self.menu_tools_reduce.setObjectName(u"menu_tools_reduce")
        self.menu_tools_clean = QAction(MainWindow)
        self.menu_tools_clean.setObjectName(u"menu_tools_clean")
        self.menu_file_open = QAction(MainWindow)
        self.menu_file_open.setObjectName(u"menu_file_open")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.tabwidget = QTabWidget(self.splitter)
        self.tabwidget.setObjectName(u"tabwidget")
        self.tabwidget.setEnabled(True)
        self.tabwidget.setDocumentMode(False)
        self.tabwidget.setMovable(False)
        self.tab_chats = QWidget()
        self.tab_chats.setObjectName(u"tab_chats")
        self.verticalLayout_4 = QVBoxLayout(self.tab_chats)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.table_chats = QTableView(self.tab_chats)
        self.table_chats.setObjectName(u"table_chats")

        self.verticalLayout_4.addWidget(self.table_chats)

        self.tabwidget.addTab(self.tab_chats, "")
        self.tab_participants = QWidget()
        self.tab_participants.setObjectName(u"tab_participants")
        self.verticalLayout_3 = QVBoxLayout(self.tab_participants)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.table_participants = QTableView(self.tab_participants)
        self.table_participants.setObjectName(u"table_participants")

        self.verticalLayout_3.addWidget(self.table_participants)

        self.tabwidget.addTab(self.tab_participants, "")
        self.tab_more = QWidget()
        self.tab_more.setObjectName(u"tab_more")
        self.tab_more.setEnabled(True)
        self.verticalLayout_7 = QVBoxLayout(self.tab_more)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.text_more = QTextEdit(self.tab_more)
        self.text_more.setObjectName(u"text_more")
        self.text_more.setVisible(False)
        self.text_more.setReadOnly(True)

        self.verticalLayout_7.addWidget(self.text_more)

        self.table_more = QTableView(self.tab_more)
        self.table_more.setObjectName(u"table_more")

        self.verticalLayout_7.addWidget(self.table_more)

        self.tabwidget.addTab(self.tab_more, "")
        self.splitter.addWidget(self.tabwidget)
        self.widget_right = QWidget(self.splitter)
        self.widget_right.setObjectName(u"widget_right")
        self.widget_right.setEnabled(True)
        self.widget_right.setMaximumSize(QSize(300, 16777215))
        self.widget_right.setBaseSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.widget_right)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.group_who = QGroupBox(self.widget_right)
        self.group_who.setObjectName(u"group_who")
        self.verticalLayout_5 = QVBoxLayout(self.group_who)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.radio_button_who_all = QRadioButton(self.group_who)
        self.radio_button_who_all.setObjectName(u"radio_button_who_all")
        self.radio_button_who_all.setChecked(True)

        self.verticalLayout_5.addWidget(self.radio_button_who_all)

        self.radio_button_who_one = QRadioButton(self.group_who)
        self.radio_button_who_one.setObjectName(u"radio_button_who_one")
        self.radio_button_who_one.setChecked(False)

        self.verticalLayout_5.addWidget(self.radio_button_who_one)

        self.line_edit_participant = QLineEdit(self.group_who)
        self.line_edit_participant.setObjectName(u"line_edit_participant")
        self.line_edit_participant.setEnabled(False)

        self.verticalLayout_5.addWidget(self.line_edit_participant)


        self.verticalLayout_2.addWidget(self.group_who)

        self.group_date = QGroupBox(self.widget_right)
        self.group_date.setObjectName(u"group_date")
        self.verticalLayout_6 = QVBoxLayout(self.group_date)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget_date_enable = QWidget(self.group_date)
        self.widget_date_enable.setObjectName(u"widget_date_enable")
        self.verticalLayout_9 = QVBoxLayout(self.widget_date_enable)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 9)
        self.radio_button_date_no = QRadioButton(self.widget_date_enable)
        self.radio_button_date_no.setObjectName(u"radio_button_date_no")
        self.radio_button_date_no.setChecked(True)

        self.verticalLayout_9.addWidget(self.radio_button_date_no)

        self.radio_button_date_yes = QRadioButton(self.widget_date_enable)
        self.radio_button_date_yes.setObjectName(u"radio_button_date_yes")

        self.verticalLayout_9.addWidget(self.radio_button_date_yes)


        self.verticalLayout_6.addWidget(self.widget_date_enable)

        self.widget_date_range = QWidget(self.group_date)
        self.widget_date_range.setObjectName(u"widget_date_range")
        self.widget_date_range.setEnabled(True)
        self.widget_date_range.setVisible(False)
        self.verticalLayout_8 = QVBoxLayout(self.widget_date_range)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.widget_date_from = QWidget(self.widget_date_range)
        self.widget_date_from.setObjectName(u"widget_date_from")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_date_from)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.checkbox_from = QCheckBox(self.widget_date_from)
        self.checkbox_from.setObjectName(u"checkbox_from")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkbox_from.sizePolicy().hasHeightForWidth())
        self.checkbox_from.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.checkbox_from)

        self.date_from = QDateEdit(self.widget_date_from)
        self.date_from.setObjectName(u"date_from")
        self.date_from.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.date_from)


        self.verticalLayout_8.addWidget(self.widget_date_from)

        self.widget_date_to = QWidget(self.widget_date_range)
        self.widget_date_to.setObjectName(u"widget_date_to")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_date_to)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.checkbox_to = QCheckBox(self.widget_date_to)
        self.checkbox_to.setObjectName(u"checkbox_to")
        sizePolicy.setHeightForWidth(self.checkbox_to.sizePolicy().hasHeightForWidth())
        self.checkbox_to.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.checkbox_to)

        self.date_to = QDateEdit(self.widget_date_to)
        self.date_to.setObjectName(u"date_to")
        self.date_to.setEnabled(False)
        self.date_to.setWrapping(False)
        self.date_to.setFrame(True)

        self.horizontalLayout_4.addWidget(self.date_to)


        self.verticalLayout_8.addWidget(self.widget_date_to)


        self.verticalLayout_6.addWidget(self.widget_date_range)


        self.verticalLayout_2.addWidget(self.group_date)

        self.groupbox_select = QGroupBox(self.widget_right)
        self.groupbox_select.setObjectName(u"groupbox_select")
        self.verticalLayout_10 = QVBoxLayout(self.groupbox_select)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.btn_select_all = QPushButton(self.groupbox_select)
        self.btn_select_all.setObjectName(u"btn_select_all")
#if QT_CONFIG(tooltip)
        self.btn_select_all.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.btn_select_all.setStatusTip(u"Vybere v\u0161echny chaty.")
#endif // QT_CONFIG(statustip)

        self.verticalLayout_10.addWidget(self.btn_select_all)

        self.btn_deselect_all = QPushButton(self.groupbox_select)
        self.btn_deselect_all.setObjectName(u"btn_deselect_all")

        self.verticalLayout_10.addWidget(self.btn_deselect_all)


        self.verticalLayout_2.addWidget(self.groupbox_select)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.group_export = QGroupBox(self.widget_right)
        self.group_export.setObjectName(u"group_export")
        self.verticalLayout = QVBoxLayout(self.group_export)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkbox_export_format = QCheckBox(self.group_export)
        self.checkbox_export_format.setObjectName(u"checkbox_export_format")

        self.verticalLayout.addWidget(self.checkbox_export_format)

        self.btn_export = QPushButton(self.group_export)
        self.btn_export.setObjectName(u"btn_export")
        self.btn_export.setEnabled(False)

        self.verticalLayout.addWidget(self.btn_export)


        self.verticalLayout_2.addWidget(self.group_export)

        self.splitter.addWidget(self.widget_right)

        self.horizontalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 858, 22))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_file.setToolTipsVisible(True)
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_tools = QMenu(self.menubar)
        self.menu_tools.setObjectName(u"menu_tools")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.menu_file_open)
        self.menu_help.addAction(self.menu_help_help)
        self.menu_help.addAction(self.menu_help_about)
        self.menu_tools.addAction(self.menu_tools_reduce)
        self.menu_tools.addAction(self.menu_tools_clean)

        self.retranslateUi(MainWindow)
        self.radio_button_who_one.toggled.connect(self.line_edit_participant.setEnabled)
        self.checkbox_from.toggled.connect(self.date_from.setEnabled)
        self.checkbox_to.toggled.connect(self.date_to.setEnabled)
        self.radio_button_date_no.clicked.connect(self.widget_date_range.hide)
        self.radio_button_date_yes.clicked.connect(self.widget_date_range.show)
        self.menu_tools_clean.triggered.connect(MainWindow.callback_menu_tools_clean)
        self.menu_tools_reduce.triggered.connect(MainWindow.callback_menu_tools_reduce)
        self.btn_select_all.clicked.connect(MainWindow.callback_btn_select_all_clicked)
        self.btn_deselect_all.clicked.connect(MainWindow.callback_btn_deselect_all_clicked)
        self.btn_export.clicked.connect(MainWindow.callback_btn_export)
        self.radio_button_who_one.toggled.connect(MainWindow.callback_check_export_is_ready)
        self.radio_button_date_yes.toggled.connect(MainWindow.callback_check_export_is_ready)
        self.line_edit_participant.textChanged.connect(MainWindow.callback_check_export_is_ready)
        self.date_from.dateChanged.connect(MainWindow.callback_check_export_is_ready)
        self.date_to.dateChanged.connect(MainWindow.callback_check_export_is_ready)
        self.checkbox_from.toggled.connect(MainWindow.callback_check_export_is_ready)
        self.checkbox_to.toggled.connect(MainWindow.callback_check_export_is_ready)
        self.radio_button_who_all.toggled.connect(self.checkbox_export_format.setEnabled)
        self.menu_file_open.triggered.connect(MainWindow.callback_menu_file_open)
        self.menu_help_help.triggered.connect(MainWindow.callback_menu_help_help)
        self.menu_help_about.triggered.connect(MainWindow.callback_menu_help_about)

        self.tabwidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menu_help_help.setText(QCoreApplication.translate("MainWindow", u"N\u00e1pov\u011bda programu", None))
#if QT_CONFIG(tooltip)
        self.menu_help_help.setToolTip(QCoreApplication.translate("MainWindow", u"Zobraz\u00ed n\u00e1pov\u011bdu programu.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.menu_help_help.setStatusTip(QCoreApplication.translate("MainWindow", u"Zobraz\u00ed n\u00e1pov\u011bdu programu.", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.menu_help_help.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.menu_help_about.setText(QCoreApplication.translate("MainWindow", u"O projektu", None))
#if QT_CONFIG(tooltip)
        self.menu_help_about.setToolTip(QCoreApplication.translate("MainWindow", u"Zobraz\u00ed v\u00edce informac\u00ed o projektu.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.menu_help_about.setStatusTip(QCoreApplication.translate("MainWindow", u"Zobraz\u00ed v\u00edce informac\u00ed o projektu.", None))
#endif // QT_CONFIG(statustip)
        self.menu_tools_reduce.setText(QCoreApplication.translate("MainWindow", u"Fejka\u0159 Otto", None))
#if QT_CONFIG(tooltip)
        self.menu_tools_reduce.setToolTip(QCoreApplication.translate("MainWindow", u"N\u00e1stroj pro zjednodu\u0161en\u00ed datab\u00e1ze.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.menu_tools_reduce.setStatusTip(QCoreApplication.translate("MainWindow", u"Sjednot\u00ed p\u0159isp\u011bvatele co maj\u00e9 m\u00e9n\u011b ne\u017e 50 zpr\u00e1v a chaty co maj\u00ed m\u00e9n\u011b ne\u017e 100 zpr\u00e1v.", None))
#endif // QT_CONFIG(statustip)
        self.menu_tools_clean.setText(QCoreApplication.translate("MainWindow", u"Vymazat", None))
#if QT_CONFIG(tooltip)
        self.menu_tools_clean.setToolTip(QCoreApplication.translate("MainWindow", u"Sma\u017ee v\u0161echna na\u010dten\u00e1 data.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.menu_tools_clean.setStatusTip(QCoreApplication.translate("MainWindow", u"Sma\u017ee v\u0161echna na\u010dten\u00e1 data.", None))
#endif // QT_CONFIG(statustip)
        self.menu_file_open.setText(QCoreApplication.translate("MainWindow", u"Otev\u0159\u00edt", None))
#if QT_CONFIG(tooltip)
        self.menu_file_open.setToolTip(QCoreApplication.translate("MainWindow", u"Otev\u0159\u00edt soubor JSON s daty o va\u0161ich konverzac\u00edch.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.menu_file_open.setStatusTip(QCoreApplication.translate("MainWindow", u"Otev\u0159\u00edt soubor JSON s daty o va\u0161ich konverzac\u00edch.", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.menu_file_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_chats), QCoreApplication.translate("MainWindow", u"Chaty", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_participants), QCoreApplication.translate("MainWindow", u"\u00da\u010dastn\u00edci", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_more), QCoreApplication.translate("MainWindow", u"V\u00edce", None))
        self.group_who.setTitle(QCoreApplication.translate("MainWindow", u"Kdo poskytene data?", None))
        self.radio_button_who_all.setText(QCoreApplication.translate("MainWindow", u"V\u0161ichni \u00fa\u010dastn\u00edci", None))
        self.radio_button_who_one.setText(QCoreApplication.translate("MainWindow", u"J\u00e1", None))
#if QT_CONFIG(tooltip)
        self.line_edit_participant.setToolTip(QCoreApplication.translate("MainWindow", u"\u00da\u010dastn\u00edku, zadejte sv\u00e9 jm\u00e9no.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.line_edit_participant.setStatusTip(QCoreApplication.translate("MainWindow", u"Zadejte sv\u00e9m jm\u00e9no.", None))
#endif // QT_CONFIG(statustip)
        self.group_date.setTitle(QCoreApplication.translate("MainWindow", u"\u010casov\u011b omezit data?", None))
        self.radio_button_date_no.setText(QCoreApplication.translate("MainWindow", u"Ne", None))
        self.radio_button_date_yes.setText(QCoreApplication.translate("MainWindow", u"Ano", None))
        self.checkbox_from.setText(QCoreApplication.translate("MainWindow", u"Od", None))
        self.date_from.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd.MM.yyyy", None))
        self.checkbox_to.setText(QCoreApplication.translate("MainWindow", u"Do", None))
        self.date_to.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd.MM.yyyy", None))
        self.groupbox_select.setTitle(QCoreApplication.translate("MainWindow", u"Pomocn\u00edk s v\u00fdb\u011bry.", None))
        self.btn_select_all.setText(QCoreApplication.translate("MainWindow", u"Onzna\u010dit v\u0161e", None))
#if QT_CONFIG(statustip)
        self.btn_deselect_all.setStatusTip(QCoreApplication.translate("MainWindow", u"Zru\u0161\u00ed aktu\u00e1ln\u00ed v\u00fdb\u011br.", None))
#endif // QT_CONFIG(statustip)
        self.btn_deselect_all.setText(QCoreApplication.translate("MainWindow", u"Odzna\u010dit v\u0161e", None))
        self.group_export.setTitle(QCoreApplication.translate("MainWindow", u"P\u0159isp\u011bte na olt\u00e1\u0159 v\u011bdy.", None))
#if QT_CONFIG(statustip)
        self.checkbox_export_format.setStatusTip(QCoreApplication.translate("MainWindow", u"Pokud je tato volba aktivn\u00ed, tak v\u00fdsledn\u00e9 soubory budou rozd\u011bleny dle chat\u016f.", None))
#endif // QT_CONFIG(statustip)
        self.checkbox_export_format.setText(QCoreApplication.translate("MainWindow", u"Rozd\u011blit na chaty", None))
#if QT_CONFIG(statustip)
        self.btn_export.setStatusTip(QCoreApplication.translate("MainWindow", u"Vegeneruje data pro korpus.", None))
#endif // QT_CONFIG(statustip)
        self.btn_export.setText(QCoreApplication.translate("MainWindow", u"Exportovat", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"Soubor", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"N\u00e1pov\u011bda", None))
        self.menu_tools.setTitle(QCoreApplication.translate("MainWindow", u"N\u00e1stroje", None))
    # retranslateUi


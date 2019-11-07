import sys
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QLabel,QLineEdit,QGroupBox, QGroupBox, QTabWidget
from PyQt5.QtCore import QSize


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Start Database Connection section
        database_section = QHBoxLayout()
        group_database = QGroupBox("Database connection")
        database_section.addWidget(group_database)
        database_layout = QVBoxLayout()
        database_inner_glayout = QGridLayout()
        database_inner_glayout.addWidget(QLabel("Host"), 0, 0) # Label at row 0, column 0
        database_inner_glayout.addWidget(QLineEdit(),0,1) # LineEdit at row 0, column 1
        database_inner_glayout.addWidget(QLabel("Port"), 1, 0)
        database_inner_glayout.addWidget(QLineEdit(), 1, 1)
        database_inner_glayout.addWidget(QLabel("DBname"), 2, 0)
        database_inner_glayout.addWidget(QLineEdit(), 2, 1)
        database_inner_glayout.addWidget(QLabel("Username"), 0, 2)
        database_inner_glayout.addWidget(QLineEdit(), 0, 3)
        database_inner_glayout.addWidget(QLabel("Password"), 1, 2)
        database_inner_glayout.addWidget(QLineEdit(), 1, 3)

        database_inner_hbox = QHBoxLayout()
        database_inner_hbox.addStretch()
        database_inner_hbox.addWidget(QPushButton("Connect"))

        database_layout.addLayout(database_inner_glayout)
        database_layout.addLayout(database_inner_hbox)
        group_database.setLayout(database_layout)

        # start of enter two query for execution (to produce query plan) section
        query_statement_section = QHBoxLayout()
        group_query_statement = QGroupBox("1. Enter Two Query")
        query_statement_section.addWidget(group_query_statement)

        query_statement_layout = QVBoxLayout()
        query_statement_inner_glayout = QGridLayout()
        query_statement_inner_glayout.addWidget(QPlainTextEdit(), 0,0)
        query_statement_inner_glayout.addWidget(QPlainTextEdit(), 0,1)

        query_statement_inner_hbox = QHBoxLayout()
        query_statement_inner_hbox.addStretch()
        query_statement_inner_hbox.addWidget(QPushButton("Generate Query Plans"))

        query_statement_layout.addLayout(query_statement_inner_glayout)
        query_statement_layout.addLayout(query_statement_inner_hbox)
        group_query_statement.setLayout(query_statement_layout)
        # end of enter two for execution section

        # start of query results (query plan,query NLP, etc) section. - I call it results because it returns two stuffs
        query_result_section = QHBoxLayout()
        group_query_result = QGroupBox("2. Query Plan and English NLP resulted from above queries")
        query_result_section.addWidget(group_query_result)

        query_result_layout = QVBoxLayout()

        # to hold the two tabs group
        query_result_tabs_hbox = QHBoxLayout()

        # left's tabs
        left_tab_group = QTabWidget()
        left_tab1 = QWidget()
        left_tab2 = QWidget()

        left_tab_group.addTab(left_tab1,"Query Plan")
        left_tab_group.addTab(left_tab2,"Explaination")

        # left tabs' content
        # query plan
        left_tab1_inner_vbox = QVBoxLayout()
        left_tab1_inner_vbox.addWidget(QPlainTextEdit("Contains query 1's query plan"))
        left_tab1.setLayout(left_tab1_inner_vbox)

        # query explaination
        left_tab2_inner_vbox = QVBoxLayout()
        left_tab2_inner_vbox.addWidget(QPlainTextEdit("Contains query 1's explaination"))
        left_tab2.setLayout(left_tab2_inner_vbox)

        # right's tabs
        right_tab_group = QTabWidget()
        right_tab1 = QWidget()
        right_tab2 = QWidget()

        right_tab_group.addTab(right_tab1, "Query Plan")
        right_tab_group.addTab(right_tab2, "Explaination")

        # right tabs' content
        # query plan
        right_tab1_inner_vbox = QVBoxLayout()
        right_tab1_inner_vbox.addWidget(QPlainTextEdit("Contains query 2's query plan"))
        right_tab1.setLayout(right_tab1_inner_vbox)

        # query explaination
        right_tab2_inner_vbox = QVBoxLayout()
        right_tab2_inner_vbox.addWidget(QPlainTextEdit("Contains query 2's explaination"))
        right_tab2.setLayout(right_tab2_inner_vbox)

        # end of tabs
        query_result_inner_hbox = QHBoxLayout()
        query_result_inner_hbox.addStretch()
        query_result_inner_hbox.addWidget(QPushButton("Generate differences"))


        query_result_tabs_hbox.addWidget(left_tab_group)
        query_result_tabs_hbox.addWidget(right_tab_group)
        query_result_layout.addLayout(query_result_tabs_hbox)
        query_result_layout.addLayout(query_result_inner_hbox)
        group_query_result.setLayout(query_result_layout)
        #end of query result section

        #start of difference between queries section
        difference_section = QHBoxLayout()
        group_difference = QGroupBox("3. Differences between two queries")
        difference_section.addWidget(group_difference)

        difference_layout = QVBoxLayout()
        difference_layout.addWidget(QPlainTextEdit("Difference"))
        group_difference.setLayout(difference_layout)
        # end of difference between queries section


        # main layout
        vbox = QVBoxLayout()
        vbox.addLayout(database_section)
        vbox.addLayout(query_statement_section)
        vbox.addLayout(query_result_section)
        vbox.addLayout(difference_section)

        self.setLayout(vbox)
        self.setWindowTitle('CZ4031')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
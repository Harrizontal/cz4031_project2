import sys
import json
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QLabel,QLineEdit,QGroupBox, QGroupBox, QTabWidget,QMessageBox
from PyQt5.QtCore import pyqtSlot, QSize
from Connection import Connection
import vocalizer2
from Session import Session

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.connection = ''
        self.session = None

        self.initUI()
        self.initConnection()

    def initUI(self):

        # Start Database Connection section

        self.lineedit_host = QLineEdit()
        self.lineedit_port = QLineEdit()
        self.lineedit_dbname = QLineEdit()
        self.lineedit_username = QLineEdit()
        self.lineedit_password = QLineEdit()



        database_section = QHBoxLayout()
        group_database = QGroupBox("Database connection")
        database_section.addWidget(group_database)
        database_layout = QVBoxLayout()
        database_inner_glayout = QGridLayout()
        database_inner_glayout.addWidget(QLabel("Host"), 0, 0) # Label at row 0, column 0
        database_inner_glayout.addWidget(self.lineedit_host,0,1) # LineEdit at row 0, column 1
        database_inner_glayout.addWidget(QLabel("Port"), 1, 0)
        database_inner_glayout.addWidget(self.lineedit_port, 1, 1)
        database_inner_glayout.addWidget(QLabel("DBname"), 2, 0)
        database_inner_glayout.addWidget(self.lineedit_dbname, 2, 1)
        database_inner_glayout.addWidget(QLabel("Username"), 0, 2)
        database_inner_glayout.addWidget(self.lineedit_username, 0, 3)
        database_inner_glayout.addWidget(QLabel("Password"), 1, 2)
        database_inner_glayout.addWidget(self.lineedit_password, 1, 3)

        database_inner_hbox = QHBoxLayout()
        database_inner_hbox.addStretch()
        database_inner_hbox.addWidget(QPushButton("Hello"))

        button = QPushButton("Connect", self)
        button.clicked.connect(self.click_connect)
        database_inner_hbox.addWidget(button)

        database_inner_glayout.addWidget(button, 2, 3)

        database_layout.addLayout(database_inner_glayout)
        #database_layout.addLayout(database_inner_hbox)
        group_database.setLayout(database_layout)

        # start of enter two query for execution (to produce query plan) section

        self.plaintextedit_query1 = QPlainTextEdit()
        self.plaintextedit_query2 = QPlainTextEdit()

        button_generate_query_plans = QPushButton("Generate Query Plans")
        button_generate_query_plans.clicked.connect(self.click_generate_query_plans)

        query_statement_section = QHBoxLayout()
        group_query_statement = QGroupBox("1. Enter Two Query")
        query_statement_section.addWidget(group_query_statement)

        query_statement_layout = QVBoxLayout()
        query_statement_inner_glayout = QGridLayout()
        query_statement_inner_glayout.addWidget(self.plaintextedit_query1, 0,0)
        query_statement_inner_glayout.addWidget(self.plaintextedit_query2, 0,1)

        query_statement_inner_hbox = QHBoxLayout()
        query_statement_inner_hbox.addStretch()
        query_statement_inner_hbox.addWidget(button_generate_query_plans)

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
        self.query_one_button = QPushButton("Show query 1 tree", self)
        self.query_one_button.setEnabled(False)
        self.query_one_button.clicked.connect(self.click_show_query_one_tree)
        self.plaintextedit_queryplan1 = QPlainTextEdit()
        left_tab1_inner_vbox = QVBoxLayout()
        left_tab1_inner_vbox.addWidget(self.plaintextedit_queryplan1)
        left_tab1_inner_vbox.addWidget(self.query_one_button)
        left_tab1.setLayout(left_tab1_inner_vbox)

        # query explaination
        left_tab2_inner_vbox = QVBoxLayout()
        self.query_one_explanation = QPlainTextEdit()
        left_tab2_inner_vbox.addWidget(self.query_one_explanation)
        left_tab2.setLayout(left_tab2_inner_vbox)

        # right's tabs
        right_tab_group = QTabWidget()
        right_tab1 = QWidget()
        right_tab2 = QWidget()

        right_tab_group.addTab(right_tab1, "Query Plan")
        right_tab_group.addTab(right_tab2, "Explaination")

        # right tabs' content
        # query
        self.query_two_button = QPushButton("Show query 2 tree", self)
        self.query_two_button.setEnabled(False)
        self.query_two_button.clicked.connect(self.click_show_query_two_tree)
        self.plaintextedit_queryplan2 = QPlainTextEdit()
        right_tab1_inner_vbox = QVBoxLayout()
        right_tab1_inner_vbox.addWidget(self.plaintextedit_queryplan2)
        right_tab1_inner_vbox.addWidget(self.query_two_button)
        right_tab1.setLayout(right_tab1_inner_vbox)

        # query explaination
        right_tab2_inner_vbox = QVBoxLayout()
        self.query_two_explaination = QPlainTextEdit()
        right_tab2_inner_vbox.addWidget(self.query_two_explaination)
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


    def initConnection(self):
        with open('config.json', 'r') as f:
            connection_dict = json.load(f)
            print(connection_dict['db'])
            self.lineedit_host.setText(str(connection_dict['db']['host']))
            self.lineedit_port.setText(str(connection_dict['db']['port']))
            self.lineedit_dbname.setText(str(connection_dict['db']['dbname']))
            self.lineedit_username.setText(str(connection_dict['db']['username']))
            self.lineedit_password.setText(str(connection_dict['db']['password']))

    def pop_up_message(self,message):
        QMessageBox.about(self, "Alert", message)

    def click_connect(self):
        host = self.lineedit_host.text()
        port = self.lineedit_port.text()
        dbname = self.lineedit_dbname.text()
        username = self.lineedit_username.text()
        password = self.lineedit_password.text()

        con = Connection()
        con.override_configuration(host=host,port=port,dbname=dbname,username=username,password=password)
        con.connect()
        if (con != None):
            self.pop_up_message("Connected")

        self.connection = con

    def click_generate_query_plans(self):
        print("generate query plans")
        if not self.plaintextedit_query1.toPlainText().strip() or not self.plaintextedit_query2.toPlainText().strip():
            self.pop_up_message("Please ensure both box has SQL query")
            return

        if not self.connection:
            self.pop_up_message("Please connect to PostgesSQL server first.")
            return

        self.session = Session(self.connection, self.plaintextedit_query1.toPlainText(), self.plaintextedit_query2.toPlainText())
        self.query_one_button.setEnabled(True)
        self.query_two_button.setEnabled(True)
        self.plaintextedit_queryplan1.setPlainText(str(json.dumps(self.session.query_one_qep_raw)))
        self.plaintextedit_queryplan2.setPlainText(str(json.dumps(self.session.query_two_qep_raw)))
        query_one_explanation_list  = vocalizer2.textVersion(self.session.query_one_qep_root_node)
        query_two_explanation_list = vocalizer2.textVersion(self.session.query_two_qep_root_node)
        self.query_one_explanation.setPlainText("\n".join(query_one_explanation_list))
        self.query_two_explaination.setPlainText("\n".join(query_two_explanation_list))

    def click_show_query_one_tree(self):
        self.session.show_query_one_graph()

    def click_show_query_two_tree(self):
        self.session.show_query_two_graph()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
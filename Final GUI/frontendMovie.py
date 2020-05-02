import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from backendMovie import backend

class Window(QWidget):

    def __init__(self, user_id):
        super().__init__()
        self.title = "Movie_App"
        self.top = 300
        self.left = 300
        self.width = 750
        self.height = 700
        self.user_id = user_id
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        layoutV = QVBoxLayout()
        self.mybackend=backend()
        oImage = QImage("mainBack.jpg")
        sImage = oImage.scaled(QSize(self.width,self.height))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.enter = QPushButton(self)
        self.enter.setText('Enter!')
        self.enter.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.text = QLineEdit()
        self.enter.clicked.connect(self.enter_onClick)
        self.filter = QComboBox()

        self.filter.addItem("Name")
        self.filter.addItem("Genre")
        self.filter.addItem("Age")

        layout= QHBoxLayout()
        layout.addWidget(self.filter)
        layout.addWidget(self.text)
        layout.addWidget(self.enter)
        layoutV.addLayout(layout)
        self.setLayout(layoutV)
        self.show()

    @pyqtSlot()
    def enter_onClick(self):
        search_text=self.text.text()
        filter_type = self.filter.currentText()
        list2 = self.mybackend.get_movie_info(search_text, filter_type)

        self.cams = Movies_list(list2,self.user_id)
        self.cams.show()
        self.close()


class Movies_list(QWidget):
    def __init__(self, movie_list, user_id):
        super().__init__()
        self.movie_list = movie_list
        self.title = "Movie_App1"
        self.top = 300
        self.left = 300
        self.width = 750
        self.height = 700
        self.user_id = user_id
        self.setWindowTitle('Movies_list')
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.mybackend=backend()
        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setText('Booking!')
        self.pushButton.clicked.connect(self.booking_onclick)

        self.pushButton1 = QPushButton(self)
        self.pushButton1.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton1.setText('Back!')
        self.pushButton1.clicked.connect(self.back_onclick)

        layoutH = QHBoxLayout()
        layoutH.addWidget(self.pushButton)
        layoutH.addWidget(self.pushButton1)

        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.vbox = QVBoxLayout()
        self.widget = QWidget()
        self.scroll.setWidget(self.widget)
        self.widget.setLayout(self.vbox)

        layoutV.addWidget(self.scroll)

        self.allList = []

        self.movie_booking_map = []

        for movie in self.movie_list:
            available_booking_map = {}
            listWidget = QListWidget(self)
            listWidget.setObjectName("listWidget")
            listWidget.setSelectionMode(QAbstractItemView.SingleSelection)

            movie_info = QLabel(self)
            movie_info.setText(self.temp(movie))
            movie_info.setStyleSheet('font-size: 11pt; font-weight: bold')
            self.vbox.addWidget(movie_info)
            available = QLabel(self)
            available.setText("Available Booking")
            self.vbox.addWidget(available)
            self.vbox.addWidget(listWidget)
            self.allList.append(listWidget)
            for booking in movie['bookings']:
                QListWidgetItem(self.processBookinginfo(booking), listWidget)
                available_booking_map[self.processBookinginfo(booking)] = [booking['book_id'], movie['Name']]

            self.movie_booking_map.append(available_booking_map)

        if len(self.movie_list) == 0:
            Notfound = QLabel(self)
            Notfound.setText("No Movie found :(")
            Notfound.setStyleSheet("font-size: 30pt; font-weight: bold ;color : red;")
            Notfound.setAlignment(Qt.AlignCenter)
            self.vbox.addWidget(Notfound)

    def processBookinginfo(self, booking):
        booking_info = ""
        booking_info += "Date: " + booking['date'].strftime("%m/%d/%Y") + "              Cost: " + str(booking['cost'])
        booking_info += "                     Available seats: " + str(booking['available']) +  "/" +str(booking['total_seats'])
        booking_info += "\nHall Name: " + booking['hall_name'] + ", " + booking['location']

        return booking_info

    def temp(self,movie_info):
        movie_details = ""
        for key, val in movie_info.items():
            if key != "bookings":
                if key == "of":
                    movie_details += key + " " + str(val) + "   "
                else:
                    movie_details += key + ": " + str(val) + "   "

        return movie_details

    def booking_onclick(self):
        selected_booking = {}
        for i in range(len(self.allList)):
            x = self.allList[i].selectedItems()
            for selected in x:
                # bookid and movie name
                selected_booking[self.movie_booking_map[i][selected.text()][0]] = self.movie_booking_map[i][selected.text()][1]

        self.cams = Last_window(selected_booking,self.movie_list,self.user_id)
        self.cams.show()
        self.close()

    def back_onclick(self):
        self.cams = Window(self.user_id)
        self.cams.show()
        self.close()


class Last_window(QWidget):
    def __init__(self, selected_booking,movie_list , user_id):
        super().__init__()
        self.movie_list = movie_list
        self.title = "Movie_App2"
        self.top = 300
        self.left = 300
        self.width = 750
        self.height = 700
        self.user_id = user_id
        self.selected_booking = selected_booking
        self.setWindowTitle('Last_window')
        self.setGeometry(self.top, self.left, self.width, self.height)
        oImage = QImage("confirm.jpg")
        sImage = oImage.scaled(QSize(self.width,self.height))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setText('Confirm!')
        self.pushButton.clicked.connect(self.confirm_onclick)
        self.mybackend=backend()
        self.pushButton1 = QPushButton(self)
        self.pushButton1.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton1.setText('Back!')
        self.pushButton1.clicked.connect(self.back_onclick)

        layoutH = QHBoxLayout()
        layoutH.addWidget(self.pushButton)
        layoutH.addWidget(self.pushButton1)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)
        booking_num = QLabel(self)
        booking_num.setText("You have selected total "+ str(len(self.selected_booking.keys())) + " bookings" )
        booking_num.setAlignment(Qt.AlignCenter)
        booking_num.setStyleSheet("font-size: 15pt; font-weight: bold ;color : white;")
        self.createFormGroupBox()
        layoutV.addWidget(booking_num)
        layoutV.addWidget(self.formGroupBox)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox()

        layout = QFormLayout()
        layout.setVerticalSpacing(20)
        movies_unreviewed = self.mybackend.getMovieToreview(self.user_id)         # <customer_id>
        self.to_get_info = {}

        for bookid, movie_name in self.selected_booking.items():
            rating_menu = QComboBox()
            available_seats = self.mybackend.getAvailableSeats(bookid)
            for i in range(available_seats):
                rating_menu.addItem(str(i+1))

            self.to_get_info[bookid] = rating_menu
            nameLabel = QLabel(movie_name)
            nameLabel.setStyleSheet('font-size: 11pt; color: white')
            layout.addRow(nameLabel, rating_menu)

        self.formGroupBox.setLayout(layout)


    def confirm_onclick(self):
        buttonReply = QMessageBox.question(self, 'Movie_App', "Do you want to confirm ?", QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        if buttonReply == QMessageBox.Yes:

            toBook = {}
            for book_id, ratem in self.to_get_info.items():
                toBook[book_id] = int(ratem.currentText())

            self.mybackend.bookTickets(toBook,self.user_id)    # <customer_id>
            self.cams = confirmScene()
            self.cams.show()
            self.close()
            print('Yes clicked.')
        else:
            print('No clicked.')
            self.show()
            sys.exit(app.exec_())

    def back_onclick(self):
        self.cams = Movies_list(self.movie_list,self.user_id)
        self.cams.show()
        self.close()

class confirmScene(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Movie_App2"
        self.top = 300
        self.left = 300
        self.width = 750
        self.height = 700
        oImage = QImage("final.jpg")
        sImage = oImage.scaled(QSize(self.width,self.height))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.setWindowTitle('Confirmed')
        self.setGeometry(self.top, self.left, self.width, self.height)
        layoutV = QVBoxLayout()
        confirmed = QLabel(self)
        confirmed.setText("Confirmed!!")
        confirmed.setStyleSheet("font-size: 30pt; font-weight: bold ;color : white; font-family: Courier;")
        confirmed.move(250, 300)
        layoutV.addWidget(confirmed)

class ReviewScreen(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.title = "Movie_App"
        self.top = 300
        self.left = 300
        self.width = 750
        self.height = 700
        self.user_id = user_id
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        layoutV = QVBoxLayout()

        oImage = QImage("review.jpg")
        sImage = oImage.scaled(QSize(self.width,self.height))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.mybackend=backend()

        self.show()
        self.createFormGroupBox()
        self.submit = QPushButton(self)
        self.submit.setText('Submit Review')
        self.submit.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.submit.clicked.connect(self.submit_onClick)


        self.skip = QPushButton(self)
        self.skip.setText('Skip!')
        self.skip.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.skip.clicked.connect(self.skip_onClick)

        upperlayout= QVBoxLayout()
        upperlayout.addWidget(self.formGroupBox)

        topHead = QLabel("Help us serve you better by filling this review")
        topHead.setStyleSheet('font-size: 20pt; color: white')
        topHead.setAlignment(Qt.AlignCenter)

        upperlayout.addWidget(topHead)

        layout= QHBoxLayout()
        layout.addWidget(self.submit)
        layout.addWidget(self.skip)

        upperlayout.addLayout(layout)
        layoutV.addLayout(upperlayout)
        self.setLayout(layoutV)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox()

        layout = QFormLayout()
        layout.setVerticalSpacing(20)
        movies_unreviewed = self.mybackend.getMovieToreview(self.user_id)         # <customer_id>
        self.to_get_info = {}

        for movie_id, name in movies_unreviewed.items():
            rating_menu = QComboBox()
            rating_menu.addItem("")
            rating_menu.addItem("1")
            rating_menu.addItem("2")
            rating_menu.addItem("3")
            rating_menu.addItem("4")
            rating_menu.addItem("5")
            self.to_get_info[movie_id] = rating_menu
            nameLabel = QLabel(name)
            nameLabel.setStyleSheet('font-size: 11pt; color: white')
            layout.addRow(nameLabel, rating_menu)

        if len(movies_unreviewed.keys()) == 0:
            print("LOLOLOl")
            self.skip_onClick()
            self.hide()
            print("llllll")

        self.formGroupBox.setLayout(layout)


    @pyqtSlot()
    def submit_onClick(self):

        ratings_by_user = {}

        for movie_id, ratem in self.to_get_info.items():
            if ratem.currentText() != '':
                ratings_by_user[movie_id] = ratem.currentText()

        self.mybackend.updateReview(self.user_id, ratings_by_user)             # <customer_id>

        self.cams = Window(self.user_id)
        self.cams.show()
        self.close()

    @pyqtSlot()
    def skip_onClick(self):
        self.cams = Window(self.user_id)
        self.cams.show()
        self.close()



def runn(self, user_id):
    print("oorro")
    mybackend = backend()
    movies_unreviewed = mybackend.getMovieToreview(self.USER_ID)
    if len(movies_unreviewed.keys()) == 0:
        self.cams = Window(self.USER_ID)
        self.cams.show()

    else:
        self.cams = ReviewScreen(self.USER_ID)
        self.cams.show()

    #ex=ReviewScreen(user_id)
    #ex.show()

    #sys.exit(app.exec_())
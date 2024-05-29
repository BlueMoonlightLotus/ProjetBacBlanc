import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer , QDate
import datetime
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate, pyqtSignal
import datetime
from PyQt5.QtGui import QIcon
# Dictionnaire global pour stocker les matrices des semaines

BDD_etudiants = ["Cedric Michel"]
BDD_etudiants_week_matrices = {"Cedric Michel": {}} # 

class PeriodSelectionWidget(QWidget):
    periodSelected = pyqtSignal(QDate, QDate, int)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()

        # Widgets de sélection de date de début et de date de fin
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())  # Définir la date de début par défaut à la date actuelle
        self.start_date_edit.dateChanged.connect(self.calculatePeriod)
        layout.addWidget(QLabel("Date de début :"))
        layout.addWidget(self.start_date_edit)

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())  # Définir la date de fin par défaut à la date actuelle
        self.end_date_edit.dateChanged.connect(self.calculatePeriod)
        layout.addWidget(QLabel("Date de fin :"))
        layout.addWidget(self.end_date_edit)

        # Labels pour afficher les résultats
        self.days_label = QLabel()
        layout.addWidget(self.days_label)
        self.weeks_label = QLabel()
        layout.addWidget(self.weeks_label)

        self.setLayout(layout)
        self.calculatePeriod()  # Calculer la période initiale lors de l'initialisation

    def calculatePeriod(self):
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()

        # Vérifier si la date de début est un samedi ou un dimanche
        if start_date.dayOfWeek() == Qt.Saturday or start_date.dayOfWeek() == Qt.Sunday:
            # Changer la date de début au lundi suivant
            start_date = start_date.addDays((Qt.Monday - start_date.dayOfWeek() + 7) % 7)
            self.start_date_edit.setDate(start_date)

        # Vérifier si la date de fin est un samedi ou un dimanche
        if end_date.dayOfWeek() == Qt.Saturday or end_date.dayOfWeek() == Qt.Sunday:
            # Changer la date de fin au vendredi précédent
            end_date = end_date.addDays((Qt.Friday - end_date.dayOfWeek() + 7) % 7)
            self.end_date_edit.setDate(end_date)

        # Calculer le nombre total de jours dans l'intervalle
        delta_days = (end_date.toJulianDay() - start_date.toJulianDay()) + 1
        if delta_days < 0:
            self.days_label.setText(f"Nombre de jours dans l'intervalle : /")
            self.weeks_label.setText(f"Nombre de semaines dans l'intervalle : /")
            return

        # Convertir les objets QDate en objets datetime.date
        start_pydate = datetime.date(start_date.year(), start_date.month(), start_date.day())
        end_pydate = datetime.date(end_date.year(), end_date.month(), end_date.day())

        # Calculer le numéro de semaine ISO pour la date de début et la date de fin
        start_year, start_week, _ = start_pydate.isocalendar()
        end_year, end_week, _ = end_pydate.isocalendar()

        # Calculer le nombre de semaines couvertes par l'intervalle
        if start_year == end_year:
            weeks = end_week - start_week + 1
        else:
            weeks_in_start_year = 52 if QDate.isLeapYear(start_year) else 53
            weeks_in_end_year = 52 if QDate.isLeapYear(end_year) else 53
            weeks = weeks_in_start_year - start_week + end_week + 1
            if QDate.isLeapYear(start_year):
                weeks += 1

        # Affichage des résultats
        self.days_label.setText(f"Nombre de jours dans l'intervalle : {delta_days}")
        self.weeks_label.setText(f"Nombre de semaines dans l'intervalle : {weeks}")

        # Émettre le signal indiquant la période sélectionnée, ainsi que le nombre de semaines
        self.periodSelected.emit(start_date, end_date, weeks)

    
class MainWindow(QWidget):
        num_rows = 22
        num_columns = 7
        num_weeks = 1
        def __init__(self):
            super().__init__()
            self.initUI()
            self.current_student = BDD_etudiants[0]
            self.week_matrices = BDD_etudiants_week_matrices[self.current_student]
            self.comboBox.currentIndexChanged.connect(self.update_current_student)
            
             
            
        def update_current_student(self):
            # Mettre à jour self.current_student avec le nom de l'élève sélectionné dans le menu déroulant
            self.current_student = self.comboBox.currentText()
            
            self.week_matrices = BDD_etudiants_week_matrices[self.current_student]
            
            
            
            # Mettre à jour la période et rafraîchir l'affichage
            self.update_period(self.period_widget.start_date_edit.date(), self.period_widget.end_date_edit.date(), self.num_weeks)  
           
            
        def initUI(self):
            self.setWindowTitle('Organisateur Bac Blanc (pour M. Michel)')
            

            # Création d'un layout vertical pour organiser les widgets
            layout = QVBoxLayout()
            layout.setContentsMargins(10, 10, 10, 10)  # Ajout de marges
            self.setLayout(layout)

            # Création de la barre horizontale en haut de l'écran
            top_bar = QWidget()
            top_bar.setStyleSheet("background-color: lightblue;")  # Définir la couleur de la barre
            layout.addWidget(top_bar)

            # Calcul de la hauteur de la barre (10% de la hauteur de la fenêtre)
            screen_size = QDesktopWidget().availableGeometry().size()
            bar_height = int(screen_size.height() * 0.1)
            top_bar.setFixedHeight(bar_height)

            # Création d'un layout horizontal pour la barre
            top_bar_layout = QHBoxLayout()
            top_bar_layout.setContentsMargins(10, 10, 10, 10)  # Ajout de marges
            top_bar_layout.setSpacing(10)  # Ajout d'espacement entre les widgets
            top_bar.setLayout(top_bar_layout)

            # Ajout du menu défilant avec tous les élèves
            self.comboBox = QComboBox()
            self.comboBox.addItems(BDD_etudiants)
            self.comboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Politique de taille
            self.comboBox.setFixedHeight(int(bar_height * 0.5))  # Définir la hauteur du menu défilant
            self.comboBox.setMaxVisibleItems(10)
            top_bar_layout.addWidget(self.comboBox)
            
            

            # Création d'un layout vertical pour organiser le bouton et la zone de texte
            button_text_layout = QVBoxLayout()
            top_bar_layout.addLayout(button_text_layout)

            # Ajout d'une zone de texte pour entrer le nom de l'élève
            self.lineEdit = QLineEdit()
            self.lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Politique de taille
            self.lineEdit.textChanged.connect(self.check_text)  # Connexion de l'événement textChanged
            button_text_layout.addWidget(self.lineEdit)

            # Création d'un layout horizontal pour organiser les boutons Ajouter/Supprimer
            add_remove_layout = QHBoxLayout()
            button_text_layout.addLayout(add_remove_layout)

            # Ajout d'un bouton "Ajouter Élève" pour ajouter l'élève à la BDD
            self.addButton = QPushButton("Ajouter Élève")
            self.addButton.setStyleSheet("background-color: green; color: white;")  # Définir la couleur du bouton
            self.addButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Politique de taille
            self.addButton.clicked.connect(self.addStudent)
            self.addButton.setEnabled(False)  # Désactiver le bouton au démarrage
            add_remove_layout.addWidget(self.addButton)

            # Ajout d'un bouton "Supprimer Élève" pour supprimer l'élève de la BDD
            self.removeButton = QPushButton("Supprimer Élève")
            self.removeButton.setStyleSheet("background-color: red; color: white;")  # Définir la couleur du bouton
            self.removeButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Politique de taille
            self.removeButton.clicked.connect(self.removeStudent)
            add_remove_layout.addWidget(self.removeButton)

            self.successIconLabel = QLabel()
            self.successIconLabel.setFixedSize(50, 50)  # Définir la taille de l'icône
            top_bar_layout.addWidget(self.successIconLabel)   
            
        
            self.lineEdit.textChanged.connect(self.check_text)  # Connexion de l'événement textChanged
            self.lineEdit.returnPressed.connect(self.addStudent)  # Connexion de l'événement returnPressed
            button_text_layout.addWidget(self.lineEdit)
            

            # Ajout d'un label pour afficher le nom de l'élève
            self.label = QLabel("Liste des élèves :")
            layout.addWidget(self.label)

            # emploi du temps 

            central_widget = QWidget()

            main_layout = QHBoxLayout()
            central_widget.setLayout(main_layout)

            # Layout pour l'emploi du temps
            schedule_layout = QVBoxLayout()
            main_layout.addLayout(schedule_layout)

            # QLabel pour afficher la semaine considérée
            self.week_label = QLabel("Semaine 1")
            self.week_date_label = QLabel("")
            schedule_layout.addWidget(self.week_label)
            schedule_layout.addWidget(self.week_date_label)

            # Boutons de navigation
            nav_layout = QHBoxLayout()
            schedule_layout.addLayout(nav_layout)

            self.prev_week_button = QPushButton("Semaine Précédente")
            self.prev_week_button.clicked.connect(self.prev_week)
            nav_layout.addWidget(self.prev_week_button)

            self.next_week_button = QPushButton("Semaine Suivante")
            self.next_week_button.clicked.connect(self.next_week)
            nav_layout.addWidget(self.next_week_button)

            self.table_widget = QTableWidget()
            schedule_layout.addWidget(self.table_widget)

            # Layout pour les boutons de couleur
            color_layout = QVBoxLayout()
            main_layout.addLayout(color_layout)

            self.green_button = QPushButton("Disponible")
            self.green_button.clicked.connect(lambda: self.set_color(2))  # Assigner la couleur verte
            color_layout.addWidget(self.green_button)

            self.orange_button = QPushButton("Pas préférable")
            self.orange_button.clicked.connect(lambda: self.set_color(1))  # Assigner la couleur orange
            color_layout.addWidget(self.orange_button)

            self.red_button = QPushButton("Indisponible")
            self.red_button.clicked.connect(lambda: self.set_color(0))  # Assigner la couleur rouge
            color_layout.addWidget(self.red_button)

            # style 
            # Ajout des icônes
            self.green_button.setIcon(QIcon("green_icon.png"))
            self.orange_button.setIcon(QIcon("orange_icon.png"))
            self.red_button.setIcon(QIcon("red_icon.png"))

            # Contraste de couleur
            self.green_button.setStyleSheet("background-color: #4CAF50; color: white;")
            self.orange_button.setStyleSheet("background-color: #FF9800; color: white;")
            self.red_button.setStyleSheet("background-color: #F44336; color: white;")

            # Effets de survol et de clic
            self.green_button.setStyleSheet("QPushButton:hover { background-color: #45a049; } QPushButton:pressed { background-color: #398438; }")
            self.orange_button.setStyleSheet("QPushButton:hover { background-color: #e68a00; } QPushButton:pressed { background-color: #c66900; }")
            self.red_button.setStyleSheet("QPushButton:hover { background-color: #d32f2f; } QPushButton:pressed { background-color: #b71c1c; }")

            # Coins arrondis
            self.green_button.setStyleSheet("border-radius: 10px;")
            self.orange_button.setStyleSheet("border-radius: 10px;")
            self.red_button.setStyleSheet("border-radius: 10px;")

            # Taille et espacement
            self.green_button.setMinimumHeight(60)
            self.orange_button.setMinimumHeight(60)
            self.red_button.setMinimumHeight(60)
            self.green_button.setMinimumWidth(120)
            self.orange_button.setMinimumWidth(120)
            self.red_button.setMinimumWidth(120)


            # Initialiser l'état des boutons de couleur
            self.active_color_button = None

            # Connecter le signal cellEntered à une fonction pour gérer le coloriage des cellules avec le clic gauche enfoncé
            self.table_widget.cellEntered.connect(self.update_cell_on_hover)

            # Ajouter le widget de sélection de période
            self.period_widget = PeriodSelectionWidget()
            self.period_widget.periodSelected.connect(self.update_period)  # Connexion du signal
            main_layout.addWidget(self.period_widget)

         # Initialiser la table pour empêcher la sélection multiple
            self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)



            layout.addWidget(central_widget)

            # Ajout d'une étiquette pour afficher les informations sur la période sélectionnée
            self.period_info_label = QLabel()
            layout.addWidget(self.period_info_label)

            # Configuration du layout pour qu'il s'étende automatiquement avec la fenêtre
            layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

            # Définition de la taille initiale de la fenêtre
            self.init_w = int(screen_size.width() * 0.5)
            self.init_h = int(screen_size.height() * 0.5)
            self.resize(self.init_w, self.init_h)

            # Appeler manuellement check_text() pour mettre à jour l'état initial du bouton
            self.check_text()

        def get_week_dates(self):
            
            
          
            # Récupérer la date de début de la période sélectionnée
            start_date = self.period_widget.start_date_edit.date()

            # Trouver le premier jour de la semaine (lundi) pour la semaine actuellement affichée
            current_week_start = start_date.addDays(-start_date.dayOfWeek() + 1 + (self.current_week_index * 7))

            # Trouver le dernier jour de la semaine (dimanche)
            current_week_end = current_week_start.addDays(6)

            return current_week_start, current_week_end

        def update_period(self, start_date, end_date, num_weeks):
            # Mettre à jour les données et l'affichage de l'emploi du temps en fonction de la période sélectionnée
            self.current_week_index = 0
            self.num_weeks = num_weeks  # Mettre à jour le nombre de semaines
            if self.week_matrices == {}:
                self.create_week_matrices()
            
            self.populate_table()
            self.update_week_label()

            # Redimensionner les colonnes pour s'adapter au contenu
            header = self.table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            self.harmonisation()

        def create_week_matrices(self):
            
            
            for i in range(self.num_weeks):
                
                self.week_matrices[i] = self.generate_initial_schedule(i)
        def date_outside_range(self,date, start_date, end_date):
            return date < start_date or date > end_date
        def generate_initial_schedule(self,i):
            # Générer une matrice initiale de 20x7
            schedule = []
            for _ in range(self.num_rows):
                row = [0] * self.num_columns
                schedule.append(row)
            week_num = i
            # Mettre à -1 les valeurs pour le samedi, le dimanche et le mercredi après 12h
            # Récupérer la plage de dates sélectionnée
            start_date = self.period_widget.start_date_edit.date()
            end_date = self.period_widget.end_date_edit.date()
            start_date_day = (start_date.dayOfWeek() - 1) % 7
            end_date_day = (end_date.dayOfWeek() - 1) % 7
            
            for i, day_row in enumerate(schedule):
                for j, _ in enumerate(day_row):
                    if j == 5 or j == 6 or (j == 2 and i > 8):
                        schedule[i][j] = -1
                    # Obtenir la date correspondante à cette cellule dans la semaine actuelle
                    if week_num == 0:
                        if j < start_date_day:
                            schedule[i][j] = -1
                    if week_num == self.num_weeks-1:
                        if j > end_date_day:
                            schedule[i][j] = -1    
                    
                    
            return schedule
        
        def populate_table(self):
            # Récupérer la matrice de données de la semaine actuelle à partir du dictionnaire global
            
            schedule_data = self.week_matrices[self.current_week_index]
            
            num_rows = len(schedule_data)
            num_columns = len(schedule_data[0]) + 1  # Ajouter une colonne pour les heures
            self.table_widget.setRowCount(num_rows)
            self.table_widget.setColumnCount(num_columns)

            # Ajout des noms des jours
            days_of_week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            for column_index, day in enumerate(days_of_week):
                item = QTableWidgetItem(day)
                self.table_widget.setItem(0, column_index + 1, item)

            # Ajout des heures
            start_time = 8
            for row_index in range(1, num_rows + 1):
                hour = start_time + (row_index - 1) // 2
                minutes = "00" if (row_index - 1) % 2 == 0 else "30"
                if hour < 18:
                    time_str = f"{hour}:{minutes}"
                    item = QTableWidgetItem(time_str)
                    self.table_widget.setItem(row_index, 0, item)

            # Ajout des données de la matrice avec les valeurs initiales
            
            for row_index, row_data in enumerate(schedule_data):
                for column_index, cell_data in enumerate(row_data):
                    # Ne pas afficher les valeurs de la matrice de couleurs
                    if cell_data != -1 and cell_data != 0 and cell_data != 1 and cell_data != 2:
                        continue  # Ne pas insérer de valeur dans la cellule
                    if self.current_student != "Cedric Michel" and BDD_etudiants_week_matrices["Cedric Michel"].get(self.current_week_index, [[]])[row_index][column_index] == -1 or 0:
                        cell_data = -1  # La cellule doit être -1 pour les autres élèves si la matrice de Cedric Michel contient -1 à cet endroit
                    item = QTableWidgetItem("")  # Cellule vide
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Désactiver l'édition

                    # Colorier la cellule en fonction de la valeur de la matrice
                    if cell_data == -1:
                        item.setBackground(Qt.gray)
                    elif cell_data == 0:
                        item.setBackground(Qt.red)
                    elif cell_data == 1:
                        item.setBackground(Qt.yellow)
                    elif cell_data == 2:
                        item.setBackground(Qt.green)
                    self.table_widget.setItem(row_index + 1, column_index + 1, item)
            
            # Redimensionner les colonnes pour s'adapter au contenu
            header = self.table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            
        def prev_week(self):
            # Charger la semaine précédente si elle existe
            if self.current_week_index > 0:
                self.current_week_index -= 1
                self.update_week_label()
                self.populate_table()
                
        def next_week(self):
            # Charger la semaine suivante si elle existe
            if self.current_week_index < self.num_weeks - 1:
                self.current_week_index += 1
                self.update_week_label()
                self.populate_table()

        def update_week_label(self):
            # Mettre à jour le QLabel pour afficher la semaine considérée
            self.week_label.setText(f"Semaine {self.current_week_index + 1}/{self.num_weeks}")
            start_date, end_date = self.get_week_dates()
            self.week_date_label.setText(f" - Début : {start_date.toString('dd/MM/yyyy')}, Fin : {end_date.toString('dd/MM/yyyy')}")
            
        def set_color(self, color):
            # Réinitialiser l'état des boutons de couleur
            if self.active_color_button:
                self.active_color_button.setStyleSheet("")  # Effacer le style actif

            # Mettre à jour l'état du bouton actif
            self.active_color_button = self.sender()
            self.active_color_button.setStyleSheet("background-color: gray;")  # Mettre en surbrillance le bouton actif

        def update_cell_on_hover(self, row, column):
            # Vérifier si le bouton gauche de la souris est enfoncé
            if QApplication.mouseButtons() == Qt.LeftButton:
                # Récupérer la matrice de données de la semaine actuelle à partir du dictionnaire global
                
                schedule_data = self.week_matrices[self.current_week_index]

                # Vérifier si la cellule peut être modifiée
                if (row == 0 or column == 0) or schedule_data[row-1][column-1] == -1:
                    return  # Ne rien faire si la cellule ne peut pas être modifiée

                # Récupérer la couleur active
                if self.active_color_button:
                    color = self.get_color_index(self.active_color_button)

                    # Mettre à jour la valeur de la matrice dans le dictionnaire global
                    schedule_data[row-1][column-1] = color

                    # Mettre à jour l'affichage de la table
                    item = self.table_widget.item(row, column)
                    if item:
                        item.setBackground(self.get_color(color))
            self.harmonisation()
            
        def get_color(self, color):
            # Fonction pour obtenir la couleur en fonction de la valeur
            if color == 0:
                return Qt.red
            elif color == 1:
                return Qt.yellow  # Orange foncé
            elif color == 2:
                return Qt.green

        def get_color_index(self, button):
            # Retourner l'index de couleur correspondant au bouton
            if button == self.green_button:
                return 2
            elif button == self.orange_button:
                return 1
            elif button == self.red_button:
                return 0
            
        
        
        
        
        def check_text(self):
            # Vérifier si le champ de texte est vide
            if self.lineEdit.text().strip() == "":
                # Désactiver le bouton si le champ de texte est vide
                self.addButton.setEnabled(False)
                self.addButton.setStyleSheet("background-color: #444444; color: white;")  # Couleur plus foncée
                
            else:
                # Activer le bouton si le champ de texte n'est pas vide
                self.addButton.setEnabled(True)
                self.addButton.setStyleSheet("background-color: green; color: white;")
                
                     
        def addStudent(self):
            # Récupérer le nom de l'élève depuis la zone de texte
            new_student = self.lineEdit.text()
            if new_student.strip() == "":
                return  # Ne rien faire si le champ est vide
            
            # Ajouter le nouvel élève à la liste et mettre à jour le menu défilant
            BDD_etudiants.append(new_student)
            self.comboBox.addItem(new_student)
            BDD_etudiants_week_matrices[new_student] = {}
            self.current_student = new_student
            # Sélectionner automatiquement le nouvel élève ajouté dans le menu déroulant
            index = self.comboBox.findText(new_student)
            self.comboBox.setCurrentIndex(index)

            # Effacer le contenu de la zone de texte après l'ajout
            self.lineEdit.clear()

            # Désactiver le bouton après l'ajout
            self.addButton.setEnabled(False)
            self.addButton.setStyleSheet("background-color: #444444; color: white;")  # Couleur plus foncée
            self.showSuccessIcon()
            week_matrices = BDD_etudiants_week_matrices[self.current_student]
            self.create_week_matrices()
            self.update_current_student()
            
        def removeStudent(self):
            # Récupérer l'index de l'élément sélectionné dans le menu défilant
            index = self.comboBox.currentIndex()
            
            # Récupérer le nom de l'élève sélectionné
            selected_student = self.comboBox.currentText()
            
            # Vérifier si l'élève sélectionné est différent de "Cedric Michel"
            if selected_student != "Cedric Michel":
                # Supprimer l'élève de la liste et mettre à jour le menu défilant
                if index != -1:
                    BDD_etudiants.remove(f"{selected_student}")
                    self.comboBox.removeItem(index)
                    del BDD_etudiants_week_matrices[selected_student]
                    self.current_student = BDD_etudiants[-1]
                    week_matrices = BDD_etudiants_week_matrices[self.current_student]
                    self.create_week_matrices()
            self.showSuccessIcon()
            
        def showSuccessIcon(self):
            # Charger l'icône de succès
            success_icon = QIcon("lapin.png")  # Remplacez "success_icon.png" par le chemin de votre icône

            # Afficher l'icône de succès dans l'étiquette
            self.successIconLabel.setPixmap(success_icon.pixmap(50, 50))  # Ajuster la taille de l'icône selon vos besoins

            # Planifier la suppression de l'icône après un certain délai 
            QTimer.singleShot(2000, self.clearSuccessIcon)

        def clearSuccessIcon(self):
            # Effacer l'icône de succès
            self.successIconLabel.clear()

        def openPeriodSelection(self):
            self.period_selection_window = PeriodSelectionWidget(self.updatePeriodInfo)
            self.period_selection_window.show()

        def updatePeriodInfo(self, start_date, end_date):
            delta_days = (end_date - start_date).days + 1
            self.period_info_label.setText(f"Période sélectionnée : du {start_date.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')} ({delta_days} jours)")

            # Calcul du nombre de semaines
            start_week = start_date.isocalendar()[1]
            end_week = end_date.isocalendar()[1]
            num_weeks = end_week - start_week + 1

            self.period_info_label.setText(self.period_info_label.text() + f"\nNombre de semaines : {num_weeks}")
            
        def harmonisation(self):
            if self.current_student != BDD_etudiants[0]:
                for h in range(22):
                    for j in range(7):
                        if BDD_etudiants_week_matrices[BDD_etudiants[0]][self.current_week_index][h][j] in (-1, 0):
                            self.week_matrices[self.current_week_index][h][j] = -1
                self.populate_table()
                
if __name__ == '__main__':
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())

import argparse
from exercise_runner import run_exercise
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtGui import QIcon
from sys import argv
app = QApplication(argv)

windows = list()


window = QWidget()
window.setWindowIcon(QIcon('icon.ico'))
window.setWindowTitle("Distributed Exercises AAU")
main = QVBoxLayout()
window.setFixedSize(600, 100)
start_button = QPushButton("start")
main.addWidget(start_button)
input_area_labels = QHBoxLayout()
input_area_areas = QHBoxLayout()
actions = {'Lecture':[print, 0], 'Algorithm': [print, 'PingPong'], 'Type': [print, 'stepping'], 'Devices': [print, 3]}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='For exercises in Distributed Systems.')
    parser.add_argument('--lecture', metavar='N', type=int, nargs=1,
                        help='Lecture number', required=False, choices=[0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    parser.add_argument('--algorithm', metavar='alg', type=str, nargs=1,
                        help='Which algorithm from the exercise to run', required=False)
    parser.add_argument('--type', metavar='nw', type=str, nargs=1,
                        help='whether to use [async] or [sync] network', required=False, choices=['async', 'sync', 'stepping'])
    parser.add_argument('--devices', metavar='N', type=int, nargs=1,
                        help='Number of devices to run', required=False)
    args = parser.parse_args()

#     #run_exercise(args.lecture[0], args.algorithm[0], args.type[0], args.devices[0])
    actions = {'Lecture':[print, args.lecture[0]], 'Algorithm': [print, args.algorithm[0]], 'Type': [print, args.type[0]], 'Devices': [print, args.devices[0]]}


for action in actions.items():
    input_area_labels.addWidget(QLabel(action[0]))
    field = QLineEdit()
    input_area_areas.addWidget(field)
    field.setText(str(action[1][1]))
    actions[action[0]][0] = field.text
main.addLayout(input_area_labels)
main.addLayout(input_area_areas)


def start_exercise():
    windows.append(run_exercise(int(actions['Lecture'][0]()), actions['Algorithm'][0](), actions['Type'][0](), int(actions['Devices'][0]())))

start_button.clicked.connect(start_exercise)
window.setLayout(main)
window.show()
app.exec()

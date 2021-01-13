print("main window controller")
import numpy as np
import cmath
from interface import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore

import pandas as pd
from pandas import ExcelWriter



e = 4.8 * 10 ** (-10)
c = 2.998 * 10 ** (10)
m_e = 9.1 * 10 ** (-28)

# Users constants
N = 10 ** 17 * 10 ** 22  # cm^-3
M = 1 * 9.1 * 10 ** (-28)  # mass of charge carriers in mass of free electrons
eps_inf = 10  # (1 - 100)
W_LO = 300  # freq. for longitudinal phonon, cm^-1
W_TO = 270  # freq. for longitudinal phonon, cm^-1
G_1 = 5  # phonon attenuation, cm^-1
G_0 = 10  # plasmon attenuation
d = 10 ** (-5)  # film thinkness, 0 - 10^-3 cm^-1

class mainWindowController(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self, parent = None):
        super(mainWindowController, self).__init__(parent)
        self.setupUi(self)
        self.calculate_pushButton.clicked.connect(self.calculateButtonClicked)
        self.N_doubleSpinBox.valueChanged.connect(self.calculateButtonClicked)
        self.M_doubleSpinBox_2.valueChanged.connect(self.calculateButtonClicked)
        self.W_TO_doubleSpinBox_3.valueChanged.connect(self.calculateButtonClicked)
        self.W_LO_doubleSpinBox.valueChanged.connect(self.calculateButtonClicked)
        self.G_0_doubleSpinBox.valueChanged.connect(self.calculateButtonClicked)
        self.G_1_doubleSpinBox.valueChanged.connect(self.calculateButtonClicked)
        self.Eps_inf_doubleSpinBox.valueChanged.connect(self.calculateButtonClicked)
        self.d_doubleSpinBox.valueChanged.connect(self.calculateButtonClicked)

        self.save_pushButton.clicked.connect(self.saveButtonClicked)
        self.eps_total_radioButton.toggled.connect(self.onClicked)
        self.im_eps_total_radioButton.toggled.connect(self.onClicked)
        self.N_w_radioButton.toggled.connect(self.onClicked)
        self.K_w_radioButton.toggled.connect(self.onClicked)
        self.R_w_radioButton.toggled.connect(self.onClicked)
        self.phi_w_radioButton.toggled.connect(self.onClicked)
        self.alpha_w_radioButton.toggled.connect(self.onClicked)
        self.T_w_radioButton.toggled.connect(self.onClicked)
        self.A_w_radioButton.toggled.connect(self.onClicked)
        # constants SGS
        self.e = 4.8 * 10 ** (-10)
        self.c = 2.998 * 10 ** (10)
        self.m_e = 9.1 * 10 ** (-28)

        # Users constants
        self.N = 3 * 10 ** 16  # cm^-3
        self.M = 1 * 9.1 * 10 ** (-28)  # mass of charge carriers in mass of free electrons
        self.eps_infinum = 10  # (1 - 100)
        self.W_LO = 300  # freq. for longitudinal phonon, cm^-1
        self.W_TO = 270  # freq. for longitudinal phonon, cm^-1
        self.G_1 = 5  # phonon attenuation, cm^-1
        self.G_0 = 10  # plasmon attenuation
        self.d = 10 ** (-5)  # film thinkness, 0 - 10^-3 cm^-1

        self.N_doubleSpinBox.setValue(300)

        self._w = [i for i in range(100, 400)]
        w = [i for i in range(100, 400)]
        self.Omega_P = self._plasmon_freq()
        self.Re_eps_total_list = [np.real(self.eps_total(_w=i)) for i in w]
        self.Im_eps_total_list = [np.imag(self.eps_total(_w=i)) for i in w]
        self.n_w_list = [np.real(self.N_w(i)) for i in w]
        self.k_w_list = [np.imag(self.N_w(i)) for i in w]
        self.R_w_list = [self.R_w(i) for i in w]
        self.phi_w_list = [self.phi_w(i) for i in w]
        self.alpha_w_list = [self.alpha_W(i) for i in w]
        self.T_w_list = [self.T_w(i) for i in w]
        self.A_w_list = [self.A_w(i) for i in w]
        self.showPlasmFreq_label.setText(str(self.Omega_P))

        '''
        self.rbtngroup = QButtonGroup()
        self.rbtngroup.addButton(self.eps_total_radioButton)
        self.rbtngroup.addButton(self.im_eps_total_radioButton)
        self.rbtngroup.addButton(self.N_w_radioButton)
        self.rbtngroup.addButton(self.K_w_radioButton)
        self.rbtngroup.addButton(self.R_w_radioButton)
        self.rbtngroup.addButton(self.phi_w_radioButton)
        self.rbtngroup.addButton(self.alpha_w_radioButton)
        self.rbtngroup.addButton(self.T_w_radioButton)
        self.rbtngroup.addButton(self.A_w_radioButton)
        '''

    def _plasmon_freq(self):
        return ((4 * np.pi * self.N) / (self.M * self.eps_infinum)) ** (1 / 2) * self.e / self.c

    def eps_total(self, _w):
        return self.eps_infinum * (1 + (self.W_LO ** 2 - self.W_TO ** 2) / (self.W_TO ** 2 - _w ** 2 - 1j * _w * self.G_1)
                                   - self.Omega_P ** 2 / (_w ** 2 + 1j * _w * self.G_0))

    def N_w(self, w):
        return (self.eps_total(_w=w)) ** (1 / 2)

    def alpha_W(self, w):
        return 4 * np.pi * np.imag(self.eps_total(_w=w)) * w

    def r_w(self, w):
        return (1 - self.N_w(w)) / (1 + self.N_w(w))

    def phi_w(self, w):
        return cmath.phase(self.r_w(w))

    def R_w(self, w):
        return abs(self.r_w(w)) ** 2#self.r_w(w) * complex(self.r_w(w)).conjugate()

    def T_w(self, w):
        return ((1 - self.R_w(w)) ** 2 * np.exp(-self.alpha_W(w) * d)) / (1 - self.R_w(w) ** 2 * np.exp(-2 * self.alpha_W(w) * d))

    def A_w(self, w):
        return -np.log(self.T_w(w))

    def onClicked(self):
        self.widget.clear()
        self.drawPlot()


    def drawPlot(self):
        self.widget.clear()
        if (self.eps_total_radioButton.isChecked()):
            self.widget.plot(self._w, self.Re_eps_total_list, pen ='r')

        if (self.im_eps_total_radioButton.isChecked()):
            self.widget.plot(self._w, self.Im_eps_total_list, pen ='r')

        if (self.N_w_radioButton.isChecked()):
            self.widget.plot(self._w, self.n_w_list, pen ='r')

        if (self.K_w_radioButton.isChecked()):
            self.widget.plot(self._w, self.k_w_list, pen ='r')

        if (self.R_w_radioButton.isChecked()):
            self.widget.plot(self._w, self.R_w_list, pen ='r')

        if (self.phi_w_radioButton.isChecked()):
            self.widget.plot(self._w, self.phi_w_list, pen ='r')

        if (self.alpha_w_radioButton.isChecked()):
            self.widget.plot(self._w, self.alpha_w_list, pen ='r')

        if (self.T_w_radioButton.isChecked()):
            self.widget.plot(self._w, self.T_w_list, pen ='r')

        if (self.A_w_radioButton.isChecked()):
            self.widget.plot(self._w, self.A_w_list, pen ='r')

    @QtCore.pyqtSlot()
    def calculateButtonClicked(self):
        self.N = self.N_doubleSpinBox.value() * 10 ** 16#self.N_doubleSpinBox.value()  # cm^-3
        self.M = self.M_doubleSpinBox_2.value() * 9.1 * 10 ** (-28) # mass of charge carriers in mass of free electrons
        self.eps_inf = self.Eps_inf_doubleSpinBox.value()  # (1 - 100)
        self.W_LO = self.W_LO_doubleSpinBox.value()  # freq. for longitudinal phonon, cm^-1
        self.W_TO = self.W_TO_doubleSpinBox_3.value()  # freq. for longitudinal phonon, cm^-1
        self.G_1 = self.G_1_doubleSpinBox.value()  # phonon attenuation, cm^-1
        self.G_0 = self.G_0_doubleSpinBox.value()  # plasmon attenuation
        self.d = self.d_doubleSpinBox.value() * 10 ** (-7) # film thinkness, 0 - 10^-3 cm^-1

        self.Omega_P = self._plasmon_freq()
        self.Re_eps_total_list = [np.real(self.eps_total(_w=i)) for i in self._w]
        self.Im_eps_total_list = [np.imag(self.eps_total(_w=i)) for i in self._w]
        self.n_w_list = [np.real(self.N_w(i)) for i in self._w]
        self.k_w_list = [np.imag(self.N_w(i)) for i in self._w]
        self.R_w_list = [self.R_w(i) for i in self._w]
        self.phi_w_list = [self.phi_w(i) for i in self._w]
        self.alpha_w_list = [self.alpha_W(i) for i in self._w]
        self.T_w_list = [self.T_w(i) for i in self._w]
        self.A_w_list = [self.A_w(i) for i in self._w]
        self.showPlasmFreq_label.setText(str(self.Omega_P))
        print("calculated")
        self.drawPlot()
        return 0

    @QtCore.pyqtSlot()
    def saveButtonClicked(self):
        df = pd.DataFrame({'a': [1, 3, 5, 7, 4, 5, 6, 4, 7, 8, 9],
                           'b': [3, 5, 6, 2, 4, 6, 7, 8, 7, 8, 9]})
        if (self.eps_total_radioButton.isChecked()):
            df = pd.DataFrame({'w': self._w,
                               're(eps_total)': self.Re_eps_total_list})

        if (self.im_eps_total_radioButton.isChecked()):
            df = pd.DataFrame({'w': self._w,
                               'im(eps_total)': self.Im_eps_total_list})

        if (self.N_w_radioButton.isChecked()):
            df = pd.DataFrame({'w': self._w,
                               'n(w)': self.n_w_list})

        if (self.K_w_radioButton.isChecked()):
            df = pd.DataFrame({'w': self._w,
                               'k(w)': self.k_w_list})

        if (self.R_w_radioButton.isChecked()):
            df = pd.DataFrame({'w': self._w,
                               'R(w)': self.R_w_list})

        if (self.phi_w_radioButton.isChecked()):
            df = pd.DataFrame({'w': self._w,
                               'phi(w)': self.phi_w_list})

        if (self.alpha_w_radioButton.isChecked()):
            df = pd.DataFrame({'w': self._w,
                               'alpha(w)': self.alpha_w_list})

        if (self.T_w_radioButton.isChecked()):
            df = pd.DataFrame({'w': self._w,
                               'T(w)': self.T_w_list})

        if (self.A_w_radioButton.isChecked()):
            df = pd.DataFrame({'w': self._w,
                               'A(w)': self.A_w_list})

        writer = ExcelWriter('plotData.xlsx')
        df.to_excel(writer, 'Sheet1', index=False)
        writer.save()
        print("saved")
        return 0
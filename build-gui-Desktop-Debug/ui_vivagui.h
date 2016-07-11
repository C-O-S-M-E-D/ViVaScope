/********************************************************************************
** Form generated from reading UI file 'vivagui.ui'
**
** Created by: Qt User Interface Compiler version 5.2.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_VIVAGUI_H
#define UI_VIVAGUI_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_ViVaGUI
{
public:
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QWidget *centralWidget;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *ViVaGUI)
    {
        if (ViVaGUI->objectName().isEmpty())
            ViVaGUI->setObjectName(QStringLiteral("ViVaGUI"));
        ViVaGUI->resize(400, 300);
        menuBar = new QMenuBar(ViVaGUI);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        ViVaGUI->setMenuBar(menuBar);
        mainToolBar = new QToolBar(ViVaGUI);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        ViVaGUI->addToolBar(mainToolBar);
        centralWidget = new QWidget(ViVaGUI);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        ViVaGUI->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(ViVaGUI);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        ViVaGUI->setStatusBar(statusBar);

        retranslateUi(ViVaGUI);

        QMetaObject::connectSlotsByName(ViVaGUI);
    } // setupUi

    void retranslateUi(QMainWindow *ViVaGUI)
    {
        ViVaGUI->setWindowTitle(QApplication::translate("ViVaGUI", "ViVaGUI", 0));
    } // retranslateUi

};

namespace Ui {
    class ViVaGUI: public Ui_ViVaGUI {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_VIVAGUI_H

#include "vivagui.h"
#include "ui_vivagui.h"

ViVaGUI::ViVaGUI(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ViVaGUI)
{
    ui->setupUi(this);
}

ViVaGUI::~ViVaGUI()
{
    delete ui;
}

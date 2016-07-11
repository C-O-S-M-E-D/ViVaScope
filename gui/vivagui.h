#ifndef VIVAGUI_H
#define VIVAGUI_H

#include <QMainWindow>

namespace Ui {
class ViVaGUI;
}

class ViVaGUI : public QMainWindow
{
    Q_OBJECT

public:
    explicit ViVaGUI(QWidget *parent = 0);
    ~ViVaGUI();

private:
    Ui::ViVaGUI *ui;
};

#endif // VIVAGUI_H

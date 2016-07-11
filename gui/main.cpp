#include "vivagui.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    ViVaGUI w;
    w.show();

    return a.exec();
}

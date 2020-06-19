import QtQuick 2.11
import QtQuick.Controls 2.3

ApplicationWindow {
    visible: true
    title: "Example application"
    id: mainWindow

    width: 450
    height: 700

    minimumWidth: width
    minimumHeight: height
    maximumWidth: width
    maximumHeight: height

    property Item currentView
    property Dashboard dashboardView: Dashboard {}

    property string grey: "#dcdcdc"

    onCurrentViewChanged: {
        if(stackView.depth > 0) {
            stackView.pop(StackView.Immediate)
        }

        if(currentView !== stackView.currentItem) {
            stackView.push(currentView, StackView.Immediate)
        }
    }

    StateGroup {
        id: appStateGroup
        states: [
            State {
                name: "dashboard"
                PropertyChanges {
                    target: mainWindow
                    currentView: dashboardView
                }
            }
        ]
    }

    Component.onCompleted: {
        appStateGroup.state = "dashboard"
    }

    StackView {
        id: stackView
        anchors.fill: parent
    }
}

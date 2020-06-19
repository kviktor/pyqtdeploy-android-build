import QtQuick 2.11
import QtQuick.Controls 2.3


Page {
    property int margin: mainWindow.width * 0.05

    contentItem: Rectangle {
        width: mainWindow.width;

        Rectangle {
            id: dashboardHeader
            width: mainWindow.width;
            height: 120
            color: "green"

            Text {
                text: "Example application"
                color: "white"
                anchors.left: parent.left
                anchors.leftMargin: margin
                anchors.verticalCenter: parent.verticalCenter
            }

            Rectangle {
                id: clickRectangle
                color: "transparent"
                width: mainWindow.width * 0.5
                height: dashboardHeader.height * 0.35
                anchors.right: parent.right
                anchors.rightMargin: margin
                anchors.top: parent.top
                anchors.topMargin: dashboardHeader.height * 0.1

                Text {
                    text: controller.click_count
                    color: "white"
                    anchors.right: clickButton.left
                    anchors.rightMargin: margin
                    anchors.verticalCenter: parent.verticalCenter
                }

                Button {
                    id: clickButton
                    text: "Click me!"
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter

                    onClicked: {
                        controller.click_event()
                    }
                }
            }

            Rectangle {
                id: notificationRectangle
                color: "transparent"
                width: mainWindow.width * 0.55
                height: dashboardHeader.height * 0.35
                anchors.right: parent.right
                anchors.rightMargin: margin
                anchors.top: clickRectangle.bottom
                anchors.topMargin: dashboardHeader.height * 0.1

                TextField {
                    id: notificationInput
                    placeholderText: "placeholder"
                    width: parent.width - notificationButton.width
                    anchors.left: parent.left
                    anchors.rightMargin: margin
                    anchors.verticalCenter: parent.verticalCenter
                }

                Button {
                    id: notificationButton
                    text: "Send!"
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter

                    onClicked: {
                        controller.send_notification(notificationInput.text)
                    }
                }
            }
        }

        Rectangle {
            width: mainWindow.width;
            height: mainWindow.height * 0.8
            anchors.top: dashboardHeader.bottom

            ScrollView {
                id: view
                anchors.fill: parent

                TextArea {
                    id: textArea
                    text: controller.system_info
                    hoverEnabled: false
                    readOnly: true
                }
            }
        }
    }
}

import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

import io.qt.textproperties 1.0

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Socket Reverse Chat")
    id: win

    Controller{
        id: controller
    }

    RowLayout{
        id: mainlayout
        Layout.fillHeight: true
        Layout.fillWidth: true
        anchors.fill: parent
        ColumnLayout{
            id: sendercol
            Layout.fillHeight: true
            Layout.fillWidth: true
            TextArea{
                id: sendertext
                text: ""
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
            Rectangle{
                id: splitter
                Layout.fillWidth: true
                Layout.preferredHeight: 5
                color: "black"
            }
            TextArea{
                id:sendingbox
                text: ""
                Layout.fillWidth: true
                Layout.preferredHeight: 150
                KeyNavigation.tab: btnSend
            }
            Button{
                id: btnSend
                text: "Send Message"
                enabled: true
                onClicked: {
                    console.log("sendbutton clicked")
                    controller.sendMessage(sendingbox.text)
                }
            }
        }
        ColumnLayout{
            id: receivercol
            Layout.fillHeight: true
            Layout.fillWidth: true
            Button{
                id: btnStart
                text: "Start Socket"
                onClicked: {
                    console.log("connect clicked")
                    controller.start()
                }
            }

            TextArea{
                id: rcvtext
                text: ""
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }
    }
    Connections{
        target: controller
        function onToSender(msg){
            console.log("ToSender called");
            const currentDate = new Date();
            const dayOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][currentDate.getDay()];
            const hours = ('0' + currentDate.getHours()).slice(-2); // Add leading zero if needed
            const minutes = ('0' + currentDate.getMinutes()).slice(-2); // Add leading zero if needed
            const formattedDateTime = `${dayOfWeek} ${hours}:${minutes}`;
            sendertext.text =formattedDateTime+": "+ msg +"\n" + sendertext.text
        }
        function onToReceiver(msg){
            console.log("ToReceiver called");
            const currentDate = new Date();
            const dayOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][currentDate.getDay()];
            const hours = ('0'+ currentDate.getHours()).slice(-2);
            const minutes = ('0'+ currentDate.getMinutes()).slice(-2);
            const formattedDateTime = `${dayOfWeek} ${hours}:${minutes}`;
            rcvtext.text = formattedDateTime + ": " + msg +"\n" + rcvtext.text
        }
    }
    Component.onCompleted: controller.notify()
}

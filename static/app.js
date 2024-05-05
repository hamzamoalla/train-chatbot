class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

onSendButton(chatbox) {
    var textField = chatbox.querySelector('input');
    let text1 = textField.value;

    if (text1 === "") {
        return;
    }

    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);
    this.updateChatText(chatbox); // Ajout pour mettre à jour la conversation avec le message de l'utilisateur

    $.ajax({
        type: "POST",
        url: "/webhook",
        contentType: "application/json",
        data: JSON.stringify({ message: text1 }),
        success: (data) => {
            data.response.forEach(message => {
                let msg2 = { name: "Sam", message: message };
                this.messages.push(msg2);
            });
            this.updateChatText(chatbox);
            textField.value = '';
        },
        error: function() {
            console.error('Erreur lors de l envoi du message au serveur.');
        }
    });
}

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();

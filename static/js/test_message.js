let messagebox = document.querySelector("#message");
let form = document.getElementById('sentmessage');

// 圖片預覽
function previewFile() {
    const preview = document.querySelector('#img');
    const file = document.querySelector('input[type=file]').files[0];
    const reader = new FileReader();
    // console.log("file", file)

    reader.addEventListener("load", function() {
        // convert image file to base64 string
        preview.src = reader.result;
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}
// 圖片上傳
form.addEventListener('submit', function(event) {
    event.preventDefault();
    let fileField = document.querySelector("input[type='file']");

    if (fileField.files[0] != null) {
        var formData = new FormData();
        formData.append('uptext', document.getElementById('sentmessagetext').value);
        formData.append('upfile', fileField.files[0]);
        console.log("圖文都有")

    } else {
        var formData = new FormData();
        formData.append('uptext', document.getElementById('sentmessagetext').value);
        console.log("只有文字")
    }

    fetch("/up_index", {
        method: 'POST',
        body: formData,
        // Other setting you need
        // 不需要設定 'Content-Type': 'multipart/form-data' ，已經用 FormData 物件作為請求內容了
    }).then(function(response) {
        return response.json();
    }).then(function(result) {
        if (result) {
            window.location.reload();
        }
    })

})

function getawsrdsdataapi() {
    fetch("/api/load_message").then(function(response) {
        return response.json();
    }).then(function(result) {
        for (let i = 0; i < result.data.length; i++) {
            if (messagebox.firstChild == null) {
                // console.log("無")
                messages = document.createElement("div");
                messages.className = "messages";
                messagebox.appendChild(messages);
            } else {
                // console.log("有")
                messages = document.createElement("div");
                messages.className = "messages";

                messagebox.insertBefore(messages, messagebox.childNodes[0]);
                //父.insertBefore(加入，被加入)
            }
            // 文字
            if(result.data[i].text){
                messagestext = document.createElement("div");
                messagestext.className = "messagestext";
                messagestext.textContent = result.data[i].text;
                messages.appendChild(messagestext);
            }
            // 圖片
            if(result.data[i].image){
                messagesimage = document.createElement("img");
                messagesimage.className = "messagesimage";
                messagesimage.src =  '/image/'+result.data[i].image;
                messages.appendChild(messagesimage);
            }
            // 分隔線
            hr = document.createElement("hr");
            messages.appendChild(hr);
        }
    })
}

getawsrdsdataapi();

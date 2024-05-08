function submitForm() {
    var form = document.getElementById('article-form');
    var formData = new FormData(form);

    // 现在你可以将 formData 用于发送表单数据
    fetch('/qa/article', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            alert(JSON.stringify(data.errors));
        } else {
            alert('提交成功！');
            // ... 处理成功提交后的逻辑 ...
        }
    });
}

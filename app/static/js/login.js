document.getElementById("login-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const username = formData.get('username');
    const password = formData.get('password');

    fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password }),
        credentials: "include"
    })
        .then(async res => {
            if (!res.ok) {
                const text = await res.text();
                throw new Error(`ログイン失敗: ${text}`);
            }
            return res.json();
        })
        .then(data => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                alert("ログインに失敗しました");
            }
        });
});

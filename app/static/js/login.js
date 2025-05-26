document.getElementById("login-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const username = formData.get('username');
    const password = formData.get('password');

    const maxRetries = 5;
    const baseDelay = 200;

    async function loginWithRetry(attempt = 1) {
        try {
            const res = await fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password }),
                credentials: "include"
            });

            if (!res.ok) {
                const text = await res.text();
                throw new Error(`ログイン失敗: ${text}`);
            }

            const data = await res.json();

            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                alert("ログインに失敗しました");
            }

        } catch (error) {
            console.warn(`ログイン試行 ${attempt}/${maxRetries} 失敗`, error);

            if (attempt < maxRetries) {
                const delay = baseDelay * Math.pow(2, attempt - 1); // 200ms → 400ms → 800ms
                await new Promise(res => setTimeout(res, delay));
                return loginWithRetry(attempt + 1);
            } else {
                alert("ログインに失敗しました。時間をおいて再度お試しください。");
            }
        }
    }

    loginWithRetry();
    /*
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
    */
});

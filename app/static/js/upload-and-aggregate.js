function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) return match[2];
}

function setupFileUpload(areaId, inputId, uploadEndpoint, aggregateEndpoint, label) {
    const area = document.getElementById(areaId);
    const input = document.getElementById(inputId);

    area.addEventListener('dragover', (e) => {
        e.preventDefault();
        area.classList.add('dragover');
    });

    area.addEventListener('dragleave', () => {
        area.classList.remove('dragover');
    });

    area.addEventListener('drop', (e) => {
        e.preventDefault();
        area.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file) {
            uploadAndAggregate(file, uploadEndpoint, aggregateEndpoint, label);
        }
    });

    area.addEventListener('click', () => {
        input.click();
    });

    input.addEventListener('change', () => {
        const file = input.files[0];
        if (file) {
            uploadAndAggregate(file, uploadEndpoint, aggregateEndpoint, label);
        }
    });
}

function uploadAndAggregate(file, uploadEndpoint, aggregateEndpoint, label) {
    if (!confirm(`"${file.name}" を${label}としてアップロード＆集計しますか？`)) {
        return;
    }

    // CSRFトークンを取得
    const csrfToken = getCookie('csrf_access_token');

    const formData = new FormData();
    formData.append('file', file);

    fetch(uploadEndpoint, {
        method: 'POST',
        body: formData,
        credentials: 'include',
        headers: {
            'X-CSRF-TOKEN': csrfToken
        }
    })
        .then(res => {
            if (!res.ok) {
                //throw new Error('アップロード失敗');
                // レスポンスが失敗した場合のエラー処理
                return res.text().then(text => {
                    throw new Error(`アップロード失敗: ${res.status} - ${text}`);
                });
            }
            return res.json();
        })
        .then(uploadData => {
            return fetch(aggregateEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': csrfToken
                },
                credentials: 'include',
                body: JSON.stringify({
                    fileId: uploadData.fileId,
                    label: label
                })
            });
        })
        .then(res => {
            if (!res.ok) {
                throw new Error('集計失敗');
            }
            alert(`${label}のアップロード＆集計完了！`);
        })
        .catch(err => {
            alert(`${label}の処理に失敗しました: ${err.message}`);
            console.error('エラー詳細:', err);
        });
}
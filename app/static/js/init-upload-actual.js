document.addEventListener('DOMContentLoaded', () => {
    setupFileUpload(
        'upload-actual-area',
        'file-input-actual',
        '/api/upload-actual',
        '/api/aggregate/actual-and-difference',
        '実績');
});
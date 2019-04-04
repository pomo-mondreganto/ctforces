let serverUrl = '';

if (process.env.NODE_ENV === 'development') {
    serverUrl = 'http://127.0.0.1:8000';
} else {
    serverUrl = 'http://127.0.0.1:8000';
}

const apiUrl = `${serverUrl}/api`;
const mediaUrl = serverUrl;
const smallWidth = 991;

export { apiUrl, mediaUrl, smallWidth };

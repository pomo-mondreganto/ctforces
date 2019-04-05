let url = '';

if (process.env.NODE_ENV === 'development') {
    url = 'http://127.0.0.1:8000';
} else {
    url = 'http://ctforces.com';
}

const serverUrl = url;

const apiUrl = `${serverUrl}/api`;
const mediaUrl = `${serverUrl}/media/`;
const smallWidth = 991;

export {
    serverUrl, apiUrl, mediaUrl, smallWidth,
};

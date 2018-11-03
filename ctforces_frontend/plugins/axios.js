export default function({ $axios }) {
    $axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    $axios.defaults.xsrfCookieName = 'csrftoken';
}

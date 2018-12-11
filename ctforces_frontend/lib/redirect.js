import Router from 'next/router';

export default function redirect(url, { res }) {
    if (res) {
        res.writeHead(302, {
            Location: url
        });
        res.end();
    } else {
        Router.push(url);
    }
}

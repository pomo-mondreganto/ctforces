import Router from 'next/router';

export default function redirect(url, ctx) {
    if (ctx && ctx.res) {
        res.writeHead(302, {
            Location: '/' + url
        });
        ctx.res.end();
    } else {
        Router.push('/' + url);
    }
}

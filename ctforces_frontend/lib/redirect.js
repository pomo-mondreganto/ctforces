import { Router } from '../server/routes';

export default function redirect(url, ctx) {
    if (ctx && ctx.res) {
        ctx.res.writeHead(302, {
            Location: '/' + (url === '/' ? '' : url)
        });
        ctx.res.end();
    } else {
        Router.pushRoute('/' + (url === '/' ? '' : url));
    }
}

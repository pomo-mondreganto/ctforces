import fetch from 'isomorphic-unfetch';
import { api_url } from '../config';
import redirect from '../lib/redirect';
import getCookie from './get_cookie';

export async function get(path, options) {
    if (options == undefined) {
        options = {};
    }
    try {
        let query = options.data
            ? Object.keys(options.data)
                  .map(
                      k =>
                          encodeURIComponent(k) +
                          '=' +
                          encodeURIComponent(options.data[k])
                  )
                  .join('&')
            : '';
        if (query !== '') {
            query = '?' + query;
        }
        let content_type = 'application/json';
        if (options.content_type !== undefined) {
            content_type = options.content_type;
        } else {
        }
        let headers = {
            Accept: 'application/json',
            'Content-Type': content_type
        };
        if (options.ctx !== undefined && options.ctx.req !== undefined) {
            headers['cookie'] = options.ctx.req.headers.cookie;
        }
        let result = await fetch(`${api_url}/${path}/${query}`, {
            method: 'get',
            headers: headers,
            credentials: 'include'
        });
        if (result.status == 404) {
            redirect('404', options.ctx);
        } else {
            return result;
        }
    } catch (e) {
        redirect('oops', options.ctx);
    }
}

export async function post(path, options) {
    if (options === undefined) {
        options = {};
    }
    try {
        let content_type = 'application/json';
        let body_data = options.data;
        if (options.content_type !== undefined) {
            content_type = options.content_type;
        } else {
            body_data = JSON.stringify(options.data);
        }
        let result = await fetch(`${api_url}/${path}/`, {
            method: 'post',
            headers: {
                Accept: 'application/json',
                'Content-Type': content_type,
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: body_data
        });
        if (result.status == 404) {
            redirect('404', options.ctx);
        } else {
            return result;
        }
    } catch (e) {
        redirect('oops', options.ctx);
    }
}

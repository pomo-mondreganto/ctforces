import fetch from 'isomorphic-unfetch';
import { api_url } from '../config';

export async function get(path, data) {
    try {
        let query = data
            ? Object.keys(data)
                  .map(
                      k =>
                          encodeURIComponent(k) +
                          '=' +
                          encodeURIComponent(data[k])
                  )
                  .join('&')
            : '';
        if (query !== '') {
            query = '?' + query;
        }
        return await fetch(`${api_url}/${path}/${query}`, {
            method: 'get',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            qs: data
        });
    } catch (e) {}
}

export async function post(path, data) {
    try {
        return await fetch(`${api_url}/${path}/`, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(data)
        });
    } catch (e) {}
}

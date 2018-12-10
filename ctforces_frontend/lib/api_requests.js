import fetch from 'isomorphic-unfetch';
import { api_url } from '../config';

export async function get(path) {
    return fetch(`${api_url}/${path}/`, {
        method: 'get',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
    });
}

export async function post(path, data) {
    console.log(data);
    return fetch(`${api_url}/${path}/`, {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: data
    });
}

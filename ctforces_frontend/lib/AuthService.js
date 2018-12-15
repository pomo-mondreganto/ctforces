import { get, post } from '../lib/api_requests';

export async function login(username, password) {
    let data = await post('login', {
        username: username,
        password: password
    });
    return data;
}

export async function loggedIn() {
    let data = await get('me');
    return data.ok;
}

export async function getUser() {
    let data = await get('me');
    if (data.ok) {
        return await data.json();
    } else {
        return false;
    }
}

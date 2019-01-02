import { get, post } from './api_requests';

export async function login(username, password) {
    let data = await post('login', {
        data: { username: username, password: password }
    });
    return data;
}

export async function register(username, email, password) {
    let data = await post('register', {
        data: { username: username, email: email, password: password }
    });
    return data;
}

export async function logout() {
    let data = await post('logout');
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

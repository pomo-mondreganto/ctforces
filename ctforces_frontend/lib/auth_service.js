import { get, post } from './api_requests';

export async function login(username, password, options) {
    let data = await post('login', {
        data: { username: username, password: password },
        ...options
    });
    return data;
}

export async function register(username, email, password, options) {
    let data = await post('register', {
        data: { username: username, email: email, password: password },
        ...options
    });
    return data;
}

export async function logout(options) {
    let data = await post('logout', options);
    return data;
}

export async function loggedIn(options) {
    let data = await get('me', options);
    return data.ok;
}

export async function getUser(options) {
    let data = await get('me', options);
    if (data.ok) {
        return await data.json();
    } else {
        return false;
    }
}

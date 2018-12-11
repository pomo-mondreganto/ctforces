import { get, post } from '../lib/api_requests';

export async function login(username, password) {
    let data = await post('login', {
        username: username,
        password: password
    });
    return data;
}

export async function loggedIn() {
    try {
        let data = await get('me');
        return data.status === 200;
    } catch (e) {
        return false;
    }
}

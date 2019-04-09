import axios from 'axios';

export default async (props, force = false) => {
    if (props.auth.requested && !force) {
        return;
    }
    try {
        const response = await axios.get('/me/');
        props.updateAuthUser({
            loggedIn: true,
            user: response.data,
            requested: true,
        });
    } catch {
        props.updateAuthUser({
            loggedIn: false,
            user: null,
            requested: true,
        });
    }
};

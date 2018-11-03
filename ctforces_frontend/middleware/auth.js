export default function({ store, redirect }) {
    if (!store.state.auth.authUser) {
        redirect('/login');
    }
}
